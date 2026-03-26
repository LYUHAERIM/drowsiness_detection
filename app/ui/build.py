from __future__ import annotations

import mimetypes
from pathlib import Path

import gradio as gr

from app.config import STAGE_MEDIA_PATH
from app.demo_logic import (
    on_start,
    on_stop,
    process_live_frame,
    process_uploaded_video,
    render_panel_html,
    show_home_view,
    show_live_report_view,
    show_live_view,
    show_upload_view,
)
from app.ui.assets import load_file_as_data_url
from app.ui.scripts import build_head_script
from app.ui.styles import build_css
from app.ui.templates import (
    build_header_html,
    build_home_footer_html,
    build_home_hero_html,
    build_home_mode_card_html,
    build_stage_html,
    build_upload_intro_html,
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
        slots=[],
    )

    with gr.Blocks() as demo:
        gr.HTML('<div id="app-root">')

        with gr.Column(
            visible=True,
            elem_classes=["view-shell", "home-view"],
        ) as home_view:
            gr.HTML(build_home_hero_html())
            with gr.Row(elem_classes=["home-card-grid"]):
                with gr.Column(elem_classes=["home-card-column", "home-card-live"]):
                    gr.HTML(
                        build_home_mode_card_html(
                            title="실시간 분석",
                            subtitle="Demo Mode",
                            description="2분 데모 영상에 내 웹캠을 오버레이하여 실시간 분석",
                            theme="live-card",
                            icon_kind="video",
                            features=[
                                (
                                    "zap",
                                    "실시간 상태 표시",
                                    "졸음, 이탈 상태를 즉시 감지",
                                ),
                                (
                                    "video",
                                    "웹캠 오버레이",
                                    "데모 영상에 나를 합성하여 분석",
                                ),
                                ("clock", "빠른 데모 체험", "2분 안에 기능 확인"),
                            ],
                        )
                    )
                    home_live_btn = gr.Button(
                        "실시간 분석 시작",
                        elem_id="home-live-btn",
                        elem_classes=[
                            "home-card-cta",
                            "home-card-button",
                            "home-live-cta",
                        ],
                    )

                with gr.Column(elem_classes=["home-card-column", "home-card-upload"]):
                    gr.HTML(
                        build_home_mode_card_html(
                            title="녹화 영상 분석",
                            subtitle="Upload Mode",
                            description="긴 수업 영상을 업로드하여 분석 리포트 생성",
                            theme="upload-card",
                            icon_kind="upload",
                            features=[
                                (
                                    "upload",
                                    "영상 업로드",
                                    "1시간 이상의 긴 수업 영상 지원",
                                ),
                                ("zap", "상세 리포트", "시간대별 분석 그래프 및 통계"),
                                ("clock", "비실시간 분석", "완료 후 종합 리포트 제공"),
                            ],
                        )
                    )
                    home_upload_btn = gr.Button(
                        "영상 업로드하기",
                        elem_id="home-upload-btn",
                        elem_classes=[
                            "home-card-cta",
                            "home-card-button",
                            "home-upload-cta",
                        ],
                    )
            gr.HTML(build_home_footer_html())

        with gr.Column(visible=False, elem_classes=["view-shell"]) as live_view:
            gr.HTML(build_header_html())
            with gr.Row(elem_id="content-wrap"):
                with gr.Column(scale=7):
                    gr.HTML(build_stage_html(stage_media_url, stage_media_kind))

                    # 슬롯 JSON 브릿지: ack 변화 시 JS가 읽어서 bbox 오버레이 갱신
                    slots_json_box = gr.Textbox(
                        value="[]",
                        label="slots-json",
                        elem_id="slots-json-output",
                        elem_classes=["bridge-hidden"],
                    )

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

        with gr.Column(visible=False, elem_classes=["view-shell"]) as upload_view:
            gr.HTML(build_header_html())
            gr.HTML(build_upload_intro_html())
            with gr.Row():
                with gr.Column(scale=7):
                    upload_video = gr.File(
                        label="영상 업로드",
                        file_types=["video"],
                        type="filepath",
                    )
                    upload_status = gr.Textbox(
                        label="분석 상태",
                        value="영상과 수업 시작 시간을 입력한 뒤 분석을 시작하세요.",
                        interactive=False,
                    )
                with gr.Column(scale=5, elem_classes=["upload-panel"]):
                    class_start_time = gr.Textbox(
                        label="수업 시작 시간",
                        placeholder="예: 09:00",
                    )
                    start_upload_analysis_btn = gr.Button(
                        "분석 시작",
                        elem_classes=["primary-btn"],
                    )
                    back_home_from_upload_btn = gr.Button(
                        "홈으로",
                        elem_classes=["secondary-btn"],
                    )

        with gr.Column(visible=False, elem_classes=["view-shell"]) as report_view:
            gr.HTML(build_header_html())
            report_html = gr.HTML("")
            with gr.Row():
                report_home_btn = gr.Button("홈으로", elem_classes=["secondary-btn"])
                report_live_btn = gr.Button(
                    "실시간으로 이동",
                    elem_classes=["secondary-btn"],
                )
                report_upload_btn = gr.Button(
                    "녹화 분석으로 이동",
                    elem_classes=["secondary-btn"],
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
        frame_submit_btn = gr.Button(
            "submit-frame",
            elem_id="frame-submit-btn",
            elem_classes=["bridge-hidden"],
        )
        go_report_btn = gr.Button(
            "go-report",
            elem_id="go-report-btn",
            elem_classes=["bridge-hidden"],
        )

        # 7개 출력: status, alert, report, panel_html, debug, ack, slots_json
        frame_submit_btn.click(
            fn=process_live_frame,
            inputs=[frame_seq_box, frame_data_box],
            outputs=[
                status_box,
                alert_box,
                report_box,
                panel_html,
                debug_box,
                frame_ack_box,
                slots_json_box,
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
                slots_json_box,
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
                slots_json_box,
            ],
            js="() => { stopOverlayCamera(); }",
        )

        home_live_btn.click(
            fn=show_live_view,
            outputs=[home_view, live_view, upload_view, report_view],
        )
        home_upload_btn.click(
            fn=show_upload_view,
            outputs=[home_view, live_view, upload_view, report_view],
        )
        back_home_from_upload_btn.click(
            fn=show_home_view,
            outputs=[home_view, live_view, upload_view, report_view],
        )
        report_home_btn.click(
            fn=show_home_view,
            outputs=[home_view, live_view, upload_view, report_view],
        )
        report_live_btn.click(
            fn=show_live_view,
            outputs=[home_view, live_view, upload_view, report_view],
        )
        report_upload_btn.click(
            fn=show_upload_view,
            outputs=[home_view, live_view, upload_view, report_view],
        )
        go_report_btn.click(
            fn=show_live_report_view,
            outputs=[home_view, live_view, upload_view, report_view, report_html],
        )
        start_upload_analysis_btn.click(
            fn=process_uploaded_video,
            inputs=[upload_video, class_start_time],
            outputs=[
                home_view,
                live_view,
                upload_view,
                report_view,
                report_html,
                upload_status,
            ],
        )

        gr.HTML("</div>")

    demo.demo_css = css
    demo.demo_head = head
    return demo
