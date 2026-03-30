from textwrap import dedent


def build_upload_css() -> str:
    return dedent(
        """
        #upload-view,
        #upload-view::before,
        #upload-view::after,
        #upload-view > .gr-block,
        #upload-view > .gr-block::before,
        #upload-view > .gr-block::after,
        #upload-view > .gr-block > .gr-block,
        #upload-view > .gr-block > .gr-block::before,
        #upload-view > .gr-block > .gr-block::after,
        #upload-view > .gr-block > .gr-block > .gr-block,
        #upload-view > .gr-block > .gr-block > .gr-block::before,
        #upload-view > .gr-block > .gr-block > .gr-block::after,
        #upload-view .gr-group,
        #upload-view .gr-group::before,
        #upload-view .gr-group::after,
        #upload-view .gr-box,
        #upload-view .gr-box::before,
        #upload-view .gr-box::after,
        #upload-view .gr-panel,
        #upload-view .gr-panel::before,
        #upload-view .gr-panel::after,
        #upload-view .block,
        #upload-view .block::before,
        #upload-view .block::after,
        #upload-view .gradio-html,
        #upload-view .gr-row,
        #upload-view .gr-column,
        #upload-view .column,
        #upload-view .html-container,
        #upload-view .prose,
        #upload-page-inner,
        #upload-page-inner::before,
        #upload-page-inner::after,
        #upload-page-inner > .gr-block,
        #upload-page-inner > .gr-block::before,
        #upload-page-inner > .gr-block::after,
        #upload-page-inner > .gr-block > .gr-block,
        #upload-page-inner > .gr-block > .gr-block::before,
        #upload-page-inner > .gr-block > .gr-block::after,
        #upload-page-inner > .gr-block > .gr-block > .gr-block,
        #upload-page-inner > .gr-block > .gr-block > .gr-block::before,
        #upload-page-inner > .gr-block > .gr-block > .gr-block::after,
        #upload-page-inner .gr-group,
        #upload-page-inner .gr-group::before,
        #upload-page-inner .gr-group::after,
        #upload-page-inner .gr-box,
        #upload-page-inner .gr-box::before,
        #upload-page-inner .gr-box::after,
        #upload-page-inner .gr-panel,
        #upload-page-inner .gr-panel::before,
        #upload-page-inner .gr-panel::after,
        #upload-page-inner .block,
        #upload-page-inner .block::before,
        #upload-page-inner .block::after {
            margin: 0 !important;
            padding: 0 !important;
            min-height: 0 !important;
            border: none !important;
            box-shadow: none !important;
            background: #0a0e1a !important;
            border-color: #0a0e1a !important;
            outline: none !important;
        }

        #upload-shell-header,
        #upload-layout-wrap,
        #upload-main-column,
        #upload-side-column,
        #upload-main-stack,
        #upload-side-stack,
        #upload-intro-block,
        #upload-feature-block,
        #upload-file-state-block,
        #upload-time-intro-block,
        #upload-time-preview-block,
        #upload-tip-block,
        #upload-status-markdown {
            margin: 0 !important;
            padding: 0 !important;
            min-height: 0 !important;
            border: none !important;
            box-shadow: none !important;
            background: transparent !important;
        }

        #upload-view.hide,
        #upload-view.hidden,
        #upload-view .hide,
        #upload-view .hidden {
            display: none !important;
            height: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            border: none !important;
        }

        .upload-page-shell {
            background:
                radial-gradient(circle at 50% 0%, rgba(17, 24, 39, 0.52), transparent 48%),
                linear-gradient(180deg, #0a0e1a 0%, #0a0e1a 100%) !important;
        }

        .upload-layout {
            display: grid !important;
            grid-template-columns: minmax(0, 1.2fr) minmax(320px, 0.8fr);
            align-items: start;
            margin: 0 !important;
            padding: 0 28px 28px !important;
            min-height: 0 !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            gap: 20px !important;
        }

        #upload-view .upload-layout > .gr-block {
            min-width: 0 !important;
        }

        .upload-main-column,
        .upload-main-column > .gr-block,
        .upload-side-column,
        .upload-side-column > .gr-block,
        .upload-main-stack,
        .upload-main-stack > .gr-block,
        .upload-side-stack,
        .upload-side-stack > .gr-block {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            min-height: 0 !important;
        }

        .upload-intro,
        .upload-feature-card {
            background: var(--bg-panel-soft);
            border: 1px solid var(--line);
            border-radius: 24px;
            box-shadow: var(--shadow-lg);
            padding: 22px;
        }

        .upload-intro {
            display: flex;
            flex-direction: column;
            gap: 14px;
        }

        .upload-intro-head {
            display: flex;
            align-items: flex-start;
            gap: 14px;
        }

        .upload-intro-icon {
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
        }

        .upload-intro h2 {
            margin: 0;
            color: var(--text);
            font-size: 38px;
            font-weight: 800;
            letter-spacing: -0.02em;
        }

        .upload-intro ul {
            margin: 0;
            padding-left: 0;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .upload-feature-card h3 {
            margin: 0;
            color: var(--text);
            font-size: 18px;
            font-weight: 700;
        }

        .upload-feature-list {
            display: flex;
            flex-direction: column;
            gap: 14px;
        }

        .upload-feature-item {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            padding: 14px;
            border-radius: 16px;
            background: rgba(15, 23, 42, 0.64);
            border: 1px solid var(--line);
        }

        .upload-feature-icon {
            width: 38px;
            height: 38px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 12px;
            flex-shrink: 0;
            font-size: 16px;
        }

        .upload-feature-icon.tone-emerald {
            background: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(16, 185, 129, 0.22);
        }

        .upload-feature-icon.tone-amber {
            background: rgba(245, 158, 11, 0.12);
            border: 1px solid rgba(245, 158, 11, 0.22);
        }

        .upload-feature-icon.tone-violet {
            background: rgba(124, 58, 237, 0.12);
            border: 1px solid rgba(124, 58, 237, 0.22);
        }

        .upload-feature-icon.tone-red {
            background: rgba(239, 68, 68, 0.10);
            border: 1px solid rgba(248, 113, 113, 0.22);
        }

        .upload-feature-copy {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .upload-feature-item strong {
            color: var(--text);
            font-size: 14px;
        }

        .upload-feature-item span {
            color: var(--text-muted);
            font-size: 13px;
            line-height: 1.6;
        }

        .upload-file-state {
            padding: 16px 18px;
            border-radius: 18px;
            background: rgba(37, 99, 235, 0.10);
            border: 1px solid rgba(96, 165, 250, 0.2);
        }

        .upload-file-empty {
            background: rgba(15, 23, 42, 0.64);
            border-color: var(--line);
        }

        .upload-file-state-title {
            color: var(--text);
            font-size: 15px;
            font-weight: 700;
        }

        .upload-file-state-copy {
            margin-top: 4px;
            color: var(--text-muted);
            font-size: 13px;
        }

        .upload-status-markdown,
        .upload-status-markdown p {
            margin: 0 !important;
            color: var(--text-soft) !important;
            line-height: 1.6 !important;
        }

        .upload-file {
            padding: 8px;
            background: rgba(15, 23, 42, 0.64) !important;
            border: 1px dashed rgba(167, 139, 250, 0.4) !important;
            border-radius: 18px !important;
        }

        .upload-file > .gr-block,
        .upload-file .gr-group,
        .upload-file .gr-box,
        .upload-file .gr-panel,
        .upload-file .block {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }

        .upload-file label {
            color: var(--text-soft) !important;
        }

        .upload-file button {
            border-radius: 14px !important;
        }

        .upload-time-card {
            padding: 18px;
            border-radius: 18px;
            border: 1px solid rgba(124, 58, 237, 0.20);
            background: linear-gradient(180deg, rgba(124, 58, 237, 0.08) 0%, rgba(37, 99, 235, 0.06) 100%);
        }

        .upload-time-head {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .upload-time-icon {
            width: 42px;
            height: 42px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 14px;
            background: rgba(124, 58, 237, 0.16);
            border: 1px solid rgba(167, 139, 250, 0.22);
            font-size: 18px;
        }

        .upload-time-head h3 {
            margin: 0;
            color: var(--text);
            font-size: 17px;
            font-weight: 700;
        }

        .upload-time-head p {
            margin: 4px 0 0;
            color: var(--text-muted);
            font-size: 13px;
            line-height: 1.5;
        }

        .upload-time-preview {
            margin-top: 14px;
            margin-bottom: 10px;
            padding: 16px 18px;
            border-radius: 18px;
            border: 1px solid rgba(167, 139, 250, 0.20);
            background: rgba(15, 23, 42, 0.74);
            text-align: center;
        }

        .upload-time-preview-label {
            color: var(--text-muted);
            font-size: 12px;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .upload-time-preview-value {
            margin-top: 6px;
            color: var(--text);
            font-size: 34px;
            font-weight: 700;
            letter-spacing: -0.04em;
        }

        .dial-slider {
            margin-top: 10px;
            padding: 12px 14px 16px;
            border-radius: 18px;
            border: 1px solid var(--line);
            background: rgba(15, 23, 42, 0.68) !important;
        }

        .dial-slider > .gr-block,
        .dial-slider .gr-group,
        .dial-slider .gr-box,
        .dial-slider .gr-panel,
        .dial-slider .block {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }

        .dial-slider label {
            color: var(--text-soft) !important;
            font-size: 13px !important;
            font-weight: 600 !important;
        }

        .dial-slider input[type="range"] {
            accent-color: #8b5cf6;
        }

        .upload-tip-card {
            padding: 18px;
            border-radius: 18px;
            border: 1px solid rgba(124, 58, 237, 0.20);
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.10) 0%, rgba(37, 99, 235, 0.08) 100%);
        }

        .upload-tip-title {
            color: var(--text-soft);
            font-size: 14px;
            font-weight: 600;
        }

        .upload-tip-list {
            margin: 10px 0 0;
            padding-left: 18px;
            color: var(--text-muted);
            font-size: 12px;
            line-height: 1.7;
        }

        @media (max-width: 1024px) {
            .upload-layout {
                grid-template-columns: 1fr !important;
            }
        }

        @media (max-width: 768px) {
            .upload-layout {
                padding: 0 16px 20px !important;
            }
        }
        """
    )
