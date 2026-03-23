from __future__ import annotations

from dataclasses import dataclass

import gradio as gr


@dataclass(frozen=True)
class DemoSnapshot:
    counter: int
    status: str
    alert: str
    report: str


def get_dummy_status(counter: int) -> tuple[str, str]:
    cycle = counter % 30
    if cycle < 18:
        return "NORMAL", "이상 없음"
    if cycle < 24:
        return "DROWSY", "졸음 감지 알림"
    return "ABSENT", "자리 이탈 알림"


def build_report(counter: int) -> str:
    normal_frames = sum(1 for i in range(counter) if get_dummy_status(i)[0] == "NORMAL")
    drowsy_frames = sum(1 for i in range(counter) if get_dummy_status(i)[0] == "DROWSY")
    absent_frames = sum(1 for i in range(counter) if get_dummy_status(i)[0] == "ABSENT")

    return (
        f"총 프레임: {counter}\n"
        f"NORMAL: {normal_frames}\n"
        f"DROWSY: {drowsy_frames}\n"
        f"ABSENT: {absent_frames}"
    )


def make_snapshot(counter: int) -> DemoSnapshot:
    status, alert = get_dummy_status(counter)
    return DemoSnapshot(
        counter=counter,
        status=status,
        alert=alert,
        report=build_report(counter),
    )


def update_demo(counter: int, is_running: bool):
    from app.ui.templates import build_status_panel_html

    counter = int(counter)
    if not is_running:
        snapshot = make_snapshot(counter)
        panel_html = build_status_panel_html(
            camera_state="OFF",
            status=snapshot.status,
            alert="카메라가 중지된 상태입니다.",
            report=snapshot.report if counter > 0 else "Start 버튼을 눌러 데모를 시작하세요.",
            is_running=False,
        )
        return counter, snapshot.status, "카메라가 중지된 상태입니다.", snapshot.report, panel_html

    snapshot = make_snapshot(counter + 1)
    panel_html = build_status_panel_html(
        camera_state="ON",
        status=snapshot.status,
        alert=snapshot.alert,
        report=snapshot.report,
        is_running=True,
    )
    return snapshot.counter, snapshot.status, snapshot.alert, snapshot.report, panel_html


def on_start(counter: int):
    from app.ui.templates import build_status_panel_html

    counter = int(counter)
    snapshot = make_snapshot(counter)
    panel_html = build_status_panel_html(
        camera_state="ON",
        status=snapshot.status,
        alert="실시간 분석을 시작했습니다.",
        report=snapshot.report if counter > 0 else "카메라가 시작되었습니다.\n상태 업데이트를 기다리는 중입니다.",
        is_running=True,
    )
    return (
        True,
        snapshot.status,
        "실시간 분석을 시작했습니다.",
        snapshot.report if counter > 0 else "",
        panel_html,
        gr.update(active=True),
    )


def on_stop(counter: int):
    from app.ui.templates import build_status_panel_html

    counter = int(counter)
    snapshot = make_snapshot(counter)
    panel_html = build_status_panel_html(
        camera_state="OFF",
        status=snapshot.status,
        alert="카메라가 중지되었습니다.",
        report=snapshot.report if counter > 0 else "카메라가 중지된 상태입니다.",
        is_running=False,
    )
    return (
        False,
        snapshot.status,
        "카메라가 중지되었습니다.",
        snapshot.report,
        panel_html,
        gr.update(active=False),
    )
