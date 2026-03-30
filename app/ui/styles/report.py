from textwrap import dedent


def build_report_css() -> str:
    return dedent(
        """
        #report-view,
        #report-view::before,
        #report-view::after,
        #report-view > .gr-block,
        #report-view > .gr-block::before,
        #report-view > .gr-block::after,
        #report-view > .gr-block > .gr-block,
        #report-view > .gr-block > .gr-block::before,
        #report-view > .gr-block > .gr-block::after,
        #report-view > .gr-block > .gr-block > .gr-block,
        #report-view > .gr-block > .gr-block > .gr-block::before,
        #report-view > .gr-block > .gr-block > .gr-block::after,
        #report-view .gr-group,
        #report-view .gr-group::before,
        #report-view .gr-group::after,
        #report-view .gr-box,
        #report-view .gr-box::before,
        #report-view .gr-box::after,
        #report-view .gr-panel,
        #report-view .gr-panel::before,
        #report-view .gr-panel::after,
        #report-view .block,
        #report-view .block::before,
        #report-view .block::after,
        #report-view .gradio-html,
        #report-view .gr-row,
        #report-view .gr-column,
        #report-view .column,
        #report-view .html-container,
        #report-view .prose,
        #report-page-inner,
        #report-page-inner::before,
        #report-page-inner::after,
        #report-page-inner > .gr-block,
        #report-page-inner > .gr-block::before,
        #report-page-inner > .gr-block::after,
        #report-page-inner > .gr-block > .gr-block,
        #report-page-inner > .gr-block > .gr-block::before,
        #report-page-inner > .gr-block > .gr-block::after,
        #report-page-inner > .gr-block > .gr-block > .gr-block,
        #report-page-inner > .gr-block > .gr-block > .gr-block::before,
        #report-page-inner > .gr-block > .gr-block > .gr-block::after,
        #report-page-inner .gr-group,
        #report-page-inner .gr-group::before,
        #report-page-inner .gr-group::after,
        #report-page-inner .gr-box,
        #report-page-inner .gr-box::before,
        #report-page-inner .gr-box::after,
        #report-page-inner .gr-panel,
        #report-page-inner .gr-panel::before,
        #report-page-inner .gr-panel::after,
        #report-page-inner .block,
        #report-page-inner .block::before,
        #report-page-inner .block::after {
            background: #0a0e1a !important;
            border: none !important;
            border-color: #0a0e1a !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
            min-height: 0 !important;
            height: auto !important;
            gap: 0 !important;
            outline: none !important;
        }

        #report-html-shell,
        #report-html-shell > .gr-block,
        #report-html-shell .gr-group,
        #report-html-shell .gr-box,
        #report-html-shell .gr-panel,
        #report-html-shell .block,
        #report-html-shell .gradio-html,
        #report-html-shell .html-container,
        #report-html-shell .prose,
        .report-html-shell,
        .report-html-shell > .gr-block,
        .report-html-shell .gr-group,
        .report-html-shell .gr-box,
        .report-html-shell .gr-panel,
        .report-html-shell .block,
        .report-html-shell .html-container,
        .report-html-shell .prose {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
            min-height: 0 !important;
            height: auto !important;
            gap: 0 !important;
        }

        #report-view.hide,
        #report-view.hidden,
        #report-view .hide,
        #report-view .hidden {
            display: none !important;
            height: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            border: none !important;
        }

        #report-view,
        #report-page-inner {
            margin: 0 !important;
            padding: 0 !important;
            min-height: 0 !important;
            background:
                radial-gradient(circle at 50% 0%, rgba(17, 24, 39, 0.52), transparent 48%),
                linear-gradient(180deg, #0a0e1a 0%, #0a0e1a 100%) !important;
        }

        .report-shell {
            background:
                radial-gradient(circle at top right, rgba(37, 99, 235, 0.12), transparent 28%),
                radial-gradient(circle at 20% 0%, rgba(124, 58, 237, 0.10), transparent 26%),
                linear-gradient(180deg, rgba(21, 27, 46, 0.96) 0%, rgba(12, 18, 32, 0.96) 100%);
            border: 1px solid rgba(96, 165, 250, 0.12);
            border-radius: 28px;
            box-shadow: var(--shadow-lg);
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            overflow: hidden;
            margin-top: 0 !important;
        }

        .report-shell-realtime {
            gap: 20px;
        }

        .report-view-shell {
            background: transparent !important;
            margin: 0 !important;
            padding: 0 !important;
            min-height: 0 !important;
        }

        .report-topbar {
            position: sticky;
            top: 16px;
            z-index: 4;
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 18px;
            padding: 20px 22px;
            border: 1px solid rgba(51, 65, 85, 0.72);
            border-radius: 20px;
            background: rgba(12, 18, 32, 0.84);
            backdrop-filter: blur(16px);
            margin-top: 0 !important;
        }

        .report-topbar-main {
            display: flex;
            align-items: flex-start;
            gap: 18px;
            min-width: 0;
            flex: 1;
        }

        .report-topbar-nav-left {
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
            flex-shrink: 0;
        }

        .report-topbar-copy {
            display: flex;
            flex-direction: column;
            gap: 6px;
            min-width: 0;
        }

        .report-topbar-kicker,
        .report-card-kicker {
            color: #93c5fd;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.14em;
            text-transform: uppercase;
        }

        .report-topbar h2 {
            margin: 0;
            font-size: 34px;
            line-height: 1.15;
            color: #f8fafc;
            letter-spacing: -0.03em;
            font-weight: 800;
        }

        .report-topbar p {
            margin: 0;
            color: #94a3b8;
            font-size: 15px;
            line-height: 1.7;
        }

        .report-topbar-actions {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: 10px;
            flex-wrap: wrap;
        }

        .report-mode-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-height: 42px;
            padding: 0 15px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            border: 1px solid transparent;
        }

        .report-mode-badge.tone-live {
            color: #bfdbfe;
            background: rgba(37, 99, 235, 0.12);
            border-color: rgba(96, 165, 250, 0.22);
        }

        .report-mode-badge.tone-upload {
            color: #ddd6fe;
            background: rgba(124, 58, 237, 0.12);
            border-color: rgba(167, 139, 250, 0.22);
        }

        .report-topbar-nav,
        .report-download-btn {
            min-height: 42px;
            padding: 0 15px;
            border-radius: 12px;
            border: 1px solid rgba(71, 85, 105, 0.78);
            background: rgba(15, 23, 42, 0.84);
            color: #cbd5e1;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            transition: background 0.18s ease, color 0.18s ease, transform 0.18s ease, border-color 0.18s ease;
        }

        .report-topbar-nav:hover,
        .report-download-btn:hover {
            background: rgba(30, 41, 59, 0.96);
            color: #f8fafc;
            transform: translateY(-1px);
        }

        .report-topbar-nav-primary {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            border-color: rgba(37, 99, 235, 0.5);
            color: #ffffff;
            box-shadow: 0 10px 24px rgba(37, 99, 235, 0.22);
        }

        .report-summary-grid,
        .report-grid {
            display: grid;
            gap: 16px;
        }

        .participant-grid {
            display: flex;
            flex-direction: column;
            gap: 14px;
            margin-top: 16px;
        }

        .report-summary-grid {
            grid-template-columns: repeat(4, minmax(0, 1fr));
        }

        .report-summary-card,
        .report-card,
        .participant-card {
            border-radius: 18px;
            border: 1px solid rgba(30, 41, 59, 0.8);
            background: rgba(15, 23, 42, 0.84);
        }

        .figma-card {
            box-shadow: none;
        }

        .report-summary-card {
            padding: 22px;
            backdrop-filter: blur(12px);
            position: relative;
            overflow: hidden;
        }

        .report-summary-card::after {
            content: "";
            position: absolute;
            inset: auto 0 0 0;
            height: 2px;
            background: linear-gradient(90deg, transparent 0%, rgba(96, 165, 250, 0.45) 50%, transparent 100%);
            opacity: 0.75;
        }

        .report-summary-top {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .report-summary-icon {
            width: 40px;
            height: 40px;
            border-radius: 12px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: rgba(30, 41, 59, 0.72);
            border: 1px solid rgba(71, 85, 105, 0.52);
            font-size: 16px;
        }

        .report-summary-label,
        .report-card-head span,
        .participant-head span,
        .report-event-head span {
            color: var(--text-muted);
            font-size: 13px;
        }

        .report-summary-value {
            margin-top: 16px;
            color: var(--text);
            font-size: 44px;
            font-weight: 800;
            letter-spacing: -0.05em;
            line-height: 1;
        }

        .report-summary-meta {
            margin-top: 10px;
            color: var(--text-muted);
            font-size: 14px;
            line-height: 1.6;
        }

        .tone-positive .report-summary-value,
        .tone-positive {
            color: #34d399;
        }

        .tone-warning .report-summary-value,
        .tone-warning {
            color: #fbbf24;
        }

        .tone-danger .report-summary-value,
        .tone-danger {
            color: #f87171;
        }

        .report-grid {
            grid-template-columns: minmax(0, 1.08fr) minmax(0, 0.92fr);
            align-items: start;
        }

        .report-card {
            padding: 22px;
            backdrop-filter: blur(12px);
        }

        .report-card-head {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 12px;
        }

        .report-card-head-spread {
            align-items: center;
        }

        .report-card-head h3 {
            margin: 8px 0 0;
            color: var(--text);
            font-size: 30px;
            line-height: 1.2;
            letter-spacing: -0.03em;
            font-weight: 800;
        }

        .report-chart-card {
            overflow: hidden;
        }

        .report-chart-legend {
            display: flex;
            align-items: center;
            gap: 16px;
            flex-wrap: wrap;
            color: var(--text-muted);
            font-size: 14px;
            font-weight: 600;
        }

        .report-chart-legend span {
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .chart-dot {
            width: 10px;
            height: 10px;
            border-radius: 999px;
            display: inline-flex;
        }

        .chart-normal {
            background: #10b981;
        }

        .chart-drowsy {
            background: #f59e0b;
        }

        .chart-absence {
            background: #ef4444;
        }

        .report-chart-wrap {
            margin-top: 18px;
            min-height: 320px;
            padding: 14px 10px 4px;
            border-radius: 16px;
            border: 1px solid rgba(30, 41, 59, 0.8);
            background: rgba(8, 13, 24, 0.38);
        }

        .report-area-chart {
            position: relative;
            width: 100%;
            height: 300px;
        }

        .report-area-chart::after {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(180deg, rgba(59, 130, 246, 0.04), transparent 40%);
            pointer-events: none;
        }

        .report-area-svg {
            width: 100%;
            height: 100%;
            display: block;
        }

        .chart-grid-line {
            stroke: rgba(148, 163, 184, 0.14);
            stroke-width: 1;
        }

        .chart-axis-label {
            fill: #64748b;
            font-size: 12px;
        }

        .area-normal-fill {
            fill: rgba(16, 185, 129, 0.20);
            animation: areaReveal 0.85s ease-out both;
            transform-origin: bottom;
        }

        .area-drowsy-fill {
            fill: rgba(245, 158, 11, 0.22);
            animation: areaReveal 0.95s ease-out both;
            transform-origin: bottom;
        }

        .area-absence-fill {
            fill: rgba(239, 68, 68, 0.20);
            animation: areaReveal 1.05s ease-out both;
            transform-origin: bottom;
        }

        .area-normal-line,
        .area-drowsy-line,
        .area-absence-line {
            fill: none;
            stroke-linecap: round;
            stroke-linejoin: round;
            stroke-width: 2.5;
            stroke-dasharray: 1200;
            stroke-dashoffset: 1200;
            animation: chartLineDraw 1.1s ease-out forwards;
        }

        .area-normal-line {
            stroke: #10b981;
        }

        .area-drowsy-line {
            stroke: #f59e0b;
        }

        .area-absence-line {
            stroke: #ef4444;
        }

        .report-event-list {
            display: flex;
            flex-direction: column;
            gap: 14px;
            margin-top: 16px;
        }

        .report-event {
            display: flex;
            align-items: flex-start;
            gap: 14px;
            padding: 16px;
            border-radius: 14px;
            border: 1px solid rgba(30, 41, 59, 0.75);
            background: rgba(8, 13, 24, 0.28);
        }

        .report-event-icon {
            width: 40px;
            height: 40px;
            flex: 0 0 40px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 12px;
            border: 1px solid rgba(148, 163, 184, 0.16);
            background: rgba(15, 23, 42, 0.72);
            font-size: 15px;
        }

        .report-event-label {
            font-size: 16px;
            font-weight: 800;
        }

        .report-event-time {
            color: #94a3b8;
            font-size: 12px;
        }

        .report-event-copy {
            flex: 1;
            min-width: 0;
        }

        .participant-head strong,
        .report-event-head strong {
            color: var(--text);
            font-size: 16px;
        }

        .participant-meta span,
        .report-event p,
        .report-highlight-list li {
            color: var(--text-muted);
            font-size: 14px;
            line-height: 1.7;
        }

        .report-highlight-list {
            margin: 0;
            padding-left: 0;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .report-event p {
            margin: 7px 0 0;
            color: #94a3b8;
            font-size: 14px;
            line-height: 1.6;
        }

        .report-event-participant {
            margin-top: 7px;
            color: #64748b;
            font-size: 13px;
        }

        .report-event.tone-positive {
            background: var(--green-soft);
            border-color: rgba(16, 185, 129, 0.24);
        }

        .report-event.tone-warning {
            background: var(--amber-soft);
            border-color: rgba(245, 158, 11, 0.24);
        }

        .report-event.tone-danger {
            background: var(--red-soft);
            border-color: rgba(239, 68, 68, 0.24);
        }

        .participant-card {
            padding: 18px;
        }

        .participant-head {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 14px;
        }

        .participant-title-wrap {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        .participant-focus-chip {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-height: 38px;
            padding: 0 14px;
            border-radius: 999px;
            background: rgba(37, 99, 235, 0.12);
            border: 1px solid rgba(96, 165, 250, 0.18);
            color: #bfdbfe;
            font-size: 13px;
            font-weight: 800;
            white-space: nowrap;
        }

        .participant-bar {
            margin-top: 14px;
            display: flex;
            height: 9px;
            border-radius: 999px;
            overflow: hidden;
            background: rgba(51, 65, 85, 0.8);
        }

        .participant-bar .tone-positive {
            background: var(--green);
        }

        .participant-bar .tone-warning {
            background: var(--amber);
        }

        .participant-bar .tone-danger {
            background: var(--red);
        }

        .participant-meta {
            margin-top: 12px;
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            color: var(--text-muted);
            font-size: 13px;
        }

        .report-insight-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 14px;
            margin-top: 16px;
        }

        .report-insight {
            padding: 18px;
            border-radius: 18px;
            border: 1px solid var(--line);
            background: rgba(8, 13, 24, 0.38);
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .report-insight-badge {
            display: inline-flex;
            width: fit-content;
            padding: 6px 10px;
            border-radius: 999px;
            background: rgba(15, 23, 42, 0.64);
            border: 1px solid rgba(71, 85, 105, 0.45);
            color: #cbd5e1;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.06em;
        }

        .report-insight strong {
            color: var(--text);
            font-size: 18px;
        }

        .report-insight p {
            margin: 0;
            color: var(--text-soft);
            font-size: 14px;
            line-height: 1.7;
        }

        .report-insight.tone-info {
            background: rgba(37, 99, 235, 0.08);
            border-color: rgba(96, 165, 250, 0.22);
        }

        .report-insight.tone-warning {
            background: rgba(245, 158, 11, 0.08);
            border-color: rgba(245, 158, 11, 0.22);
        }

        .report-animate {
            opacity: 0;
            transform: translateY(18px);
            animation: reportCardIn 0.55s ease-out forwards;
        }

        .report-summary-grid .report-animate:nth-child(1) { animation-delay: 0.04s; }
        .report-summary-grid .report-animate:nth-child(2) { animation-delay: 0.09s; }
        .report-summary-grid .report-animate:nth-child(3) { animation-delay: 0.14s; }
        .report-summary-grid .report-animate:nth-child(4) { animation-delay: 0.19s; }
        .report-grid .report-animate:nth-child(1) { animation-delay: 0.22s; }
        .report-grid .report-animate:nth-child(2) { animation-delay: 0.28s; }
        .participant-grid .report-animate:nth-child(1) { animation-delay: 0.30s; }
        .participant-grid .report-animate:nth-child(2) { animation-delay: 0.34s; }
        .participant-grid .report-animate:nth-child(3) { animation-delay: 0.38s; }

        @keyframes chartLineDraw {
            to {
                stroke-dashoffset: 0;
            }
        }

        @keyframes areaReveal {
            from {
                opacity: 0;
                transform: translateY(18px) scaleY(0.92);
            }
            to {
                opacity: 1;
                transform: translateY(0) scaleY(1);
            }
        }

        @keyframes reportCardIn {
            from {
                opacity: 0;
                transform: translateY(18px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .report-placeholder,
        .report-empty {
            padding: 24px;
            border-radius: 16px;
            text-align: center;
            background: rgba(21, 27, 46, 0.96);
            border: 1px solid rgba(30, 41, 59, 0.8);
            color: var(--text-muted);
            font-size: 15px;
        }

        .report-empty h2 {
            margin: 0 0 8px;
            color: var(--text);
            font-size: 28px;
        }

        @media (max-width: 1024px) {
            .report-summary-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .report-grid,
            .report-insight-grid,
            .live-layout,
            .upload-layout {
                grid-template-columns: 1fr !important;
            }

            .report-topbar {
                flex-direction: column;
            }

            .report-topbar-actions {
                justify-content: flex-start;
            }
        }

        @media (max-width: 768px) {
            #app-root {
                padding: 10px 14px 20px !important;
            }

            .shell-header,
            .home-hero,
            .live-layout,
            .upload-layout,
            .report-actions {
                padding-left: 16px !important;
                padding-right: 16px !important;
            }

            #home-card-grid,
            .home-card-grid {
                padding-left: 16px !important;
                padding-right: 16px !important;
            }

            .shell-header,
            .shell-header-main,
            .report-topbar,
            .report-topbar-main {
                flex-direction: column;
            }

            .shell-copy h1,
            .home-hero h1 {
                font-size: 36px;
            }

            .report-topbar h2 {
                font-size: 28px;
            }

            .hero-note {
                font-size: 18px;
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

            #home-card-grid,
            .home-card-grid {
                grid-template-columns: 1fr !important;
                padding-top: 20px !important;
            }

            #home-footer-section,
            .home-footer {
                padding-top: 20px;
                padding-bottom: 0;
            }

            .report-shell {
                padding: 18px;
                border-radius: 22px;
            }

            .report-summary-grid {
                grid-template-columns: 1fr;
            }

            .participant-head {
                flex-direction: column;
                align-items: flex-start;
            }
        }
        """
    )
