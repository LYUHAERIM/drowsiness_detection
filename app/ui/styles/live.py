from textwrap import dedent

from app.config import BG_H, BG_W, SLOT_H, SLOT_W, SLOT_X, SLOT_Y


def build_live_css() -> str:
    return dedent(
        f"""
        #live-view,
        #live-view::before,
        #live-view::after,
        #live-view > .gr-block,
        #live-view > .gr-block::before,
        #live-view > .gr-block::after,
        #live-view > .gr-block > .gr-block,
        #live-view > .gr-block > .gr-block::before,
        #live-view > .gr-block > .gr-block::after,
        #live-view .gr-group,
        #live-view .gr-group::before,
        #live-view .gr-group::after,
        #live-view .gr-box,
        #live-view .gr-box::before,
        #live-view .gr-box::after,
        #live-view .gr-panel,
        #live-view .gr-panel::before,
        #live-view .gr-panel::after,
        #live-view .block,
        #live-view .block::before,
        #live-view .block::after,
        #live-view .gradio-html,
        #live-view .gr-row,
        #live-view .gr-column,
        #live-view .column,
        #live-view .html-container,
        #live-view .prose,
        #live-page-inner,
        #live-page-inner::before,
        #live-page-inner::after,
        #live-page-inner > .gr-block,
        #live-page-inner > .gr-block::before,
        #live-page-inner > .gr-block::after,
        #live-page-inner > .gr-block > .gr-block,
        #live-page-inner > .gr-block > .gr-block::before,
        #live-page-inner > .gr-block > .gr-block::after,
        #live-page-inner .gr-group,
        #live-page-inner .gr-group::before,
        #live-page-inner .gr-group::after,
        #live-page-inner .gr-box,
        #live-page-inner .gr-box::before,
        #live-page-inner .gr-box::after,
        #live-page-inner .gr-panel,
        #live-page-inner .gr-panel::before,
        #live-page-inner .gr-panel::after,
        #live-page-inner .block,
        #live-page-inner .block::before,
        #live-page-inner .block::after {{
            margin: 0 !important;
            padding: 0 !important;
            min-height: 0 !important;
            border: none !important;
            box-shadow: none !important;
            background: #0a0e1a !important;
            border-color: #0a0e1a !important;
            outline: none !important;
        }}

        #live-shell-header,
        #live-layout-wrap,
        #live-stage-column,
        #live-panel-column,
        #live-panel-html,
        #live-stage-html,
        #debug-panel-wrap,
        #slots-json-output {{
            margin: 0 !important;
            padding: 0 !important;
            min-height: 0 !important;
            border: none !important;
            box-shadow: none !important;
            background: transparent !important;
        }}

        #debug-panel-wrap {{
            width: 100% !important;
            max-width: 100% !important;
            max-height: none !important;
            overflow: hidden !important;
        }}

        #debug-panel-wrap .gradio-accordion,
        #debug-panel-wrap .gradio-accordion > div,
        #debug-panel-wrap .gradio-accordion .wrap,
        #debug-panel-wrap .gradio-accordion .content,
        #debug-panel-wrap > .gr-block,
        #debug-panel-wrap .gr-block,
        #debug-panel-wrap .gr-form,
        #debug-panel-wrap .form,
        #debug-panel-wrap .wrap,
        #debug-panel-wrap .content {{
            width: 100% !important;
            max-width: 100% !important;
            max-height: none !important;
            overflow: hidden !important;
        }}

        #debug-panel-wrap * {{
            max-width: 100% !important;
            overflow-x: hidden !important;
            box-sizing: border-box !important;
        }}

        #live-view.hide,
        #live-view.hidden,
        #live-view .hide,
        #live-view .hidden {{
            display: none !important;
            height: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            border: none !important;
        }}

        #live-layout-wrap.hide,
        #live-layout-wrap.hidden,
        #live-stage-column.hide,
        #live-stage-column.hidden,
        #live-panel-column.hide,
        #live-panel-column.hidden,
        #debug-panel-wrap.hide,
        #debug-panel-wrap.hidden {{
            display: none !important;
            height: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            border: none !important;
        }}

        #live-view .form.hidden,
        #live-view .form.hide,
        #live-view .wrap.hide,
        #live-view .wrap.hidden {{
            display: none !important;
            height: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            border: none !important;
        }}

        .live-page-shell {{
            background:
                radial-gradient(circle at 50% 0%, rgba(17, 24, 39, 0.52), transparent 48%),
                linear-gradient(180deg, #0a0e1a 0%, #0a0e1a 100%) !important;
        }}

        .live-layout {{
            display: grid !important;
            grid-template-columns: minmax(0, 1.5fr) minmax(360px, 0.9fr);
            align-items: start !important;
            margin: 0 !important;
            padding: 0 28px 28px !important;
            min-height: 0 !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            gap: 20px !important;
        }}

        #live-view .live-layout > .gr-block {{
            min-width: 0 !important;
        }}

        .live-stage-column,
        .live-stage-column > .gr-block,
        .live-panel-column,
        .live-panel-column > .gr-block {{
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            min-height: 0 !important;
        }}

        #stage-shell,
        .panel-shell {{
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
        """
    )
