import mimetypes
from pathlib import Path

import gradio as gr

from app.config import STAGE_MEDIA_PATH
from app.demo_logic import (
    analyze_uploaded_video,
    build_empty_report_data,
    build_live_report_data,
    describe_uploaded_file,
    on_start,
    on_stop,
    process_live_frame,
    render_panel_html,
    render_report_html,
)
from app.ui.assets import load_file_as_data_url
from app.ui.scripts import build_head_script
from app.ui.styles import build_css
from app.ui.templates import (
    build_home_card_html,
    build_home_hero_html,
    build_shell_header_html,
    build_stage_html,
    build_upload_feature_html,
    build_upload_file_state_html,
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


def _view_updates(target: str):
    return (
        gr.update(visible=target == "home"),
        gr.update(visible=target == "live"),
        gr.update(visible=target == "upload"),
        gr.update(visible=target == "report"),
    )


def _go_home():
    return _view_updates("home")


def _go_live():
    return _view_updates("live")


def _go_upload():
    return _view_updates("upload")


def _go_report():
    return _view_updates("report")


def _stop_live_to_home(frame_ack: int):
    stopped = on_stop(frame_ack)
    return (*_view_updates("home"), *stopped)


def _stop_live_to_report(frame_ack: int):
    stopped = on_stop(frame_ack)
    report_data = build_live_report_data()
    return (*_view_updates("report"), report_data, render_report_html(report_data), *stopped)


def _analyze_and_open_report(
    file_path: str | None,
    class_start_time: str,
    progress=gr.Progress(track_tqdm=True),
):
    report_data, status_text = analyze_uploaded_video(file_path, class_start_time, progress)
    return (
        *_view_updates("report"),
        report_data,
        render_report_html(report_data),
        status_text,
    )


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
    initial_report_data = build_empty_report_data()

    with gr.Blocks() as demo:
        report_state = gr.State(initial_report_data)
        gr.HTML('<div id="app-root">')

        nav_live_btn = gr.Button("", elem_id="nav-live-btn", elem_classes=["bridge-hidden"])
        nav_upload_btn = gr.Button("", elem_id="nav-upload-btn", elem_classes=["bridge-hidden"])
        live_home_btn = gr.Button("", elem_id="live-home-btn", elem_classes=["bridge-hidden"])
        live_report_btn = gr.Button("", elem_id="live-report-btn", elem_classes=["bridge-hidden"])
        upload_home_btn = gr.Button("", elem_id="upload-home-btn", elem_classes=["bridge-hidden"])
        report_home_btn = gr.Button("", elem_id="report-home-btn", elem_classes=["bridge-hidden"])
        report_live_btn = gr.Button("", elem_id="report-live-btn", elem_classes=["bridge-hidden"])
        report_upload_btn = gr.Button("", elem_id="report-upload-btn", elem_classes=["bridge-hidden"])

        with gr.Group(visible=True, elem_classes=["view-shell", "home-shell"]) as home_view:
            gr.HTML(build_home_hero_html())
            with gr.Row(elem_classes=["home-card-grid"]):
                gr.HTML(
                    build_home_card_html(
                        tone="blue",
                        icon="🎥",
                        title="실시간 분석",
                        subtitle="Realtime Mode",
                        description="2분 데모 영상에 내 웹캠을 오버레이하여 실시간 분석",
                        features=[
                            ("실시간 상태 표시", "졸음, 이탈 상태를 즉시 감지", "⚡"),
                            ("웹캠 오버레이", "데모 영상에 나를 합성하여 분석", "🎥"),
                            ("빠른 데모 체험", "2분 안에 기능 확인", "🕒"),
                        ],
                        button_label="실시간 분석 시작",
                        target_id="nav-live-btn",
                    )
                )
                gr.HTML(
                    build_home_card_html(
                        tone="violet",
                        icon="📤",
                        title="녹화 영상 분석",
                        subtitle="Upload Mode",
                        description="긴 수업 영상을 업로드하여 분석 리포트 생성",
                        features=[
                            ("영상 업로드", "1시간 이상의 긴 수업 영상 지원", "📤"),
                            ("상세 리포트", "시간대별 분석 그래프 및 통계", "📊"),
                            ("비실시간 분석", "완료 후 종합 리포트 제공", "🕒"),
                        ],
                        button_label="영상 업로드하기",
                        target_id="nav-upload-btn",
                    )
                )

        with gr.Group(visible=False, elem_classes=["view-shell", "view-card"]) as live_view:
            gr.HTML(
                build_shell_header_html(
                    "Realtime Analysis",
                    "실시간 분석",
                    "실시간 화면에서는 리포트를 우측 상단 버튼으로 분리했습니다.",
                    back_target="live-home-btn",
                    back_label="홈으로",
                    badge="LIVE",
                    action_target="live-report-btn",
                    action_label="리포트 보기",
                    action_tone="primary",
                )
            )

            with gr.Row(elem_classes=["live-layout"]):
                with gr.Column(scale=7):
                    gr.HTML(build_stage_html(stage_media_url, stage_media_kind))
                    slots_json_box = gr.Textbox(
                        value="[]",
                        label="slots-json",
                        elem_id="slots-json-output",
                        elem_classes=["bridge-hidden"],
                    )

                with gr.Column(scale=4):
                    panel_html = gr.HTML(initial_panel_html)
                    with gr.Accordion("디버그 / 원본 상태값", open=False, elem_classes=["debug-panel"]):
                        status_box = gr.Textbox(label="Status", value="NORMAL")
                        alert_box = gr.Textbox(label="Alert", value="카메라가 꺼져 있습니다.")
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

        with gr.Group(visible=False, elem_classes=["view-shell", "view-card"]) as upload_view:
            gr.HTML(
                build_shell_header_html(
                    "Upload Analysis",
                    "녹화 영상 분석",
                    "영상 업로드, 시간 지정, 추론 완료 후 자동 리포트 이동 흐름을 제공합니다.",
                    back_target="upload-home-btn",
                    back_label="홈으로",
                    badge="UPLOAD",
                )
            )

            with gr.Row(elem_classes=["upload-layout"]):
                with gr.Column(scale=6):
                    gr.HTML(build_upload_intro_html())
                    file_state_html = gr.HTML(build_upload_file_state_html(None))
                    upload_file = gr.File(
                        label="수업 영상 업로드",
                        file_count="single",
                        type="filepath",
                        elem_classes=["upload-file"],
                    )
                    upload_status = gr.Markdown(
                        "영상 파일과 수업 시작 시간을 입력하면 분석을 시작할 수 있습니다.",
                        elem_classes=["upload-status-markdown"],
                    )

                with gr.Column(scale=4):
                    gr.HTML(build_upload_feature_html())
                    class_start_time = gr.Textbox(
                        label="수업 시작 시간",
                        placeholder="예: 09:00",
                        elem_classes=["upload-time-box"],
                    )
                    analyze_btn = gr.Button("추론 시작", elem_classes=["secondary-action"])

        with gr.Group(visible=False, elem_classes=["view-shell", "view-card"]) as report_view:
            gr.HTML(
                build_shell_header_html(
                    "Report",
                    "분석 리포트",
                    "실시간 세션과 녹화 분석 결과를 같은 리포트 화면 언어로 정리했습니다.",
                    back_target="report-home-btn",
                    back_label="홈으로",
                    badge="REPORT",
                )
            )
            report_html = gr.HTML(render_report_html(initial_report_data))
            with gr.Row(elem_classes=["report-actions"]):
                gr.Button("홈으로 이동", elem_id="report-home-visible", elem_classes=["ghost-action"]).click(
                    fn=_go_home,
                    outputs=[home_view, live_view, upload_view, report_view],
                )
                gr.Button("실시간 보기", elem_id="report-live-visible", elem_classes=["primary-action"]).click(
                    fn=_go_live,
                    outputs=[home_view, live_view, upload_view, report_view],
                )
                gr.Button("녹화 분석 보기", elem_id="report-upload-visible", elem_classes=["secondary-action"]).click(
                    fn=_go_upload,
                    outputs=[home_view, live_view, upload_view, report_view],
                )

        is_running_state = gr.State(False)

        start_btn = gr.Button("Start Camera", elem_id="real-start-btn", elem_classes=["bridge-hidden"])
        stop_btn = gr.Button("Stop Camera", elem_id="real-stop-btn", elem_classes=["bridge-hidden"])

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
        frame_submit_btn = gr.Button("submit-frame", elem_id="frame-submit-btn", elem_classes=["bridge-hidden"])

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

        nav_live_btn.click(
            fn=_go_live,
            outputs=[home_view, live_view, upload_view, report_view],
        )
        nav_upload_btn.click(
            fn=_go_upload,
            outputs=[home_view, live_view, upload_view, report_view],
        )
        upload_home_btn.click(
            fn=_go_home,
            outputs=[home_view, live_view, upload_view, report_view],
        )
        report_home_btn.click(
            fn=_go_home,
            outputs=[home_view, live_view, upload_view, report_view],
        )
        report_live_btn.click(
            fn=_go_live,
            outputs=[home_view, live_view, upload_view, report_view],
        )
        report_upload_btn.click(
            fn=_go_upload,
            outputs=[home_view, live_view, upload_view, report_view],
        )

        live_home_btn.click(
            fn=_stop_live_to_home,
            inputs=[frame_ack_box],
            outputs=[
                home_view,
                live_view,
                upload_view,
                report_view,
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

        live_report_btn.click(
            fn=_stop_live_to_report,
            inputs=[frame_ack_box],
            outputs=[
                home_view,
                live_view,
                upload_view,
                report_view,
                report_state,
                report_html,
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

        upload_file.change(
            fn=describe_uploaded_file,
            inputs=[upload_file],
            outputs=[file_state_html],
        )

        analyze_btn.click(
            fn=lambda: "AI가 영상을 분석하는 중입니다. 완료되면 자동으로 리포트 화면으로 이동합니다.",
            outputs=[upload_status],
            show_progress="hidden",
        ).then(
            fn=_analyze_and_open_report,
            inputs=[upload_file, class_start_time],
            outputs=[
                home_view,
                live_view,
                upload_view,
                report_view,
                report_state,
                report_html,
                upload_status,
            ],
        )

        gr.HTML("</div>")

    demo.demo_css = css
    demo.demo_head = head
    return demo
