from app.config import APP_SUBTITLE, APP_TITLE


def build_header_html(page_title: str = "", page_subtitle: str = "", live_badge: str = "") -> str:
    page_copy = ""
    if page_title:
        badge_html = (
            f'<div class="page-status-badge">{live_badge}</div>' if live_badge else ""
        )
        page_copy = f"""
        <div class="page-heading">
            <div class="page-heading-top">
                <h2>{page_title}</h2>
                {badge_html}
            </div>
            <p>{page_subtitle}</p>
        </div>
        """

    return f"""
    <div id="app-header" class="top-header">
        <div class="brand-wrap">
            <div class="brand-mark">AI</div>
            <div class="brand-copy">
                <h1>{APP_TITLE}</h1>
                <p>{APP_SUBTITLE}</p>
            </div>
        </div>
        {page_copy}
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
        "file": """
            <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <path d="M14 2v6h6"></path>
            </svg>
        """,
        "spark": """
            <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M12 3l1.9 4.9L19 10l-5.1 2.1L12 17l-1.9-4.9L5 10l5.1-2.1z"></path>
            </svg>
        """,
        "trend": """
            <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M3 17l6-6 4 4 7-7"></path>
                <path d="M14 8h6v6"></path>
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
        <div class="upload-copy upload-hero-card">
            <div class="section-badge">Upload Analysis</div>
            <h2>녹화 영상 분석</h2>
            <p>업로드, 시간 입력, 추론 시작, 리포트 이동까지 한 화면 흐름으로 정리했습니다.</p>
            <div class="upload-step-list">
                <div class="upload-step-item">
                    <div class="upload-step-number">1</div>
                    <div>
                        <div class="upload-step-title">영상 업로드</div>
                        <div class="upload-step-desc">MP4, AVI, MOV 등 녹화본을 선택합니다.</div>
                    </div>
                </div>
                <div class="upload-step-item">
                    <div class="upload-step-number">2</div>
                    <div>
                        <div class="upload-step-title">수업 시작 시간 지정</div>
                        <div class="upload-step-desc">리포트 타임라인 기준 시각으로 사용합니다.</div>
                    </div>
                </div>
                <div class="upload-step-item">
                    <div class="upload-step-number">3</div>
                    <div>
                        <div class="upload-step-title">추론 시작 후 자동 리포트 이동</div>
                        <div class="upload-step-desc">기존 추론 함수를 연결할 준비가 된 흐름입니다.</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="upload-feature-list">
            <div class="upload-feature-card">
                <div class="feature-icon emerald">{_home_icon_svg("video")}</div>
                <div class="feature-title">얼굴 감지 및 추적</div>
                <div class="feature-desc">학생별 상태를 누적해 요약 카드와 이벤트 영역으로 연결합니다.</div>
            </div>
            <div class="upload-feature-card">
                <div class="feature-icon amber">{_home_icon_svg("spark")}</div>
                <div class="feature-title">졸음 감지</div>
                <div class="feature-desc">졸음 및 하품 감지 결과를 업로드 리포트에도 연결할 수 있게 준비합니다.</div>
            </div>
            <div class="upload-feature-card">
                <div class="feature-icon red">{_home_icon_svg("clock")}</div>
                <div class="feature-title">이탈 감지</div>
                <div class="feature-desc">이탈 횟수와 핵심 이벤트 영역을 리포트 카드 형태로 표시합니다.</div>
            </div>
        </div>
    </div>
    """


def build_upload_status_html(
    file_name: str = "아직 선택된 파일이 없습니다.",
    file_meta: str = "영상을 업로드하면 파일 상태가 이 영역에 표시됩니다.",
    is_ready: bool = False,
) -> str:
    state_class = "upload-dropzone ready" if is_ready else "upload-dropzone"
    state_label = "업로드 완료" if is_ready else "업로드 대기"
    action_text = "다른 파일을 선택하려면 다시 업로드하세요." if is_ready else "클릭하거나 파일을 끌어다 놓아 선택할 수 있습니다."

    return f"""
    <div class="{state_class}">
        <div class="upload-drop-icon">{_home_icon_svg("file")}</div>
        <div class="upload-drop-copy">
            <div class="upload-drop-state">{state_label}</div>
            <div class="upload-drop-title">{file_name}</div>
            <div class="upload-drop-meta">{file_meta}</div>
            <div class="upload-drop-help">{action_text}</div>
        </div>
    </div>
    """


def build_report_shell_html(content: str, title: str = "분석 리포트", subtitle: str = "") -> str:
    report_subtitle = subtitle or "실시간 분석 누적 상태 또는 업로드 분석 결과를 이 화면에서 확인합니다."
    return f"""
    <div class="report-shell">
        <div class="report-page-header">
            <div>
                <div class="section-badge">Analysis Report</div>
                <h2>{title}</h2>
                <p>{report_subtitle}</p>
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
