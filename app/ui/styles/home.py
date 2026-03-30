from textwrap import dedent


def build_home_css() -> str:
    return dedent(
        """
        #bridge-root {
            margin: 0 !important;
            padding: 0 !important;
            min-height: 0 !important;
            height: 0 !important;
            overflow: hidden !important;
            border: none !important;
            background: transparent !important;
        }

        #bridge-root > .gr-block,
        #bridge-root > .gr-block > .gr-block,
        #bridge-root .gr-group,
        #bridge-root .gr-box,
        #bridge-root .gr-panel,
        #bridge-root .block,
        #bridge-root .wrap {
            margin: 0 !important;
            padding: 0 !important;
            min-height: 0 !important;
            height: 0 !important;
            overflow: hidden !important;
            border: none !important;
            background: transparent !important;
        }

        .bridge-hidden,
        .bridge-hidden > *,
        .bridge-hidden .wrap {
            opacity: 0 !important;
            min-height: 0 !important;
            height: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            border: none !important;
            overflow: hidden !important;
        }

        #home-view {
            position: relative;
            min-height: 0 !important;
            gap: 0 !important;
            background:
                radial-gradient(circle at 50% 0%, rgba(17, 24, 39, 0.52), transparent 48%),
                linear-gradient(180deg, #0a0e1a 0%, #0a0e1a 100%);
            border: none !important;
            box-shadow: none !important;
            overflow: visible;
            border-radius: var(--radius-xl);
            isolation: isolate;
            margin: 0 !important;
            padding: 0 !important;
        }

        /* 홈 화면에서 생기는 wrapper/line 색을 배경과 동일하게 강제 */
        .home-shell,
        .home-shell::before,
        .home-shell::after,
        .home-shell > .gr-block,
        .home-shell > .gr-block::before,
        .home-shell > .gr-block::after,
        .home-shell > .gr-block > .gr-block,
        .home-shell > .gr-block > .gr-block::before,
        .home-shell > .gr-block > .gr-block::after,
        .home-shell .gr-group,
        .home-shell .gr-group::before,
        .home-shell .gr-group::after,
        .home-shell .gr-box,
        .home-shell .gr-box::before,
        .home-shell .gr-box::after,
        .home-shell .gr-panel,
        .home-shell .gr-panel::before,
        .home-shell .gr-panel::after,
        .home-shell .block,
        .home-shell .block::before,
        .home-shell .block::after,
        .home-shell .gradio-html,
        .home-shell .gr-row,
        .home-shell .gr-column,
        .home-shell .column,
        .home-shell .html-container,
        .home-shell .prose,
        #home-view,
        #home-view::before,
        #home-view::after,
        #home-view > .gr-block,
        #home-view > .gr-block::before,
        #home-view > .gr-block::after,
        #home-view > .gr-block > .gr-block,
        #home-view > .gr-block > .gr-block::before,
        #home-view > .gr-block > .gr-block::after,
        #home-view > .gr-block > .gr-block > .gr-block,
        #home-view > .gr-block > .gr-block > .gr-block::before,
        #home-view > .gr-block > .gr-block > .gr-block::after,
        #home-view .gr-group,
        #home-view .gr-group::before,
        #home-view .gr-group::after,
        #home-view .gr-box,
        #home-view .gr-box::before,
        #home-view .gr-box::after,
        #home-view .gr-panel,
        #home-view .gr-panel::before,
        #home-view .gr-panel::after,
        #home-view .block,
        #home-view .block::before,
        #home-view .block::after,
        #home-view .gradio-html,
        #home-view .gr-row,
        #home-view .gr-column,
        #home-view .column,
        #home-view .html-container,
        #home-view .prose,
        #home-shell-inner,
        #home-shell-inner::before,
        #home-shell-inner::after,
        #home-shell-inner > .gr-block,
        #home-shell-inner > .gr-block::before,
        #home-shell-inner > .gr-block::after,
        #home-shell-inner > .gr-block > .gr-block,
        #home-shell-inner > .gr-block > .gr-block::before,
        #home-shell-inner > .gr-block > .gr-block::after,
        #home-shell-inner > .gr-block > .gr-block > .gr-block,
        #home-shell-inner > .gr-block > .gr-block > .gr-block::before,
        #home-shell-inner > .gr-block > .gr-block > .gr-block::after,
        #home-shell-inner .gr-group,
        #home-shell-inner .gr-group::before,
        #home-shell-inner .gr-group::after,
        #home-shell-inner .gr-box,
        #home-shell-inner .gr-box::before,
        #home-shell-inner .gr-box::after,
        #home-shell-inner .gr-panel,
        #home-shell-inner .gr-panel::before,
        #home-shell-inner .gr-panel::after,
        #home-shell-inner .block,
        #home-shell-inner .block::before,
        #home-shell-inner .block::after,
        #home-shell-inner .gradio-html,
        #home-shell-inner .gr-row,
        #home-shell-inner .gr-column,
        #home-shell-inner .column,
        #home-shell-inner .html-container,
        #home-shell-inner .prose {
            background: #0a0e1a !important;
            border: none !important;
            border-color: #0a0e1a !important;
            box-shadow: none !important;
            outline: none !important;
            margin: 0 !important;
            padding: 0 !important;
            min-height: 0 !important;
            height: auto !important;
            gap: 0 !important;
        }

        #home-view,
        #home-shell-inner {
            display: flex;
            flex-direction: column;
            gap: 0 !important;
        }

        #home-shell-inner {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }

        #home-hero-block,
        #home-footer-block,
        #home-card-grid-block,
        #home-hero-block > .gr-block,
        #home-footer-block > .gr-block,
        #home-card-grid-block > .gr-block,
        #home-hero-block .gradio-html,
        #home-footer-block .gradio-html,
        #home-card-grid-block .gradio-html,
        #home-hero-block .html-container,
        #home-footer-block .html-container,
        #home-card-grid-block .html-container,
        #home-hero-block .prose,
        #home-footer-block .prose,
        #home-card-grid-block .prose,
        #home-view .home-html-wrap,
        #home-view .home-html-wrap > .gr-block,
        #home-view .home-html-wrap .gradio-html,
        #home-view .home-html-wrap .html-container,
        #home-view .home-html-wrap .prose {
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
            box-shadow: none !important;
            min-height: 0 !important;
            height: auto !important;
            background: transparent !important;
        }

        #home-footer-block,
        #home-footer-block > .gr-block,
        #home-footer-block .html-container,
        #home-footer-block .prose {
            min-height: 0 !important;
            height: auto !important;
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }

        #home-hero-block,
        #home-hero-block.gradio-html,
        #home-hero-block > .html-container,
        #home-hero-block .html-container,
        #home-hero-block .prose {
            margin: 0 !important;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            min-height: 0 !important;
            height: auto !important;
        }

        #home-hero-section,
        .home-hero {
            position: relative;
            padding: 60px 24px 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            gap: 10px;
            overflow: hidden;
        }

        #home-hero-section h1,
        .home-hero h1 {
            max-width: 1080px;
            margin-top: 0;
            margin-bottom: 14px;
            font-size: 56px;
            line-height: 1.06;
            font-weight: 800;
        }

        .hero-note {
            max-width: 860px;
            color: #94a3b8;
            font-size: 24px;
            line-height: 1.55;
        }

        .home-bg {
            position: absolute;
            border-radius: 999px;
            filter: blur(80px);
            pointer-events: none;
            opacity: 0.9;
        }

        .home-bg-blue {
            width: 620px;
            height: 360px;
            top: -140px;
            left: calc(50% - 310px);
            background: rgba(17, 24, 39, 0.44);
        }

        .home-bg-violet {
            display: none;
        }

        #home-hero-section .hero-badge,
        .hero-badge {
            margin-bottom: 14px;
            padding: 10px 18px;
            border-radius: 999px;
            border: 1px solid rgba(59, 130, 246, 0.20);
            background: rgba(59, 130, 246, 0.10);
            color: #93c5fd;
            font-size: 16px;
            font-weight: 500;
        }

        .hero-badge-icon {
            color: #60a5fa;
            font-size: 14px;
            line-height: 1;
        }

        #home-card-grid-block,
        #home-card-grid-block > .gr-block,
        #home-card-grid-block .gradio-html,
        #home-card-grid-block .html-container,
        #home-card-grid-block .prose {
            width: 100% !important;
            max-width: none !important;
            margin: 0 !important;
            padding: 28px !important;
            border: none !important;
            box-shadow: none !important;
            background: transparent !important;
            min-height: 0 !important;
        }

        #home-card-grid,
        .home-card-grid {
            max-width: 1200px;
            margin: 0 auto;
            width: 100%;
            display: grid !important;
            grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
            align-items: stretch !important;
            gap: 28px;
            padding: 32px 24px 0 !important;
            box-sizing: border-box;
        }

        #home-card-grid .home-card-item {
            min-width: 0 !important;
            width: 100% !important;
            display: flex !important;
            align-self: stretch !important;
        }

        #home-card-grid .home-card-item > * {
            width: 100% !important;
            display: flex !important;
            flex: 1 1 auto !important;
            min-width: 0 !important;
        }

        #home-card-grid .home-card-item .html-container,
        #home-card-grid .home-card-item .prose {
            width: 100% !important;
            display: flex !important;
            flex: 1 1 auto !important;
            min-width: 0 !important;
            background: transparent !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        #home-live-card,
        #home-upload-card,
        .mode-card {
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
        }

        .mode-card-body {
            display: flex;
            flex: 1 1 auto;
            flex-direction: column;
            min-height: 0;
            height: 100%;
        }

        .mode-card:hover {
            transform: translateY(-2px);
        }

        .mode-card-blue:hover {
            border-color: rgba(51, 65, 85, 0.98);
            box-shadow: 0 22px 44px rgba(37, 99, 235, 0.14);
        }

        .mode-card-violet:hover {
            border-color: rgba(51, 65, 85, 0.98);
            box-shadow: 0 22px 44px rgba(124, 58, 237, 0.14);
        }

        .mode-card-icon {
            width: 72px;
            height: 72px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 16px;
            margin-bottom: 22px;
            background: rgba(15, 23, 42, 0.28);
            font-size: 30px;
        }

        .mode-card-blue .mode-card-icon {
            background: rgba(59, 130, 246, 0.10);
            border: 1px solid rgba(59, 130, 246, 0.20);
            color: #60a5fa;
        }

        .mode-card-violet .mode-card-icon {
            background: rgba(168, 85, 247, 0.10);
            border: 1px solid rgba(168, 85, 247, 0.20);
            color: #c084fc;
        }

        .mode-card-copy {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-bottom: 18px;
        }

        .mode-card h2 {
            margin: 0;
            color: var(--text);
            font-size: 38px;
            font-weight: 800;
            letter-spacing: -0.02em;
        }

        .mode-card-subtitle {
            color: #94a3b8;
            font-size: 19px;
            font-weight: 500;
            letter-spacing: 0;
            text-transform: none;
        }

        .mode-card p {
            margin: 0;
            color: #cbd5e1;
            line-height: 1.65;
            font-size: 20px;
        }

        .mode-card-list {
            margin: 0;
            padding-left: 0;
            display: flex;
            flex-direction: column;
            gap: 10px;
            flex: 1 1 auto;
        }

        .mode-feature {
            display: flex;
            align-items: flex-start;
            gap: 12px;
        }

        .mode-feature-icon {
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
            flex-shrink: 0;
            margin-top: 2px;
            font-size: 16px;
        }

        .mode-card-blue .mode-feature-icon {
            background: rgba(59, 130, 246, 0.10);
            color: #60a5fa;
        }

        .mode-card-violet .mode-feature-icon {
            background: rgba(168, 85, 247, 0.10);
            color: #c084fc;
        }

        .mode-feature-copy {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }

        .mode-feature-title {
            color: #e2e8f0;
            font-size: 18px;
            line-height: 1.5;
            font-weight: 600;
        }

        .mode-feature-desc {
            color: #64748b;
            font-size: 15px;
            line-height: 1.5;
        }

        .mode-feature-title,
        .mode-card h2,
        .mode-card-cta {
            letter-spacing: -0.01em;
        }

        .mode-card-action-row {
            display: flex;
            margin-top: auto;
            padding-top: 28px;
        }

        .mode-card-cta {
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
        }

        .mode-card-blue .mode-card-cta {
            background: #2563eb;
            box-shadow: 0 12px 28px rgba(37, 99, 235, 0.20);
        }

        .mode-card-violet .mode-card-cta {
            background: #9333ea;
            box-shadow: 0 12px 28px rgba(147, 51, 234, 0.20);
        }

        #home-footer-section,
        .home-footer {
            padding: 28px 24px 0;
            text-align: center;
            margin: 0 !important;
        }

        .home-footer p {
            margin: 0;
            color: #475569;
            font-size: 16px;
        }

        @media (max-width: 768px) {
            #home-card-grid,
            .home-card-grid {
                grid-template-columns: 1fr !important;
                padding-top: 20px !important;
            }

            .mode-card {
                height: auto;
                min-height: 560px;
                max-height: none;
                padding: 28px;
            }

            #home-hero-section,
            .home-hero {
                padding-top: 0;
            }

            #home-footer-section,
            .home-footer {
                padding-top: 20px;
                padding-bottom: 0;
            }
        }
        """
    )
