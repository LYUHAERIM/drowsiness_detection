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


def build_home_hero_html() -> str:
    return """
    <div class="home-shell">
        <div class="home-bg-glow"></div>
        <div class="home-hero">
            <div class="home-badge-wrap">
                <div class="home-badge">
                    <span class="home-badge-icon">
                        <svg viewBox="0 0 24 24" aria-hidden="true">
                            <path d="M3 12h3l2-6 4 12 2-6h7" />
                        </svg>
                    </span>
                    <span>AI-Powered Monitoring System</span>
                </div>
            </div>
            <h2>AI 수업 집중도 분석 시스템</h2>
            <p>온라인 수업에서 졸음 및 이탈 상태를 실시간으로 모니터링합니다</p>
        </div>
    </div>
    """


def _home_icon_svg(kind: str) -> str:
    icons = {
        "video": """
            <svg viewBox="0 0 24 24" aria-hidden="true">
                <rect x="3" y="7" width="11" height="10" rx="2"></rect>
                <path d="M14 10.5l5-3v9l-5-3z"></path>
            </svg>
        """,
        "upload": """
            <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M12 16V5"></path>
                <path d="M8 9l4-4 4 4"></path>
                <path d="M5 19v1a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-1"></path>
            </svg>
        """,
        "zap": """
            <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M13 2L4 14h6l-1 8 9-12h-6z"></path>
            </svg>
        """,
        "clock": """
            <svg viewBox="0 0 24 24" aria-hidden="true">
                <circle cx="12" cy="12" r="9"></circle>
                <path d="M12 7v5l3 2"></path>
            </svg>
        """,
    }
    return icons[kind]


def build_home_mode_card_html(
    title: str,
    subtitle: str,
    description: str,
    theme: str,
    icon_kind: str,
    features: list[tuple[str, str, str]],
) -> str:
    feature_items = []
    for feature_icon, feature_title, feature_desc in features:
        feature_items.append(
            f"""
            <div class="home-feature-item">
                <div class="home-feature-icon">{_home_icon_svg(feature_icon)}</div>
                <div>
                    <div class="home-feature-title">{feature_title}</div>
                    <div class="home-feature-desc">{feature_desc}</div>
                </div>
            </div>
            """
        )

    return f"""
    <div class="home-mode-card {theme}">
        <div class="home-mode-card-body">
            <div class="home-mode-icon">{_home_icon_svg(icon_kind)}</div>
            <div class="home-mode-title">{title}</div>
            <div class="home-mode-subtitle">{subtitle}</div>
            <div class="home-mode-description">{description}</div>
            <div class="home-feature-list">
                {"".join(feature_items)}
            </div>
        </div>
    </div>
    """


def build_home_footer_html() -> str:
    return """
    <div class="home-footer-note">
        AI 기반 실시간 졸음 감지 및 이탈 분석 시스템
    </div>
    """


def build_upload_intro_html() -> str:
    return """
    <div class="upload-shell">
        <div class="upload-copy">
            <div class="section-badge">Upload Analysis</div>
            <h2>녹화 영상 분석</h2>
            <p>수업 영상을 업로드하고 수업 시작 시간을 입력하면 분석 완료 후 리포트 화면으로 이동합니다.</p>
        </div>
        <div class="upload-feature-list">
            <div class="upload-feature-card">
                <div class="feature-title">영상 업로드</div>
                <div class="feature-desc">MP4, AVI, MOV 등 수업 녹화본을 선택합니다.</div>
            </div>
            <div class="upload-feature-card">
                <div class="feature-title">수업 시작 시간</div>
                <div class="feature-desc">리포트 시간대 표기와 요약 문구에 활용됩니다.</div>
            </div>
            <div class="upload-feature-card">
                <div class="feature-title">분석 후 리포트</div>
                <div class="feature-desc">현재는 UI 흐름 우선 구현이며, 추후 배치 추론 함수 연결이 가능합니다.</div>
            </div>
        </div>
    </div>
    """


def build_report_shell_html(content: str) -> str:
    return f"""
    <div class="report-shell">
        <div class="report-page-header">
            <div>
                <div class="section-badge">Analysis Report</div>
                <h2>분석 리포트</h2>
                <p>실시간 분석 누적 상태 또는 업로드 분석 결과를 이 화면에서 확인합니다.</p>
            </div>
        </div>
        <div class="report-page-body">
            {content}
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
            <div class="stage-topbar-actions">
                <div class="topbar-badge">DEMO</div>
                <button
                    class="report-link-btn"
                    type="button"
                    onclick="document.getElementById('go-report-btn')?.click()"
                >
                    리포트 보기
                </button>
            </div>
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
        "YAWN":   "status-yawn",
        "ABSENT": "status-absent",
    }
    status_desc_map = {
        "NORMAL": "수업에 집중하고 있습니다",
        "DROWSY": "졸음이 감지되었습니다",
        "YAWN":   "하품이 감지되었습니다",
        "ABSENT": "자리를 이탈했습니다",
    }
    status_ko_map = {
        "NORMAL": "정상",
        "DROWSY": "졸음",
        "YAWN":   "하품",
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
