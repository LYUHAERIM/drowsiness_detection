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

    function setBridgeValue(rootId, value) {{
        const input = queryBridgeInput(rootId);
        if (!input) return;
        setNativeValue(input, value);
        input.dispatchEvent(new Event("input", {{ bubbles: true }}));
        input.dispatchEvent(new Event("change", {{ bubbles: true }}));
    }}

    function setReportDownloadButtonsDisabled(disabled) {{
        for (const button of Array.from(document.querySelectorAll(".report-download-btn"))) {{
            button.disabled = disabled;
            button.style.opacity = disabled ? "0.72" : "1";
            button.style.pointerEvents = disabled ? "none" : "auto";
            button.textContent = disabled ? "PDF 생성 중..." : "↓ 리포트 다운로드";
        }}
    }}

    function tryAutoDownloadReportFile() {{
        if (!window.__reportPendingAutoDownload) return false;

        const root = document.getElementById("report-download-file");
        if (!root) return false;

        const link = root.querySelector("a[href]");
        if (!link) return false;

        const href = link.getAttribute("href");
        if (!href || window.__lastAutoDownloadedReportHref === href) return false;

        window.__lastAutoDownloadedReportHref = href;
        window.__reportPendingAutoDownload = false;
        link.click();
        return true;
    }}

    function wait(ms) {{
        return new Promise((resolve) => window.setTimeout(resolve, ms));
    }}

    function loadExternalScript(url) {{
        return new Promise((resolve, reject) => {{
            const existing = document.querySelector(`script[data-codex-src="${{url}}"]`);
            if (existing) {{
                if (existing.dataset.loaded === "true") {{
                    resolve();
                    return;
                }}
                existing.addEventListener("load", () => resolve(), {{ once: true }});
                existing.addEventListener("error", () => reject(new Error(`Failed to load ${{url}}`)), {{ once: true }});
                return;
            }}

            const script = document.createElement("script");
            script.src = url;
            script.async = true;
            script.dataset.codexSrc = url;
            script.addEventListener("load", () => {{
                script.dataset.loaded = "true";
                resolve();
            }}, {{ once: true }});
            script.addEventListener("error", () => reject(new Error(`Failed to load ${{url}}`)), {{ once: true }});
            document.head.appendChild(script);
        }});
    }}

    async function loadHtml2CanvasLibrary() {{
        if (window.html2canvas) return window.html2canvas;

        const sources = [
            "https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js",
            "https://unpkg.com/html2canvas@1.4.1/dist/html2canvas.min.js",
        ];

        let lastError = null;
        for (const source of sources) {{
            try {{
                await loadExternalScript(source);
                if (window.html2canvas) {{
                    return window.html2canvas;
                }}
            }} catch (error) {{
                lastError = error;
            }}
        }}

        throw lastError || new Error("html2canvas 라이브러리를 불러오지 못했습니다.");
    }}

    function canvasSliceToDataUrl(sourceCanvas, topPx, sliceHeightPx) {{
        const sliceCanvas = document.createElement("canvas");
        sliceCanvas.width = sourceCanvas.width;
        sliceCanvas.height = sliceHeightPx;

        const context = sliceCanvas.getContext("2d");
        context.drawImage(
            sourceCanvas,
            0,
            topPx,
            sourceCanvas.width,
            sliceHeightPx,
            0,
            0,
            sourceCanvas.width,
            sliceHeightPx
        );

        return sliceCanvas.toDataURL("image/jpeg", 0.96);
    }}

    async function captureReportForPdf() {{
        if (window.__reportCaptureBusy) return;

        const target = document.getElementById("report-capture-root");
        if (!target) {{
            console.error("리포트 캡처 대상을 찾을 수 없습니다.");
            return;
        }}

        window.__reportCaptureBusy = true;
        setReportDownloadButtonsDisabled(true);

        try {{
            await wait(700);
            const html2canvas = await loadHtml2CanvasLibrary();
            const width = Math.ceil(target.scrollWidth || target.clientWidth || target.offsetWidth);
            const totalHeight = Math.ceil(target.scrollHeight || target.clientHeight || target.offsetHeight);
            const pixelRatio = Math.max(1, Math.min(window.devicePixelRatio || 1.5, 2));

            const renderedCanvas = await html2canvas(target, {{
                backgroundColor: "#0a0e1a",
                scale: pixelRatio,
                useCORS: true,
                logging: false,
                width,
                height: totalHeight,
                windowWidth: Math.max(document.documentElement.clientWidth, width),
                windowHeight: Math.max(document.documentElement.clientHeight, totalHeight),
                scrollX: 0,
                scrollY: -window.scrollY,
                onclone: (clonedDocument) => {{
                    for (const node of Array.from(clonedDocument.querySelectorAll(".report-animate"))) {{
                        node.style.opacity = "1";
                        node.style.transform = "none";
                        node.style.animation = "none";
                        node.style.transition = "none";
                    }}
                }},
            }});

            const slices = [];
            const sliceCssHeight = 1400;
            const slicePixelHeight = Math.max(1, Math.round(sliceCssHeight * pixelRatio));
            for (let offsetPx = 0; offsetPx < renderedCanvas.height; offsetPx += slicePixelHeight) {{
                const currentSlicePixelHeight = Math.min(
                    slicePixelHeight,
                    renderedCanvas.height - offsetPx
                );
                const dataUrl = canvasSliceToDataUrl(
                    renderedCanvas,
                    offsetPx,
                    currentSlicePixelHeight
                );
                const cssOffsetY = Math.round(offsetPx / pixelRatio);
                const cssSliceHeight = Math.round(currentSlicePixelHeight / pixelRatio);
                slices.push({{
                    index: slices.length,
                    offset_y: cssOffsetY,
                    width: renderedCanvas.width,
                    height: currentSlicePixelHeight,
                    css_width: width,
                    css_height: cssSliceHeight,
                    data_url: dataUrl,
                }});
            }}

            setBridgeValue(
                "report-capture-payload",
                JSON.stringify({{
                    title: target.dataset.reportTitle || "report",
                    captured_at: new Date().toISOString(),
                    slices,
                }})
            );
            await wait(120);
            window.__reportPendingAutoDownload = true;
            clickHiddenButton("report-download-submit-btn");
        }} catch (error) {{
            console.error("리포트 PDF 캡처 실패:", error);
            window.__reportPendingAutoDownload = false;
            window.alert("리포트 PDF 생성에 실패했습니다. 잠시 후 다시 시도해주세요.");
        }} finally {{
            setReportDownloadButtonsDisabled(false);
            window.__reportCaptureBusy = false;
        }}
    }}

    window.captureReportForPdf = captureReportForPdf;
    window.tryAutoDownloadReportFile = tryAutoDownloadReportFile;

    const reportDownloadObserver = new MutationObserver(() => {{
        tryAutoDownloadReportFile();
    }});
    reportDownloadObserver.observe(document.documentElement, {{
        childList: true,
        subtree: true,
    }});

    function getStageBackgroundVideo() {{
        const bgVideo = document.getElementById("stage-bg-video");
        return (bgVideo && bgVideo.tagName === "VIDEO") ? bgVideo : null;
    }}

    async function startStageBackgroundVideo() {{
        const bgVideo = getStageBackgroundVideo();
        if (!bgVideo) return;

        try {{
            bgVideo.pause();
            bgVideo.currentTime = 0;
        }} catch (err) {{
            console.warn("배경영상 초기화 실패:", err);
        }}

        try {{
            await bgVideo.play();
        }} catch (err) {{
            console.warn("배경영상 재생 실패:", err);
        }}
    }}

    function stopStageBackgroundVideo() {{
        const bgVideo = getStageBackgroundVideo();
        if (!bgVideo) return;

        try {{
            bgVideo.pause();
            bgVideo.currentTime = 0;
        }} catch (err) {{
            console.warn("배경영상 정지 실패:", err);
        }}
    }}

    async function captureAndSubmitFrame() {{
        const state = overlayState();
        const webcam  = document.getElementById("student-cam");
        const bgVideo = getStageBackgroundVideo();
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

        // 웹캠을 center-crop해서 1:1 비율로 슬롯에 합성
        // 원본 웹캠(16:9)을 슬롯(1:1)에 그대로 넣으면 얼굴이 찌그러져 FaceMesh 오탐
        const camW = webcam.videoWidth  || webcam.width;
        const camH = webcam.videoHeight || webcam.height;
        const cropSize = Math.min(camW, camH);
        const cropX = (camW - cropSize) / 2;
        const cropY = (camH - cropSize) / 2;

        ctx.save();
        ctx.translate(slotX + slotW, slotY);
        ctx.scale(-1, 1);
        ctx.drawImage(webcam, cropX, cropY, cropSize, cropSize, 0, 0, slotW, slotH);
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

    // infer_video.py STATE_COLORS (BGR→RGB 변환) 기준
    const BBOX_COLORS = {{
        NORMAL: "rgba(70,  220, 70,  0.90)",
        DROWSY: "rgba(255, 0,   0,   0.95)",
        ABSENT: "rgba(255, 165, 0,   0.95)",
        IGNORE: "rgba(160, 160, 160, 0.85)",
    }};
    const NOFACE_COLOR = "rgba(160, 160, 160, 0.85)";
    const TEACHER_COLOR = "rgba(160, 160, 160, 0.90)";

    const STATUS_KO = {{
        NORMAL: "정상", DROWSY: "졸음", ABSENT: "이탈",
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
            const isTeacher = Boolean(s.is_teacher);

            // YAWN은 실시간 화면에서 NORMAL로 보여줌
            const uiStatus = (s.status === "YAWN") ? "NORMAL" : s.status;
            // infer_video.py 동일 로직: noface면 status 무시, NOT FOUND 표시
            const displayState = isTeacher ? "" : (s.noface ? "NOT FOUND" : uiStatus);
            const color = isTeacher
                ? TEACHER_COLOR
                : (s.noface ? NOFACE_COLOR : (BBOX_COLORS[uiStatus] || BBOX_COLORS.NORMAL));
            const lw = (displayState === "DROWSY" || displayState === "ABSENT") ? 3 : 2;

            // bbox 테두리
            ctx.strokeStyle = color;
            ctx.lineWidth   = lw;
            ctx.strokeRect(x, y, w, h);

            // 상단 안쪽 라벨: infer_video.py와 동일하게 noface면 "NOT FOUND"로 대체
            if (!isTeacher) {{
                const label = `ID${{s.slot_id}}  ${{displayState}}`;
                ctx.font = "bold 11px monospace";
                const tw = ctx.measureText(label).width;
                const lh = 17;

                // 라벨 배경은 bbox 상단 안쪽에
                ctx.fillStyle = color;
                ctx.fillRect(x, y, tw + 10, lh);
                ctx.fillStyle = "#fff";
                ctx.fillText(label, x + 5, y + lh - 4);
            }}

            // FaceMesh face_box inner box (마젠타 점선)
            if (!isTeacher && s.face_box_pct && s.face_box_pct.length === 4) {{
                const [fx1p, fy1p, fx2p, fy2p] = s.face_box_pct;
                const fx = fx1p * rect.width;
                const fy = fy1p * rect.height;
                const fw = (fx2p - fx1p) * rect.width;
                const fh = (fy2p - fy1p) * rect.height;
                if (fw >= 4 && fh >= 4) {{
                    ctx.save();
                    ctx.strokeStyle = "rgba(232, 121, 249, 0.85)";
                    ctx.lineWidth   = 1.5;
                    ctx.setLineDash([4, 3]);
                    ctx.strokeRect(fx, fy, fw, fh);
                    ctx.restore();
                }}
            }}
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
            await startStageBackgroundVideo();

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
            stopStageBackgroundVideo();
            if (placeholder) {{
                placeholder.innerText = "카메라 권한이 필요합니다.";
                placeholder.style.display = "flex";
            }}
        }}
    }}

    function stopOverlayCamera(deferTrackStop = false) {{
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
        video.pause();
        video.srcObject = null;

        if (stream) {{
            const stopTracks = () => {{
                stream.getTracks().forEach(track => track.stop());
            }};
            if (deferTrackStop) {{
                window.setTimeout(stopTracks, 0);
            }} else {{
                stopTracks();
            }}
        }}

        if (placeholder) {{
            placeholder.innerText = "Start 버튼을 눌러 카메라를 켜세요.";
            placeholder.style.display = "flex";
        }}

        stopStageBackgroundVideo();
    }}

    window.startStageBackgroundVideo = startStageBackgroundVideo;
    window.stopStageBackgroundVideo = stopStageBackgroundVideo;

    window.setTimeout(() => {{
        stopStageBackgroundVideo();
    }}, 0);
    </script>
    """
