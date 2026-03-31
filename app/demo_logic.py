import json
import time
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import cv2
import gradio as gr

from app.config import BASE_DIR, YOLO_CHECKPOINT_PATH
from app.inference.runtime import RUNTIME, RuntimeSnapshot
from app.ui.templates import build_report_html, build_upload_file_state_html
from scripts.infer_video import run_inference
from src.teacher import is_teacher_name, student_slots

Status = str

ALERT_COOLDOWN_SEC = 30

PANEL_STATE: dict[str, Any] = {
    "is_running": False,
    "session_started_at": None,
    "is_warming_up": False,
    "warmup_until": None,
    "pipeline_ready": False,
    "slot_stats": {},
    "prev_statuses": {},
    "last_alert_time": {},
    "alerts": [],
    "timeline": [],
    "last_timeline_bucket": -1,
}


def _clear_panel_metrics(started_at: float | None = None) -> None:
    PANEL_STATE["session_started_at"] = started_at
    PANEL_STATE["slot_stats"] = {}
    PANEL_STATE["prev_statuses"] = {}
    PANEL_STATE["last_alert_time"] = {}
    PANEL_STATE["alerts"] = []
    PANEL_STATE["timeline"] = []
    PANEL_STATE["last_timeline_bucket"] = -1


def _reset_panel_state() -> None:
    PANEL_STATE["is_running"] = True
    _clear_panel_metrics()
    PANEL_STATE["is_warming_up"] = True
    PANEL_STATE["warmup_until"] = None
    PANEL_STATE["pipeline_ready"] = False


def _stop_panel_state() -> None:
    PANEL_STATE["is_running"] = False
    PANEL_STATE["is_warming_up"] = False
    PANEL_STATE["warmup_until"] = None
    PANEL_STATE["pipeline_ready"] = False


def _apply_runtime_flags(snapshot: RuntimeSnapshot) -> None:
    PANEL_STATE["is_warming_up"] = snapshot.is_warming_up
    PANEL_STATE["warmup_until"] = snapshot.warmup_until or None
    PANEL_STATE["pipeline_ready"] = snapshot.pipeline_ready


def _begin_active_session() -> None:
    _clear_panel_metrics(started_at=time.time())


def _now_ts() -> datetime:
    return datetime.now()


def _status_meta(status: str) -> dict[str, str]:
    normalized = (status or "NORMAL").upper()
    if normalized == "YAWN":
        normalized = "NORMAL"

    if normalized == "DROWSY":
        return {
            "label": "졸음",
            "color": "#fbbf24",
            "bg": "rgba(245, 158, 11, 0.12)",
            "desc": "졸음이 감지되었습니다",
            "icon": "졸음",
        }
    if normalized == "ABSENT":
        return {
            "label": "이탈",
            "color": "#f87171",
            "bg": "rgba(248, 113, 113, 0.12)",
            "desc": "자리를 이탈했습니다",
            "icon": "이탈",
        }
    if normalized == "IGNORE":
        return {
            "label": "무시",
            "color": "#94a3b8",
            "bg": "rgba(148, 163, 184, 0.12)",
            "desc": "감지 제외 상태",
            "icon": "무시",
        }
    return {
        "label": "정상",
        "color": "#34d399",
        "bg": "rgba(52, 211, 153, 0.12)",
        "desc": "수업에 집중하고 있습니다",
        "icon": "정상",
    }


def _make_alert(alert_type: Status, message: str) -> dict[str, Any]:
    return {
        "id": f"{int(time.time() * 1000)}-{len(PANEL_STATE['alerts'])}",
        "type": alert_type,
        "message": message,
        "timestamp": _now_ts(),
    }


def _push_alert(alert_type: Status, message: str) -> None:
    new_alert = _make_alert(alert_type, message)
    PANEL_STATE["alerts"] = [new_alert, *PANEL_STATE["alerts"][:9]]


def _sync_panel_state(snapshot: RuntimeSnapshot) -> None:
    if not PANEL_STATE["is_running"]:
        return

    was_ready = PANEL_STATE["pipeline_ready"]
    _apply_runtime_flags(snapshot)
    if snapshot.is_warming_up:
        return
    if snapshot.pipeline_ready and not was_ready:
        _begin_active_session()

    for slot in snapshot.slots:
        if slot.is_teacher:
            continue

        sid = slot.slot_id
        name = slot.name or f"학생 {sid}"
        status = slot.status
        panel_status = "NORMAL" if status == "YAWN" else status

        if sid not in PANEL_STATE["slot_stats"]:
            PANEL_STATE["slot_stats"][sid] = {
                "name": name,
                "normal": 0,
                "drowsy": 0,
                "absent": 0,
            }
        else:
            PANEL_STATE["slot_stats"][sid]["name"] = name

        stat = PANEL_STATE["slot_stats"][sid]
        if panel_status == "DROWSY":
            stat["drowsy"] += 1
        elif panel_status == "ABSENT":
            stat["absent"] += 1
        else:
            stat["normal"] += 1

        prev = PANEL_STATE["prev_statuses"].get(sid, "NORMAL")
        if prev != panel_status and panel_status != "NORMAL":
            now = time.time()
            last_t = PANEL_STATE["last_alert_time"].get(sid, 0)
            if now - last_t >= ALERT_COOLDOWN_SEC:
                if panel_status == "DROWSY":
                    _push_alert("DROWSY", f"{name} 학생에게 졸음이 감지되었습니다.")
                elif panel_status == "ABSENT":
                    _push_alert("ABSENT", f"{name} 학생이 자리를 이탈했습니다.")
                PANEL_STATE["last_alert_time"][sid] = now

        PANEL_STATE["prev_statuses"][sid] = panel_status

    _append_timeline_sample(snapshot)


def _format_time(dt: datetime) -> str:
    return dt.strftime("%H:%M:%S")


def _format_duration(seconds: int) -> str:
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins}:{secs:02d}"


def _elapsed_sec() -> int:
    if PANEL_STATE["session_started_at"] is None:
        return 0
    return int(time.time() - PANEL_STATE["session_started_at"])


def _append_timeline_sample(snapshot: RuntimeSnapshot) -> None:
    elapsed = _elapsed_sec()
    bucket = elapsed // 15
    if bucket == PANEL_STATE["last_timeline_bucket"]:
        return

    student_slots = [slot for slot in snapshot.slots if not slot.is_teacher]
    normal = sum(1 for slot in student_slots if slot.status == "NORMAL")
    drowsy = sum(1 for slot in student_slots if slot.status == "DROWSY")
    absent = sum(1 for slot in student_slots if slot.status == "ABSENT")

    PANEL_STATE["timeline"].append(
        {
            "time": _format_duration(elapsed),
            "normal": normal,
            "drowsy": drowsy,
            "absence": absent,
        }
    )
    PANEL_STATE["timeline"] = PANEL_STATE["timeline"][-10:]
    PANEL_STATE["last_timeline_bucket"] = bucket


def _alert_tone(alert_type: str) -> str:
    if alert_type == "DROWSY":
        return "warning"
    if alert_type == "ABSENT":
        return "danger"
    return "positive"


def _safe_pct(part: int | float, whole: int | float) -> int:
    if not whole:
        return 0
    return int(round((float(part) / float(whole)) * 100))


def _video_duration_sec(video_path: str) -> int:
    capture = cv2.VideoCapture(video_path)
    try:
        fps = capture.get(cv2.CAP_PROP_FPS) or 0
        frame_count = capture.get(cv2.CAP_PROP_FRAME_COUNT) or 0
        if fps <= 0:
            return 0
        return int(frame_count / fps)
    finally:
        capture.release()


def _latest_alert_text() -> str:
    if not PANEL_STATE["alerts"]:
        return "알림이 없습니다."
    return PANEL_STATE["alerts"][0]["message"]


def _report_text() -> str:
    stats = PANEL_STATE["slot_stats"]
    elapsed = _elapsed_sec()
    lines = [f"Total Time: {_format_duration(elapsed)}"]

    for _, stat in sorted(stats.items()):
        total = stat["normal"] + stat["drowsy"] + stat["absent"]
        pct = _safe_pct(stat["normal"], total)
        lines.append(f"{stat['name']}: {pct}% 정상")

    return "\n".join(lines)


def _debug_text(snapshot: RuntimeSnapshot) -> str:
    return snapshot.debug_text


def _slots_to_json(slots) -> str:
    return json.dumps(
        [
            {
                "slot_id": s.slot_id,
                "name": s.name,
                "is_teacher": s.is_teacher,
                "status": s.status,
                "ear": round(float(s.ear), 3),
                "mar": round(float(s.mar), 3),
                "box_pct": [round(v, 6) for v in s.box_pct],
                "face_box_pct": (
                    [round(v, 6) for v in s.face_box_pct] if s.face_box_pct else []
                ),
                "noface": s.noface,
            }
            for s in slots
        ]
    )


def _build_control_panel(is_running: bool) -> str:
    start_disabled = "is-disabled" if is_running else ""
    stop_disabled = "is-disabled" if not is_running else ""
    start_onclick = "" if is_running else 'onclick="triggerPanelStart()"'
    stop_onclick = "" if not is_running else 'onclick="triggerPanelStop()"'
    live_chip = (
        '<div class="panel-live-chip">실시간 분석 중</div>' if is_running else ""
    )

    return f"""
    <section class="panel-card">
        <div class="panel-card-head">
            <div>
                <div class="panel-eyebrow">Control</div>
                <h3>실시간 제어</h3>
            </div>
            {live_chip}
        </div>
        <div class="panel-button-row">
            <button class="panel-action panel-action-primary {start_disabled}" {start_onclick}>시작</button>
            <button class="panel-action panel-action-danger {stop_disabled}" {stop_onclick}>중지</button>
        </div>
    </section>
    """


def _build_slot_list(slots: list) -> str:
    slots = student_slots(slots)
    rows = []
    for slot in slots:
        meta = _status_meta(slot.status)
        rows.append(
            f"""
            <div class="panel-list-item">
                <div class="panel-list-meta">
                    <span class="panel-status-dot" style="background:{meta['color']};"></span>
                    <strong>{slot.name}</strong>
                </div>
                <span style="color:{meta['color']};">{meta['label']}</span>
            </div>
            """
        )

    items_html = (
        "".join(rows)
        if rows
        else '<div class="panel-empty">감지된 수강생이 없습니다.</div>'
    )
    return f"""
    <section class="panel-card">
        <div class="panel-card-head">
            <div>
                <div class="panel-eyebrow">Participants</div>
                <h3>수강생 현황</h3>
            </div>
        </div>
        <div class="panel-list-wrap">{items_html}</div>
    </section>
    """


def _build_alert_card(alerts: list[dict[str, Any]]) -> str:
    items = []
    label_map = {
        "DROWSY": "졸음",
        "ABSENT": "이탈",
        "NORMAL": "정상",
    }

    for alert in alerts[:10]:
        tone = _alert_tone(alert["type"])
        label = label_map.get(alert["type"], alert["type"])
        items.append(
            f"""
            <div class="panel-alert tone-{tone}">
                <div class="panel-alert-head">
                    <strong>{label}</strong>
                    <span>{_format_time(alert['timestamp'])}</span>
                </div>
                <p>{alert['message']}</p>
            </div>
            """
        )

    items_html = (
        "".join(items)
        if items
        else '<div class="panel-empty">실시간 알림이 없습니다.</div>'
    )
    return f"""
    <section class="panel-card">
        <div class="panel-card-head">
            <div>
                <div class="panel-eyebrow">Alerts</div>
                <h3>실시간 알림</h3>
            </div>
        </div>
        <div class="panel-list-wrap">{items_html}</div>
    </section>
    """


def render_panel_html(
    camera_state: str,
    status: str,
    alert: str,
    report: str,
    is_running: bool,
    slots: Optional[list] = None,
) -> str:
    del camera_state

    if slots is None:
        slots = []

    alerts = deepcopy(PANEL_STATE["alerts"])
    return f"""
    <div class="panel-shell">
        {_build_control_panel(is_running)}
        {_build_slot_list(slots)}
        {_build_alert_card(alerts)}
    </div>
    """


def build_empty_report_data() -> dict[str, Any]:
    return {
        "badge": "Report",
        "title": "분석 리포트가 아직 없습니다",
        "subtitle": "실시간 모드 실행 또는 녹화 영상 분석 후 결과가 여기에 표시됩니다.",
        "source_label": "Waiting for analysis",
        "summary_cards": [
            {"label": "총 참여자", "value": "0명", "tone": "neutral"},
            {"label": "평균 집중도", "value": "0%", "tone": "neutral"},
            {"label": "졸음 감지", "value": "0", "tone": "warning"},
            {"label": "이탈 감지", "value": "0", "tone": "danger"},
        ],
        "events": [],
        "participants": [],
        "highlights": [
            "현재는 연결된 리포트 데이터가 없습니다.",
            "홈 화면에서 실시간 분석 또는 녹화 분석을 시작해주세요.",
        ],
        "insights": [],
        "chart_title": "시간대별 상태 분석",
        "chart_subtitle": "분석 데이터가 쌓이면 상태 변화 그래프가 표시됩니다.",
        "chart_points": [],
    }


def build_live_report_data() -> dict[str, Any]:
    stats = PANEL_STATE["slot_stats"]
    snapshot = RUNTIME.snapshot()

    participants = []
    total_focus = 0
    drowsy_students = 0
    absent_students = 0

    for _, stat in sorted(stats.items()):
        total = stat["normal"] + stat["drowsy"] + stat["absent"]
        focus = _safe_pct(stat["normal"], total)
        drowsy = _safe_pct(stat["drowsy"], total)
        absent = _safe_pct(stat["absent"], total)

        participants.append(
            {
                "name": stat["name"],
                "focus": focus,
                "normal": focus,
                "drowsy": drowsy,
                "absence": absent,
            }
        )
        total_focus += focus
        if stat["drowsy"] > 0:
            drowsy_students += 1
        if stat["absent"] > 0:
            absent_students += 1

    if not participants and snapshot.slots:
        fallback_slots = [slot for slot in snapshot.slots if not slot.is_teacher]
        for slot in fallback_slots:
            normalized_status = "NORMAL" if slot.status == "YAWN" else slot.status
            focus = 100 if normalized_status == "NORMAL" else 0
            drowsy = 100 if slot.status == "DROWSY" else 0
            absent = 100 if slot.status == "ABSENT" else 0
            participants.append(
                {
                    "name": slot.name,
                    "focus": focus,
                    "normal": focus,
                    "drowsy": drowsy,
                    "absence": absent,
                }
            )

        total_focus = sum(item["focus"] for item in participants)
        drowsy_students = sum(1 for item in participants if item["drowsy"] > 0)
        absent_students = sum(1 for item in participants if item["absence"] > 0)

    timeline = deepcopy(PANEL_STATE["timeline"])
    if not timeline and snapshot.slots:
        fallback_students = [slot for slot in snapshot.slots if not slot.is_teacher]
        timeline = [
            {
                "time": _format_duration(_elapsed_sec()),
                "normal": sum(
                    1
                    for slot in fallback_students
                    if slot.status in ("NORMAL", "YAWN")
                ),
                "drowsy": sum(
                    1 for slot in fallback_students if slot.status == "DROWSY"
                ),
                "absence": sum(
                    1 for slot in fallback_students if slot.status == "ABSENT"
                ),
            }
        ]

    if not participants:
        return build_empty_report_data()

    alerts = deepcopy(PANEL_STATE["alerts"])
    events = [
        {
            "title": "졸음 감지" if alert["type"] == "DROWSY" else "자리 이탈",
            "detail": alert["message"],
            "time": _format_time(alert["timestamp"]),
            "tone": _alert_tone(alert["type"]),
        }
        for alert in alerts[:8]
    ]

    avg_focus = _safe_pct(total_focus, len(participants) * 100) if participants else 0
    elapsed = _format_duration(_elapsed_sec())
    weakest = (
        min(participants, key=lambda item: item["focus"]) if participants else None
    )

    highlights = [
        f"실시간 분석이 {elapsed} 동안 누적되었습니다.",
        f"참여자 {len(participants)}명 기준 평균 집중도는 {avg_focus}%입니다.",
    ]
    if weakest:
        highlights.append(
            f"가장 집중도가 낮았던 학생은 {weakest['name']}이며 집중도 {weakest['focus']}%로 집계되었습니다."
        )

    return {
        "badge": "Live Report",
        "title": "실시간 분석 리포트",
        "subtitle": f"세션 누적 시간 {elapsed} 기준의 실시간 요약 결과입니다.",
        "source_label": "Realtime session summary",
        "summary_cards": [
            {
                "label": "총 참여자",
                "value": f"{len(participants)}명",
                "tone": "neutral",
            },
            {"label": "평균 집중도", "value": f"{avg_focus}%", "tone": "positive"},
            {
                "label": "졸음 감지 학생",
                "value": f"{drowsy_students}명",
                "tone": "warning",
            },
            {
                "label": "이탈 감지 학생",
                "value": f"{absent_students}명",
                "tone": "danger",
            },
        ],
        "events": events,
        "participants": participants,
        "highlights": highlights,
        "insights": [
            {
                "tone": "info",
                "title": "분석 결과 요약",
                "detail": f"전체적으로 평균 집중도 {avg_focus}%를 유지했습니다.",
            },
            {
                "tone": "warning",
                "title": "추가 확인 권장",
                "detail": (
                    f"{weakest['name']} 학생은 상대적으로 집중도 편차가 커서 이벤트 발생 구간을 함께 확인하는 것이 좋습니다."
                    if weakest
                    else "현재는 추가 확인할 학생 데이터가 없습니다."
                ),
            },
        ],
        "chart_title": "시간대별 상태 분석",
        "chart_subtitle": "15초 단위로 집계한 정상 / 졸음 / 이탈 상태 변화입니다.",
        "chart_points": timeline,
    }


def build_upload_report_data(
    track_summary: list[dict[str, Any]],
    *,
    video_name: str,
    class_start_time: str,
    duration_sec: int,
) -> dict[str, Any]:
    participants = []
    total_focus = 0
    drowsy_students = 0
    absent_students = 0

    for row in track_summary:
        if bool(row.get("is_teacher")) or is_teacher_name(row.get("name")):
            continue
        total_frames = int(row.get("total_frames", 0) or 0)
        focus = _safe_pct(row.get("frames_normal", 0), total_frames)
        drowsy = _safe_pct(row.get("frames_drowsy", 0), total_frames)
        absent = _safe_pct(row.get("frames_absent", 0), total_frames)
        participant_name = row.get("name") or f"학생 {row.get('slot_id', '-')}"

        participants.append(
            {
                "name": participant_name,
                "focus": focus,
                "normal": focus,
                "drowsy": drowsy,
                "absence": absent,
            }
        )
        total_focus += focus

        if row.get("frames_drowsy", 0):
            drowsy_students += 1
        if row.get("frames_absent", 0):
            absent_students += 1

    participants.sort(key=lambda item: item["focus"])
    avg_focus = _safe_pct(total_focus, len(participants) * 100) if participants else 0
    duration_text = (
        f"{duration_sec // 60}분 {duration_sec % 60}초"
        if duration_sec
        else "길이 미확인"
    )

    events = [
        {
            "title": "집계 기반 리포트",
            "detail": "현재 업로드 분석은 학생별 누적 프레임 통계 중심으로 요약되며, 시점별 상세 이벤트 로그는 후속 연결 대상입니다.",
            "time": class_start_time or "시간 미지정",
            "tone": "warning",
        }
    ]

    highlights = [
        f"{video_name} 분석이 완료되었습니다.",
        f"수업 시작 시각은 {class_start_time or '미지정'}로 반영되었습니다.",
        f"총 영상 길이는 {duration_text}이며 평균 집중도는 {avg_focus}%입니다.",
    ]

    weakest = participants[0] if participants else None
    if weakest:
        highlights.append(
            f"추가 확인이 필요한 학생은 {weakest['name']}이며 집중도 {weakest['focus']}%입니다."
        )

    if not participants:
        return {
            "badge": "Upload Report",
            "title": "영상 분석 결과",
            "subtitle": "분석은 완료되었지만 요약 가능한 학생 데이터가 없습니다.",
            "source_label": video_name,
            "summary_cards": [
                {"label": "총 참여자", "value": "0명", "tone": "neutral"},
                {"label": "평균 집중도", "value": "0%", "tone": "neutral"},
                {"label": "졸음 감지 학생", "value": "0명", "tone": "warning"},
                {"label": "이탈 감지 학생", "value": "0명", "tone": "danger"},
            ],
            "events": events,
            "participants": [],
            "highlights": highlights,
            "insights": [],
            "chart_title": "시간대별 상태 분석",
            "chart_subtitle": "업로드 분석의 시계열 데이터가 아직 연결되지 않았습니다.",
            "chart_points": [],
        }

    return {
        "badge": "Upload Report",
        "title": "녹화 영상 분석 리포트",
        "subtitle": f"{class_start_time or '시간 미지정'} 수업 기준 요약 결과입니다.",
        "source_label": video_name,
        "summary_cards": [
            {
                "label": "총 참여자",
                "value": f"{len(participants)}명",
                "tone": "neutral",
            },
            {"label": "평균 집중도", "value": f"{avg_focus}%", "tone": "positive"},
            {
                "label": "졸음 감지 학생",
                "value": f"{drowsy_students}명",
                "tone": "warning",
            },
            {
                "label": "이탈 감지 학생",
                "value": f"{absent_students}명",
                "tone": "danger",
            },
        ],
        "events": events,
        "participants": participants,
        "highlights": highlights,
        "insights": [
            {
                "tone": "info",
                "title": "업로드 분석 요약",
                "detail": f"총 {len(participants)}명의 참여자 데이터를 기준으로 평균 집중도 {avg_focus}%가 집계되었습니다.",
            },
            {
                "tone": "warning",
                "title": "추가 확인 권장",
                "detail": (
                    f"{weakest['name']} 학생은 상대적으로 집중도 편차가 커서 해당 구간 원본 영상을 다시 확인하는 것이 좋습니다."
                    if weakest
                    else "추가 확인이 필요한 학생 데이터가 없습니다."
                ),
            },
        ],
        "chart_title": "시간대별 상태 분석",
        "chart_subtitle": "업로드 분석의 시계열 데이터는 현재 준비 중입니다.",
        "chart_points": [],
    }


def render_report_html(report_data: dict[str, Any] | None) -> str:
    return build_report_html(report_data or build_empty_report_data())


def prepare_live_report_data() -> dict[str, Any]:
    _stop_panel_state()
    RUNTIME.stop()
    return build_live_report_data()


def describe_uploaded_file(file_path: str | None) -> str:
    return build_upload_file_state_html(file_path)


def compose_class_start_time(hour: float | int, minute: float | int) -> str:
    return f"{int(hour):02d}:{int(minute):02d}"


def analyze_uploaded_video(
    file_path: str | None,
    class_start_time: str,
    progress=gr.Progress(track_tqdm=True),
) -> tuple[dict[str, Any], str]:
    if not file_path:
        raise gr.Error("분석할 영상 파일을 먼저 업로드해주세요.")
    if not class_start_time.strip():
        raise gr.Error("수업 시작 시간을 입력해주세요. 예: 09:00")

    video_path = Path(file_path)
    if not video_path.exists():
        raise gr.Error("업로드된 파일을 찾을 수 없습니다.")
    if not Path(YOLO_CHECKPOINT_PATH).exists():
        raise gr.Error(f"YOLO 체크포인트를 찾을 수 없습니다: {YOLO_CHECKPOINT_PATH}")

    progress(0.05, desc="업로드 영상 확인 중")
    output_dir = BASE_DIR / "outputs" / "upload_reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_video = output_dir / f"{video_path.stem}_report.mp4"

    progress(0.12, desc="기존 추론 파이프라인 초기화 중")

    def _forward_inference_progress(ratio: float, desc: str) -> None:
        clamped = max(0.0, min(1.0, float(ratio)))
        progress(0.12 + (0.80 * clamped), desc=desc)

    track_summary = run_inference(
        input_path=video_path,
        checkpoint=YOLO_CHECKPOINT_PATH,
        output_path=output_video,
        fps=7.0,
        teacher_names=["강경미"],
        progress_callback=_forward_inference_progress,
    )

    progress(0.92, desc="리포트 구성 중")
    duration_sec = _video_duration_sec(str(video_path))
    report_data = build_upload_report_data(
        track_summary,
        video_name=video_path.name,
        class_start_time=class_start_time.strip(),
        duration_sec=duration_sec,
    )

    progress(1.0, desc="완료")
    return (
        report_data,
        f"`{video_path.name}` 분석이 완료되었습니다. 리포트 화면으로 이동합니다.",
    )


def _render_outputs(snapshot: RuntimeSnapshot, ack: int, _annotated_frame=None):
    slots = list(snapshot.slots)
    alert_text = _latest_alert_text()
    report_text = _report_text()
    panel_html = render_panel_html(
        camera_state="ON" if snapshot.running else "OFF",
        status=snapshot.status,
        alert=alert_text,
        report=report_text,
        is_running=snapshot.running,
        slots=student_slots(slots),
    )
    return (
        snapshot.status,
        alert_text,
        report_text,
        panel_html,
        _debug_text(snapshot),
        ack,
        _slots_to_json(slots),
    )


def on_start():
    _reset_panel_state()
    snapshot = RUNTIME.start()
    _apply_runtime_flags(snapshot)

    panel_html = render_panel_html(
        camera_state="ON",
        status=snapshot.status,
        alert=_latest_alert_text(),
        report=_report_text(),
        is_running=True,
        slots=[],
    )
    return (
        True,
        snapshot.status,
        _latest_alert_text(),
        _report_text(),
        panel_html,
        _debug_text(snapshot),
        0,
        "[]",
    )


def on_stop(frame_ack: int):
    _stop_panel_state()
    snapshot = RUNTIME.stop()
    _apply_runtime_flags(snapshot)

    panel_html = render_panel_html(
        camera_state="OFF",
        status=snapshot.status,
        alert=_latest_alert_text(),
        report=_report_text(),
        is_running=False,
        slots=student_slots(snapshot.slots),
    )
    return (
        False,
        snapshot.status,
        _latest_alert_text(),
        _report_text(),
        panel_html,
        _debug_text(snapshot),
        frame_ack,
        "[]",
    )


def process_live_frame(frame_seq: int, frame_data: str):
    frame_seq = int(frame_seq or 0)
    snapshot, annotated_frame = RUNTIME.process_frame(frame_data)
    _sync_panel_state(snapshot)
    return _render_outputs(snapshot, frame_seq, annotated_frame)
