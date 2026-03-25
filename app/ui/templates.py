from __future__ import annotations

from app.config import APP_SUBTITLE, APP_TITLE


def build_header_html() -> str:
    return f"""
    <div id="app-header">
        <div class="brand-mark">AI</div>
        <div class="brand-copy">
            <h1>{APP_TITLE}</h1>
            <p>{APP_SUBTITLE}</p>
        </div>
    </div>
    """


def build_stage_media_html(stage_media_url: str, stage_media_kind: str) -> str:
    if stage_media_kind == "video":
        return f"""
        <video id="stage-bg-video" autoplay muted loop playsinline preload="metadata">
            <source src="{stage_media_url}" type="video/mp4">
        </video>
        """

    return f"""
    <div id="stage-bg-image" style="background-image: url('{stage_media_url}');"></div>
    """


def build_stage_html(stage_media_url: str, stage_media_kind: str) -> str:
    stage_media_html = build_stage_media_html(stage_media_url, stage_media_kind)

    return f"""
    <div id="stage-shell">
        <div id="stage-topbar">
            <div>
                <div class="topbar-label">LIVE CLASS VIEW</div>
                <div class="topbar-title">Zoom Lecture Layout</div>
            </div>
            <div class="topbar-badge">DEMO</div>
        </div>

        <div id="demo-stage">
            {stage_media_html}
            <div id="cam-placeholder">Start 버튼을 눌러 카메라를 켜세요.</div>
            <video id="student-cam" autoplay muted playsinline></video>
            <canvas id="bbox-overlay"></canvas>
        </div>

        <div id="stage-caption">
            실시간 감지 결과가 화면 위에 직접 표시됩니다.
        </div>
    </div>
    """


def build_status_panel_html(
    camera_state: str, status: str, alert: str, report: str, is_running: bool
) -> str:
    camera_class = "cam-on" if camera_state == "ON" else "cam-off"

    status_class_map = {
        "NORMAL": "status-normal",
        "DROWSY": "status-drowsy",
        "ABSENT": "status-absent",
    }
    status_desc_map = {
        "NORMAL": "수업에 집중하고 있습니다",
        "DROWSY": "졸음이 감지되었습니다",
        "ABSENT": "자리를 이탈했습니다",
    }
    status_ko_map = {
        "NORMAL": "정상",
        "DROWSY": "졸음",
        "ABSENT": "이탈",
    }

    status_class = status_class_map.get(status, "status-unknown")
    status_desc = status_desc_map.get(status, "상태를 확인할 수 없습니다")
    status_label = status_ko_map.get(status, status)
    live_text = "실시간 분석 중" if is_running else "대기 중"

    return f"""
    <div class="panel-shell">
        <div class="panel-header">
            <div>
                <div class="panel-eyebrow">MONITORING PANEL</div>
                <div class="panel-title">Student Status</div>
            </div>
            <div class="camera-chip {camera_class}">{camera_state}</div>
        </div>

        <div class="hero-card {status_class}">
            <div class="hero-card-row">
                <div>
                    <div class="hero-label">현재 상태</div>
                    <div class="hero-value">{status_label}</div>
                    <div class="hero-desc">{status_desc}</div>
                </div>
                <div class="hero-dot"></div>
            </div>
        </div>

        <div class="info-grid">
            <div class="info-card compact-card">
                <div class="card-label">Camera</div>
                <div class="card-value">{camera_state}</div>
            </div>
            <div class="info-card compact-card">
                <div class="card-label">Runtime</div>
                <div class="card-value">{live_text}</div>
            </div>
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
