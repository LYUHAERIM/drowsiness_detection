from __future__ import annotations

import mimetypes
from pathlib import Path

import gradio as gr

from app.config import STAGE_MEDIA_PATH
from app.demo_logic import on_start, on_stop, process_live_frame, render_panel_html
from app.ui.assets import load_file_as_data_url
from app.ui.scripts import build_head_script
from app.ui.styles import build_css
from app.ui.templates import (
    build_header_html,
    build_stage_html,
)


def resolve_stage_media(path: str | Path) -> tuple[str, str]:
    media_path = Path(path)
    if not media_path.exists():
        raise FileNotFoundError(f"배경 미디어 파일이 없습니다: {media_path}")

    mime_type, _ = mimetypes.guess_type(str(media_path))
    media_kind = "video" if mime_type and mime_type.startswith("video/") else "image"

    if media_kind == "image":
        media_url = load_file_as_data_url(media_path)
    else:
        media_url = f"/gradio_api/file={media_path.resolve()}"

    return media_url, media_kind


def create_demo() -> gr.Blocks:
    stage_media_url, stage_media_kind = resolve_stage_media(STAGE_MEDIA_PATH)
    css = build_css()
    head = build_head_script()

    initial_panel_html = render_panel_html(
        camera_state="OFF",
        status="NORMAL",
        alert="카메라가 꺼져 있습니다.",
        report="Start 버튼을 눌러 데모를 시작하세요.",
        is_running=False,
    )

    with gr.Blocks() as demo:
        gr.HTML('<div id="app-root">')
        gr.HTML(build_header_html())

        with gr.Row(elem_id="content-wrap"):
            with gr.Column(scale=7):
                gr.HTML(build_stage_html(stage_media_url, stage_media_kind))

            with gr.Column(scale=3, elem_id="right-panel"):
                panel_html = gr.HTML(initial_panel_html)

                with gr.Accordion(
                    "디버그 / 원본 상태값",
                    open=False,
                    elem_id="debug-accordion",
                ):
                    status_box = gr.Textbox(label="Status", value="NORMAL")
                    alert_box = gr.Textbox(
                        label="Alert", value="카메라가 꺼져 있습니다."
                    )
                    report_box = gr.Textbox(
                        label="Final Report",
                        lines=10,
                        value="Start 버튼을 눌러 데모를 시작하세요.",
                    )
                    debug_box = gr.Textbox(
                        label="Debug",
                        lines=8,
                        value="running=False frame_received=False",
                    )

        is_running_state = gr.State(False)

        # 실제 동작 버튼 (화면에는 숨김)
        start_btn = gr.Button(
            "Start Camera",
            elem_id="real-start-btn",
            elem_classes=["bridge-hidden"],
        )
        stop_btn = gr.Button(
            "Stop Camera",
            elem_id="real-stop-btn",
            elem_classes=["bridge-hidden"],
        )

        frame_seq_box = gr.Number(
            value=0,
            precision=0,
            label="frame-seq",
            elem_id="frame-seq-input",
            elem_classes=["bridge-hidden"],
        )
        frame_data_box = gr.Textbox(
            value="",
            label="frame-data",
            elem_id="frame-data-input",
            elem_classes=["bridge-hidden"],
        )
        frame_ack_box = gr.Number(
            value=0,
            precision=0,
            label="frame-ack",
            elem_id="frame-ack-output",
            elem_classes=["bridge-hidden"],
        )
        overlay_frame_box = gr.Textbox(
            value="",
            label="overlay-frame",
            elem_id="overlay-frame-output",
            elem_classes=["bridge-hidden"],
        )
        frame_submit_btn = gr.Button(
            "submit-frame",
            elem_id="frame-submit-btn",
            elem_classes=["bridge-hidden"],
        )

        frame_submit_btn.click(
            fn=process_live_frame,
            inputs=[frame_seq_box, frame_data_box, is_running_state],
            outputs=[
                status_box,
                alert_box,
                report_box,
                panel_html,
                debug_box,
                frame_ack_box,
                overlay_frame_box,
            ],
            queue=False,
            show_progress="hidden",
        )

        start_btn.click(
            fn=on_start,
            outputs=[
                is_running_state,
                status_box,
                alert_box,
                report_box,
                panel_html,
                debug_box,
                frame_ack_box,
                overlay_frame_box,
            ],
            js="() => { startOverlayCamera(); }",
        )

        stop_btn.click(
            fn=on_stop,
            inputs=[frame_ack_box],
            outputs=[
                is_running_state,
                status_box,
                alert_box,
                report_box,
                panel_html,
                debug_box,
                frame_ack_box,
                overlay_frame_box,
            ],
            js="() => { stopOverlayCamera(); }",
        )

        gr.HTML("</div>")

    demo.demo_css = css
    demo.demo_head = head
    return demo
