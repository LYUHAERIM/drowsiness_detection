from app.config import BG_W, BG_H, SLOT_X, SLOT_Y, SLOT_W, SLOT_H


def build_head_script() -> str:
    slot_left_pct = SLOT_X / BG_W
    slot_top_pct = SLOT_Y / BG_H
    slot_w_pct = SLOT_W / BG_W
    slot_h_pct = SLOT_H / BG_H

    return f"""
    <script>
    // 슬롯 위치 (Python config에서 주입)
    const SLOT_LEFT_PCT = {slot_left_pct:.6f};
    const SLOT_TOP_PCT  = {slot_top_pct:.6f};
    const SLOT_W_PCT    = {slot_w_pct:.6f};
    const SLOT_H_PCT    = {slot_h_pct:.6f};
    // 배경 원본 해상도 비율
    const BG_ASPECT     = {BG_W} / {BG_H};

    function overlayState() {{
        if (!window.__overlayCameraState) {{
            window.__overlayCameraState = {{
                intervalId: null,
                canvas: null,
                nextSeq: 0,
                inFlightSeq: 0,
                inFlight: false,
            }};
        }}
        return window.__overlayCameraState;
    }}

    function queryBridgeInput(rootId) {{
        const root = document.getElementById(rootId);
        if (!root) return null;
        return root.querySelector("textarea, input");
    }}

    function queryBridgeButton(rootId) {{
        const root = document.getElementById(rootId);
        if (!root) return null;
        return root.querySelector("button") || root;
    }}

    function setNativeValue(element, value) {{
        const prototype = Object.getPrototypeOf(element);
        const descriptor = Object.getOwnPropertyDescriptor(prototype, "value");
        if (descriptor && descriptor.set) {{
            descriptor.set.call(element, value);
        }} else {{
            element.value = value;
        }}
    }}

    function currentAck() {{
        const ackInput = queryBridgeInput("frame-ack-output");
        const ackValue = ackInput ? parseInt(ackInput.value || "0", 10) : 0;
        return Number.isFinite(ackValue) ? ackValue : 0;
    }}

    function clickHiddenButton(buttonId) {{
        const root = document.getElementById(buttonId);
        if (!root) return;
        const btn = root.querySelector("button") || root;
        btn.click();
    }}

    function triggerPanelStart() {{
        clickHiddenButton("real-start-btn");
    }}

    function triggerPanelStop() {{
        clickHiddenButton("real-stop-btn");
    }}

    async function captureAndSubmitFrame() {{
        const state = overlayState();
        const webcam  = document.getElementById("student-cam");
        const bgVideo = document.getElementById("stage-bg-video");
        const frameInput = queryBridgeInput("frame-data-input");
        const seqInput   = queryBridgeInput("frame-seq-input");
        const submitBtn  = queryBridgeButton("frame-submit-btn");

        if (!webcam || !frameInput || !seqInput || !submitBtn) return;
        if (!webcam.srcObject || webcam.readyState < 2) return;

        if (state.inFlight && currentAck() >= state.inFlightSeq) {{
            state.inFlight = false;
            // ack가 돌아왔다 = 서버가 이 프레임 처리 완료 → bbox JSON 즉시 읽기
            const slotsEl = queryBridgeInput("slots-json-output");
            if (slotsEl && slotsEl.value) {{
                try {{
                    const slots = JSON.parse(slotsEl.value);
                    window.drawBboxOverlay && window.drawBboxOverlay(slots);
                }} catch(e) {{}}
            }}
        }}
        if (state.inFlight) return;

        // 캔버스 크기: 배경 원본 비율 유지, 1920px (슬롯 180×180px 원본 크기 유지)
        const canvasW = 1920;
        const canvasH = Math.round(canvasW / BG_ASPECT);

        if (!state.canvas) {{
            state.canvas = document.createElement("canvas");
        }}
        state.canvas.width  = canvasW;
        state.canvas.height = canvasH;

        const ctx = state.canvas.getContext("2d", {{ willReadFrequently: false }});

        // ① 배경 줌 영상 그리기
        if (bgVideo && bgVideo.readyState >= 2) {{
            ctx.drawImage(bgVideo, 0, 0, canvasW, canvasH);
        }} else {{
            ctx.fillStyle = "#09090b";
            ctx.fillRect(0, 0, canvasW, canvasH);
        }}

        // ② 3번 슬롯 위치에 웹캠 합성 (CSS의 scaleX(-1) 미러 동일하게 적용)
        const slotX = SLOT_LEFT_PCT * canvasW;
        const slotY = SLOT_TOP_PCT  * canvasH;
        const slotW = SLOT_W_PCT    * canvasW;
        const slotH = SLOT_H_PCT    * canvasH;

        ctx.save();
        ctx.translate(slotX + slotW, slotY);
        ctx.scale(-1, 1);
        ctx.drawImage(webcam, 0, 0, slotW, slotH);
        ctx.restore();

        const dataUrl = state.canvas.toDataURL("image/jpeg", 0.85);

        const nextSeq = currentAck() + 1;
        state.nextSeq     = nextSeq;
        state.inFlightSeq = nextSeq;
        state.inFlight    = true;

        setNativeValue(seqInput, String(nextSeq));
        seqInput.dispatchEvent(new Event("input",  {{ bubbles: true }}));
        seqInput.dispatchEvent(new Event("change", {{ bubbles: true }}));

        setNativeValue(frameInput, dataUrl);
        frameInput.dispatchEvent(new Event("input",  {{ bubbles: true }}));
        frameInput.dispatchEvent(new Event("change", {{ bubbles: true }}));

        submitBtn.click();
    }}

    // ── bbox 오버레이 렌더링 ────────────────────────────────────────────────────

    const BBOX_COLORS = {{
        NORMAL: "rgba(34, 197, 94, 0.90)",
        DROWSY: "rgba(239, 68, 68, 0.95)",
        YAWN:   "rgba(245, 158, 11, 0.90)",
        ABSENT: "rgba(239, 68, 68, 0.95)",
    }};

    const STATUS_KO = {{
        NORMAL: "정상", DROWSY: "졸음", YAWN: "하품", ABSENT: "이탈",
    }};

    function drawBboxOverlay(slots) {{
        // slots: 이미 파싱된 배열 (img onerror에서 JSON.parse(atob(...))로 전달)
        const overlay = document.getElementById("bbox-overlay");
        if (!overlay) return;
        const stage = document.getElementById("demo-stage");
        if (!stage) return;

        const rect = stage.getBoundingClientRect();
        const dpr = window.devicePixelRatio || 1;
        overlay.width  = Math.round(rect.width  * dpr);
        overlay.height = Math.round(rect.height * dpr);

        const ctx = overlay.getContext("2d");
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        ctx.clearRect(0, 0, rect.width, rect.height);

        if (!Array.isArray(slots) || slots.length === 0) return;

        for (const s of slots) {{
            const [x1p, y1p, x2p, y2p] = s.box_pct;
            const x = x1p * rect.width;
            const y = y1p * rect.height;
            const w = (x2p - x1p) * rect.width;
            const h = (y2p - y1p) * rect.height;
            if (w < 4 || h < 4) continue;

            const color = BBOX_COLORS[s.status] || BBOX_COLORS.NORMAL;
            const lw = s.status === "DROWSY" || s.status === "ABSENT" ? 3 : 2;

            // bbox 테두리
            ctx.strokeStyle = color;
            ctx.lineWidth   = lw;
            ctx.strokeRect(x, y, w, h);

            // 상단 안쪽 라벨: "ID{{n}}  NORMAL" 형식 (두 번째 사진처럼)
            const statusEn = s.status;  // NORMAL / DROWSY / YAWN / ABSENT
            const label = `ID${{s.slot_id}}  ${{statusEn}}`;
            ctx.font = "bold 11px monospace";
            const tw = ctx.measureText(label).width;
            const lh = 17;

            // 라벨 배경은 bbox 상단 안쪽에
            ctx.fillStyle = color;
            ctx.fillRect(x, y, tw + 10, lh);
            ctx.fillStyle = "#fff";
            ctx.fillText(label, x + 5, y + lh - 4);
        }}
    }}

    window.drawBboxOverlay = drawBboxOverlay;

    // ── 웹캠 오버레이 ────────────────────────────────────────────────────────────

    async function startOverlayCamera() {{
        const state = overlayState();
        const video = document.getElementById("student-cam");
        const placeholder = document.getElementById("cam-placeholder");
        if (!video) return;

        try {{
            if (video.srcObject && state.intervalId) return;

            const stream = await navigator.mediaDevices.getUserMedia({{
                video: {{
                    facingMode: "user",
                    width:  {{ ideal: 1280 }},
                    height: {{ ideal: 720 }},
                }},
                audio: false,
            }});

            video.srcObject = stream;
            await video.play();

            state.inFlight    = false;
            state.inFlightSeq = 0;
            state.nextSeq     = currentAck();

            if (state.intervalId) {{
                window.clearInterval(state.intervalId);
            }}

            state.intervalId = window.setInterval(() => {{
                captureAndSubmitFrame().catch((err) => {{
                    console.error("프레임 전송 실패:", err);
                }});
            }}, 220);

            if (placeholder) {{
                placeholder.style.display = "none";
            }}
        }} catch (err) {{
            console.error("웹캠 시작 실패:", err);
            if (placeholder) {{
                placeholder.innerText = "카메라 권한이 필요합니다.";
                placeholder.style.display = "flex";
            }}
        }}
    }}

    function stopOverlayCamera() {{
        const state = overlayState();
        const video = document.getElementById("student-cam");
        const placeholder = document.getElementById("cam-placeholder");
        if (!video) return;

        if (state.intervalId) {{
            window.clearInterval(state.intervalId);
            state.intervalId = null;
        }}
        state.inFlight    = false;
        state.inFlightSeq = 0;

        const stream = video.srcObject;
        if (stream) {{
            stream.getTracks().forEach(track => track.stop());
        }}

        video.pause();
        video.srcObject = null;

        if (placeholder) {{
            placeholder.innerText = "Start 버튼을 눌러 카메라를 켜세요.";
            placeholder.style.display = "flex";
        }}
    }}
    </script>
    """
