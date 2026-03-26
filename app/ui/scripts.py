from app.config import BG_H, BG_W


def build_head_script() -> str:
    return """
    <script>
    const STAGE_CAPTURE_WIDTH = __BG_W__;
    const STAGE_CAPTURE_HEIGHT = __BG_H__;
    const FRAME_SEND_INTERVAL_MS = 320;
    const FRAME_JPEG_QUALITY = 0.78;

    function overlayState() {
        if (!window.__overlayCameraState) {
            window.__overlayCameraState = {
                intervalId: null,
                renderIntervalId: null,
                canvas: null,
                nextSeq: 0,
                inFlightSeq: 0,
                inFlight: false,
                lastRenderedDataUrl: "",
            };
        }
        return window.__overlayCameraState;
    }

    function queryBridgeInput(rootId) {
        const root = document.getElementById(rootId);
        if (!root) return null;
        return root.querySelector("textarea, input");
    }

    function queryBridgeButton(rootId) {
        const root = document.getElementById(rootId);
        if (!root) return null;
        return root.querySelector("button") || root;
    }

    function setNativeValue(element, value) {
        const prototype = Object.getPrototypeOf(element);
        const descriptor = Object.getOwnPropertyDescriptor(prototype, "value");
        if (descriptor && descriptor.set) {
            descriptor.set.call(element, value);
        } else {
            element.value = value;
        }
    }

    function currentAck() {
        const ackInput = queryBridgeInput("frame-ack-output");
        const ackValue = ackInput ? parseInt(ackInput.value || "0", 10) : 0;
        return Number.isFinite(ackValue) ? ackValue : 0;
    }

    function clickHiddenButton(buttonId) {
        const root = document.getElementById(buttonId);
        if (!root) return;
        const btn = root.querySelector("button") || root;
        btn.click();
    }

    function triggerPanelStart() {
        clickHiddenButton("real-start-btn");
    }

    function triggerPanelStop() {
        clickHiddenButton("real-stop-btn");
    }

    function getStageElements() {
        return {
            stage: document.getElementById("demo-stage"),
            stageVideo: document.getElementById("stage-bg-video"),
            stageImage: document.getElementById("stage-bg-image"),
            studentVideo: document.getElementById("student-cam"),
            overlayImg: document.getElementById("student-cam-overlay"),
            placeholder: document.getElementById("cam-placeholder"),
        };
    }

    function ensureStageCanvas(stageWidth, stageHeight) {
        const state = overlayState();
        if (!state.canvas) {
            state.canvas = document.createElement("canvas");
        }
        state.canvas.width = Math.max(1, Math.round(stageWidth));
        state.canvas.height = Math.max(1, Math.round(stageHeight));
        return state.canvas;
    }

    function drawCoverSource(ctx, source, destWidth, destHeight) {
        const sourceWidth = source.videoWidth || source.naturalWidth || source.width || destWidth;
        const sourceHeight = source.videoHeight || source.naturalHeight || source.height || destHeight;
        if (!sourceWidth || !sourceHeight) return;

        const scale = Math.max(destWidth / sourceWidth, destHeight / sourceHeight);
        const drawWidth = sourceWidth * scale;
        const drawHeight = sourceHeight * scale;
        const dx = (destWidth - drawWidth) / 2;
        const dy = (destHeight - drawHeight) / 2;
        ctx.drawImage(source, dx, dy, drawWidth, drawHeight);
    }

    function drawElementIntoStage(ctx, source, stageRect, targetRect, mirror = false) {
        const dx = ((targetRect.left - stageRect.left) / stageRect.width) * ctx.canvas.width;
        const dy = ((targetRect.top - stageRect.top) / stageRect.height) * ctx.canvas.height;
        const dw = (targetRect.width / stageRect.width) * ctx.canvas.width;
        const dh = (targetRect.height / stageRect.height) * ctx.canvas.height;

        if (mirror) {
            ctx.save();
            ctx.translate(dx + dw, dy);
            ctx.scale(-1, 1);
            ctx.drawImage(source, 0, 0, dw, dh);
            ctx.restore();
            return;
        }

        ctx.drawImage(source, dx, dy, dw, dh);
    }

    function composeStageFrame() {
        const { stage, stageVideo, stageImage, studentVideo, overlayImg } = getStageElements();
        if (!stage || !studentVideo) return null;
        if (!studentVideo.srcObject || studentVideo.readyState < 2) return null;

        const stageRect = stage.getBoundingClientRect();
        if (!stageRect.width || !stageRect.height) return null;

        const canvas = ensureStageCanvas(STAGE_CAPTURE_WIDTH, STAGE_CAPTURE_HEIGHT);
        const ctx = canvas.getContext("2d", { willReadFrequently: false });
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // 1. 사용자가 보는 온라인 강의 배경을 stage 전체에 먼저 합성합니다.
        if (stageVideo && stageVideo.readyState >= 2) {
            drawCoverSource(ctx, stageVideo, canvas.width, canvas.height);
        } else if (stageImage && stageImage.complete) {
            drawCoverSource(ctx, stageImage, canvas.width, canvas.height);
        } else {
            ctx.fillStyle = "#09090b";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        }

        // 2. 내 웹캠 오버레이를 실제 stage 상의 슬롯 위치에 그대로 합성합니다.
        const studentRect = studentVideo.getBoundingClientRect();
        drawElementIntoStage(ctx, studentVideo, stageRect, studentRect, true);

        // 3. 디버그 bbox 는 백엔드가 stage 좌표계로 다시 그려서 반환하므로 입력 합성 단계에서는 제외합니다.
        void overlayImg;

        return canvas;
    }

    function captureStageToDataUrl() {
        const canvas = composeStageFrame();
        if (!canvas) return "";
        return canvas.toDataURL("image/jpeg", FRAME_JPEG_QUALITY);
    }

    function sendComposedStageFrame() {
        const state = overlayState();
        const frameInput = queryBridgeInput("frame-data-input");
        const seqInput = queryBridgeInput("frame-seq-input");
        const submitBtn = queryBridgeButton("frame-submit-btn");
        if (!frameInput || !seqInput || !submitBtn) return;

        if (state.inFlight && currentAck() >= state.inFlightSeq) {
            state.inFlight = false;
        }
        if (state.inFlight) return;

        const dataUrl = captureStageToDataUrl();
        if (!dataUrl) return;

        const nextSeq = currentAck() + 1;
        state.nextSeq = nextSeq;
        state.inFlightSeq = nextSeq;
        state.inFlight = true;

        setNativeValue(seqInput, String(nextSeq));
        seqInput.dispatchEvent(new Event("input", { bubbles: true }));
        seqInput.dispatchEvent(new Event("change", { bubbles: true }));

        setNativeValue(frameInput, dataUrl);
        frameInput.dispatchEvent(new Event("input", { bubbles: true }));
        frameInput.dispatchEvent(new Event("change", { bubbles: true }));

        submitBtn.click();
    }

    function syncRenderedFrame() {
        const state = overlayState();
        const overlayInput = queryBridgeInput("overlay-frame-output");
        const { overlayImg } = getStageElements();
        if (!overlayInput || !overlayImg) return;

        const nextDataUrl = overlayInput.value || "";
        if (!nextDataUrl) {
            if (state.lastRenderedDataUrl) {
                overlayImg.removeAttribute("src");
                overlayImg.style.display = "none";
                state.lastRenderedDataUrl = "";
            }
            return;
        }

        if (state.lastRenderedDataUrl === nextDataUrl) return;

        overlayImg.src = nextDataUrl;
        overlayImg.style.display = "block";
        state.lastRenderedDataUrl = nextDataUrl;
    }

    async function startOverlayCamera() {
        const state = overlayState();
        const { studentVideo, placeholder } = getStageElements();
        const video = studentVideo;
        if (!video) return;

        try {
            if (video.srcObject && state.intervalId) return;

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

            state.inFlight = false;
            state.inFlightSeq = 0;
            state.nextSeq = currentAck();

            if (state.intervalId) {
                window.clearInterval(state.intervalId);
            }
            if (state.renderIntervalId) {
                window.clearInterval(state.renderIntervalId);
            }

            state.intervalId = window.setInterval(() => {
                try {
                    sendComposedStageFrame();
                } catch (err) {
                    console.error("프레임 전송 실패:", err);
                }
            }, FRAME_SEND_INTERVAL_MS);

            state.renderIntervalId = window.setInterval(() => {
                syncRenderedFrame();
            }, 120);

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
        const state = overlayState();
        const { studentVideo, placeholder, overlayImg } = getStageElements();
        const video = studentVideo;
        if (!video) return;

        if (state.intervalId) {
            window.clearInterval(state.intervalId);
            state.intervalId = null;
        }
        if (state.renderIntervalId) {
            window.clearInterval(state.renderIntervalId);
            state.renderIntervalId = null;
        }
        state.inFlight = false;
        state.inFlightSeq = 0;
        state.lastRenderedDataUrl = "";

        const stream = video.srcObject;
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }

        video.pause();
        video.srcObject = null;

        if (overlayImg) {
            overlayImg.removeAttribute("src");
            overlayImg.style.display = "none";
        }

        if (placeholder) {
            placeholder.innerText = "Start 버튼을 눌러 카메라를 켜세요.";
            placeholder.style.display = "flex";
        }
    }
    </script>
    """.replace("__BG_W__", str(BG_W)).replace("__BG_H__", str(BG_H))
