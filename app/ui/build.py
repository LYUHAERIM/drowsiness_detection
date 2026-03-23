from __future__ import annotations

import gradio as gr

from app.config import BG_PATH
from app.demo_logic import on_start, on_stop, update_demo
from app.ui.assets import load_file_as_data_url
from app.ui.scripts import build_head_script
from app.ui.styles import build_css
from app.ui.templates import build_header_html, build_stage_html, build_status_panel_html


def create_demo() -> gr.Blocks:
    bg_data_url = load_file_as_data_url(BG_PATH)
    css = build_css(bg_data_url)
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
                gr.HTML(build_stage_html())

                with gr.Row(elem_id="control-row"):
                    start_btn = gr.Button("Start Camera", elem_classes=["primary-btn"])
                    stop_btn = gr.Button("Stop Camera", elem_classes=["secondary-btn"])

                with gr.Accordion("디버그 / 원본 상태값", open=False, elem_id="debug-accordion"):
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
            outputs=[is_running_state, status_box, alert_box, report_box, panel_html, timer],
            js="() => { startOverlayCamera(); }",
        )

        stop_btn.click(
            fn=on_stop,
            inputs=[counter_state],
            outputs=[is_running_state, status_box, alert_box, report_box, panel_html, timer],
            js="() => { stopOverlayCamera(); }",
        )

        gr.HTML('</div>')

    return demo
