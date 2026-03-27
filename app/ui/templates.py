import html
from pathlib import Path
from typing import Any

from app.config import APP_SUBTITLE, APP_TITLE


def _action_button_html(target_id: str, label: str, tone: str = "secondary") -> str:
    return (
        f'<button class="shell-action shell-action-{tone}" '
        f'onclick="clickHiddenButton(\'{target_id}\')">{html.escape(label)}</button>'
    )


def build_shell_header_html(
    eyebrow: str,
    title: str,
    description: str,
    *,
    back_target: str | None = None,
    back_label: str = "홈으로",
    badge: str | None = None,
    action_target: str | None = None,
    action_label: str | None = None,
    action_tone: str = "primary",
) -> str:
    back_html = (
        _action_button_html(back_target, back_label, "ghost") if back_target else ""
    )
    action_html = (
        _action_button_html(action_target, action_label or "", action_tone)
        if action_target and action_label
        else ""
    )
    badge_html = (
        f'<div class="shell-badge">{html.escape(badge)}</div>' if badge else ""
    )
    return f"""
    <section class="shell-header">
        <div class="shell-header-main">
            {back_html}
            <div class="shell-copy">
                <div class="shell-eyebrow">{html.escape(eyebrow)}</div>
                <h1>{html.escape(title)}</h1>
                <p>{html.escape(description)}</p>
            </div>
        </div>
        <div class="shell-header-actions">
            {badge_html}
            {action_html}
        </div>
    </section>
    """


def build_home_hero_html() -> str:
    return f"""
    <section class="home-hero">
        <div class="home-bg home-bg-blue"></div>
        <div class="home-bg home-bg-violet"></div>
        <div class="hero-badge">
            <span class="hero-badge-icon">📡</span>
            <span>AI-Powered Monitoring System</span>
        </div>
        <h1>{APP_TITLE}</h1>
        <p>{APP_SUBTITLE}</p>
        <div class="hero-note">
            온라인 수업에서 졸음 및 이탈 상태를 실시간으로 모니터링합니다
        </div>
    </section>
    """


def build_home_card_html(
    *,
    tone: str,
    icon: str,
    title: str,
    subtitle: str,
    description: str,
    features: list[tuple[str, str, str]],
    button_label: str,
    target_id: str,
) -> str:
    features_html = "".join(
        f"""
        <div class="mode-feature">
            <div class="mode-feature-icon">{html.escape(feature_icon)}</div>
            <div class="mode-feature-copy">
                <div class="mode-feature-title">{html.escape(feature_title)}</div>
                <div class="mode-feature-desc">{html.escape(feature_desc)}</div>
            </div>
        </div>
        """
        for feature_title, feature_desc, feature_icon in features
    )
    return f"""
    <article class="mode-card mode-card-{html.escape(tone)}" onclick="clickHiddenButton('{target_id}')">
        <div class="mode-card-icon">{html.escape(icon)}</div>
        <div class="mode-card-copy">
            <div class="mode-card-subtitle">{html.escape(subtitle)}</div>
            <h2>{html.escape(title)}</h2>
            <p>{html.escape(description)}</p>
        </div>
        <div class="mode-card-list">{features_html}</div>
        <div class="mode-card-cta">{html.escape(button_label)}</div>
    </article>
    """


def build_stage_media_html(stage_media_url: str, stage_media_kind: str) -> str:
    if stage_media_kind == "video":
        return f"""
        <video id="stage-bg-video" autoplay muted loop playsinline preload="metadata">
            <source src="{stage_media_url}" type="video/mp4">
        </video>
        """

    return (
        "<div id=\"stage-bg-image\" "
        f"style=\"background-image: url('{stage_media_url}');\"></div>"
    )


def build_stage_html(stage_media_url: str, stage_media_kind: str) -> str:
    stage_media_html = build_stage_media_html(stage_media_url, stage_media_kind)

    return f"""
    <section id="stage-shell">
        <div id="stage-topbar">
            <div>
                <div class="topbar-label">Realtime Analysis</div>
                <div class="topbar-title">Zoom Lecture Overlay</div>
            </div>
            <div class="topbar-badge">LIVE DEMO</div>
        </div>

        <div id="demo-stage">
            {stage_media_html}
            <div id="cam-placeholder">Start 버튼을 눌러 웹캠 오버레이를 시작하세요.</div>
            <video id="student-cam" autoplay muted playsinline></video>
            <canvas id="bbox-overlay"></canvas>
        </div>

        <div id="stage-caption">
            강의 레이아웃 위에 실시간 감지 결과와 내 웹캠 프레임을 함께 표시합니다.
        </div>
    </section>
    """


def build_upload_intro_html() -> str:
    return """
    <section class="upload-intro">
        <div class="upload-intro-badge">Upload Workflow</div>
        <h2>녹화 영상 분석</h2>
        <p>업로드, 시간 지정, 추론, 리포트 이동까지 한 번에 연결합니다.</p>
        <ul>
            <li>영상 파일 업로드 후 현재 선택 상태를 즉시 표시합니다.</li>
            <li>수업 시작 시간을 입력하면 리포트 기준 시각으로 사용합니다.</li>
            <li>분석이 끝나면 자동으로 리포트 화면으로 전환됩니다.</li>
        </ul>
    </section>
    """


def build_upload_feature_html() -> str:
    return """
    <section class="upload-feature-card">
        <h3>분석 포인트</h3>
        <div class="upload-feature-list">
            <div class="upload-feature-item">
                <strong>얼굴 감지 및 추적</strong>
                <span>기존 파이프라인을 재사용해 참여자별 상태를 집계합니다.</span>
            </div>
            <div class="upload-feature-item">
                <strong>졸음 / 하품 / 이탈 집계</strong>
                <span>학생별 프레임 통계를 묶어 리포트 카드로 변환합니다.</span>
            </div>
            <div class="upload-feature-item">
                <strong>자동 리포트 전환</strong>
                <span>분석 완료 시 별도 클릭 없이 결과 화면으로 이동합니다.</span>
            </div>
        </div>
    </section>
    """


def build_upload_file_state_html(file_path: str | None) -> str:
    if not file_path:
        return """
        <div class="upload-file-state upload-file-empty">
            <div class="upload-file-state-title">업로드 대기 중</div>
            <div class="upload-file-state-copy">MP4, MOV, AVI 등 수업 영상을 선택해주세요.</div>
        </div>
        """

    path = Path(file_path)
    size_mb = path.stat().st_size / (1024 * 1024) if path.exists() else 0
    return f"""
    <div class="upload-file-state">
        <div class="upload-file-state-title">{html.escape(path.name)}</div>
        <div class="upload-file-state-copy">선택 완료 · {size_mb:.1f} MB</div>
    </div>
    """


def build_report_html(report_data: dict[str, Any] | None) -> str:
    if not report_data:
        return """
        <section class="report-shell">
            <div class="report-empty">
                <h2>리포트 준비 중</h2>
                <p>실시간 분석을 실행하거나 녹화 영상을 업로드하면 결과가 여기에 표시됩니다.</p>
            </div>
        </section>
        """

    summary_cards = "".join(
        f"""
        <article class="report-summary-card tone-{html.escape(card.get('tone', 'neutral'))}">
            <div class="report-summary-label">{html.escape(card.get('label', ''))}</div>
            <div class="report-summary-value">{html.escape(str(card.get('value', '-')))}</div>
        </article>
        """
        for card in report_data.get("summary_cards", [])
    )

    events = report_data.get("events", [])
    events_html = (
        "".join(
            f"""
            <div class="report-event tone-{html.escape(event.get('tone', 'neutral'))}">
                <div class="report-event-head">
                    <strong>{html.escape(event.get('title', '이벤트'))}</strong>
                    <span>{html.escape(event.get('time', ''))}</span>
                </div>
                <p>{html.escape(event.get('detail', ''))}</p>
            </div>
            """
            for event in events
        )
        if events
        else '<div class="report-placeholder">표시할 이벤트가 없습니다.</div>'
    )

    participants = report_data.get("participants", [])
    participants_html = (
        "".join(
            f"""
            <div class="participant-card">
                <div class="participant-head">
                    <strong>{html.escape(item.get('name', '참여자'))}</strong>
                    <span>집중도 {html.escape(str(item.get('focus', 0)))}%</span>
                </div>
                <div class="participant-bar">
                    <div class="tone-positive" style="width:{item.get('normal', 0)}%"></div>
                    <div class="tone-warning" style="width:{item.get('drowsy', 0)}%"></div>
                    <div class="tone-danger" style="width:{item.get('absence', 0)}%"></div>
                </div>
                <div class="participant-meta">
                    <span>정상 {html.escape(str(item.get('normal', 0)))}%</span>
                    <span>졸음 {html.escape(str(item.get('drowsy', 0)))}%</span>
                    <span>이탈 {html.escape(str(item.get('absence', 0)))}%</span>
                </div>
            </div>
            """
            for item in participants
        )
        if participants
        else '<div class="report-placeholder">참여자 통계가 아직 없습니다.</div>'
    )

    highlights = report_data.get("highlights", [])
    highlight_html = "".join(
        f"<li>{html.escape(text)}</li>" for text in highlights
    )
    chart_points = report_data.get("chart_points", [])
    chart_columns = (
        "".join(
            f"""
            <div class="report-chart-col">
                <div class="report-chart-stack">
                    <div class="chart-segment chart-normal" style="height:{max(point.get('normal', 0) * 18, 6)}px;"></div>
                    <div class="chart-segment chart-drowsy" style="height:{max(point.get('drowsy', 0) * 18, 0)}px;"></div>
                    <div class="chart-segment chart-absence" style="height:{max(point.get('absence', 0) * 18, 0)}px;"></div>
                </div>
                <div class="report-chart-label">{html.escape(point.get('time', ''))}</div>
            </div>
            """
            for point in chart_points
        )
        if chart_points
        else '<div class="report-placeholder">그래프를 표시할 실시간 히스토리가 아직 없습니다.</div>'
    )
    chart_html = (
        f"""
        <section class="report-card report-chart-card">
            <div class="report-card-head">
                <div>
                    <h3>{html.escape(report_data.get('chart_title', '시간대별 상태 분석'))}</h3>
                    <span>{html.escape(report_data.get('chart_subtitle', ''))}</span>
                </div>
                <div class="report-chart-legend">
                    <span><i class="chart-dot chart-normal"></i>정상</span>
                    <span><i class="chart-dot chart-drowsy"></i>졸음</span>
                    <span><i class="chart-dot chart-absence"></i>이탈</span>
                </div>
            </div>
            <div class="report-chart-wrap">{chart_columns}</div>
        </section>
        """
        if chart_points
        else ""
    )

    return f"""
    <section class="report-shell">
        <div class="report-hero">
            <div>
                <div class="report-eyebrow">{html.escape(report_data.get('badge', 'Report'))}</div>
                <h2>{html.escape(report_data.get('title', '분석 리포트'))}</h2>
                <p>{html.escape(report_data.get('subtitle', ''))}</p>
            </div>
            <div class="report-source">{html.escape(report_data.get('source_label', ''))}</div>
        </div>

        <div class="report-summary-grid">{summary_cards}</div>

        {chart_html}

        <div class="report-grid">
            <section class="report-card">
                <div class="report-card-head">
                    <h3>주요 상태 / 이벤트</h3>
                    <span>{html.escape(str(len(events)))} items</span>
                </div>
                <div class="report-event-list">{events_html}</div>
            </section>

            <section class="report-card">
                <div class="report-card-head">
                    <h3>분석 요약</h3>
                    <span>Highlights</span>
                </div>
                <ul class="report-highlight-list">{highlight_html or '<li>요약 데이터가 없습니다.</li>'}</ul>
            </section>
        </div>

        <section class="report-card">
            <div class="report-card-head">
                <h3>참여자별 상태 분포</h3>
                <span>{html.escape(str(len(participants)))} participants</span>
            </div>
            <div class="participant-grid">{participants_html}</div>
        </section>
    </section>
    """
