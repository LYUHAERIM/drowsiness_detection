import html
from pathlib import Path
from typing import Any

from app.config import APP_TITLE


def _action_button_html(target_id: str, label: str, tone: str = "secondary") -> str:
    return (
        f'<button class="shell-action shell-action-{tone}" '
        f"onclick=\"clickHiddenButton('{target_id}')\">{html.escape(label)}</button>"
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
    badge_html = f'<div class="shell-badge">{html.escape(badge)}</div>' if badge else ""
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
    <section id="home-hero-section" class="home-hero">
        <div class="home-bg home-bg-blue"></div>
        <div class="home-bg home-bg-violet"></div>

        <div class="hero-badge">
            <span class="hero-badge-icon">📡</span>
            <span>AI-Powered Monitoring System</span>
        </div>

        <h1>{APP_TITLE}</h1>
        <div class="hero-note">
            온라인 수업에서 졸음 및 이탈 상태를 실시간으로 모니터링합니다
        </div>
    </section>
    """


def build_home_card_html(
    *,
    card_id: str | None = None,
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

    card_id_attr = f' id="{html.escape(card_id)}"' if card_id else ""

    return f"""
    <article{card_id_attr} class="mode-card mode-card-{html.escape(tone)}" onclick="clickHiddenButton('{target_id}')">
        <div class="mode-card-icon">{html.escape(icon)}</div>

        <div class="mode-card-body">
            <div class="mode-card-copy">
                <h2>{html.escape(title)}</h2>
                <div class="mode-card-subtitle">{html.escape(subtitle)}</div>
                <p>{html.escape(description)}</p>
            </div>

            <div class="mode-card-list">
                {features_html}
            </div>
        </div>

        <div class="mode-card-action-row">
            <div class="mode-card-cta">{html.escape(button_label)}</div>
        </div>
    </article>
    """


def build_home_footer_html() -> str:
    return """
    <section id="home-footer-section" class="home-footer">
        <p>AI 기반 실시간 졸음 감지 및 이탈 분석 시스템</p>
    </section>
    """


def build_stage_media_html(stage_media_url: str, stage_media_kind: str) -> str:
    if stage_media_kind == "video":
        return f"""
        <video id="stage-bg-video" autoplay muted loop playsinline preload="metadata">
            <source src="{stage_media_url}" type="video/mp4">
        </video>
        """

    return (
        '<div id="stage-bg-image" '
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
        <div class="upload-intro-head">
            <div class="upload-intro-icon">⤴</div>
            <div class="upload-intro-copy">
                <div class="upload-intro-badge">Upload Analysis</div>
                <h2>녹화 영상 업로드</h2>
                <p>수업 영상을 업로드하고 수업 시작 시간을 선택하면 자동으로 분석 리포트를 생성합니다.</p>
            </div>
        </div>
    </section>
    """


def build_upload_feature_html() -> str:
    return """
    <section class="upload-feature-card">
        <div class="report-card-head">
            <div>
                <h3>분석 기능</h3>
            </div>
        </div>

        <div class="upload-feature-list">
            <div class="upload-feature-item">
                <div class="upload-feature-icon tone-emerald">🎞</div>
                <div class="upload-feature-copy">
                    <strong>참여자 감지 및 추적</strong>
                    <span>수업 영상 속 참여자 상태를 구간별로 확인합니다.</span>
                </div>
            </div>

            <div class="upload-feature-item">
                <div class="upload-feature-icon tone-amber">😴</div>
                <div class="upload-feature-copy">
                    <strong>졸음 감지</strong>
                    <span>눈, 얼굴 방향, 움직임 신호를 바탕으로 졸음 상태를 분석합니다.</span>
                </div>
            </div>

            <div class="upload-feature-item">
                <div class="upload-feature-icon tone-red">🚶</div>
                <div class="upload-feature-copy">
                    <strong>이탈 감지</strong>
                    <span>자리 비움 또는 화면 이탈 구간을 리포트에 기록합니다.</span>
                </div>
            </div>

            <div class="upload-feature-item">
                <div class="upload-feature-icon tone-violet">📊</div>
                <div class="upload-feature-copy">
                    <strong>리포트 자동 생성</strong>
                    <span>분석 완료 후 이벤트 로그와 참여자별 통계를 자동으로 정리합니다.</span>
                </div>
            </div>
        </div>
    </section>
    """


def build_upload_tip_html() -> str:
    return """
    <section class="upload-tip-card">
        <div class="upload-tip-title">💡 분석 팁</div>
        <ul class="upload-tip-list">
            <li>참여자 얼굴이 비교적 선명한 영상을 사용하면 정확도가 높아집니다.</li>
            <li>Zoom, Meet 등 썸네일이 잘 보이는 수업 영상을 권장합니다.</li>
            <li>영상 길이가 길수록 추론 시간이 더 소요될 수 있습니다.</li>
        </ul>
    </section>
    """


def build_upload_time_intro_html() -> str:
    return """
    <section class="upload-time-card">
        <div class="upload-time-head">
            <div class="upload-time-icon">🕘</div>
            <div>
                <h3>수업 시작 시간 설정</h3>
                <p>리포트의 이벤트 시간 표시를 맞추기 위해 실제 수업 시작 시간을 선택합니다.</p>
            </div>
        </div>
    </section>
    """


def build_upload_time_preview_html(time_text: str) -> str:
    return f"""
    <div class="upload-time-preview">
        <div class="upload-time-preview-label">선택된 시작 시간</div>
        <div class="upload-time-preview-value">{html.escape(time_text)}</div>
    </div>
    """


def build_upload_file_state_html(file_path: str | None) -> str:
    if not file_path:
        return """
        <div class="upload-file-state upload-file-empty">
            <div class="upload-file-state-title">업로드 대기 중</div>
            <div class="upload-file-state-copy">MP4, MOV, AVI 등 수업 영상 파일을 선택해주세요.</div>
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

    summary_meta_map = {
        "총 참여자": "수업 전체 기준 집계",
        "평균 집중도": "참여자 평균 집중 상태",
        "졸음 감지 학생": "졸음 이벤트 발생 기준",
        "졸음 감지": "졸음 이벤트 발생 기준",
        "이탈 감지 학생": "이탈 이벤트 발생 기준",
        "이탈 감지": "이탈 이벤트 발생 기준",
    }

    summary_cards = "".join(
        f"""
        <article class="report-summary-card report-animate tone-{html.escape(card.get('tone', 'neutral'))} figma-card">
            <div class="report-summary-label">{html.escape(card.get('label', ''))}</div>
            <div class="report-summary-value">{html.escape(str(card.get('value', '-')))}</div>
            <div class="report-summary-meta">{html.escape(summary_meta_map.get(card.get('label', ''), '분석 결과 요약 지표'))}</div>
        </article>
        """
        for card in report_data.get("summary_cards", [])
    )

    events = report_data.get("events", [])
    event_config = {
        "positive": ("정상", "집중 상태가 유지되었습니다", "◉"),
        "warning": ("졸음", "졸음이 감지되었습니다", "▲"),
        "danger": ("이탈", "자리를 이탈했습니다", "●"),
        "neutral": ("이벤트", "상태가 기록되었습니다", "◆"),
    }

    events_html = (
        "".join(
            f"""
            <div class="report-event report-animate tone-{html.escape(event.get('tone', 'neutral'))}">
                <div class="report-event-icon">{event_config.get(event.get('tone', 'neutral'), event_config['neutral'])[2]}</div>
                <div class="report-event-copy">
                    <div class="report-event-head">
                        <strong class="report-event-label">{html.escape(event_config.get(event.get('tone', 'neutral'), event_config['neutral'])[0])}</strong>
                        <span class="report-event-time">{html.escape(event.get('time', ''))}</span>
                    </div>
                    <p>{html.escape(event_config.get(event.get('tone', 'neutral'), event_config['neutral'])[1])}</p>
                    <div class="report-event-participant">{html.escape(event.get('detail', ''))}</div>
                </div>
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
            <div class="participant-card report-animate figma-card">
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
    chart_points = report_data.get("chart_points", [])
    insights = report_data.get("insights", [])

    def _build_area_svg(points: list[dict[str, Any]]) -> str:
        if not points:
            return '<div class="report-placeholder">그래프를 표시할 히스토리가 아직 없습니다.</div>'

        width = 760
        height = 280
        left = 42
        right = 18
        top = 18
        bottom = 34
        chart_w = width - left - right
        chart_h = height - top - bottom

        max_total = max(
            max(
                int(point.get("normal", 0))
                + int(point.get("drowsy", 0))
                + int(point.get("absence", 0)),
                1,
            )
            for point in points
        )

        def x_at(idx: int) -> float:
            if len(points) == 1:
                return left + chart_w / 2
            return left + (chart_w * idx / (len(points) - 1))

        def y_at(value: float) -> float:
            return top + chart_h - ((value / max_total) * chart_h)

        xs = [x_at(idx) for idx in range(len(points))]
        normal_vals = [float(point.get("normal", 0)) for point in points]
        drowsy_vals = [
            float(point.get("normal", 0)) + float(point.get("drowsy", 0))
            for point in points
        ]
        absence_vals = [
            float(point.get("normal", 0))
            + float(point.get("drowsy", 0))
            + float(point.get("absence", 0))
            for point in points
        ]

        def polygon(top_values: list[float], bottom_values: list[float]) -> str:
            top_points = " ".join(
                f"{x:.1f},{y_at(v):.1f}" for x, v in zip(xs, top_values)
            )
            bottom_points = " ".join(
                f"{x:.1f},{y_at(v):.1f}"
                for x, v in zip(reversed(xs), reversed(bottom_values))
            )
            return f"{top_points} {bottom_points}"

        def polyline(values: list[float]) -> str:
            return " ".join(f"{x:.1f},{y_at(v):.1f}" for x, v in zip(xs, values))

        grid = "".join(
            f'<line x1="{left}" y1="{y_at(level):.1f}" x2="{width-right}" y2="{y_at(level):.1f}" class="chart-grid-line" />'
            for level in range(0, max_total + 1)
        )
        labels = "".join(
            f'<text x="{x:.1f}" y="{height-10}" text-anchor="middle" class="chart-axis-label">{html.escape(str(point.get("time", "")))}</text>'
            for x, point in zip(xs, points)
        )
        y_labels = "".join(
            f'<text x="{left-10}" y="{y_at(level)+4:.1f}" text-anchor="end" class="chart-axis-label">{level}</text>'
            for level in range(0, max_total + 1)
        )

        return f"""
        <div class="report-area-chart">
            <svg viewBox="0 0 {width} {height}" class="report-area-svg" preserveAspectRatio="none">
                {grid}
                <polygon points="{polygon(normal_vals, [0.0] * len(points))}" class="area-normal-fill" />
                <polygon points="{polygon(drowsy_vals, normal_vals)}" class="area-drowsy-fill" />
                <polygon points="{polygon(absence_vals, drowsy_vals)}" class="area-absence-fill" />
                <polyline points="{polyline(normal_vals)}" class="area-normal-line" />
                <polyline points="{polyline(drowsy_vals)}" class="area-drowsy-line" />
                <polyline points="{polyline(absence_vals)}" class="area-absence-line" />
                {labels}
                {y_labels}
            </svg>
        </div>
        """

    chart_html = (
        f"""
        <section class="report-card report-chart-card report-animate figma-card">
            <div class="report-card-head">
                <div>
                    <h3>↗ {html.escape(report_data.get('chart_title', '시간대별 상태 분석'))}</h3>
                    <span>{html.escape(report_data.get('chart_subtitle', '시간 흐름에 따른 상태 변화'))}</span>
                </div>
                <div class="report-chart-legend">
                    <span><i class="chart-dot chart-normal"></i>정상</span>
                    <span><i class="chart-dot chart-drowsy"></i>졸음</span>
                    <span><i class="chart-dot chart-absence"></i>이탈</span>
                </div>
            </div>
            <div class="report-chart-wrap">
                {_build_area_svg(chart_points)}
            </div>
        </section>
        """
        if chart_points
        else ""
    )

    insights_html = (
        "".join(
            f"""
            <div class="report-insight report-animate tone-{html.escape(item.get('tone', 'info'))}">
                <strong>{html.escape(item.get('title', '인사이트'))}</strong>
                <p>{html.escape(item.get('detail', ''))}</p>
            </div>
            """
            for item in insights
        )
        if insights
        else ""
    )

    is_upload_report = str(report_data.get("badge", "")).lower().startswith("upload")
    back_target = "report-upload-btn" if is_upload_report else "report-live-btn"
    action_buttons = (
        '<button class="report-download-btn">↓ PDF</button><button class="report-download-btn">↓ Excel</button>'
        if is_upload_report
        else '<button class="report-download-btn">↓ 리포트 다운로드</button>'
    )

    title = report_data.get("title", "실시간 분석 리포트")
    subtitle = report_data.get("subtitle", "분석 결과 요약")

    fallback_primary = (
        highlights[0]
        if highlights
        else "전체 수업 흐름과 주요 상태 변화를 종합해 확인할 수 있습니다."
    )
    fallback_secondary = (
        highlights[-1] if highlights else "이벤트가 발생한 시간대를 다시 확인해 주세요."
    )

    return f"""
    <section class="report-shell report-shell-realtime">
        <div class="report-topbar">
            <div class="report-topbar-main">
                <button class="report-topbar-back" onclick="clickHiddenButton('{back_target}')">←</button>
                <div>
                    <h2>{html.escape(title)}</h2>
                    <p>{html.escape(subtitle)}</p>
                </div>
            </div>
            <div class="report-topbar-actions">
                {action_buttons}
            </div>
        </div>

        <div class="report-summary-grid">
            {summary_cards}
        </div>

        {chart_html}

        <div class="report-grid">
            <section class="report-card report-animate figma-card">
                <div class="report-card-head">
                    <div>
                        <h3>⊙ 이벤트 로그</h3>
                        <span>졸음 및 이탈 발생 시점</span>
                    </div>
                </div>
                <div class="report-event-list">
                    {events_html}
                </div>
            </section>

            <section class="report-card report-animate figma-card">
                <div class="report-card-head">
                    <div>
                        <h3>참여자별 통계</h3>
                        <span>개인별 집중도 및 상태 분석</span>
                    </div>
                </div>
                <div class="participant-grid">
                    {participants_html}
                </div>
            </section>
        </div>

        <section class="report-card report-animate figma-card">
            <div class="report-card-head">
                <div>
                    <h3>분석 결과 및 제안</h3>
                    <span>전체 수업 흐름 요약</span>
                </div>
            </div>

            <div class="report-insight-grid">
                {insights_html or f'''
                <div class="report-insight report-animate tone-info">
                    <strong>분석 결과 요약</strong>
                    <p>{html.escape(fallback_primary)}</p>
                </div>
                '''}
                <div class="report-insight report-animate tone-warning">
                    <strong>추가 확인 권장</strong>
                    <p>{html.escape(fallback_secondary)}</p>
                </div>
            </div>
        </section>
    </section>
    """
