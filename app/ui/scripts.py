def build_head_script() -> str:
    return """
    <script>
    async function startOverlayCamera() {
        const video = document.getElementById("student-cam");
        const placeholder = document.getElementById("cam-placeholder");
        if (!video) return;

        try {
            if (video.srcObject) return;

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
