import gradio as gr
import base64
import mimetypes
from pathlib import Path

BG_PATH = "assets/demo_bg.png"

# 3번째 학생 슬롯 좌표
SLOT_X = 1720
SLOT_Y = 450
SLOT_W = 180
SLOT_H = 180

# 배경 크기
BG_W = 1920
BG_H = 1080


def load_bg_as_data_url(path: str) -> str:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"배경 이미지가 없습니다: {path}")

    mime_type, _ = mimetypes.guess_type(str(file_path))
    if mime_type is None:
        mime_type = "image/png"

    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    return f"data:{mime_type};base64,{encoded}"


BG_DATA_URL = load_bg_as_data_url(BG_PATH)


def get_dummy_status(counter: int):
    cycle = counter % 30

    if cycle < 18:
        return "NORMAL", "이상 없음"
    elif cycle < 24:
        return "DROWSY", "졸음 감지 알림"
    else:
        return "ABSENT", "자리 이탈 알림"


def build_report(counter: int) -> str:
    normal_frames = sum(1 for i in range(counter) if get_dummy_status(i)[0] == "NORMAL")
    drowsy_frames = sum(1 for i in range(counter) if get_dummy_status(i)[0] == "DROWSY")
    absent_frames = sum(1 for i in range(counter) if get_dummy_status(i)[0] == "ABSENT")

    report = (
        f"총 프레임: {counter}\n"
        f"NORMAL: {normal_frames}\n"
        f"DROWSY: {drowsy_frames}\n"
        f"ABSENT: {absent_frames}"
    )
    return report


def update_demo(counter):
    counter = int(counter) + 1
    status, alert = get_dummy_status(counter)
    report = build_report(counter)

    status_html = build_status_panel_html(
        camera_state="ON",
        status=status,
        alert=alert,
        report=report,
    )

    return counter, status, alert, report, status_html


def build_status_panel_html(camera_state: str, status: str, alert: str, report: str) -> str:
    camera_class = "cam-on" if camera_state == "ON" else "cam-off"

    if status == "NORMAL":
        status_class = "status-normal"
    elif status == "DROWSY":
        status_class = "status-drowsy"
    elif status == "ABSENT":
        status_class = "status-absent"
    else:
        status_class = "status-unknown"

    return f"""
    <div class="panel-shell">
        <div class="panel-header">
            <div>
                <div class="panel-eyebrow">LIVE DEMO</div>
                <div class="panel-title">Monitoring Panel</div>
            </div>
            <div class="camera-chip {camera_class}">{camera_state}</div>
        </div>

        <div class="info-card">
            <div class="card-label">Current Status</div>
            <div class="status-pill {status_class}">{status}</div>
        </div>

        <div class="info-card">
            <div class="card-label">Alert</div>
            <div class="card-value">{alert}</div>
        </div>

        <div class="info-card report-card">
            <div class="card-label">Final Report</div>
            <pre class="report-text">{report}</pre>
        </div>
    </div>
    """


def on_start(counter):
    counter = int(counter)
    status, alert = get_dummy_status(counter)
    report = build_report(counter)

    status_html = build_status_panel_html(
        camera_state="ON",
        status=status,
        alert=alert,
        report=report if counter > 0 else "카메라가 시작되었습니다.\n상태 업데이트를 기다리는 중입니다.",
    )

    return status_html


def on_stop(counter):
    counter = int(counter)
    status, alert = get_dummy_status(counter)
    report = build_report(counter)

    status_html = build_status_panel_html(
        camera_state="OFF",
        status=status,
        alert="카메라가 중지되었습니다.",
        report=report if counter > 0 else "카메라가 중지된 상태입니다.",
    )

    return status_html


css = f"""
:root {{
    --bg-0: #0b1120;
    --bg-1: #111827;
    --panel: rgba(17, 24, 39, 0.92);
    --line: rgba(255, 255, 255, 0.08);
    --text: #e5e7eb;
    --muted: #94a3b8;
    --blue: #60a5fa;
    --green: #22c55e;
    --yellow: #f59e0b;
    --red: #ef4444;
}}

.gradio-container {{
    background: linear-gradient(180deg, #0b1120 0%, #111827 100%);
}}

#page-title {{
    margin-bottom: 8px;
}}

#page-title h2 {{
    margin: 0;
    color: white;
    font-size: 28px;
    font-weight: 700;
}}

#page-title p {{
    margin: 8px 0 0 0;
    color: var(--muted);
    font-size: 14px;
}}

#demo-wrap {{
    display: flex;
    gap: 24px;
    align-items: flex-start;
}}

#stage-wrap {{
    width: min(100%, 1100px);
}}

#demo-stage {{
    position: relative;
    width: 100%;
    aspect-ratio: {BG_W} / {BG_H};
    background-image: url('{BG_DATA_URL}');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid var(--line);
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.28);
}}

#student-cam {{
    position: absolute;
    left: {SLOT_X / BG_W * 100:.6f}%;
    top: {SLOT_Y / BG_H * 100:.6f}%;
    width: {SLOT_W / BG_W * 100:.6f}%;
    height: {SLOT_H / BG_H * 100:.6f}%;
    object-fit: cover;
    border: 2px solid rgba(96, 165, 250, 0.8);
    border-radius: 12px;
    background: #111;
    z-index: 2;
    transform: scaleX(-1);
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.28);
}}

#cam-placeholder {{
    position: absolute;
    left: {SLOT_X / BG_W * 100:.6f}%;
    top: {SLOT_Y / BG_H * 100:.6f}%;
    width: {SLOT_W / BG_W * 100:.6f}%;
    height: {SLOT_H / BG_H * 100:.6f}%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #e5e7eb;
    background: rgba(0, 0, 0, 0.45);
    border-radius: 12px;
    z-index: 1;
    font-size: 13px;
    text-align: center;
    padding: 8px;
    box-sizing: border-box;
    border: 1px dashed rgba(255, 255, 255, 0.16);
}}

#stage-caption {{
    margin-top: 10px;
    color: var(--muted);
    font-size: 13px;
}}

#right-panel {{
    min-width: 360px;
}}

.panel-shell {{
    display: flex;
    flex-direction: column;
    gap: 14px;
    min-height: 620px;
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 18px;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.22);
}}

.panel-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 12px;
}}

.panel-eyebrow {{
    color: var(--blue);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.08em;
}}

.panel-title {{
    margin-top: 4px;
    color: white;
    font-size: 24px;
    font-weight: 700;
}}

.camera-chip {{
    padding: 8px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    border: 1px solid transparent;
}}

.cam-on {{
    background: rgba(34, 197, 94, 0.12);
    color: #86efac;
    border-color: rgba(34, 197, 94, 0.24);
}}

.cam-off {{
    background: rgba(239, 68, 68, 0.12);
    color: #fca5a5;
    border-color: rgba(239, 68, 68, 0.24);
}}

.info-card {{
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 16px;
}}

.card-label {{
    color: var(--muted);
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 10px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}}

.card-value {{
    color: white;
    font-size: 16px;
    line-height: 1.5;
}}

.status-pill {{
    display: inline-flex;
    align-items: center;
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 14px;
    font-weight: 700;
}}

.status-normal {{
    background: rgba(34, 197, 94, 0.12);
    color: #86efac;
    border: 1px solid rgba(34, 197, 94, 0.24);
}}

.status-drowsy {{
    background: rgba(245, 158, 11, 0.12);
    color: #fcd34d;
    border: 1px solid rgba(245, 158, 11, 0.24);
}}

.status-absent {{
    background: rgba(239, 68, 68, 0.12);
    color: #fca5a5;
    border: 1px solid rgba(239, 68, 68, 0.24);
}}

.status-unknown {{
    background: rgba(107, 114, 128, 0.12);
    color: #d1d5db;
    border: 1px solid rgba(107, 114, 128, 0.24);
}}

.report-card {{
    flex: 1;
}}

.report-text {{
    margin: 0;
    color: #e5e7eb;
    font-size: 14px;
    line-height: 1.6;
    white-space: pre-wrap;
    font-family: inherit;
}}

#control-row {{
    margin-top: 12px;
    gap: 10px;
}}

button.primary-btn {{
    background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%) !important;
    color: white !important;
    border: none !important;
}}

button.secondary-btn {{
    background: rgba(255, 255, 255, 0.06) !important;
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
}}

#hidden-status-mirror,
#hidden-alert-mirror {{
    display: none;
}}

@media (max-width: 1100px) {{
    #demo-wrap {{
        flex-direction: column;
    }}

    #right-panel {{
        width: 100%;
        min-width: unset;
    }}

    .panel-shell {{
        min-height: auto;
    }}
}}
"""

head = """
<script>
async function startOverlayCamera() {
    const video = document.getElementById("student-cam");
    const placeholder = document.getElementById("cam-placeholder");

    if (!video) return;

    try {
        // 이미 켜져 있으면 중복 실행 방지
        if (video.srcObject) {
            return;
        }

        const stream = await navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: "user",
                width: { ideal: 1280 },
                height: { ideal: 720 }
            },
            audio: false
        });

        video.srcObject = stream;
        await video.play();

        if (placeholder) {
            placeholder.style.display = "none";
        }
    } catch (err) {
        console.error("웹캠 시작 실패:", err);
        if (placeholder) {
            placeholder.innerText = "카메라 권한이 필요합니다.";
            placeholder.style.display = "flex";
        }
    }
}

function stopOverlayCamera() {
    const video = document.getElementById("student-cam");
    const placeholder = document.getElementById("cam-placeholder");

    if (!video) return;

    const stream = video.srcObject;
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }

    video.pause();
    video.srcObject = null;

    if (placeholder) {
        placeholder.innerText = "Start 버튼을 눌러 카메라를 켜세요.";
        placeholder.style.display = "flex";
    }
}
</script>
"""

stage_html = """
<div id="demo-wrap">
  <div id="stage-wrap">
    <div id="demo-stage">
      <div id="cam-placeholder">Start 버튼을 눌러 카메라를 켜세요.</div>
      <video id="student-cam" autoplay muted playsinline></video>
    </div>
    <div id="stage-caption">
      발표용 데모 화면: 배경 레이아웃 위에 webcam을 3번째 학생 슬롯에만 오버레이
    </div>
  </div>
</div>
"""

initial_panel_html = build_status_panel_html(
    camera_state="OFF",
    status="NORMAL",
    alert="카메라가 꺼져 있습니다.",
    report="Start 버튼을 눌러 데모를 시작하세요.",
)

with gr.Blocks(css=css, head=head) as demo:
    gr.HTML("""
    <div id="page-title">
        <h2>Drowsiness Detection Demo</h2>
        <p>실시간 webcam overlay + 상태/알림/리포트 분리형 발표 데모</p>
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=7):
            gr.HTML(stage_html)

            with gr.Row(elem_id="control-row"):
                start_btn = gr.Button("Start Camera", elem_classes=["primary-btn"])
                stop_btn = gr.Button("Stop Camera", elem_classes=["secondary-btn"])

        with gr.Column(scale=3, elem_id="right-panel"):
            panel_html = gr.HTML(initial_panel_html)

            # 원본 디버그/상태값도 유지
            status_box = gr.Textbox(label="Status", value="NORMAL")
            alert_box = gr.Textbox(label="Alert", value="이상 없음")
            report_box = gr.Textbox(label="Final Report", lines=8, value="")

    hidden_status = gr.Textbox(value="NORMAL", elem_id="hidden-status-mirror")
    hidden_alert = gr.Textbox(value="이상 없음", elem_id="hidden-alert-mirror")
    counter_state = gr.State(0)

    timer = gr.Timer(1.0)
    timer.tick(
        fn=update_demo,
        inputs=[counter_state],
        outputs=[counter_state, status_box, alert_box, report_box, panel_html],
    )

    status_box.change(lambda x: x, inputs=status_box, outputs=hidden_status)
    alert_box.change(lambda x: x, inputs=alert_box, outputs=hidden_alert)

    start_btn.click(
        fn=on_start,
        inputs=[counter_state],
        outputs=[panel_html],
        js="() => { startOverlayCamera(); }"
    )

    stop_btn.click(
        fn=on_stop,
        inputs=[counter_state],
        outputs=[panel_html],
        js="() => { stopOverlayCamera(); }"
    )

demo.launch(server_name="0.0.0.0", server_port=7860)