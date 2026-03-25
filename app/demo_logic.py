from __future__ import annotations

import html
import math
import time
from copy import deepcopy
from datetime import datetime

from app.inference.runtime import RUNTIME, RuntimeSnapshot

Status = str

MOCK_CSV_DATA = [
    {
        "timestamp": "00:00:00",
        "student1": "NORMAL",
        "student2": "NORMAL",
        "student4": "NORMAL",
        "student5": "NORMAL",
    },
    {
        "timestamp": "00:00:02",
        "student1": "NORMAL",
        "student2": "DROWSY",
        "student4": "NORMAL",
        "student5": "NORMAL",
    },
    {
        "timestamp": "00:00:04",
        "student1": "DROWSY",
        "student2": "NORMAL",
        "student4": "NORMAL",
        "student5": "NORMAL",
    },
    {
        "timestamp": "00:00:06",
        "student1": "NORMAL",
        "student2": "NORMAL",
        "student4": "ABSENT",
        "student5": "NORMAL",
    },
    {
        "timestamp": "00:00:08",
        "student1": "NORMAL",
        "student2": "NORMAL",
        "student4": "NORMAL",
        "student5": "DROWSY",
    },
    {
        "timestamp": "00:00:10",
        "student1": "ABSENT",
        "student2": "NORMAL",
        "student4": "NORMAL",
        "student5": "NORMAL",
    },
]

STUDENT_NAMES = {
    "student1": "강현민",
    "student2": "박현승",
    "student3": "나",
    "student4": "김주원",
    "student5": "김대희",
}


def _initial_report_data():
    return {
        "students": [
            {"id": 1, "name": "강현민", "normal": 0, "drowsy": 0, "absent": 0},
            {"id": 2, "name": "박현승", "normal": 0, "drowsy": 0, "absent": 0},
            {"id": 3, "name": "나", "normal": 0, "drowsy": 0, "absent": 0},
            {"id": 4, "name": "김주원", "normal": 0, "drowsy": 0, "absent": 0},
            {"id": 5, "name": "김대희", "normal": 0, "drowsy": 0, "absent": 0},
        ],
        "total_time": 0,
    }


PANEL_STATE = {
    "is_running": False,
    "session_started_at": None,
    "last_csv_step": 0,
    "last_report_second": 0,
    "current_data_index": 0,
    "my_status": "NORMAL",
    "prev_my_status": "NORMAL",
    "other_students_status": {
        "student1": "NORMAL",
        "student2": "NORMAL",
        "student4": "NORMAL",
        "student5": "NORMAL",
    },
    "alerts": [],
    "report_data": _initial_report_data(),
}


def _reset_panel_state() -> None:
    PANEL_STATE["is_running"] = True
    PANEL_STATE["session_started_at"] = time.time()
    PANEL_STATE["last_csv_step"] = 0
    PANEL_STATE["last_report_second"] = 0
    PANEL_STATE["current_data_index"] = 0
    PANEL_STATE["my_status"] = "NORMAL"
    PANEL_STATE["prev_my_status"] = "NORMAL"
    PANEL_STATE["other_students_status"] = {
        "student1": "NORMAL",
        "student2": "NORMAL",
        "student4": "NORMAL",
        "student5": "NORMAL",
    }
    PANEL_STATE["alerts"] = []
    PANEL_STATE["report_data"] = _initial_report_data()


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
    if normalized == "ABSENT":
        return {
            "label": "이탈",
            "color": "#ef4444",
            "bg": "rgba(239, 68, 68, 0.10)",
            "desc": "자리를 이탈했습니다",
            "icon": "◌",
        }
    return {
        "label": "정상",
        "color": "#10b981",
        "bg": "rgba(16, 185, 129, 0.10)",
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


def _advance_other_students(elapsed_sec: int) -> None:
    target_step = elapsed_sec // 2
    while PANEL_STATE["last_csv_step"] < target_step:
        next_index = (PANEL_STATE["current_data_index"] + 1) % len(MOCK_CSV_DATA)
        current_data = MOCK_CSV_DATA[next_index]

        new_statuses = {
            "student1": current_data["student1"].upper(),
            "student2": current_data["student2"].upper(),
            "student4": current_data["student4"].upper(),
            "student5": current_data["student5"].upper(),
        }

        for key, status in new_statuses.items():
            prev_status = PANEL_STATE["other_students_status"][key]
            if prev_status != status and status != "NORMAL":
                student_name = STUDENT_NAMES[key]
                message = (
                    f"⚠️ {student_name} 학생의 졸음이 감지되었습니다!"
                    if status == "DROWSY"
                    else f"🚨 {student_name} 학생이 자리를 이탈했습니다!"
                )
                _push_alert(status, message)

        PANEL_STATE["other_students_status"] = new_statuses
        PANEL_STATE["current_data_index"] = next_index
        PANEL_STATE["last_csv_step"] += 1


def _advance_my_status(snapshot_status: str) -> None:
    current_status = (snapshot_status or "NORMAL").upper()
    prev_status = PANEL_STATE["prev_my_status"]

    if prev_status != current_status and current_status != "NORMAL":
        message = (
            "⚠️ 내 졸음이 감지되었습니다. 집중해 주세요!"
            if current_status == "DROWSY"
            else "🚨 내가 자리를 이탈했습니다!"
        )
        _push_alert(current_status, message)

    PANEL_STATE["my_status"] = current_status
    PANEL_STATE["prev_my_status"] = current_status


def _advance_report(elapsed_sec: int) -> None:
    while PANEL_STATE["last_report_second"] < elapsed_sec:
        status_map = {
            1: PANEL_STATE["other_students_status"]["student1"],
            2: PANEL_STATE["other_students_status"]["student2"],
            3: PANEL_STATE["my_status"],
            4: PANEL_STATE["other_students_status"]["student4"],
            5: PANEL_STATE["other_students_status"]["student5"],
        }

        for student in PANEL_STATE["report_data"]["students"]:
            current_status = status_map[student["id"]]
            if current_status == "NORMAL":
                student["normal"] += 1
            elif current_status == "DROWSY":
                student["drowsy"] += 1
            else:
                student["absent"] += 1

        PANEL_STATE["report_data"]["total_time"] += 1
        PANEL_STATE["last_report_second"] += 1


def _sync_panel_state(snapshot: RuntimeSnapshot) -> None:
    if not PANEL_STATE["is_running"] or PANEL_STATE["session_started_at"] is None:
        return

    elapsed_sec = int(time.time() - PANEL_STATE["session_started_at"])
    _advance_other_students(elapsed_sec)
    _advance_my_status(snapshot.status)
    _advance_report(elapsed_sec)


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


def _student_normal_percent(student: dict) -> str:
    total = student["normal"] + student["drowsy"] + student["absent"]
    if total <= 0:
        return "0%"
    return f"{round((student['normal'] / total) * 100)}%"


def _get_total_stats(report_data: dict) -> dict:
    normal = sum(s["normal"] for s in report_data["students"])
    drowsy = sum(s["drowsy"] for s in report_data["students"])
    absent = sum(s["absent"] for s in report_data["students"])
    total = normal + drowsy + absent
    return {
        "normal": normal,
        "drowsy": drowsy,
        "absent": absent,
        "total": total,
    }


def _alert_color(alert_type: str) -> tuple[str, str]:
    if alert_type == "DROWSY":
        return ("rgba(245, 158, 11, 0.05)", "rgba(245, 158, 11, 0.30)")
    if alert_type == "ABSENT":
        return ("rgba(239, 68, 68, 0.05)", "rgba(239, 68, 68, 0.30)")
    return ("rgba(16, 185, 129, 0.05)", "rgba(16, 185, 129, 0.30)")


def _build_control_panel(is_running: bool) -> str:
    start_disabled = (
        "opacity:0.5;cursor:not-allowed;" if is_running else "cursor:pointer;"
    )
    stop_disabled = (
        "opacity:0.5;cursor:not-allowed;" if not is_running else "cursor:pointer;"
    )

    start_onclick = "" if is_running else 'onclick="triggerPanelStart()"'
    stop_onclick = "" if not is_running else 'onclick="triggerPanelStop()"'

    live_html = (
        """
    <div style="
        margin-top:16px;
        padding:12px;
        border-radius:12px;
        background:rgba(16,185,129,0.10);
        border:1px solid rgba(16,185,129,0.30);
        text-align:center;
        color:#34d399;
        font-size:14px;
    ">
        ● 실시간 분석 중...
    </div>
    """
        if is_running
        else ""
    )

    return f"""
    <div style="
        border-radius:12px;
        padding:24px;
        background:rgba(24,24,27,0.5);
        border:1px solid #27272a;
    ">
        <div style="
            color:#d4d4d8;
            font-size:18px;
            font-weight:600;
            margin-bottom:16px;
        ">제어</div>

        <div style="display:flex; gap:12px;">
            <button {start_onclick} style="
                flex:1;
                display:flex;
                align-items:center;
                justify-content:center;
                gap:8px;
                padding:12px 24px;
                border:none;
                border-radius:8px;
                background:#10b981;
                color:white;
                font-size:16px;
                font-weight:600;
                transition:all 0.2s ease;
                {start_disabled}
            ">
                ▶ 시작
            </button>

            <button {stop_onclick} style="
                flex:1;
                display:flex;
                align-items:center;
                justify-content:center;
                gap:8px;
                padding:12px 24px;
                border:none;
                border-radius:8px;
                background:#ef4444;
                color:white;
                font-size:16px;
                font-weight:600;
                transition:all 0.2s ease;
                {stop_disabled}
            ">
                ■ 중지
            </button>
        </div>

        {live_html}
    </div>
    """


def _build_status_card(status: str) -> str:
    meta = _status_meta(status)

    return f"""
    <div style="
        border-radius:12px;
        padding:24px;
        background:{meta['bg']};
        border:1px solid #27272a;
    ">
        <div style="
            display:flex;
            align-items:center;
            justify-content:space-between;
            margin-bottom:16px;
        ">
            <div style="
                font-size:18px;
                font-weight:600;
                color:#d4d4d8;
            ">현재 상태</div>

            <div style="
                width:12px;
                height:12px;
                border-radius:9999px;
                background:{meta['color']};
                animation:pulse 1.4s infinite;
            "></div>
        </div>

        <div style="display:flex; align-items:center; gap:16px;">
            <div style="
                width:64px;
                height:64px;
                border-radius:9999px;
                background:{meta['bg']};
                display:flex;
                align-items:center;
                justify-content:center;
                color:{meta['color']};
                font-size:28px;
                font-weight:800;
            ">
                {meta['icon']}
            </div>

            <div style="flex:1;">
                <div style="
                    font-size:30px;
                    font-weight:700;
                    color:{meta['color']};
                    margin-bottom:4px;
                ">
                    {html.escape(meta['label'])}
                </div>
                <div style="
                    font-size:14px;
                    color:#a1a1aa;
                ">
                    {html.escape(meta['desc'])}
                </div>
            </div>
        </div>
    </div>
    """


def _build_alert_card(alerts: list[dict]) -> str:
    if not alerts:
        items_html = """
        <div style="
            text-align:center;
            padding:32px 0;
            color:#71717a;
        ">
            알림이 없습니다
        </div>
        """
    else:
        cards = []
        for alert in alerts[:10]:
            bg, border = _alert_color(alert["type"])
            cards.append(
                f"""
                <div style="
                    border-radius:8px;
                    padding:16px;
                    border:1px solid {border};
                    background:{bg};
                ">
                    <div style="display:flex; align-items:flex-start; gap:12px;">
                        <div style="
                            width:20px;
                            min-width:20px;
                            margin-top:2px;
                            color:#a1a1aa;
                            font-size:16px;
                        ">!</div>
                        <div style="flex:1; min-width:0;">
                            <div style="
                                font-size:14px;
                                color:#e4e4e7;
                                line-height:1.5;
                            ">
                                {html.escape(alert['message'])}
                            </div>
                            <div style="
                                margin-top:4px;
                                font-size:12px;
                                color:#71717a;
                            ">
                                {html.escape(_format_time(alert['timestamp']))}
                            </div>
                        </div>
                    </div>
                </div>
                """
            )
        items_html = "".join(cards)

    return f"""
    <div style="
        border-radius:12px;
        padding:24px;
        background:rgba(24,24,27,0.5);
        border:1px solid #27272a;
    ">
        <div style="
            font-size:18px;
            font-weight:600;
            color:#d4d4d8;
            margin-bottom:16px;
        ">알림</div>

        <div style="
            display:flex;
            flex-direction:column;
            gap:12px;
            max-height:256px;
            overflow-y:auto;
        ">
            {items_html}
        </div>
    </div>
    """


def _build_donut_chart(normal_pct: float, drowsy_pct: float, absent_pct: float) -> str:
    normal_end = normal_pct
    drowsy_end = normal_pct + drowsy_pct
    absent_end = normal_pct + drowsy_pct + absent_pct

    return f"""
    <div style="
        height:192px;
        display:flex;
        align-items:center;
        justify-content:center;
        margin-bottom:24px;
    ">
        <div style="
            width:140px;
            height:140px;
            border-radius:9999px;
            background:
                conic-gradient(
                    #10b981 0% {normal_end}%,
                    #f59e0b {normal_end}% {drowsy_end}%,
                    #ef4444 {drowsy_end}% {absent_end}%,
                    #27272a {absent_end}% 100%
                );
            display:flex;
            align-items:center;
            justify-content:center;
        ">
            <div style="
                width:78px;
                height:78px;
                border-radius:9999px;
                background:#18181b;
                border:1px solid #3f3f46;
            "></div>
        </div>
    </div>
    """


def _build_report_card(report_data: dict) -> str:
    total_stats = _get_total_stats(report_data)
    total = total_stats["total"]

    normal_pct = 0.0 if total <= 0 else (total_stats["normal"] / total) * 100
    drowsy_pct = 0.0 if total <= 0 else (total_stats["drowsy"] / total) * 100
    absent_pct = 0.0 if total <= 0 else (total_stats["absent"] / total) * 100

    student_rows = []
    for student in report_data["students"]:
        student_total = student["normal"] + student["drowsy"] + student["absent"]

        if student_total > 0:
            normal_width = (student["normal"] / student_total) * 100
            drowsy_width = (student["drowsy"] / student_total) * 100
            absent_width = (student["absent"] / student_total) * 100
        else:
            normal_width = drowsy_width = absent_width = 0

        student_rows.append(
            f"""
            <div style="
                padding:8px;
                border-radius:8px;
                background:rgba(39,39,42,0.5);
                font-size:12px;
            ">
                <div style="
                    display:flex;
                    align-items:center;
                    justify-content:space-between;
                    margin-bottom:4px;
                ">
                    <span style="color:#d4d4d8; font-weight:500;">{html.escape(student['name'])}</span>
                    <span style="color:#a1a1aa;">{_student_normal_percent(student)} 정상</span>
                </div>

                <div style="
                    display:flex;
                    gap:1px;
                    height:6px;
                    border-radius:9999px;
                    overflow:hidden;
                    background:#3f3f46;
                ">
                    <div style="background:#10b981; width:{normal_width}%;"></div>
                    <div style="background:#f59e0b; width:{drowsy_width}%;"></div>
                    <div style="background:#ef4444; width:{absent_width}%;"></div>
                </div>
            </div>
            """
        )

    chart_html = (
        _build_donut_chart(normal_pct, drowsy_pct, absent_pct) if total > 0 else ""
    )

    return f"""
    <div style="
        border-radius:12px;
        padding:24px;
        background:rgba(24,24,27,0.5);
        border:1px solid #27272a;
    ">
        <div style="
            display:flex;
            align-items:center;
            gap:8px;
            margin-bottom:24px;
        ">
            <div style="font-size:18px; color:#a1a1aa;">▣</div>
            <div style="
                font-size:18px;
                font-weight:600;
                color:#d4d4d8;
            ">리포트</div>
        </div>

        <div style="
            margin-bottom:24px;
            padding:16px;
            border-radius:8px;
            background:rgba(39,39,42,0.5);
        ">
            <div style="
                display:flex;
                align-items:center;
                gap:8px;
                color:#a1a1aa;
                font-size:14px;
                margin-bottom:4px;
            ">
                <span>◷</span>
                <span>총 분석 시간</span>
            </div>
            <div style="
                font-size:28px;
                font-weight:700;
                color:#ffffff;
            ">
                {_format_duration(report_data['total_time'])}
            </div>
        </div>

        <div style="display:flex; flex-direction:column; gap:12px; margin-bottom:24px;">
            <div style="display:flex; align-items:center; justify-content:space-between;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <div style="width:12px; height:12px; border-radius:9999px; background:#10b981;"></div>
                    <span style="font-size:14px; color:#d4d4d8;">정상</span>
                </div>
                <div style="font-size:14px; font-weight:600; color:#e4e4e7;">{_percent(total_stats['normal'], total)}</div>
            </div>

            <div style="display:flex; align-items:center; justify-content:space-between;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <div style="width:12px; height:12px; border-radius:9999px; background:#f59e0b;"></div>
                    <span style="font-size:14px; color:#d4d4d8;">졸음</span>
                </div>
                <div style="font-size:14px; font-weight:600; color:#e4e4e7;">{_percent(total_stats['drowsy'], total)}</div>
            </div>

            <div style="display:flex; align-items:center; justify-content:space-between;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <div style="width:12px; height:12px; border-radius:9999px; background:#ef4444;"></div>
                    <span style="font-size:14px; color:#d4d4d8;">이탈</span>
                </div>
                <div style="font-size:14px; font-weight:600; color:#e4e4e7;">{_percent(total_stats['absent'], total)}</div>
            </div>
        </div>

        {chart_html}

        <div style="
            border-top:1px solid #27272a;
            padding-top:16px;
        ">
            <div style="
                display:flex;
                align-items:center;
                gap:8px;
                color:#a1a1aa;
                font-size:14px;
                margin-bottom:12px;
            ">
                <span>👥</span>
                <span>학생별 통계</span>
            </div>

            <div style="
                display:flex;
                flex-direction:column;
                gap:8px;
                max-height:192px;
                overflow-y:auto;
            ">
                {''.join(student_rows)}
            </div>
        </div>
    </div>
    """


def render_panel_html(
    camera_state: str,
    status: str,
    alert: str,
    report: str,
    is_running: bool,
) -> str:
    del camera_state, alert, report

    alerts = deepcopy(PANEL_STATE["alerts"])
    report_data = deepcopy(PANEL_STATE["report_data"])

    return f"""
    <div style="
        height:100%;
        padding:24px;
        background:#18181b;
        display:flex;
        flex-direction:column;
        gap:16px;
        overflow-y:auto;
        box-sizing:border-box;
    ">
        {_build_control_panel(is_running)}
        {_build_status_card(status)}
        {_build_alert_card(alerts)}
        {_build_report_card(report_data)}
    </div>
    """


def _debug_text(snapshot: RuntimeSnapshot) -> str:
    report_data = PANEL_STATE["report_data"]
    total = report_data["total_time"]
    alerts_count = len(PANEL_STATE["alerts"])

    return (
        f"{snapshot.debug_text}\n"
        f"panel_running={PANEL_STATE['is_running']} "
        f"my_status={PANEL_STATE['my_status']} "
        f"csv_index={PANEL_STATE['current_data_index']} "
        f"total_time={total} "
        f"alerts={alerts_count}"
    )


def _report_text() -> str:
    report_data = PANEL_STATE["report_data"]
    total_stats = _get_total_stats(report_data)
    students = report_data["students"]

    student_lines = [
        f"{student['name']}: {_student_normal_percent(student)} 정상"
        for student in students
    ]

    return (
        f"Total Time: {_format_duration(report_data['total_time'])}\n"
        f"Normal: {_percent(total_stats['normal'], total_stats['total'])}\n"
        f"Drowsy: {_percent(total_stats['drowsy'], total_stats['total'])}\n"
        f"Absent: {_percent(total_stats['absent'], total_stats['total'])}\n"
        + "\n".join(student_lines)
    )


def _latest_alert_text() -> str:
    if not PANEL_STATE["alerts"]:
        return "알림이 없습니다."
    latest = PANEL_STATE["alerts"][0]
    return latest["message"]


def _render_outputs(snapshot: RuntimeSnapshot, ack: int):
    panel_html = render_panel_html(
        camera_state="ON" if snapshot.running else "OFF",
        status=snapshot.status,
        alert=_latest_alert_text(),
        report=_report_text(),
        is_running=snapshot.running,
    )
    return (
        snapshot.status,
        _latest_alert_text(),
        _report_text(),
        panel_html,
        _debug_text(snapshot),
        ack,
    )


def on_start():
    _reset_panel_state()
    snapshot = RUNTIME.start()
    _sync_panel_state(snapshot)
    return (
        True,
        snapshot.status,
        _latest_alert_text(),
        _report_text(),
        render_panel_html(
            camera_state="ON",
            status=snapshot.status,
            alert=_latest_alert_text(),
            report=_report_text(),
            is_running=True,
        ),
        _debug_text(snapshot),
        0,
    )


def on_stop(frame_ack: int):
    _stop_panel_state()
    snapshot = RUNTIME.stop()
    return (
        False,
        snapshot.status,
        _latest_alert_text(),
        _report_text(),
        render_panel_html(
            camera_state="OFF",
            status=snapshot.status,
            alert=_latest_alert_text(),
            report=_report_text(),
            is_running=False,
        ),
        _debug_text(snapshot),
        frame_ack,
    )


def process_live_frame(frame_seq: int, frame_data: str, is_running: bool):
    frame_seq = int(frame_seq or 0)

    if not is_running:
        return _render_outputs(RUNTIME.snapshot(), frame_seq)

    snapshot = RUNTIME.process_frame(frame_data)
    _sync_panel_state(snapshot)
    return _render_outputs(snapshot, frame_seq)
