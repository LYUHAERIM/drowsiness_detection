from textwrap import dedent


def build_base_css() -> str:
    return dedent(
        f"""
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

        .report-actions {{
            display: flex !important;
            flex-wrap: wrap;
        }}

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

        .upload-time-box textarea,
        .upload-time-box input,
        .debug-panel textarea,
        .debug-panel input {{
            background: rgba(15, 23, 42, 0.80) !important;
            color: var(--text) !important;
            border: 1px solid var(--line) !important;
            border-radius: 14px !important;
        }}

        .bridge-hidden {{
            display: none !important;
        }}

        """
    )
