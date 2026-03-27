import html
import json
import time
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Optional

import gradio as gr

from app.inference.runtime import RUNTIME, RuntimeSnapshot
from app.ui.templates import build_report_shell_html, build_upload_status_html

Status = str

ALERT_COOLDOWN_SEC = 30

PANEL_STATE: dict = {
    "is_running": False,
    "session_started_at": None,
    "slot_stats": {},
    "prev_statuses": {},
    "last_alert_time": {},
    "alerts": [],
}

UPLOAD_ANALYSIS_STATE: dict = {
    "video_name": None,
    "class_start_time": None,
    "completed_at": None,
    "summary": "아직 업로드 분석이 실행되지 않았습니다.",
}


def _reset_panel_state() -> None:
    PANEL_STATE["is_running"] = True
    PANEL_STATE["session_started_at"] = time.time()
    PANEL_STATE["slot_stats"] = {}
    PANEL_STATE["prev_statuses"] = {}
    PANEL_STATE["last_alert_time"] = {}
    PANEL_STATE["alerts"] = []


def _stop_panel_state() -> None:
    PANEL_STATE["is_running"] = False


def _now_ts() -> datetime:
    return datetime.now()


def _status_meta(status: str) -> dict[str, str]:
    normalized = (status or "NORMAL").upper()
    if normalized == "DROWSY":
        return {
            "label": "졸음",
            "color": "#f59e0b",
            "bg": "rgba(245, 158, 11, 0.10)",
            "desc": "졸음이 감지되었습니다",
            "icon": "⚠",
        }
    if normalized == "YAWN":
        return {
            "label": "하품",
            "color": "#fb923c",
            "bg": "rgba(251, 146, 60, 0.10)",
            "desc": "하품이 감지되었습니다",
            "icon": "○",
        }
    if normalized == "ABSENT":
        return {
            "label": "이탈",
            "color": "#ef4444",
            "bg": "rgba(239, 68, 68, 0.10)",
            "desc": "자리를 이탈했습니다",
            "icon": "◌",
        }
    if normalized == "IGNORE":
        return {
            "label": "무시",
            "color": "#94a3b8",
            "bg": "rgba(148, 163, 184, 0.10)",
            "desc": "감지 제외 상태",
            "icon": "—",
        }
    return {
        "label": "정상",
        "color": "#34d399",
        "bg": "rgba(52, 211, 153, 0.10)",
        "desc": "수업에 집중하고 있습니다",
        "icon": "◉",
    }


def _make_alert(alert_type: Status, message: str) -> dict:
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

    for slot in snapshot.slots:
        if slot.is_teacher:
            continue

        sid = slot.slot_id
        name = slot.name
        status = slot.status

        if sid not in PANEL_STATE["slot_stats"]:
            PANEL_STATE["slot_stats"][sid] = {
                "name": name,
                "normal": 0,
                "drowsy": 0,
                "absent": 0,
                "yawn": 0,
            }
        else:
            PANEL_STATE["slot_stats"][sid]["name"] = name

        stat = PANEL_STATE["slot_stats"][sid]
        if status == "DROWSY":
            stat["drowsy"] += 1
        elif status == "ABSENT":
            stat["absent"] += 1
        elif status == "YAWN":
            stat["yawn"] += 1
        else:
            stat["normal"] += 1

        prev = PANEL_STATE["prev_statuses"].get(sid, "NORMAL")
        if prev != status and status not in ("NORMAL", "YAWN"):
            now = time.time()
            last_t = PANEL_STATE["last_alert_time"].get(name, 0)
            if now - last_t >= ALERT_COOLDOWN_SEC:
                if status == "DROWSY":
                    _push_alert("DROWSY", f"{name} 졸음이 감지되었습니다.")
                elif status == "ABSENT":
                    _push_alert("ABSENT", f"{name} 자리를 이탈했습니다.")
                PANEL_STATE["last_alert_time"][name] = now
        PANEL_STATE["prev_statuses"][sid] = status


def _format_time(dt: datetime) -> str:
    return dt.strftime("%p %I:%M:%S").replace("AM", "오전").replace("PM", "오후")


def _format_duration(seconds: int) -> str:
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins}:{secs:02d}"


def _elapsed_sec() -> int:
    if PANEL_STATE["session_started_at"] is None:
        return 0
    return int(time.time() - PANEL_STATE["session_started_at"])


def _alert_color(alert_type: str) -> tuple[str, str, str]:
    if alert_type == "DROWSY":
        return ("rgba(245, 158, 11, 0.06)", "rgba(245, 158, 11, 0.24)", "#fbbf24")
    if alert_type == "ABSENT":
        return ("rgba(239, 68, 68, 0.06)", "rgba(239, 68, 68, 0.24)", "#f87171")
    return ("rgba(52, 211, 153, 0.06)", "rgba(52, 211, 153, 0.24)", "#6ee7b7")


def _view_updates(active: str):
    return (
        gr.update(visible=active == "home"),
        gr.update(visible=active == "live"),
        gr.update(visible=active == "upload"),
        gr.update(visible=active == "report"),
    )


def _build_control_panel(is_running: bool) -> str:
    start_disabled = "is-disabled" if is_running else ""
    stop_disabled = "is-disabled" if not is_running else ""
    start_onclick = "" if is_running else 'onclick="triggerPanelStart()"'
    stop_onclick = "" if not is_running else 'onclick="triggerPanelStop()"'
    live_chip = (
        '<div class="live-panel-status"><span class="dot"></span>실시간 분석 중</div>'
        if is_running
        else '<div class="live-panel-status idle"><span class="dot"></span>카메라 대기 중</div>'
    )

    return f"""
    <div class="live-panel-card">
        <div class="live-panel-card-head">
            <div>
                <div class="live-panel-eyebrow">Control Center</div>
                <div class="live-panel-title">카메라 제어</div>
            </div>
            {live_chip}
        </div>
        <div class="live-control-grid">
            <button class="panel-action primary {start_disabled}" {start_onclick}>시작</button>
            <button class="panel-action secondary {stop_disabled}" {stop_onclick}>중지</button>
        </div>
    </div>
    """


def _build_status_card(status: str, slots: list) -> str:
    meta = _status_meta(status)
    slot_count = len([slot for slot in slots if not slot.is_teacher])
    drowsy_count = sum(1 for s in slots if s.status == "DROWSY")
    absent_count = sum(1 for s in slots if s.status == "ABSENT")
    yawn_count = sum(1 for s in slots if s.status == "YAWN")

    chips = [f"감지 학생 {slot_count}명"]
    if drowsy_count:
        chips.append(f"졸음 {drowsy_count}명")
    if absent_count:
        chips.append(f"이탈 {absent_count}명")
    if yawn_count:
        chips.append(f"하품 {yawn_count}명")

    chip_html = "".join(f'<span class="status-chip">{html.escape(chip)}</span>' for chip in chips)
    return f"""
    <div class="live-panel-card status-card" style="--status-bg:{meta['bg']}; --status-color:{meta['color']};">
        <div class="live-panel-card-head">
            <div>
                <div class="live-panel-eyebrow">Current Status</div>
                <div class="live-panel-title">현재 상태</div>
            </div>
            <div class="status-orb">{meta['icon']}</div>
        </div>
        <div class="status-hero">{html.escape(meta['label'])}</div>
        <div class="status-description">{html.escape(meta['desc'])}</div>
        <div class="status-chip-row">{chip_html}</div>
    </div>
    """


def _build_slot_list(slots: list) -> str:
    visible_slots = [slot for slot in slots if not slot.is_teacher]
    if not visible_slots:
        body = '<div class="empty-block">감지된 수강생이 없습니다.</div>'
    else:
        rows = []
        for slot in visible_slots:
            meta = _status_meta(slot.status)
            rows.append(
                f"""
                <div class="participant-row">
                    <div class="participant-main">
                        <span class="participant-dot" style="background:{meta['color']};"></span>
                        <div>
                            <div class="participant-name">{html.escape(slot.name)}</div>
                            <div class="participant-copy">{html.escape(meta['desc'])}</div>
                        </div>
                    </div>
                    <div class="participant-state" style="color:{meta['color']};">{html.escape(meta['label'])}</div>
                </div>
                """
            )
        body = "".join(rows)

    return f"""
    <div class="live-panel-card">
        <div class="live-panel-card-head">
            <div>
                <div class="live-panel-eyebrow">Participants</div>
                <div class="live-panel-title">현재 상태 리스트</div>
            </div>
        </div>
        <div class="participant-list">{body}</div>
    </div>
    """


def _build_alert_card(alerts: list[dict]) -> str:
    if not alerts:
        body = '<div class="empty-block">기록된 실시간 알림이 없습니다.</div>'
    else:
        rows = []
        for alert in alerts[:8]:
            bg, border, color = _alert_color(alert["type"])
            rows.append(
                f"""
                <div class="alert-row" style="background:{bg}; border-color:{border};">
                    <div class="alert-icon" style="color:{color};">●</div>
                    <div class="alert-copy">
                        <div class="alert-title">{html.escape(alert['message'])}</div>
                        <div class="alert-time">{html.escape(_format_time(alert['timestamp']))}</div>
                    </div>
                </div>
                """
            )
        body = "".join(rows)

    return f"""
    <div class="live-panel-card">
        <div class="live-panel-card-head">
            <div>
                <div class="live-panel-eyebrow">Realtime Alerts</div>
                <div class="live-panel-title">실시간 알림</div>
            </div>
        </div>
        <div class="alert-list">{body}</div>
    </div>
    """


def render_panel_html(
    camera_state: str,
    status: str,
    alert: str,
    report: str,
    is_running: bool,
    slots: Optional[list] = None,
) -> str:
    del camera_state, alert, report
    slots = slots or []
    alerts = deepcopy(PANEL_STATE["alerts"])
    return f"""
    <div class="live-panel-shell">
        {_build_control_panel(is_running)}
        {_build_status_card(status, slots)}
        {_build_slot_list(slots)}
        {_build_alert_card(alerts)}
    </div>
    """


def _latest_alert_text() -> str:
    if not PANEL_STATE["alerts"]:
        return "알림이 없습니다."
    return PANEL_STATE["alerts"][0]["message"]


def _report_text() -> str:
    stats = PANEL_STATE["slot_stats"]
    elapsed = _elapsed_sec()
    lines = [f"Total Time: {_format_duration(elapsed)}"]
    for _, stat in sorted(stats.items()):
        total = stat["normal"] + stat["drowsy"] + stat["absent"] + stat["yawn"]
        pct = round((stat["normal"] / total) * 100) if total > 0 else 0
        lines.append(f"{stat['name']}: {pct}% 정상")
    return "\n".join(lines)


def _build_recommendation_block(title: str, body: str, tone: str = "neutral") -> str:
    return f"""
    <div class="report-recommendation tone-{tone}">
        <div class="report-recommendation-title">{title}</div>
        <div class="report-recommendation-text">{body}</div>
    </div>
    """


def _live_report_html() -> str:
    stats = PANEL_STATE["slot_stats"]
    alerts = deepcopy(PANEL_STATE["alerts"])
    student_count = len(stats)
    total_frames = sum(
        stat["normal"] + stat["drowsy"] + stat["absent"] + stat["yawn"]
        for stat in stats.values()
    )
    normal_frames = sum(stat["normal"] for stat in stats.values())
    drowsy_events = sum(stat["drowsy"] for stat in stats.values())
    absent_events = sum(stat["absent"] for stat in stats.values())
    focus_rate = round((normal_frames / total_frames) * 100) if total_frames > 0 else 0

    summary_html = "".join(
        f"""
        <div class="report-stat-card">
            <div class="report-stat-label">{label}</div>
            <div class="report-stat-value">{value}</div>
        </div>
        """
        for label, value in [
            ("총 참여자", f"{student_count}명"),
            ("평균 집중도", f"{focus_rate}%"),
            ("졸음 감지", f"{drowsy_events}회"),
            ("이탈 감지", f"{absent_events}회"),
        ]
    )

    if stats:
        participant_rows = []
        for _, stat in sorted(stats.items()):
            total = stat["normal"] + stat["drowsy"] + stat["absent"] + stat["yawn"]
            normal_pct = round((stat["normal"] / total) * 100) if total > 0 else 0
            drowsy_pct = round((stat["drowsy"] / total) * 100) if total > 0 else 0
            absent_pct = round((stat["absent"] / total) * 100) if total > 0 else 0
            participant_rows.append(
                f"""
                <div class="participant-summary-row">
                    <div class="participant-summary-top">
                        <span class="participant-summary-name">{html.escape(stat['name'])}</span>
                        <span class="participant-summary-rate">집중도 {normal_pct}%</span>
                    </div>
                    <div class="participant-bar">
                        <span class="bar-normal" style="width:{normal_pct}%;"></span>
                        <span class="bar-drowsy" style="width:{drowsy_pct}%;"></span>
                        <span class="bar-absent" style="width:{absent_pct}%;"></span>
                    </div>
                    <div class="participant-summary-meta">정상 {normal_pct}% · 졸음 {stat['drowsy']}회 · 이탈 {stat['absent']}회 · 하품 {stat['yawn']}회</div>
                </div>
                """
            )
        participant_html = "".join(participant_rows)
    else:
        participant_html = '<div class="report-empty">아직 누적된 실시간 분석 데이터가 없습니다.</div>'

    if alerts:
        event_html = "".join(
            f"""
            <div class="report-event">
                <div class="report-event-title">{html.escape(alert['message'])}</div>
                <div class="report-event-meta">{html.escape(_format_time(alert['timestamp']))}</div>
            </div>
            """
            for alert in alerts[:8]
        )
    else:
        event_html = '<div class="report-empty">기록된 알림이 없습니다.</div>'

    recommendations = "".join(
        [
            _build_recommendation_block(
                "실시간 요약",
                f"분석 시간 {_format_duration(_elapsed_sec())} 동안 누적된 상태를 요약했습니다. 최신 이벤트는 {_latest_alert_text()}",
                "blue",
            ),
            _build_recommendation_block(
                "분석 관찰 포인트",
                "현재 Python UI에서는 누적 이벤트와 참여자 비율 중심으로 연결했습니다. figmaApp의 차트형 구성은 추후 실데이터 축적 시 확장할 수 있도록 카드 구조를 분리해 두었습니다.",
                "purple",
            ),
        ]
    )

    return f"""
    <div class="report-summary-grid">
        {summary_html}
    </div>
    <div class="report-two-column">
        <div class="report-block">
            <div class="report-block-title">참여자별 통계</div>
            {participant_html}
        </div>
        <div class="report-block">
            <div class="report-block-title">이벤트 로그</div>
            <div class="report-events">{event_html}</div>
        </div>
    </div>
    <div class="report-block">
        <div class="report-block-title">분석 결과 및 제안</div>
        <div class="report-recommendation-grid">{recommendations}</div>
    </div>
    """


def _upload_report_html() -> str:
    video_name = UPLOAD_ANALYSIS_STATE["video_name"] or "선택된 영상 없음"
    class_start_time = UPLOAD_ANALYSIS_STATE["class_start_time"] or "-"
    completed_at = UPLOAD_ANALYSIS_STATE["completed_at"] or "-"
    summary = UPLOAD_ANALYSIS_STATE["summary"]
    event_placeholder = """
    <div class="report-event">
        <div class="report-event-title">배치 추론 이벤트 placeholder</div>
        <div class="report-event-meta">실제 업로드 분석 함수 결과 연결 전 임시 카드입니다.</div>
    </div>
    """
    return f"""
    <div class="report-summary-grid">
        <div class="report-stat-card">
            <div class="report-stat-label">업로드 파일</div>
            <div class="report-stat-value report-stat-value-sm">{html.escape(video_name)}</div>
        </div>
        <div class="report-stat-card">
            <div class="report-stat-label">수업 시작</div>
            <div class="report-stat-value">{html.escape(class_start_time)}</div>
        </div>
        <div class="report-stat-card">
            <div class="report-stat-label">분석 상태</div>
            <div class="report-stat-value accent-purple">완료</div>
        </div>
        <div class="report-stat-card">
            <div class="report-stat-label">리포트 생성</div>
            <div class="report-stat-value report-stat-value-sm">{html.escape(completed_at)}</div>
        </div>
    </div>
    <div class="report-two-column">
        <div class="report-block">
            <div class="report-block-title">업로드 분석 요약</div>
            <div class="report-block-text">{html.escape(summary)}</div>
            <div class="report-helper-note">
                TODO: 실제 배치 추론 결과가 준비되면 이 카드에 시간대별 분석 차트와 핵심 지표를 연결하세요.
            </div>
        </div>
        <div class="report-block">
            <div class="report-block-title">주요 상태 / 이벤트 영역</div>
            <div class="report-events">
                {event_placeholder}
                {event_placeholder}
            </div>
        </div>
    </div>
    <div class="report-block">
        <div class="report-block-title">연결 메모</div>
        <div class="report-block-text">
            현재는 기존 Python 프로젝트의 UI/상태 전환을 우선 정리한 단계입니다.
            <code>process_uploaded_video(...)</code> 내부에 실제 배치 추론 함수를 연결하면 이 리포트 카드 구조를 그대로 재사용할 수 있습니다.
        </div>
    </div>
    """


def show_home_view():
    return _view_updates("home")


def show_live_view():
    return _view_updates("live")


def show_upload_view():
    return _view_updates("upload")


def show_live_report_view():
    return (
        *_view_updates("report"),
        build_report_shell_html(
            _live_report_html(),
            title="실시간 분석 리포트",
            subtitle="실시간 페이지 우측 상단 버튼에서 이동한 누적 리포트입니다.",
        ),
    )


def show_upload_report_view():
    return (
        *_view_updates("report"),
        build_report_shell_html(
            _upload_report_html(),
            title="업로드 분석 리포트",
            subtitle="녹화 분석 완료 후 자동으로 이동한 결과 화면입니다.",
        ),
    )


def describe_uploaded_file(video_path: str | None):
    if not video_path:
        return (
            build_upload_status_html(),
            "영상과 수업 시작 시간을 입력한 뒤 분석을 시작하세요.",
        )

    path = Path(video_path)
    size_bytes = path.stat().st_size if path.exists() else 0
    size_mb = size_bytes / (1024 * 1024) if size_bytes else 0
    meta = f"파일 크기 {size_mb:.2f} MB"
    return (
        build_upload_status_html(path.name, meta, is_ready=True),
        f"{path.name} 업로드가 준비되었습니다. 수업 시작 시간을 입력하고 분석을 시작하세요.",
    )


def process_uploaded_video(video_path: str | None, class_start_time: str):
    if not video_path:
        error_html = """
        <div class="report-block">
            <div class="report-block-title">업로드 오류</div>
            <div class="report-block-text">분석할 영상을 먼저 업로드해 주세요.</div>
        </div>
        """
        return (
            *_view_updates("upload"),
            build_report_shell_html(error_html),
            "영상 파일을 먼저 선택해 주세요.",
        )

    if not class_start_time:
        error_html = """
        <div class="report-block">
            <div class="report-block-title">입력 오류</div>
            <div class="report-block-text">수업 시작 시간을 입력해 주세요.</div>
        </div>
        """
        return (
            *_view_updates("upload"),
            build_report_shell_html(error_html),
            "수업 시작 시간을 입력해 주세요.",
        )

    UPLOAD_ANALYSIS_STATE["video_name"] = Path(video_path).name
    UPLOAD_ANALYSIS_STATE["class_start_time"] = class_start_time
    UPLOAD_ANALYSIS_STATE["completed_at"] = _now_ts().strftime("%Y-%m-%d %H:%M")
    UPLOAD_ANALYSIS_STATE["summary"] = (
        f"{Path(video_path).name} 파일에 대한 업로드 분석 흐름이 완료되었습니다. "
        f"수업 시작 시간은 {class_start_time}로 기록되었고, 분석 완료 후 리포트 페이지로 자동 이동했습니다."
    )
    return (
        *_view_updates("report"),
        build_report_shell_html(
            _upload_report_html(),
            title="업로드 분석 리포트",
            subtitle="녹화 분석 완료 후 자동으로 이동한 결과 화면입니다.",
        ),
        f"{Path(video_path).name} 분석이 완료되어 리포트 화면으로 이동했습니다.",
    )


def _debug_text(snapshot: RuntimeSnapshot) -> str:
    return snapshot.debug_text


def _slots_to_json(slots) -> str:
    return json.dumps(
        [
            {
                "slot_id": s.slot_id,
                "name": s.name,
                "status": s.status,
                "ear": round(float(s.ear), 3),
                "mar": round(float(s.mar), 3),
                "box_pct": [round(v, 6) for v in s.box_pct],
                "face_box_pct": [round(v, 6) for v in s.face_box_pct] if s.face_box_pct else [],
                "noface": s.noface,
            }
            for s in slots
            if not s.is_teacher
        ]
    )


def _render_outputs(snapshot: RuntimeSnapshot, ack: int, _annotated_frame=None):
    slots = list(snapshot.slots)
    panel_html = render_panel_html(
        camera_state="ON" if snapshot.running else "OFF",
        status=snapshot.status,
        alert=_latest_alert_text(),
        report=_report_text(),
        is_running=snapshot.running,
        slots=slots,
    )
    return (
        snapshot.status,
        _latest_alert_text(),
        _report_text(),
        panel_html,
        _debug_text(snapshot),
        ack,
        _slots_to_json(slots),
    )


def on_start():
    _reset_panel_state()
    snapshot = RUNTIME.start()
    _sync_panel_state(snapshot)
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
    panel_html = render_panel_html(
        camera_state="OFF",
        status=snapshot.status,
        alert=_latest_alert_text(),
        report=_report_text(),
        is_running=False,
        slots=list(snapshot.slots),
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
