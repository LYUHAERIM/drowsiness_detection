def build_head_script() -> str:
    return """
    <script>
    function overlayState() {
        if (!window.__overlayCameraState) {
            window.__overlayCameraState = {
                intervalId: null,
                canvas: null,
                nextSeq: 0,
                inFlightSeq: 0,
                inFlight: false,
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

    async function captureAndSubmitFrame() {
        const state = overlayState();
        const video = document.getElementById("student-cam");
        const frameInput = queryBridgeInput("frame-data-input");
        const seqInput = queryBridgeInput("frame-seq-input");
        const submitBtn = queryBridgeButton("frame-submit-btn");

        if (!video || !frameInput || !seqInput || !submitBtn) return;
        if (!video.srcObject || video.readyState < 2) return;

        if (state.inFlight && currentAck() >= state.inFlightSeq) {
            state.inFlight = false;
        }
        if (state.inFlight) return;

        const width = Math.min(video.videoWidth || 640, 640);
        const height = Math.max(1, Math.round(width * ((video.videoHeight || 480) / (video.videoWidth || 640))));

        if (!state.canvas) {
            state.canvas = document.createElement("canvas");
        }
        state.canvas.width = width;
        state.canvas.height = height;

        const ctx = state.canvas.getContext("2d", { willReadFrequently: false });
        ctx.drawImage(video, 0, 0, width, height);
        const dataUrl = state.canvas.toDataURL("image/jpeg", 0.82);

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

    async function startOverlayCamera() {
        const state = overlayState();
        const video = document.getElementById("student-cam");
        const placeholder = document.getElementById("cam-placeholder");
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
            state.intervalId = window.setInterval(() => {
                captureAndSubmitFrame().catch((err) => {
                    console.error("프레임 전송 실패:", err);
                });
            }, 220);

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
        const video = document.getElementById("student-cam");
        const placeholder = document.getElementById("cam-placeholder");
        if (!video) return;

        if (state.intervalId) {
            window.clearInterval(state.intervalId);
            state.intervalId = null;
        }
        state.inFlight = false;
        state.inFlightSeq = 0;

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
