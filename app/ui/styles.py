from app.config import BG_H, BG_W, SLOT_H, SLOT_W, SLOT_X, SLOT_Y


def build_css() -> str:
    return f"""
    :root {{
        --bg-page: #0a0e1a;
        --bg-shell: #10172a;
        --bg-panel: #151b2e;
        --bg-panel-soft: rgba(21, 27, 46, 0.82);
        --bg-muted: #0f1729;
        --bg-elevated: #1b2540;
        --line: rgba(148, 163, 184, 0.14);
        --line-strong: rgba(96, 165, 250, 0.28);
        --text: #f8fafc;
        --text-soft: #cbd5e1;
        --text-muted: #94a3b8;
        --blue: #2563eb;
        --blue-soft: rgba(37, 99, 235, 0.12);
        --violet: #7c3aed;
        --violet-soft: rgba(124, 58, 237, 0.12);
        --green: #10b981;
        --green-soft: rgba(16, 185, 129, 0.14);
        --amber: #f59e0b;
        --amber-soft: rgba(245, 158, 11, 0.14);
        --red: #ef4444;
        --red-soft: rgba(239, 68, 68, 0.14);
        --radius-lg: 24px;
        --radius-md: 18px;
        --radius-sm: 14px;
        --shadow-xl: 0 30px 80px rgba(2, 6, 23, 0.42);
        --shadow-lg: 0 18px 40px rgba(2, 6, 23, 0.30);
    }}

    html, body {{
        margin: 0;
        padding: 0;
        overflow-x: hidden;
        background:
            radial-gradient(circle at top, rgba(37, 99, 235, 0.18), transparent 30%),
            radial-gradient(circle at 80% 10%, rgba(124, 58, 237, 0.14), transparent 24%),
            linear-gradient(180deg, #09111f 0%, #0a0e1a 55%, #080d18 100%);
    }}

    body {{
        color: var(--text);
    }}

    .gradio-container,
    .gradio-container .main,
    .gradio-container .wrap,
    .gradio-container .contain {{
        background: transparent !important;
        margin: 0 !important;
        padding: 0 !important;
        max-width: 100% !important;
    }}

    .gradio-container {{
        min-height: 100vh;
        color: var(--text);
    }}

    #app-root {{
        width: 100%;
        max-width: 1280px;
        margin: 0 auto;
        padding: 28px 24px 40px;
        box-sizing: border-box;
    }}

    .view-shell {{
        display: flex;
        flex-direction: column;
        gap: 24px;
    }}

    .view-card {{
        background: linear-gradient(180deg, rgba(21, 27, 46, 0.96) 0%, rgba(14, 20, 38, 0.96) 100%);
        border: 1px solid var(--line);
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-xl);
        overflow: hidden;
    }}

    .shell-header {{
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 16px;
        padding: 26px 28px 0;
    }}

    .shell-header-main {{
        display: flex;
        align-items: flex-start;
        gap: 14px;
    }}

    .shell-copy {{
        display: flex;
        flex-direction: column;
        gap: 6px;
    }}

    .shell-eyebrow,
    .report-eyebrow,
    .topbar-label,
    .mode-card-subtitle {{
        color: #93c5fd;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }}

    .shell-copy h1,
    .home-hero h1,
    .report-hero h2 {{
        margin: 0;
        font-size: 40px;
        line-height: 1.05;
        font-weight: 700;
        letter-spacing: -0.03em;
        color: var(--text);
    }}

    .shell-copy p,
    .home-hero p,
    .report-hero p,
    .upload-intro p,
    .upload-intro li {{
        margin: 0;
        color: var(--text-muted);
        font-size: 15px;
        line-height: 1.6;
    }}

    .shell-header-actions {{
        display: flex;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
    }}

    .shell-badge,
    .hero-badge,
    .upload-intro-badge,
    .topbar-badge,
    .report-source {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 10px 14px;
        border-radius: 999px;
        border: 1px solid rgba(96, 165, 250, 0.22);
        background: rgba(37, 99, 235, 0.12);
        color: #bfdbfe;
        font-size: 12px;
        font-weight: 600;
    }}

    .shell-action {{
        border: none;
        border-radius: 14px;
        padding: 12px 18px;
        color: var(--text);
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        transition: transform 0.18s ease, background 0.18s ease, border-color 0.18s ease;
    }}

    .shell-action:hover {{
        transform: translateY(-1px);
    }}

    .shell-action-primary {{
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        box-shadow: 0 12px 30px rgba(37, 99, 235, 0.25);
    }}

    .shell-action-secondary {{
        background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
        box-shadow: 0 12px 30px rgba(124, 58, 237, 0.22);
    }}

    .shell-action-ghost {{
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid var(--line);
    }}

    .home-shell {{
        position: relative;
        min-height: calc(100vh - 68px);
        background: transparent;
        border: none;
        box-shadow: none;
        overflow: visible;
    }}

    .home-hero {{
        position: relative;
        padding: 36px 28px 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        gap: 16px;
        overflow: hidden;
    }}

    .home-hero h1 {{
        max-width: 920px;
        font-size: 48px;
        line-height: 1.08;
    }}

    .hero-note {{
        max-width: 760px;
        color: #94a3b8;
        font-size: 20px;
        line-height: 1.55;
    }}

    .home-bg {{
        position: absolute;
        border-radius: 999px;
        filter: blur(80px);
        pointer-events: none;
        opacity: 0.9;
    }}

    .home-bg-blue {{
        width: 360px;
        height: 240px;
        top: -30px;
        left: 16%;
        background: rgba(37, 99, 235, 0.18);
    }}

    .home-bg-violet {{
        width: 320px;
        height: 220px;
        top: 20px;
        right: 18%;
        background: rgba(124, 58, 237, 0.16);
    }}

    .hero-badge-icon {{
        color: #60a5fa;
        font-size: 14px;
        line-height: 1;
    }}

    .home-card-grid {{
        max-width: 1024px;
        margin: 0 auto;
        gap: 24px;
        padding: 22px 28px 28px;
    }}

    .mode-card {{
        height: 100%;
        min-height: 540px;
        padding: 30px;
        border-radius: 24px;
        border: 1px solid rgba(71, 85, 105, 0.55);
        background:
            linear-gradient(180deg, rgba(31, 41, 55, 0.98) 0%, rgba(30, 41, 59, 0.98) 100%);
        box-shadow: 0 16px 34px rgba(2, 6, 23, 0.24);
        cursor: pointer;
        transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease, background 0.22s ease;
    }}

    .mode-card:hover {{
        transform: translateY(-6px);
    }}

    .mode-card-blue:hover {{
        border-color: rgba(59, 130, 246, 0.46);
        box-shadow: 0 22px 44px rgba(37, 99, 235, 0.14);
    }}

    .mode-card-violet:hover {{
        border-color: rgba(168, 85, 247, 0.46);
        box-shadow: 0 22px 44px rgba(124, 58, 237, 0.14);
    }}

    .mode-card-icon {{
        width: 56px;
        height: 56px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 14px;
        margin-bottom: 18px;
        background: rgba(255, 255, 255, 0.05);
        font-size: 26px;
    }}

    .mode-card-blue .mode-card-icon {{
        background: rgba(59, 130, 246, 0.10);
        border: 1px solid rgba(59, 130, 246, 0.20);
        color: #60a5fa;
    }}

    .mode-card-violet .mode-card-icon {{
        background: rgba(168, 85, 247, 0.10);
        border: 1px solid rgba(168, 85, 247, 0.20);
        color: #c084fc;
    }}

    .mode-card-copy {{
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-bottom: 18px;
    }}

    .mode-card h2,
    .upload-intro h2 {{
        margin: 0;
        color: var(--text);
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.02em;
    }}

    .mode-card p {{
        margin: 0;
        color: #cbd5e1;
        line-height: 1.7;
        font-size: 16px;
    }}

    .mode-card-list,
    .upload-intro ul,
    .report-highlight-list {{
        margin: 0;
        padding-left: 0;
        display: flex;
        flex-direction: column;
        gap: 12px;
    }}

    .mode-feature {{
        display: flex;
        align-items: flex-start;
        gap: 12px;
    }}

    .mode-feature-icon {{
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        flex-shrink: 0;
        margin-top: 2px;
        font-size: 14px;
    }}

    .mode-card-blue .mode-feature-icon {{
        background: rgba(59, 130, 246, 0.10);
        color: #60a5fa;
    }}

    .mode-card-violet .mode-feature-icon {{
        background: rgba(168, 85, 247, 0.10);
        color: #c084fc;
    }}

    .mode-feature-copy {{
        display: flex;
        flex-direction: column;
        gap: 3px;
    }}

    .mode-feature-title {{
        color: #e2e8f0;
        font-size: 14px;
        line-height: 1.5;
    }}

    .mode-feature-desc {{
        color: #64748b;
        font-size: 12px;
        line-height: 1.55;
    }}

    .mode-feature-title,
    .mode-card h2,
    .mode-card-cta {{
        letter-spacing: -0.01em;
    }}

    .mode-card-cta {{
        margin-top: 26px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        min-height: 48px;
        border-radius: 14px;
        font-weight: 700;
        background: rgba(255, 255, 255, 0.06);
        color: white;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08);
    }}

    .mode-card-blue .mode-card-cta {{
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        box-shadow: 0 18px 30px rgba(37, 99, 235, 0.18);
    }}

    .mode-card-violet .mode-card-cta {{
        background: linear-gradient(135deg, #9333ea 0%, #7e22ce 100%);
        box-shadow: 0 18px 30px rgba(147, 51, 234, 0.18);
    }}

    .live-layout,
    .upload-layout,
    .report-actions {{
        gap: 20px;
        padding: 0 28px 28px !important;
    }}

    .live-layout {{
        display: grid !important;
        grid-template-columns: minmax(0, 1.5fr) minmax(360px, 0.9fr);
        align-items: start;
    }}

    .upload-layout {{
        display: grid !important;
        grid-template-columns: minmax(0, 1.2fr) minmax(320px, 0.8fr);
        align-items: start;
    }}

    .report-actions {{
        display: flex !important;
        flex-wrap: wrap;
    }}

    #stage-shell,
    .panel-shell,
    .upload-intro,
    .upload-feature-card,
    .report-shell {{
        background: var(--bg-panel-soft);
        border: 1px solid var(--line);
        border-radius: 24px;
        box-shadow: var(--shadow-lg);
    }}

    #stage-shell {{
        padding: 22px;
    }}

    #stage-topbar {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 16px;
    }}

    .topbar-title {{
        margin-top: 6px;
        color: var(--text);
        font-size: 22px;
        font-weight: 700;
    }}

    #demo-stage {{
        position: relative;
        width: 100%;
        aspect-ratio: {BG_W} / {BG_H};
        border-radius: 20px;
        overflow: hidden;
        border: 1px solid var(--line);
        background: #050816;
    }}

    #stage-bg-video,
    #stage-bg-image {{
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        z-index: 0;
    }}

    #stage-bg-video {{
        object-fit: cover;
        background: #050816;
    }}

    #stage-bg-image {{
        background-position: center;
        background-repeat: no-repeat;
        background-size: cover;
    }}

    #student-cam,
    #cam-placeholder {{
        position: absolute;
        left: {SLOT_X / BG_W * 100:.6f}%;
        top: {SLOT_Y / BG_H * 100:.6f}%;
        width: {SLOT_W / BG_W * 100:.6f}%;
        height: {SLOT_H / BG_H * 100:.6f}%;
        border-radius: 18px;
        box-sizing: border-box;
        z-index: 3;
    }}

    #student-cam {{
        object-fit: cover;
        transform: scaleX(-1);
        background: #0a0a0a;
        border: 3px solid rgba(59, 130, 246, 0.85);
        box-shadow: 0 18px 34px rgba(2, 6, 23, 0.42);
        z-index: 4;
    }}

    #cam-placeholder {{
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 12px;
        color: #dbeafe;
        font-size: 13px;
        line-height: 1.5;
        background: rgba(15, 23, 42, 0.66);
        border: 1px dashed rgba(96, 165, 250, 0.35);
    }}

    #bbox-overlay {{
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        z-index: 5;
        pointer-events: none;
    }}

    #stage-caption {{
        margin-top: 12px;
        color: var(--text-muted);
        font-size: 13px;
    }}

    .panel-shell {{
        padding: 22px;
        display: flex;
        flex-direction: column;
        gap: 16px;
        min-height: 100%;
    }}

    .panel-card {{
        padding: 18px;
        border-radius: 20px;
        border: 1px solid var(--line);
        background: rgba(15, 23, 42, 0.64);
    }}

    .panel-card-head {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
    }}

    .panel-card-head h3,
    .panel-status-card h3 {{
        margin: 4px 0 0;
        color: var(--text);
        font-size: 20px;
        font-weight: 700;
    }}

    .panel-eyebrow {{
        color: #93c5fd;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }}

    .panel-live-chip {{
        padding: 8px 12px;
        border-radius: 999px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.28);
        color: #6ee7b7;
        font-size: 12px;
        font-weight: 600;
    }}

    .panel-button-row {{
        margin-top: 16px;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
    }}

    .panel-action {{
        min-height: 48px;
        border: none;
        border-radius: 14px;
        font-size: 15px;
        font-weight: 700;
        color: white;
        cursor: pointer;
    }}

    .panel-action-primary {{
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    }}

    .panel-action-danger {{
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    }}

    .panel-action.is-disabled {{
        opacity: 0.45;
        cursor: not-allowed;
    }}

    .panel-status-dot {{
        width: 11px;
        height: 11px;
        border-radius: 999px;
        display: inline-flex;
        flex-shrink: 0;
    }}

    .panel-status-desc,
    .panel-status-summary,
    .panel-empty,
    .panel-alert p {{
        margin: 12px 0 0;
        color: var(--text-muted);
        font-size: 13px;
        line-height: 1.6;
    }}

    .panel-list-wrap {{
        margin-top: 14px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        max-height: 280px;
        overflow: auto;
    }}

    .panel-list-item,
    .panel-alert {{
        padding: 12px 14px;
        border-radius: 16px;
        border: 1px solid var(--line);
        background: rgba(8, 13, 24, 0.34);
    }}

    .panel-list-item {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        color: var(--text-soft);
    }}

    .panel-list-meta {{
        display: flex;
        align-items: center;
        gap: 10px;
    }}

    .panel-alert-head {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
    }}

    .panel-alert.tone-warning {{
        background: rgba(245, 158, 11, 0.10);
        border-color: rgba(245, 158, 11, 0.24);
    }}

    .panel-alert.tone-danger {{
        background: rgba(239, 68, 68, 0.10);
        border-color: rgba(239, 68, 68, 0.24);
    }}

    .upload-intro,
    .upload-feature-card,
    .report-shell {{
        padding: 22px;
    }}

    .upload-intro {{
        display: flex;
        flex-direction: column;
        gap: 14px;
    }}

    .upload-feature-card h3,
    .report-card-head h3 {{
        margin: 0;
        color: var(--text);
        font-size: 18px;
        font-weight: 700;
    }}

    .upload-feature-list {{
        display: flex;
        flex-direction: column;
        gap: 14px;
    }}

    .upload-feature-item {{
        display: flex;
        flex-direction: column;
        gap: 4px;
        padding: 14px;
        border-radius: 16px;
        background: rgba(15, 23, 42, 0.64);
        border: 1px solid var(--line);
    }}

    .upload-feature-item strong,
    .participant-head strong,
    .report-event-head strong {{
        color: var(--text);
        font-size: 14px;
    }}

    .upload-feature-item span,
    .participant-meta span,
    .report-event p,
    .report-highlight-list li {{
        color: var(--text-muted);
        font-size: 13px;
        line-height: 1.6;
    }}

    .upload-file-state {{
        padding: 16px 18px;
        border-radius: 18px;
        background: rgba(37, 99, 235, 0.10);
        border: 1px solid rgba(96, 165, 250, 0.2);
    }}

    .upload-file-empty {{
        background: rgba(15, 23, 42, 0.64);
        border-color: var(--line);
    }}

    .upload-file-state-title {{
        color: var(--text);
        font-size: 15px;
        font-weight: 700;
    }}

    .upload-file-state-copy {{
        margin-top: 4px;
        color: var(--text-muted);
        font-size: 13px;
    }}

    .upload-status-markdown,
    .upload-status-markdown p {{
        margin: 0 !important;
        color: var(--text-soft) !important;
        line-height: 1.6 !important;
    }}

    .primary-action button,
    .secondary-action button,
    .ghost-action button {{
        min-height: 52px;
        border-radius: 16px !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        transition: transform 0.18s ease, filter 0.18s ease !important;
    }}

    .primary-action button:hover,
    .secondary-action button:hover,
    .ghost-action button:hover {{
        transform: translateY(-1px);
        filter: brightness(1.04);
    }}

    .primary-action button {{
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: white !important;
        box-shadow: 0 12px 26px rgba(37, 99, 235, 0.24);
    }}

    .secondary-action button {{
        background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%) !important;
        color: white !important;
        box-shadow: 0 12px 26px rgba(124, 58, 237, 0.22);
    }}

    .ghost-action button {{
        background: rgba(15, 23, 42, 0.72) !important;
        color: var(--text) !important;
        border: 1px solid var(--line) !important;
    }}

    .upload-file,
    .upload-time-box,
    .debug-panel,
    .report-action-wrap {{
        border-radius: 18px;
        overflow: hidden;
    }}

    .upload-file {{
        padding: 8px;
        background: rgba(15, 23, 42, 0.64);
        border: 1px dashed rgba(167, 139, 250, 0.4);
    }}

    .upload-file label {{
        color: var(--text-soft) !important;
    }}

    .upload-file button {{
        border-radius: 14px !important;
    }}

    .upload-time-box textarea,
    .upload-time-box input,
    .debug-panel textarea,
    .debug-panel input {{
        background: rgba(15, 23, 42, 0.80) !important;
        color: var(--text) !important;
        border: 1px solid var(--line) !important;
        border-radius: 14px !important;
    }}

    .report-shell {{
        display: flex;
        flex-direction: column;
        gap: 20px;
    }}

    .report-hero {{
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 16px;
    }}

    .report-summary-grid,
    .report-grid,
    .participant-grid {{
        display: grid;
        gap: 16px;
    }}

    .report-summary-grid {{
        grid-template-columns: repeat(4, minmax(0, 1fr));
    }}

    .report-summary-card,
    .report-card,
    .participant-card {{
        border-radius: 20px;
        border: 1px solid var(--line);
        background: rgba(15, 23, 42, 0.66);
    }}

    .report-summary-card {{
        padding: 18px;
    }}

    .report-summary-label,
    .report-card-head span,
    .participant-head span,
    .report-event-head span {{
        color: var(--text-muted);
        font-size: 12px;
    }}

    .report-summary-value {{
        margin-top: 10px;
        color: var(--text);
        font-size: 32px;
        font-weight: 700;
        letter-spacing: -0.03em;
    }}

    .tone-positive .report-summary-value,
    .tone-positive {{
        color: #34d399;
    }}

    .tone-warning .report-summary-value,
    .tone-warning {{
        color: #fbbf24;
    }}

    .tone-danger .report-summary-value,
    .tone-danger {{
        color: #f87171;
    }}

    .report-grid {{
        grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr);
    }}

    .report-card {{
        padding: 20px;
    }}

    .report-chart-card {{
        overflow: hidden;
    }}

    .report-chart-legend {{
        display: flex;
        align-items: center;
        gap: 14px;
        flex-wrap: wrap;
        color: var(--text-muted);
        font-size: 12px;
    }}

    .report-chart-legend span {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }}

    .chart-dot {{
        width: 10px;
        height: 10px;
        border-radius: 999px;
        display: inline-flex;
    }}

    .chart-normal {{
        background: #10b981;
    }}

    .chart-drowsy {{
        background: #f59e0b;
    }}

    .chart-absence {{
        background: #ef4444;
    }}

    .report-chart-wrap {{
        margin-top: 18px;
        min-height: 260px;
        padding: 18px 14px 12px;
        border-radius: 18px;
        border: 1px solid var(--line);
        background:
            linear-gradient(180deg, rgba(15, 23, 42, 0.78) 0%, rgba(8, 13, 24, 0.82) 100%);
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(54px, 1fr));
        gap: 12px;
        align-items: end;
    }}

    .report-chart-col {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
        min-width: 0;
    }}

    .report-chart-stack {{
        width: 100%;
        min-height: 190px;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        gap: 4px;
    }}

    .chart-segment {{
        width: 100%;
        border-radius: 10px 10px 4px 4px;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.14);
    }}

    .report-chart-label {{
        color: var(--text-muted);
        font-size: 11px;
        text-align: center;
        white-space: nowrap;
    }}

    .report-card-head,
    .participant-head,
    .report-event-head {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
    }}

    .report-event-list,
    .participant-grid {{
        display: flex;
        flex-direction: column;
        gap: 12px;
        margin-top: 14px;
    }}

    .report-event {{
        padding: 14px;
        border-radius: 16px;
        border: 1px solid var(--line);
        background: rgba(8, 13, 24, 0.42);
    }}

    .report-event.tone-positive {{
        background: var(--green-soft);
        border-color: rgba(16, 185, 129, 0.24);
    }}

    .report-event.tone-warning {{
        background: var(--amber-soft);
        border-color: rgba(245, 158, 11, 0.24);
    }}

    .report-event.tone-danger {{
        background: var(--red-soft);
        border-color: rgba(239, 68, 68, 0.24);
    }}

    .report-placeholder,
    .report-empty {{
        padding: 22px;
        border-radius: 18px;
        text-align: center;
        background: rgba(15, 23, 42, 0.64);
        border: 1px solid var(--line);
        color: var(--text-muted);
    }}

    .report-empty h2 {{
        margin: 0 0 8px;
        color: var(--text);
    }}

    .participant-card {{
        padding: 16px;
    }}

    .participant-bar {{
        margin-top: 12px;
        display: flex;
        height: 8px;
        border-radius: 999px;
        overflow: hidden;
        background: rgba(51, 65, 85, 0.8);
    }}

    .participant-bar .tone-positive {{
        background: var(--green);
    }}

    .participant-bar .tone-warning {{
        background: var(--amber);
    }}

    .participant-bar .tone-danger {{
        background: var(--red);
    }}

    .participant-meta {{
        margin-top: 10px;
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
    }}

    .bridge-hidden {{
        display: none !important;
    }}

    @media (max-width: 1024px) {{
        .report-summary-grid {{
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }}

        .report-grid,
        .live-layout,
        .upload-layout {{
            grid-template-columns: 1fr !important;
        }}
    }}

    @media (max-width: 768px) {{
        #app-root {{
            padding: 18px 14px 28px;
        }}

        .shell-header,
        .home-hero,
        .home-card-grid,
        .live-layout,
        .upload-layout,
        .report-actions {{
            padding-left: 16px !important;
            padding-right: 16px !important;
        }}

        .shell-header,
        .shell-header-main,
        .report-hero {{
            flex-direction: column;
        }}

        .shell-copy h1,
        .home-hero h1,
        .report-hero h2 {{
            font-size: 30px;
        }}

        .hero-note {{
            font-size: 16px;
        }}

        .mode-card {{
            min-height: auto;
            padding: 24px;
        }}

        .report-summary-grid {{
            grid-template-columns: 1fr;
        }}
    }}
    """
