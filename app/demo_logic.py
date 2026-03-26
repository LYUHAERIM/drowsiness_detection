from __future__ import annotations

import html
import json
import time
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Optional

import gradio as gr

from app.inference.runtime import RUNTIME, RuntimeSnapshot
from app.ui.templates import build_report_shell_html

Status = str


# ─────────────────────────────────────────────────────────────────────────────
# PANEL_STATE: 동적 슬롯 기반 (실시간 YOLO 결과 사용)
# ─────────────────────────────────────────────────────────────────────────────

ALERT_COOLDOWN_SEC = 30  # 같은 학생에게 동일 알림 재발생 최소 간격

PANEL_STATE: dict = {
    "is_running": False,
    "session_started_at": None,
    "slot_stats": {},           # slot_id -> {"name", "normal", "drowsy", "absent", "yawn"}
    "prev_statuses": {},        # slot_id -> 이전 상태
    "last_alert_time": {},      # name -> 마지막 알림 시각 (스팸 방지)
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
    # infer_video.py STATE_COLORS (BGR→RGB) 기준으로 통일
    normalized = (status or "NORMAL").upper()
    if normalized == "DROWSY":
        return {"label": "졸음", "color": "#ff0000", "bg": "rgba(255, 0, 0, 0.10)", "desc": "졸음이 감지되었습니다", "icon": "⚠"}
    if normalized == "YAWN":
        return {"label": "하품", "color": "#ff8000", "bg": "rgba(255, 128, 0, 0.10)", "desc": "하품이 감지되었습니다", "icon": "○"}
    if normalized == "ABSENT":
        return {"label": "이탈", "color": "#ffa500", "bg": "rgba(255, 165, 0, 0.10)", "desc": "자리를 이탈했습니다", "icon": "◌"}
    if normalized == "IGNORE":
        return {"label": "무시", "color": "#a0a0a0", "bg": "rgba(160, 160, 160, 0.10)", "desc": "감지 제외 상태", "icon": "—"}
    return {"label": "정상", "color": "#46dc46", "bg": "rgba(70, 220, 70, 0.10)", "desc": "수업에 집중하고 있습니다", "icon": "◉"}


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

        # 슬롯 통계 초기화
        if sid not in PANEL_STATE["slot_stats"]:
            PANEL_STATE["slot_stats"][sid] = {
                "name": name,
                "normal": 0, "drowsy": 0, "absent": 0, "yawn": 0,
            }
        else:
            PANEL_STATE["slot_stats"][sid]["name"] = name

        # 프레임 카운트 누적
        stat = PANEL_STATE["slot_stats"][sid]
        if status == "DROWSY":
            stat["drowsy"] += 1
        elif status == "ABSENT":
            stat["absent"] += 1
        elif status == "YAWN":
            stat["yawn"] += 1
        else:
            stat["normal"] += 1

        # 상태 변화 알림 (이름 기준 쿨다운으로 스팸 방지)
        prev = PANEL_STATE["prev_statuses"].get(sid, "NORMAL")
        if prev != status and status not in ("NORMAL", "YAWN"):
            now = time.time()
            last_t = PANEL_STATE["last_alert_time"].get(name, 0)
            if now - last_t >= ALERT_COOLDOWN_SEC:
                if status == "DROWSY":
                    _push_alert("DROWSY", f"⚠️ {name} 졸음이 감지되었습니다!")
                elif status == "ABSENT":
                    _push_alert("ABSENT", f"🚨 {name} 자리를 이탈했습니다!")
                PANEL_STATE["last_alert_time"][name] = now
        PANEL_STATE["prev_statuses"][sid] = status


def _format_time(dt: datetime) -> str:
    return dt.strftime("%p %I:%M:%S").replace("AM", "오전").replace("PM", "오후")


def _format_duration(seconds: int) -> str:
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins}:{secs:02d}"


def _percent(part: int, whole: int) -> str:
    if whole <= 0:
        return "0.0%"
    return f"{(part / whole) * 100:.1f}%"


def _elapsed_sec() -> int:
    if PANEL_STATE["session_started_at"] is None:
        return 0
    return int(time.time() - PANEL_STATE["session_started_at"])


def _alert_color(alert_type: str) -> tuple[str, str]:
    if alert_type == "DROWSY":
        return ("rgba(245, 158, 11, 0.05)", "rgba(245, 158, 11, 0.30)")
    if alert_type == "ABSENT":
        return ("rgba(239, 68, 68, 0.05)", "rgba(239, 68, 68, 0.30)")
    return ("rgba(16, 185, 129, 0.05)", "rgba(16, 185, 129, 0.30)")


def _view_updates(active: str):
    return (
        gr.update(visible=active == "home"),
        gr.update(visible=active == "live"),
        gr.update(visible=active == "upload"),
        gr.update(visible=active == "report"),
    )


# ─────────────────────────────────────────────────────────────────────────────
# HTML 빌더
# ─────────────────────────────────────────────────────────────────────────────

def _build_control_panel(is_running: bool) -> str:
    start_disabled = "opacity:0.5;cursor:not-allowed;" if is_running else "cursor:pointer;"
    stop_disabled = "opacity:0.5;cursor:not-allowed;" if not is_running else "cursor:pointer;"
    start_onclick = "" if is_running else 'onclick="triggerPanelStart()"'
    stop_onclick = "" if not is_running else 'onclick="triggerPanelStop()"'

    live_html = (
        """
    <div style="
        margin-top:16px; padding:12px; border-radius:12px;
        background:rgba(16,185,129,0.10); border:1px solid rgba(16,185,129,0.30);
        text-align:center; color:#34d399; font-size:14px;
    ">● 실시간 분석 중...</div>
    """ if is_running else ""
    )

    return f"""
    <div style="border-radius:12px; padding:24px; background:rgba(24,24,27,0.5); border:1px solid #27272a;">
        <div style="color:#d4d4d8; font-size:18px; font-weight:600; margin-bottom:16px;">제어</div>
        <div style="display:flex; gap:12px;">
            <button {start_onclick} style="flex:1; display:flex; align-items:center; justify-content:center; gap:8px;
                padding:12px 24px; border:none; border-radius:8px; background:#10b981; color:white;
                font-size:16px; font-weight:600; transition:all 0.2s ease; {start_disabled}">
                ▶ 시작
            </button>
            <button {stop_onclick} style="flex:1; display:flex; align-items:center; justify-content:center; gap:8px;
                padding:12px 24px; border:none; border-radius:8px; background:#ef4444; color:white;
                font-size:16px; font-weight:600; transition:all 0.2s ease; {stop_disabled}">
                ■ 중지
            </button>
        </div>
        {live_html}
    </div>
    """


def _build_status_card(status: str, slots: list) -> str:
    meta = _status_meta(status)
    slot_count = len(slots)
    drowsy_count = sum(1 for s in slots if s.status == "DROWSY")
    yawn_count   = sum(1 for s in slots if s.status == "YAWN")
    absent_count = sum(1 for s in slots if s.status == "ABSENT")

    summary = f"감지된 학생 {slot_count}명"
    if drowsy_count:
        summary += f" | 졸음 {drowsy_count}명"
    if yawn_count:
        summary += f" | 하품 {yawn_count}명"
    if absent_count:
        summary += f" | 이탈 {absent_count}명"

    return f"""
    <div style="border-radius:12px; padding:24px; background:{meta['bg']}; border:1px solid #27272a;">
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:16px;">
            <div style="font-size:18px; font-weight:600; color:#d4d4d8;">현재 상태</div>
            <div style="width:12px; height:12px; border-radius:9999px; background:{meta['color']};"></div>
        </div>
        <div style="display:flex; align-items:center; gap:16px;">
            <div style="width:64px; height:64px; border-radius:9999px; background:{meta['bg']};
                display:flex; align-items:center; justify-content:center;
                color:{meta['color']}; font-size:28px; font-weight:800;">
                {meta['icon']}
            </div>
            <div style="flex:1;">
                <div style="font-size:30px; font-weight:700; color:{meta['color']}; margin-bottom:4px;">
                    {html.escape(meta['label'])}
                </div>
                <div style="font-size:13px; color:#a1a1aa;">{html.escape(summary)}</div>
            </div>
        </div>
    </div>
    """


def _build_slot_list(slots: list) -> str:
    if not slots:
        return """
        <div style="border-radius:12px; padding:24px; background:rgba(24,24,27,0.5); border:1px solid #27272a;">
            <div style="color:#d4d4d8; font-size:18px; font-weight:600; margin-bottom:12px;">수강생 현황</div>
            <div style="text-align:center; padding:24px 0; color:#71717a;">감지된 수강생이 없습니다</div>
        </div>
        """

    rows = []
    for s in slots:
        if s.is_teacher:
            continue
        meta = _status_meta(s.status)
        rows.append(f"""
        <div style="display:flex; align-items:center; gap:12px; padding:10px;
            border-radius:8px; background:rgba(39,39,42,0.5);">
            <div style="width:10px; height:10px; border-radius:9999px; background:{meta['color']}; flex-shrink:0;"></div>
            <div style="flex:1; font-size:14px; color:#e4e4e7;">{html.escape(s.name)}</div>
            <div style="font-size:13px; color:{meta['color']}; font-weight:600;">{html.escape(meta['label'])}</div>
        </div>
        """)

    items_html = "".join(rows) if rows else '<div style="text-align:center;padding:16px 0;color:#71717a;">감지된 수강생이 없습니다</div>'

    return f"""
    <div style="border-radius:12px; padding:24px; background:rgba(24,24,27,0.5); border:1px solid #27272a;">
        <div style="color:#d4d4d8; font-size:18px; font-weight:600; margin-bottom:12px;">수강생 현황</div>
        <div style="display:flex; flex-direction:column; gap:8px; max-height:240px; overflow-y:auto;">
            {items_html}
        </div>
    </div>
    """


def _build_alert_card(alerts: list[dict]) -> str:
    if not alerts:
        items_html = '<div style="text-align:center; padding:32px 0; color:#71717a;">알림이 없습니다</div>'
    else:
        cards = []
        for alert in alerts[:10]:
            bg, border = _alert_color(alert["type"])
            cards.append(f"""
            <div style="border-radius:8px; padding:16px; border:1px solid {border}; background:{bg};">
                <div style="display:flex; align-items:flex-start; gap:12px;">
                    <div style="width:20px; min-width:20px; margin-top:2px; color:#a1a1aa; font-size:16px;">!</div>
                    <div style="flex:1; min-width:0;">
                        <div style="font-size:14px; color:#e4e4e7; line-height:1.5;">
                            {html.escape(alert['message'])}
                        </div>
                        <div style="margin-top:4px; font-size:12px; color:#71717a;">
                            {html.escape(_format_time(alert['timestamp']))}
                        </div>
                    </div>
                </div>
            </div>
            """)
        items_html = "".join(cards)

    return f"""
    <div style="border-radius:12px; padding:24px; background:rgba(24,24,27,0.5); border:1px solid #27272a;">
        <div style="font-size:18px; font-weight:600; color:#d4d4d8; margin-bottom:16px;">알림</div>
        <div style="display:flex; flex-direction:column; gap:12px; max-height:256px; overflow-y:auto;">
            {items_html}
        </div>
    </div>
    """


def _build_report_card() -> str:
    stats = PANEL_STATE["slot_stats"]
    elapsed = _elapsed_sec()

    if not stats:
        return f"""
        <div style="border-radius:12px; padding:24px; background:rgba(24,24,27,0.5); border:1px solid #27272a;">
            <div style="font-size:18px; font-weight:600; color:#d4d4d8; margin-bottom:16px;">리포트</div>
            <div style="font-size:28px; font-weight:700; color:#fff; margin-bottom:8px;">
                {_format_duration(elapsed)}
            </div>
            <div style="text-align:center; padding:16px 0; color:#71717a;">분석 데이터 없음</div>
        </div>
        """

    student_rows = []
    for sid, stat in sorted(stats.items()):
        total = stat["normal"] + stat["drowsy"] + stat["absent"] + stat["yawn"]
        if total <= 0:
            continue
        normal_w = (stat["normal"] / total) * 100
        drowsy_w = (stat["drowsy"] / total) * 100
        absent_w = (stat["absent"] / total) * 100
        normal_pct = round((stat["normal"] / total) * 100)
        student_rows.append(f"""
        <div style="padding:8px; border-radius:8px; background:rgba(39,39,42,0.5); font-size:12px;">
            <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:4px;">
                <span style="color:#d4d4d8; font-weight:500;">{html.escape(stat['name'])}</span>
                <span style="color:#a1a1aa;">{normal_pct}% 정상</span>
            </div>
            <div style="display:flex; gap:1px; height:6px; border-radius:9999px; overflow:hidden; background:#3f3f46;">
                <div style="background:#10b981; width:{normal_w}%;"></div>
                <div style="background:#f59e0b; width:{drowsy_w}%;"></div>
                <div style="background:#ef4444; width:{absent_w}%;"></div>
            </div>
        </div>
        """)

    rows_html = "".join(student_rows)

    return f"""
    <div style="border-radius:12px; padding:24px; background:rgba(24,24,27,0.5); border:1px solid #27272a;">
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:24px;">
            <div style="font-size:18px; color:#a1a1aa;">▣</div>
            <div style="font-size:18px; font-weight:600; color:#d4d4d8;">리포트</div>
        </div>
        <div style="margin-bottom:24px; padding:16px; border-radius:8px; background:rgba(39,39,42,0.5);">
            <div style="display:flex; align-items:center; gap:8px; color:#a1a1aa; font-size:14px; margin-bottom:4px;">
                <span>◷</span><span>총 분석 시간</span>
            </div>
            <div style="font-size:28px; font-weight:700; color:#fff;">{_format_duration(elapsed)}</div>
        </div>
        <div style="display:flex; flex-direction:column; gap:8px; max-height:200px; overflow-y:auto;">
            {rows_html}
        </div>
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
    if slots is None:
        slots = []

    alerts = deepcopy(PANEL_STATE["alerts"])

    return f"""
    <div style="height:100%; padding:24px; background:#18181b; display:flex; flex-direction:column;
        gap:16px; overflow-y:auto; box-sizing:border-box;">
        {_build_control_panel(is_running)}
        {_build_status_card(status, slots)}
        {_build_slot_list(slots)}
        {_build_alert_card(alerts)}
        {_build_report_card()}
    </div>
    """


# ─────────────────────────────────────────────────────────────────────────────
# 공개 API
# ─────────────────────────────────────────────────────────────────────────────

def _latest_alert_text() -> str:
    if not PANEL_STATE["alerts"]:
        return "알림이 없습니다."
    return PANEL_STATE["alerts"][0]["message"]


def _report_text() -> str:
    stats = PANEL_STATE["slot_stats"]
    elapsed = _elapsed_sec()
    lines = [f"Total Time: {_format_duration(elapsed)}"]
    for sid, stat in sorted(stats.items()):
        total = stat["normal"] + stat["drowsy"] + stat["absent"] + stat["yawn"]
        pct = round((stat["normal"] / total) * 100) if total > 0 else 0
        lines.append(f"{stat['name']}: {pct}% 정상")
    return "\n".join(lines)


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

    summary_rows = [
        ("총 참여자", f"{student_count}명"),
        ("평균 집중도", f"{focus_rate}%"),
        ("졸음 감지", f"{drowsy_events}회"),
        ("이탈 감지", f"{absent_events}회"),
    ]
    summary_html = "".join(
        f"""
        <div class="report-stat-card">
            <div class="report-stat-label">{label}</div>
            <div class="report-stat-value">{value}</div>
        </div>
        """
        for label, value in summary_rows
    )

    if stats:
        participant_items = []
        for _, stat in sorted(stats.items()):
            total = stat["normal"] + stat["drowsy"] + stat["absent"] + stat["yawn"]
            normal_pct = round((stat["normal"] / total) * 100) if total > 0 else 0
            participant_items.append(
                f"<li>{html.escape(stat['name'])}: 정상 {normal_pct}%, 졸음 {stat['drowsy']}회, 이탈 {stat['absent']}회, 하품 {stat['yawn']}회</li>"
            )
        participant_html = f'<ul class="report-list">{"".join(participant_items)}</ul>'
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

    return f"""
    <div class="report-summary-grid">
        {summary_html}
    </div>
    <div class="report-block">
        <div class="report-block-title">실시간 요약</div>
        <div class="report-block-text">
            분석 시간 {_format_duration(_elapsed_sec())} 동안 누적된 실시간 상태를 정리했습니다.
            최신 상태는 {_latest_alert_text()}
        </div>
    </div>
    <div class="report-block">
        <div class="report-block-title">참여자별 통계</div>
        {participant_html}
    </div>
    <div class="report-block">
        <div class="report-block-title">이벤트 로그</div>
        <div class="report-events">{event_html}</div>
    </div>
    """


def _upload_report_html() -> str:
    video_name = UPLOAD_ANALYSIS_STATE["video_name"] or "선택된 영상 없음"
    class_start_time = UPLOAD_ANALYSIS_STATE["class_start_time"] or "-"
    completed_at = UPLOAD_ANALYSIS_STATE["completed_at"] or "-"
    summary = UPLOAD_ANALYSIS_STATE["summary"]
    return f"""
    <div class="report-summary-grid">
        <div class="report-stat-card">
            <div class="report-stat-label">업로드 파일</div>
            <div class="report-stat-value">{html.escape(video_name)}</div>
        </div>
        <div class="report-stat-card">
            <div class="report-stat-label">수업 시작</div>
            <div class="report-stat-value">{html.escape(class_start_time)}</div>
        </div>
        <div class="report-stat-card">
            <div class="report-stat-label">분석 상태</div>
            <div class="report-stat-value">완료</div>
        </div>
        <div class="report-stat-card">
            <div class="report-stat-label">리포트 생성</div>
            <div class="report-stat-value">{html.escape(completed_at)}</div>
        </div>
    </div>
    <div class="report-block">
        <div class="report-block-title">업로드 분석 요약</div>
        <div class="report-block-text">{html.escape(summary)}</div>
    </div>
    <div class="report-block">
        <div class="report-block-title">추후 배치 추론 연결 위치</div>
        <div class="report-block-text">
            현재는 UI 흐름 확인용 결과입니다. 실제 배치 추론 결과를 연결할 때는
            <code>process_uploaded_video(...)</code> 내부에서 분석 실행 후 이 리포트 HTML을 갱신하면 됩니다.
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
    return (*_view_updates("report"), build_report_shell_html(_live_report_html()))


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
        f"수업 시작 시간은 {class_start_time}로 기록되었으며, "
        "추후 실제 배치 추론 결과를 이 위치에 연결할 수 있습니다."
    )
    return (
        *_view_updates("report"),
        build_report_shell_html(_upload_report_html()),
        f"{Path(video_path).name} 분석이 완료되어 리포트 화면으로 이동했습니다.",
    )


def _debug_text(snapshot: RuntimeSnapshot) -> str:
    return snapshot.debug_text


def _slots_to_json(slots) -> str:
    """SlotInfo 목록을 JS bbox 오버레이용 JSON 문자열로 직렬화."""
    return json.dumps([{
        "slot_id": s.slot_id,
        "name": s.name,
        "status": s.status,
        "ear": round(float(s.ear), 3),
        "mar": round(float(s.mar), 3),
        "box_pct": [round(v, 6) for v in s.box_pct],
        "face_box_pct": [round(v, 6) for v in s.face_box_pct] if s.face_box_pct else [],
        "noface": s.noface,
    } for s in slots if not s.is_teacher])


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
    # is_running_state(gr.State) 대신 RUNTIME 내부 상태를 직접 참조
    # (queue=False race condition 방지)
    snapshot, annotated_frame = RUNTIME.process_frame(frame_data)
    _sync_panel_state(snapshot)
    return _render_outputs(snapshot, frame_seq, annotated_frame)
