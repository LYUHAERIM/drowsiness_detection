from __future__ import annotations

from app.inference.runtime import RUNTIME, RuntimeSnapshot


def _render_panel(snapshot: RuntimeSnapshot) -> str:
    from app.ui.templates import build_status_panel_html

    return build_status_panel_html(
        camera_state="ON" if snapshot.running else "OFF",
        status=snapshot.status,
        alert=snapshot.alert,
        report=snapshot.report,
        is_running=snapshot.running,
    )


def _render_outputs(snapshot: RuntimeSnapshot, ack: int):
    panel_html = _render_panel(snapshot)
    return (
        snapshot.status,
        snapshot.alert,
        snapshot.report,
        panel_html,
        snapshot.debug_text,
        ack,
    )


def on_start():
    snapshot = RUNTIME.start()
    return (
        True,
        snapshot.status,
        snapshot.alert,
        snapshot.report,
        _render_panel(snapshot),
        snapshot.debug_text,
        0,
    )


def on_stop(frame_ack: int):
    snapshot = RUNTIME.stop()
    return (
        False,
        snapshot.status,
        snapshot.alert,
        snapshot.report,
        _render_panel(snapshot),
        snapshot.debug_text,
        frame_ack,
    )


def process_live_frame(frame_seq: int, frame_data: str, is_running: bool):
    frame_seq = int(frame_seq or 0)

    if not is_running:
        return _render_outputs(RUNTIME.snapshot(), frame_seq)

    snapshot = RUNTIME.process_frame(frame_data)
    return _render_outputs(snapshot, frame_seq)
