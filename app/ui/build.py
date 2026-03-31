import mimetypes
from pathlib import Path

import gradio as gr

from app.config import STAGE_MEDIA_PATH
from app.demo_logic import (
    analyze_uploaded_video,
    build_empty_report_data,
    describe_uploaded_file,
    on_start,
    on_stop,
    process_live_frame,
    prepare_live_report_data,
    render_panel_html,
    render_report_html,
)
from app.ui.assets import load_file_as_data_url
from app.ui.scripts import build_head_script
from app.ui.styles import build_css
from app.ui.templates import (
    build_home_card_html,
    build_home_footer_html,
    build_home_hero_html,
    build_shell_header_html,
    build_stage_html,
    build_upload_feature_html,
    build_upload_file_state_html,
    build_upload_info_card_html,
    build_upload_tip_html,
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


def _open_live_report_fast():
    report_data = prepare_live_report_data()
    return (*_view_updates("report"), report_data, render_report_html(report_data))


def _to_24h_hour(meridiem: str, hour_12: str | int) -> int:
    meridiem = str(meridiem or "오전").strip()
    hour_12 = int(hour_12)

    if meridiem == "오전":
        return 0 if hour_12 == 12 else hour_12
    return 12 if hour_12 == 12 else hour_12 + 12


def _compose_upload_start_time(
    meridiem: str,
    hour_12: str | int,
    minute: str | int,
) -> str:
    hour_24 = _to_24h_hour(meridiem, hour_12)
    minute_int = int(minute)
    return f"{hour_24:02d}:{minute_int:02d}"


def _preview_upload_start_time(
    meridiem: str,
    hour_12: str | int,
    minute: str | int,
) -> str:
    return f"{str(meridiem)} {int(hour_12):02d}:{int(minute):02d}"


def _analyze_upload_only(
    file_path: str | None,
    class_start_time: str,
    progress=gr.Progress(track_tqdm=True),
):
    report_data, status_text = analyze_uploaded_video(
        file_path, class_start_time, progress
    )
    return (
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

    live_card_html = build_home_card_html(
        card_id="home-live-card",
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

    upload_card_html = build_home_card_html(
        card_id="home-upload-card",
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

    home_cards_grid_html = f"""
    <div id="home-card-grid" class="home-card-grid">
        <div class="home-card-item home-card-item-live">
            {live_card_html}
        </div>
        <div class="home-card-item home-card-item-upload">
            {upload_card_html}
        </div>
    </div>
    """

    meridiem_choices = ["오전", "오후"]
    hour_choices = [f"{i:02d}" for i in range(1, 13)]
    minute_choices = [f"{i:02d}" for i in range(0, 60)]

    with gr.Blocks(
        elem_id="demo-root",
        elem_classes=["demo-root", "figma-app-root"],
    ) as demo:
        report_state = gr.State(initial_report_data)

        with gr.Group(
            elem_id="bridge-root",
            elem_classes=["bridge-hidden-root"],
        ):
            nav_live_btn = gr.Button(
                "", elem_id="nav-live-btn", elem_classes=["bridge-hidden"]
            )
            nav_upload_btn = gr.Button(
                "", elem_id="nav-upload-btn", elem_classes=["bridge-hidden"]
            )
            live_home_btn = gr.Button(
                "", elem_id="live-home-btn", elem_classes=["bridge-hidden"]
            )
            live_report_btn = gr.Button(
                "", elem_id="live-report-btn", elem_classes=["bridge-hidden"]
            )
            upload_home_btn = gr.Button(
                "", elem_id="upload-home-btn", elem_classes=["bridge-hidden"]
            )
            report_home_btn = gr.Button(
                "", elem_id="report-home-btn", elem_classes=["bridge-hidden"]
            )
            report_live_btn = gr.Button(
                "", elem_id="report-live-btn", elem_classes=["bridge-hidden"]
            )
            report_upload_btn = gr.Button(
                "", elem_id="report-upload-btn", elem_classes=["bridge-hidden"]
            )

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

        with gr.Column(
            visible=True,
            elem_id="home-view",
            elem_classes=["view-shell", "home-shell", "home-view-column"],
        ) as home_view:
            with gr.Column(
                elem_id="home-shell-inner",
                elem_classes=["home-shell-inner", "home-shell-bg"],
            ):
                gr.HTML(
                    build_home_hero_html(),
                    elem_id="home-hero-block",
                    elem_classes=["home-hero-wrap", "home-html-wrap"],
                )

                gr.HTML(
                    home_cards_grid_html,
                    elem_id="home-card-grid-block",
                    elem_classes=["home-card-grid-wrap", "home-html-wrap"],
                )

                gr.HTML(
                    build_home_footer_html(),
                    elem_id="home-footer-block",
                    elem_classes=["home-footer-wrap", "home-html-wrap"],
                )

        with gr.Group(
            visible=False,
            elem_id="live-view",
            elem_classes=["view-shell", "page-shell", "live-page-shell"],
        ) as live_view:
            with gr.Column(
                elem_id="live-page-inner",
                elem_classes=["live-page-inner"],
            ):
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
                    ),
                    elem_id="live-shell-header",
                    elem_classes=["shell-header-wrap"],
                )

                with gr.Column(
                    elem_id="live-layout-wrap",
                    elem_classes=["live-layout"],
                ):
                    with gr.Column(
                        scale=7,
                        elem_id="live-stage-column",
                        elem_classes=["live-stage-column"],
                    ):
                        gr.HTML(
                            build_stage_html(stage_media_url, stage_media_kind),
                            elem_id="live-stage-html",
                            elem_classes=["live-stage-html"],
                        )
                        slots_json_box = gr.Textbox(
                            value="[]",
                            label="slots-json",
                            elem_id="slots-json-output",
                            elem_classes=["bridge-hidden"],
                        )

                    with gr.Column(
                        scale=4,
                        elem_id="live-panel-column",
                        elem_classes=["live-panel-column"],
                    ):
                        panel_html = gr.HTML(
                            initial_panel_html,
                            elem_id="live-panel-html",
                            elem_classes=["live-panel-html"],
                        )

                        with gr.Group(
                            visible=False,
                            elem_id="debug-panel-wrap",
                            elem_classes=["bridge-hidden", "debug-panel"],
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

        with gr.Group(
            visible=False,
            elem_id="upload-view",
            elem_classes=["view-shell", "page-shell", "upload-page-shell"],
        ) as upload_view:
            with gr.Column(
                elem_id="upload-page-inner",
                elem_classes=["upload-page-inner"],
            ):
                gr.HTML(
                    build_shell_header_html(
                        "Upload Analysis",
                        "녹화 영상 분석",
                        "수업 영상을 업로드하여 분석하세요.",
                        back_target="upload-home-btn",
                        back_label="홈으로",
                        badge="UPLOAD",
                    ),
                    elem_id="upload-shell-header",
                    elem_classes=["shell-header-wrap"],
                )

                with gr.Column(
                    elem_id="upload-layout-wrap",
                    elem_classes=["upload-layout"],
                ):
                    with gr.Column(
                        elem_id="upload-main-column",
                        elem_classes=["upload-main-column"],
                    ):
                        with gr.Column(
                            elem_id="upload-upload-card",
                            elem_classes=["upload-upload-card"],
                        ):
                            file_state_html = gr.HTML(
                                build_upload_file_state_html(None),
                                elem_id="upload-file-state-block",
                                elem_classes=["upload-file-state-wrap"],
                            )

                            upload_file = gr.File(
                                label="",
                                file_count="single",
                                type="filepath",
                                elem_id="upload-file-input",
                                elem_classes=["upload-file", "figma-upload-input"],
                            )

                            upload_status = gr.Markdown(
                                "영상 파일과 수업 시작 시간을 입력하면 분석을 시작할 수 있습니다.",
                                elem_id="upload-status-markdown",
                                elem_classes=["upload-status-markdown"],
                            )

                        gr.HTML(
                            build_upload_tip_html(),
                            elem_id="upload-tip-block",
                            elem_classes=["upload-tip-wrap"],
                        )

                    with gr.Column(
                        elem_id="upload-side-column",
                        elem_classes=["upload-side-column"],
                    ):
                        with gr.Column(
                            elem_id="upload-info-card",
                            elem_classes=["upload-info-card"],
                        ):
                            gr.HTML(
                                build_upload_info_card_html(),
                                elem_id="upload-info-card-block",
                                elem_classes=["upload-info-card-wrap"],
                            )

                            with gr.Row(
                                elem_id="upload-time-picker-row",
                                elem_classes=["upload-time-picker-row"],
                            ):
                                meridiem_dropdown = gr.Dropdown(
                                    choices=meridiem_choices,
                                    value="오전",
                                    label="",
                                    container=False,
                                    elem_id="upload-meridiem-dropdown",
                                    elem_classes=[
                                        "upload-time-dropdown",
                                        "time-meridiem",
                                    ],
                                )
                                hour_dropdown = gr.Dropdown(
                                    choices=hour_choices,
                                    value="09",
                                    label="",
                                    container=False,
                                    elem_id="upload-hour-dropdown",
                                    elem_classes=["upload-time-dropdown", "time-hour"],
                                )
                                minute_dropdown = gr.Dropdown(
                                    choices=minute_choices,
                                    value="00",
                                    label="",
                                    container=False,
                                    elem_id="upload-minute-dropdown",
                                    elem_classes=[
                                        "upload-time-dropdown",
                                        "time-minute",
                                    ],
                                )

                            time_preview = gr.HTML(
                                '<div class="upload-time-inline-note">리포트의 시간 표시에 사용됩니다.</div>',
                                elem_id="upload-time-preview-block",
                                elem_classes=["upload-time-preview-wrap"],
                            )

                            analyze_btn = gr.Button(
                                "✦ 분석 시작",
                                elem_id="analyze-btn",
                                elem_classes=["secondary-action", "upload-analyze-btn"],
                            )

                        gr.HTML(
                            build_upload_feature_html(),
                            elem_id="upload-feature-block",
                            elem_classes=["upload-feature-wrap"],
                        )

        with gr.Group(
            visible=False,
            elem_id="report-view",
            elem_classes=["view-shell", "page-shell", "report-view-shell"],
        ) as report_view:
            with gr.Column(
                elem_id="report-page-inner",
                elem_classes=["report-page-inner"],
            ):
                report_html = gr.HTML(
                    render_report_html(initial_report_data),
                    elem_id="report-html-shell",
                    elem_classes=["report-html-shell"],
                )

        is_running_state = gr.State(False)

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
            fn=_open_live_report_fast,
            outputs=[
                home_view,
                live_view,
                upload_view,
                report_view,
                report_state,
                report_html,
            ],
            js="() => { stopOverlayCamera(true); }",
            queue=False,
            show_progress="hidden",
        )

        upload_file.change(
            fn=describe_uploaded_file,
            inputs=[upload_file],
            outputs=[file_state_html],
        )

        meridiem_dropdown.change(
            fn=_preview_upload_start_time,
            inputs=[meridiem_dropdown, hour_dropdown, minute_dropdown],
            outputs=[time_preview],
        )
        hour_dropdown.change(
            fn=_preview_upload_start_time,
            inputs=[meridiem_dropdown, hour_dropdown, minute_dropdown],
            outputs=[time_preview],
        )
        minute_dropdown.change(
            fn=_preview_upload_start_time,
            inputs=[meridiem_dropdown, hour_dropdown, minute_dropdown],
            outputs=[time_preview],
        )

        analyze_btn.click(
            fn=lambda: "AI가 영상을 분석하는 중입니다. 완료되면 자동으로 리포트 화면으로 이동합니다.",
            outputs=[upload_status],
            show_progress="hidden",
        ).then(
            fn=lambda file_path, meridiem, hour, minute: _analyze_upload_only(
                file_path,
                _compose_upload_start_time(meridiem, hour, minute),
            ),
            inputs=[
                upload_file,
                meridiem_dropdown,
                hour_dropdown,
                minute_dropdown,
            ],
            outputs=[
                report_state,
                report_html,
                upload_status,
            ],
            show_progress="minimal",
        ).then(
            fn=_go_report,
            outputs=[home_view, live_view, upload_view, report_view],
            show_progress="hidden",
        )

    demo.demo_css = css
    demo.demo_head = head
    return demo
