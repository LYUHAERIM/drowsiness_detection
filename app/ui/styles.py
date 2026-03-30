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
        --radius-xl: 28px;
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
    .gradio-container .contain,
    #demo-root,
    #demo-root > .gr-block,
    .demo-root,
    .figma-app-root {{
        background: transparent !important;
        margin: 0 !important;
        padding: 0 !important;
        max-width: 100% !important;
        border: none !important;
        box-shadow: none !important;
    }}

    .gradio-container {{
        min-height: 100vh;
        color: var(--text);
    }}

    #app-root {{
        width: 100%;
        max-width: 1280px;
        margin: 0 auto !important;
        padding: 6px 24px 20px !important;
        box-sizing: border-box;
        gap: 0 !important;
    }}

    #app-root,
    #app-root > .gr-block,
    #app-root > .gr-block > .gr-block,
    #app-root .gr-group,
    #app-root .gr-box,
    #app-root .gr-panel,
    #app-root .block,
    #app-root .gradio-html,
    #app-root .gr-row,
    #app-root .gr-column {{
        margin-top: 0 !important;
    }}

    .view-shell {{
        display: flex;
        flex-direction: column;
        gap: 24px;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    .view-shell > .gr-block,
    .view-shell .gr-group,
    .view-shell .gr-box,
    .view-shell .gr-panel,
    .view-shell .block,
    .view-shell .gradio-html {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    .page-shell {{
        background: transparent;
        border: none;
        box-shadow: none;
    }}

    .shell-header-wrap,
    .home-hero-wrap,
    .home-footer-wrap,
    .home-card-grid-wrap,
    .home-top-spacer-wrap,
    .live-stage-html,
    .live-panel-html,
    .upload-intro-wrap,
    .upload-file-state-wrap,
    .upload-feature-wrap,
    .upload-time-intro-wrap,
    .upload-time-preview-wrap,
    .upload-tip-wrap,
    .report-html-shell {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
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
        position: sticky;
        top: 16px;
        z-index: 5;
        padding: 16px 20px;
        border-radius: 20px;
        border: 1px solid rgba(30, 41, 59, 0.78);
        background: rgba(21, 27, 46, 0.86);
        backdrop-filter: blur(12px);
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
        font-size: 22px;
        line-height: 1.15;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: var(--text);
    }}

    .shell-copy p,
    .home-hero p,
    .report-hero p,
    .upload-intro p,
    .upload-intro li {{
        margin: 0;
        color: var(--text-muted);
        font-size: 13px;
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

    #home-view {{
        position: relative;
        min-height: 0;
        gap: 0;
        background:
            radial-gradient(circle at 50% 0%, rgba(17, 24, 39, 0.52), transparent 48%),
            linear-gradient(180deg, #0a0e1a 0%, #0a0e1a 100%);
        border: none;
        box-shadow: none;
        overflow: visible;
        border-radius: var(--radius-xl);
        isolation: isolate;
    }}

    #home-view,
    #home-view > .gr-block,
    #home-view > .gr-block > .gr-block,
    #home-view .gr-group,
    #home-view .gr-box,
    #home-view .gr-panel,
    #home-view .block,
    #home-view .gradio-html,
    #home-view .gr-row,
    #home-view .gr-column,
    #home-shell-inner,
    #home-shell-inner > .gr-block,
    #home-shell-inner > .gr-block > .gr-block,
    #home-shell-inner .gr-group,
    #home-shell-inner .gr-box,
    #home-shell-inner .gr-panel,
    #home-shell-inner .block,
    #home-shell-inner .gradio-html,
    #home-shell-inner .gr-row,
    #home-shell-inner .gr-column {{
        background: #0a0e1a !important;
        border: none !important;
        box-shadow: none !important;
        margin: 0 !important;
        padding: 0 !important;
        min-height: 0 !important;
    }}

    #home-view,
    #home-shell-inner {{
        display: flex;
        flex-direction: column;
        gap: 0;
    }}

    #home-shell-inner {{
        padding-top: 20px !important;
    }}

    #home-top-spacer,
    #home-top-spacer > .gr-block,
    #home-top-spacer .gradio-html,
    #home-top-spacer .html-container,
    #home-top-spacer .prose {{
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        box-shadow: none !important;
        background: transparent !important;
        min-height: 0 !important;
    }}

    .home-top-spacer {{
        height: 20px;
        width: 100%;
        display: block;
    }}

    #home-hero-block,
    #home-footer-block,
    #home-card-grid-block,
    #home-hero-block > .gr-block,
    #home-footer-block > .gr-block,
    #home-card-grid-block > .gr-block,
    #home-view .home-html-wrap,
    #home-view .home-html-wrap .gradio-html,
    #home-view .home-html-wrap .prose {{
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        box-shadow: none !important;
        min-height: 0 !important;
        background: transparent !important;
    }}

    #home-hero-block,
    #home-hero-block.gradio-html,
    #home-hero-block > .html-container,
    #home-hero-block .html-container,
    #home-hero-block .html-container.svelte-1jts93g,
    #home-hero-block .prose {{
        margin: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        min-height: 0 !important;
        height: auto !important;
    }}

    #home-hero-section,
    .home-hero {{
        position: relative;
        padding: 0 24px 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        gap: 10px;
        overflow: hidden;
    }}

    #home-hero-section h1,
    .home-hero h1 {{
        max-width: 1080px;
        margin-top: 0;
        margin-bottom: 14px;
        font-size: 56px;
        line-height: 1.06;
        font-weight: 800;
    }}

    .hero-note {{
        max-width: 860px;
        color: #94a3b8;
        font-size: 24px;
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
        width: 620px;
        height: 360px;
        top: -140px;
        left: calc(50% - 310px);
        background: rgba(17, 24, 39, 0.44);
    }}

    .home-bg-violet {{
        display: none;
    }}

    #home-hero-section .hero-badge,
    .hero-badge {{
        margin-bottom: 14px;
        padding: 10px 18px;
        border-radius: 999px;
        border: 1px solid rgba(59, 130, 246, 0.20);
        background: rgba(59, 130, 246, 0.10);
        color: #93c5fd;
        font-size: 16px;
        font-weight: 500;
    }}

    .hero-badge-icon {{
        color: #60a5fa;
        font-size: 14px;
        line-height: 1;
    }}

    #home-card-grid-block,
    #home-card-grid-block > .gr-block,
    #home-card-grid-block .gradio-html,
    #home-card-grid-block .html-container,
    #home-card-grid-block .prose {{
        width: 100% !important;
        max-width: none !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        box-shadow: none !important;
        background: transparent !important;
    }}

    #home-card-grid,
    .home-card-grid {{
        max-width: 1200px;
        margin: 0 auto;
        width: 100%;
        display: grid !important;
        grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
        align-items: stretch !important;
        gap: 28px;
        padding: 32px 24px 0 !important;
        box-sizing: border-box;
    }}

    #home-card-grid .home-card-item {{
        min-width: 0 !important;
        width: 100% !important;
        display: flex !important;
        align-self: stretch !important;
    }}

    #home-card-grid .home-card-item > * {{
        width: 100% !important;
        display: flex !important;
        flex: 1 1 auto !important;
        min-width: 0 !important;
    }}

    #home-card-grid .home-card-item .html-container,
    #home-card-grid .home-card-item .prose {{
        width: 100% !important;
        display: flex !important;
        flex: 1 1 auto !important;
        min-width: 0 !important;
        background: transparent !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    #home-live-card,
    #home-upload-card,
    .mode-card {{
        display: flex;
        flex-direction: column;
        align-items: stretch;
        width: 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
        height: 640px;
        min-height: 640px;
        max-height: 640px;
        padding: 40px;
        border-radius: 18px;
        border: 1px solid rgba(30, 41, 59, 0.95);
        background: #151b2e;
        box-shadow: none;
        cursor: pointer;
        transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease, background 0.22s ease;
        box-sizing: border-box;
    }}

    .mode-card-body {{
        display: flex;
        flex: 1 1 auto;
        flex-direction: column;
        min-height: 0;
        height: 100%;
    }}

    .mode-card:hover {{
        transform: translateY(-2px);
    }}

    .mode-card-blue:hover {{
        border-color: rgba(51, 65, 85, 0.98);
        box-shadow: 0 22px 44px rgba(37, 99, 235, 0.14);
    }}

    .mode-card-violet:hover {{
        border-color: rgba(51, 65, 85, 0.98);
        box-shadow: 0 22px 44px rgba(124, 58, 237, 0.14);
    }}

    .mode-card-icon {{
        width: 72px;
        height: 72px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 16px;
        margin-bottom: 22px;
        background: rgba(15, 23, 42, 0.28);
        font-size: 30px;
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
        font-size: 38px;
        font-weight: 800;
        letter-spacing: -0.02em;
    }}

    .mode-card-subtitle {{
        color: #94a3b8;
        font-size: 19px;
        font-weight: 500;
        letter-spacing: 0;
        text-transform: none;
    }}

    .mode-card p {{
        margin: 0;
        color: #cbd5e1;
        line-height: 1.65;
        font-size: 20px;
    }}

    .mode-card-list,
    .upload-intro ul,
    .report-highlight-list {{
        margin: 0;
        padding-left: 0;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }}

    .mode-card-list {{
        flex: 1 1 auto;
    }}

    .mode-feature {{
        display: flex;
        align-items: flex-start;
        gap: 12px;
    }}

    .mode-feature-icon {{
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        flex-shrink: 0;
        margin-top: 2px;
        font-size: 16px;
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
        gap: 2px;
    }}

    .mode-feature-title {{
        color: #e2e8f0;
        font-size: 18px;
        line-height: 1.5;
        font-weight: 600;
    }}

    .mode-feature-desc {{
        color: #64748b;
        font-size: 15px;
        line-height: 1.5;
    }}

    .mode-feature-title,
    .mode-card h2,
    .mode-card-cta {{
        letter-spacing: -0.01em;
    }}

    .mode-card-action-row {{
        display: flex;
        margin-top: auto;
        padding-top: 28px;
    }}

    .mode-card-cta {{
        margin-top: auto;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        min-height: 56px;
        border-radius: 12px;
        font-size: 17px;
        font-weight: 700;
        background: rgba(255, 255, 255, 0.06);
        color: white;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08);
    }}

    .mode-card-blue .mode-card-cta {{
        background: #2563eb;
        box-shadow: 0 12px 28px rgba(37, 99, 235, 0.20);
    }}

    .mode-card-violet .mode-card-cta {{
        background: #9333ea;
        box-shadow: 0 12px 28px rgba(147, 51, 234, 0.20);
    }}

    #home-footer-section,
    .home-footer {{
        padding: 28px 24px 8px;
        text-align: center;
    }}

    .home-footer p {{
        margin: 0;
        color: #475569;
        font-size: 16px;
    }}

    .live-page-shell,
    .upload-page-shell,
    .report-view-shell {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    .live-page-shell > .gr-block,
    .live-page-shell .gr-group,
    .live-page-shell .gr-box,
    .live-page-shell .gr-panel,
    .live-page-shell .block,
    .live-page-inner,
    .live-page-inner > .gr-block,
    .live-page-inner .gr-group,
    .live-page-inner .gr-box,
    .live-page-inner .gr-panel,
    .live-page-inner .block,
    .upload-page-shell > .gr-block,
    .upload-page-shell .gr-group,
    .upload-page-shell .gr-box,
    .upload-page-shell .gr-panel,
    .upload-page-shell .block,
    .upload-page-inner,
    .upload-page-inner > .gr-block,
    .upload-page-inner .gr-group,
    .upload-page-inner .gr-box,
    .upload-page-inner .gr-panel,
    .upload-page-inner .block,
    .report-view-shell > .gr-block,
    .report-view-shell .gr-group,
    .report-view-shell .gr-box,
    .report-view-shell .gr-panel,
    .report-view-shell .block,
    .report-page-inner,
    .report-page-inner > .gr-block,
    .report-page-inner .gr-group,
    .report-page-inner .gr-box,
    .report-page-inner .gr-panel,
    .report-page-inner .block {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    .live-page-inner,
    .upload-page-inner,
    .report-page-inner {{
        display: flex;
        flex-direction: column;
        gap: 24px;
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

    .live-stage-column,
    .live-stage-column > .gr-block,
    .live-panel-column,
    .live-panel-column > .gr-block,
    .upload-main-column,
    .upload-main-column > .gr-block,
    .upload-side-column,
    .upload-side-column > .gr-block,
    .upload-main-stack,
    .upload-main-stack > .gr-block,
    .upload-side-stack,
    .upload-side-stack > .gr-block,
    .report-action-btn,
    .report-action-btn > .gr-block,
    .report-html-shell,
    .report-html-shell > .gr-block {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    .upload-main-stack,
    .upload-side-stack {{
        display: flex;
        flex-direction: column;
        gap: 16px;
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

    .upload-intro-head {{
        display: flex;
        align-items: flex-start;
        gap: 14px;
    }}

    .upload-intro-icon {{
        width: 44px;
        height: 44px;
        border-radius: 14px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: rgba(124, 58, 237, 0.10);
        border: 1px solid rgba(167, 139, 250, 0.22);
        color: #c084fc;
        font-size: 18px;
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
        align-items: flex-start;
        gap: 12px;
        padding: 14px;
        border-radius: 16px;
        background: rgba(15, 23, 42, 0.64);
        border: 1px solid var(--line);
    }}

    .upload-feature-icon {{
        width: 38px;
        height: 38px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        flex-shrink: 0;
        font-size: 16px;
    }}

    .upload-feature-icon.tone-emerald {{
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.22);
    }}

    .upload-feature-icon.tone-amber {{
        background: rgba(245, 158, 11, 0.12);
        border: 1px solid rgba(245, 158, 11, 0.22);
    }}

    .upload-feature-icon.tone-violet {{
        background: rgba(124, 58, 237, 0.12);
        border: 1px solid rgba(124, 58, 237, 0.22);
    }}

    .upload-feature-icon.tone-red {{
        background: rgba(239, 68, 68, 0.10);
        border: 1px solid rgba(248, 113, 113, 0.22);
    }}

    .upload-feature-copy {{
        display: flex;
        flex-direction: column;
        gap: 4px;
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

    .primary-action,
    .secondary-action,
    .ghost-action {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
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
        background: rgba(15, 23, 42, 0.64) !important;
        border: 1px dashed rgba(167, 139, 250, 0.4) !important;
    }}

    .upload-file > .gr-block,
    .upload-file .gr-group,
    .upload-file .gr-box,
    .upload-file .gr-panel,
    .upload-file .block {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
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

    .upload-time-card {{
        padding: 18px;
        border-radius: 18px;
        border: 1px solid rgba(124, 58, 237, 0.20);
        background: linear-gradient(180deg, rgba(124, 58, 237, 0.08) 0%, rgba(37, 99, 235, 0.06) 100%);
    }}

    .upload-time-head {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}

    .upload-time-icon {{
        width: 42px;
        height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 14px;
        background: rgba(124, 58, 237, 0.16);
        border: 1px solid rgba(167, 139, 250, 0.22);
        font-size: 18px;
    }}

    .upload-time-head h3 {{
        margin: 0;
        color: var(--text);
        font-size: 17px;
        font-weight: 700;
    }}

    .upload-time-head p {{
        margin: 4px 0 0;
        color: var(--text-muted);
        font-size: 13px;
        line-height: 1.5;
    }}

    .upload-time-preview {{
        margin-top: 14px;
        margin-bottom: 10px;
        padding: 16px 18px;
        border-radius: 18px;
        border: 1px solid rgba(167, 139, 250, 0.20);
        background: rgba(15, 23, 42, 0.74);
        text-align: center;
    }}

    .upload-time-preview-label {{
        color: var(--text-muted);
        font-size: 12px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }}

    .upload-time-preview-value {{
        margin-top: 6px;
        color: var(--text);
        font-size: 34px;
        font-weight: 700;
        letter-spacing: -0.04em;
    }}

    .dial-slider {{
        margin-top: 10px;
        padding: 12px 14px 16px;
        border-radius: 18px;
        border: 1px solid var(--line);
        background: rgba(15, 23, 42, 0.68) !important;
    }}

    .dial-slider > .gr-block,
    .dial-slider .gr-group,
    .dial-slider .gr-box,
    .dial-slider .gr-panel,
    .dial-slider .block {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    .dial-slider label {{
        color: var(--text-soft) !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }}

    .dial-slider input[type="range"] {{
        accent-color: #8b5cf6;
    }}

    .upload-tip-card {{
        padding: 18px;
        border-radius: 18px;
        border: 1px solid rgba(124, 58, 237, 0.20);
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.10) 0%, rgba(37, 99, 235, 0.08) 100%);
    }}

    .upload-tip-title {{
        color: var(--text-soft);
        font-size: 14px;
        font-weight: 600;
    }}

    .upload-tip-list {{
        margin: 10px 0 0;
        padding-left: 18px;
        color: var(--text-muted);
        font-size: 12px;
        line-height: 1.7;
    }}

    .report-html-shell,
    .report-html-shell > .gr-block,
    .report-html-shell .gr-group,
    .report-html-shell .gr-box,
    .report-html-shell .gr-panel,
    .report-html-shell .block {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }}

    .report-shell {{
        display: flex;
        flex-direction: column;
        gap: 20px;
    }}

    .report-shell-realtime {{
        gap: 20px;
    }}

    .report-view-shell {{
        background: transparent;
    }}

    .report-topbar {{
        position: sticky;
        top: 16px;
        z-index: 4;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 14px;
        padding: 14px 18px;
        border: 1px solid rgba(30, 41, 59, 0.8);
        border-radius: 18px;
        background: rgba(21, 27, 46, 0.86);
        backdrop-filter: blur(12px);
    }}

    .report-topbar-main {{
        display: flex;
        align-items: center;
        gap: 14px;
    }}

    .report-topbar-actions {{
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
    }}

    .report-topbar-back,
    .report-download-btn {{
        border: 1px solid rgba(71, 85, 105, 0.85);
        background: rgba(15, 23, 42, 0.84);
        color: #cbd5e1;
        cursor: pointer;
        transition: background 0.18s ease, color 0.18s ease, transform 0.18s ease;
    }}

    .report-topbar-back:hover,
    .report-download-btn:hover {{
        background: rgba(30, 41, 59, 0.96);
        color: #f8fafc;
        transform: translateY(-1px);
    }}

    .report-topbar-back {{
        width: 36px;
        height: 36px;
        border-radius: 10px;
        font-size: 18px;
        line-height: 1;
    }}

    .report-download-btn {{
        padding: 10px 14px;
        border-radius: 12px;
        font-size: 13px;
        font-weight: 600;
    }}

    .report-topbar h2 {{
        margin: 0;
        font-size: 20px;
        color: #f8fafc;
        letter-spacing: -0.02em;
    }}

    .report-topbar p {{
        margin: 4px 0 0;
        color: #64748b;
        font-size: 12px;
    }}

    .report-summary-grid,
    .report-grid,
    .participant-grid {{
        display: grid;
        gap: 14px;
    }}

    .report-summary-grid {{
        grid-template-columns: repeat(4, minmax(0, 1fr));
    }}

    .report-summary-card,
    .report-card,
    .participant-card {{
        border-radius: 16px;
        border: 1px solid rgba(30, 41, 59, 0.8);
        background: rgba(21, 27, 46, 0.98);
    }}

    .figma-card {{
        box-shadow: none;
    }}

    .report-summary-card {{
        padding: 18px 18px 16px;
        backdrop-filter: blur(12px);
    }}

    .report-summary-label,
    .report-card-head span,
    .participant-head span,
    .report-event-head span {{
        color: var(--text-muted);
        font-size: 11px;
    }}

    .report-summary-value {{
        margin-top: 6px;
        color: var(--text);
        font-size: 30px;
        font-weight: 700;
        letter-spacing: -0.03em;
    }}

    .report-summary-meta {{
        margin-top: 8px;
        color: var(--text-muted);
        font-size: 12px;
        line-height: 1.5;
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
        padding: 18px;
        backdrop-filter: blur(12px);
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
        margin-top: 14px;
        min-height: 320px;
        padding: 12px 8px 4px;
        border-radius: 14px;
        border: 1px solid rgba(30, 41, 59, 0.8);
        background: rgba(15, 23, 42, 0.54);
    }}

    .report-area-chart {{
        position: relative;
        width: 100%;
        height: 268px;
    }}

    .report-area-chart::after {{
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(180deg, rgba(59, 130, 246, 0.04), transparent 40%);
        pointer-events: none;
    }}

    .report-area-svg {{
        width: 100%;
        height: 100%;
        display: block;
    }}

    .chart-grid-line {{
        stroke: rgba(148, 163, 184, 0.14);
        stroke-width: 1;
    }}

    .chart-axis-label {{
        fill: #64748b;
        font-size: 11px;
    }}

    .area-normal-fill {{
        fill: rgba(16, 185, 129, 0.20);
        animation: areaReveal 0.85s ease-out both;
        transform-origin: bottom;
    }}

    .area-drowsy-fill {{
        fill: rgba(245, 158, 11, 0.22);
        animation: areaReveal 0.95s ease-out both;
        transform-origin: bottom;
    }}

    .area-absence-fill {{
        fill: rgba(239, 68, 68, 0.20);
        animation: areaReveal 1.05s ease-out both;
        transform-origin: bottom;
    }}

    .area-normal-line,
    .area-drowsy-line,
    .area-absence-line {{
        fill: none;
        stroke-linecap: round;
        stroke-linejoin: round;
        stroke-width: 2.5;
        stroke-dasharray: 1200;
        stroke-dashoffset: 1200;
        animation: chartLineDraw 1.1s ease-out forwards;
    }}

    .area-normal-line {{
        stroke: #10b981;
    }}

    .area-drowsy-line {{
        stroke: #f59e0b;
    }}

    .area-absence-line {{
        stroke: #ef4444;
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
        gap: 10px;
        margin-top: 12px;
    }}

    .report-event {{
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 12px;
        border-radius: 12px;
        border: 1px solid rgba(30, 41, 59, 0.75);
        background: rgba(8, 13, 24, 0.28);
    }}

    .report-event-icon {{
        width: 34px;
        height: 34px;
        flex: 0 0 34px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        border: 1px solid rgba(148, 163, 184, 0.16);
        background: rgba(15, 23, 42, 0.72);
        font-size: 13px;
    }}

    .report-event-label {{
        font-size: 12px;
        font-weight: 600;
    }}

    .report-event-time {{
        color: #94a3b8;
        font-size: 10px;
    }}

    .report-event-copy {{
        flex: 1;
        min-width: 0;
    }}

    .report-event p {{
        margin: 5px 0 0;
        color: #94a3b8;
        font-size: 12px;
        line-height: 1.45;
    }}

    .report-event-participant {{
        margin-top: 5px;
        color: #475569;
        font-size: 11px;
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

    .report-animate {{
        opacity: 0;
        transform: translateY(18px);
        animation: reportCardIn 0.55s ease-out forwards;
    }}

    .report-summary-grid .report-animate:nth-child(1) {{ animation-delay: 0.04s; }}
    .report-summary-grid .report-animate:nth-child(2) {{ animation-delay: 0.09s; }}
    .report-summary-grid .report-animate:nth-child(3) {{ animation-delay: 0.14s; }}
    .report-summary-grid .report-animate:nth-child(4) {{ animation-delay: 0.19s; }}
    .report-grid .report-animate:nth-child(1) {{ animation-delay: 0.22s; }}
    .report-grid .report-animate:nth-child(2) {{ animation-delay: 0.28s; }}
    .participant-grid .report-animate:nth-child(1) {{ animation-delay: 0.30s; }}
    .participant-grid .report-animate:nth-child(2) {{ animation-delay: 0.34s; }}
    .participant-grid .report-animate:nth-child(3) {{ animation-delay: 0.38s; }}

    .report-insight-grid {{
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 14px;
    }}

    .report-insight {{
        padding: 16px;
        border-radius: 18px;
        border: 1px solid var(--line);
        background: rgba(8, 13, 24, 0.38);
    }}

    .report-insight strong {{
        color: var(--text);
        font-size: 14px;
    }}

    .report-insight p {{
        margin: 8px 0 0;
        color: var(--text-soft);
        font-size: 13px;
        line-height: 1.6;
    }}

    .report-insight.tone-info {{
        background: rgba(37, 99, 235, 0.08);
        border-color: rgba(96, 165, 250, 0.22);
    }}

    .report-insight.tone-warning {{
        background: rgba(245, 158, 11, 0.08);
        border-color: rgba(245, 158, 11, 0.22);
    }}

    @keyframes chartLineDraw {{
        to {{
            stroke-dashoffset: 0;
        }}
    }}

    @keyframes areaReveal {{
        from {{
            opacity: 0;
            transform: translateY(18px) scaleY(0.92);
        }}
        to {{
            opacity: 1;
            transform: translateY(0) scaleY(1);
        }}
    }}

    @keyframes reportCardIn {{
        from {{
            opacity: 0;
            transform: translateY(18px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    .report-placeholder,
    .report-empty {{
        padding: 22px;
        border-radius: 16px;
        text-align: center;
        background: rgba(21, 27, 46, 0.96);
        border: 1px solid rgba(30, 41, 59, 0.8);
        color: var(--text-muted);
    }}

    .report-empty h2 {{
        margin: 0 0 8px;
        color: var(--text);
    }}

    .participant-card {{
        padding: 14px;
    }}

    .participant-bar {{
        margin-top: 10px;
        display: flex;
        height: 7px;
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
        margin-top: 8px;
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        color: var(--text-muted);
        font-size: 11px;
    }}

    .report-card-head h3 {{
        margin: 0;
        font-size: 17px;
        line-height: 1.2;
        letter-spacing: -0.02em;
    }}

    .report-chart-card .report-card-head h3 {{
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .report-insight-grid {{
        gap: 12px;
    }}

    .report-insight {{
        padding: 14px;
        border-radius: 14px;
    }}

    .report-insight strong {{
        font-size: 13px;
    }}

    .report-insight p {{
        margin-top: 6px;
        font-size: 12px;
        line-height: 1.5;
    }}

    .bridge-hidden {{
        display: none !important;
    }}

    @media (max-width: 1024px) {{
        .report-summary-grid {{
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }}

        .report-grid,
        .report-insight-grid,
        .live-layout,
        .upload-layout {{
            grid-template-columns: 1fr !important;
        }}
    }}

    @media (max-width: 768px) {{
        #app-root {{
            padding: 10px 14px 20px !important;
        }}

        .shell-header,
        .home-hero,
        .live-layout,
        .upload-layout,
        .report-actions {{
            padding-left: 16px !important;
            padding-right: 16px !important;
        }}

        #home-card-grid,
        .home-card-grid {{
            padding-left: 16px !important;
            padding-right: 16px !important;
        }}

        .shell-header,
        .shell-header-main,
        .report-topbar,
        .report-topbar-main {{
            flex-direction: column;
        }}

        .shell-copy h1,
        .home-hero h1,
        .report-topbar h2 {{
            font-size: 36px;
        }}

        .hero-note {{
            font-size: 18px;
        }}

        .mode-card {{
            height: auto;
            min-height: 560px;
            max-height: none;
            padding: 28px;
        }}

        #home-hero-section,
        .home-hero {{
            padding-top: 0;
        }}

        #home-card-grid,
        .home-card-grid {{
            grid-template-columns: 1fr !important;
            padding-top: 20px !important;
        }}

        #home-footer-section,
        .home-footer {{
            padding-top: 20px;
            padding-bottom: 0;
        }}

        .report-summary-grid {{
            grid-template-columns: 1fr;
        }}
    }}
    """
