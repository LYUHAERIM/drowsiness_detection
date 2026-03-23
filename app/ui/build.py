from __future__ import annotations

import mimetypes
from pathlib import Path

import gradio as gr

from app.config import STAGE_MEDIA_PATH
from app.demo_logic import on_start, on_stop, update_demo
from app.ui.assets import load_file_as_data_url
from app.ui.scripts import build_head_script
from app.ui.styles import build_css
from app.ui.templates import (
    build_header_html,
    build_stage_html,
    build_status_panel_html,
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
        # Windows 경로도 포함해서 Gradio가 접근할 수 있도록 실제 파일 경로 사용
        media_url = f"/gradio_api/file={media_path.resolve()}"

    return media_url, media_kind


def create_demo() -> gr.Blocks:
    stage_media_url, stage_media_kind = resolve_stage_media(STAGE_MEDIA_PATH)
    css = build_css()
    head = build_head_script()

    initial_panel_html = build_status_panel_html(
        camera_state="OFF",
        status="NORMAL",
        alert="카메라가 꺼져 있습니다.",
        report="Start 버튼을 눌러 데모를 시작하세요.",
        is_running=False,
    )

    with gr.Blocks(css=css, head=head) as demo:
        gr.HTML('<div id="app-root">')
        gr.HTML(build_header_html())

        with gr.Row(elem_id="content-wrap"):
            with gr.Column(scale=7):
                gr.HTML(build_stage_html(stage_media_url, stage_media_kind))

                with gr.Row(elem_id="control-row"):
                    start_btn = gr.Button("Start Camera", elem_classes=["primary-btn"])
                    stop_btn = gr.Button("Stop Camera", elem_classes=["secondary-btn"])

                with gr.Accordion(
                    "디버그 / 원본 상태값",
                    open=False,
                    elem_id="debug-accordion",
                ):
                    status_box = gr.Textbox(label="Status", value="NORMAL")
                    alert_box = gr.Textbox(label="Alert", value="이상 없음")
                    report_box = gr.Textbox(label="Final Report", lines=8, value="")

            with gr.Column(scale=3, elem_id="right-panel"):
                panel_html = gr.HTML(initial_panel_html)

        is_running_state = gr.State(False)
        counter_state = gr.State(0)
        timer = gr.Timer(1.0, active=False)

        timer.tick(
            fn=update_demo,
            inputs=[counter_state, is_running_state],
            outputs=[counter_state, status_box, alert_box, report_box, panel_html],
        )

        start_btn.click(
            fn=on_start,
            inputs=[counter_state],
            outputs=[
                is_running_state,
                status_box,
                alert_box,
                report_box,
                panel_html,
                timer,
            ],
            js="() => { startOverlayCamera(); }",
        )

        stop_btn.click(
            fn=on_stop,
            inputs=[counter_state],
            outputs=[
                is_running_state,
                status_box,
                alert_box,
                report_box,
                panel_html,
                timer,
            ],
            js="() => { stopOverlayCamera(); }",
        )

        gr.HTML("</div>")

    return demo
