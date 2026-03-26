from __future__ import annotations

from app.config import BG_H, BG_W, SLOT_H, SLOT_W, SLOT_X, SLOT_Y


def build_css() -> str:
    return f"""
    :root {{
        --bg-0: #09090b;
        --bg-1: #111827;
        --bg-2: #18181b;
        --panel: rgba(24, 24, 27, 0.92);
        --card: rgba(39, 39, 42, 0.82);
        --line: rgba(255, 255, 255, 0.08);
        --line-strong: rgba(255, 255, 255, 0.14);
        --text: #f4f4f5;
        --muted: #a1a1aa;
        --green: #22c55e;
        --orange: #f59e0b;
        --red: #ef4444;
        --blue: #60a5fa;
    }}

    html, body {{
        margin: 0;
        padding: 0;
        height: 100%;
        overflow-x: hidden;
    }}

    body {{
        background: #0a0e1a;
    }}

    .gradio-container {{
        background: #0a0e1a !important;
        color: var(--text);
        margin: 0 !important;
        padding: 0 !important;
        min-height: 100vh;
        overflow-x: hidden;
    }}

    .gradio-container .main,
    .gradio-container .wrap,
    .gradio-container .contain {{
        margin: 0 !important;
        padding: 0 !important;
        background: transparent !important;
    }}

    #app-root {{
        width: 100%;
        max-width: 100%;
        padding: 0 16px;
        box-sizing: border-box;
    }}

    #app-header {{
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 16px 4px 16px 4px;
    }}

    .brand-mark {{
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 0;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        font-size: 20px;
        font-weight: 800;
        box-shadow: 0 10px 24px rgba(16, 185, 129, 0.25);
    }}

    .brand-copy h1 {{
        margin: 0;
        color: white;
        font-size: 24px;
        font-weight: 700;
        line-height: 1.2;
    }}

    .brand-copy p {{
        margin: 4px 0 0 0;
        color: var(--muted);
        font-size: 13px;
    }}

    #content-wrap {{
        display: grid;
        grid-template-columns: minmax(0, 1.7fr) minmax(360px, 0.8fr);
        gap: 20px;
        align-items: start;
        margin: 0 !important;
    }}

    .view-shell {{
        margin: 0 !important;
        padding: 0 !important;
    }}

    .home-view {{
        min-height: 100dvh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 56px 0 40px 0;
        box-sizing: border-box;
        background: transparent !important;
    }}

    .section-badge {{
        display: inline-flex;
        align-items: center;
        padding: 8px 14px;
        border-radius: 999px;
        border: 1px solid rgba(96, 165, 250, 0.18);
        background: rgba(96, 165, 250, 0.10);
        color: #bfdbfe;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }}

    .home-shell {{
        position: relative;
        width: 100%;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        gap: 0;
        padding: 0;
        overflow: hidden;
    }}

    .home-hero {{
        position: relative;
        z-index: 1;
        width: 100%;
        max-width: 1152px;
        text-align: center;
        margin: 0 0 56px 0;
    }}

    .home-bg-glow {{
        position: absolute;
        inset: -140px 0 auto 0;
        height: 420px;
        background: radial-gradient(circle at 50% 50%, rgba(17, 24, 39, 0.5), transparent 50%);
        pointer-events: none;
    }}

    .home-badge-wrap {{
        display: inline-flex;
        align-items: center;
        margin-bottom: 18px;
    }}

    .home-badge {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        border-radius: 999px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        background: rgba(59, 130, 246, 0.1);
        color: #93c5fd;
        font-size: 14px;
        font-weight: 500;
    }}

    .home-badge-icon {{
        width: 18px;
        height: 18px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }}

    .home-badge-icon svg {{
        width: 18px;
        height: 18px;
        stroke: currentColor;
        stroke-width: 1.9;
        fill: none;
        stroke-linecap: round;
        stroke-linejoin: round;
    }}

    .home-hero h2,
    .upload-copy h2,
    .report-page-header h2 {{
        margin: 0 0 14px 0;
        color: #f8fafc;
        font-size: 60px;
        line-height: 1.05;
        font-weight: 500;
        letter-spacing: -0.03em;
    }}

    .home-hero p,
    .upload-copy p,
    .report-page-header p {{
        margin: 0;
        max-width: 100%;
        color: #94a3b8;
        font-size: 18px;
        line-height: 1.6;
    }}

    .home-card-grid {{
        width: 100%;
        max-width: 1024px;
        display: grid !important;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 24px;
        margin: 0 !important;
        padding: 0 !important;
        flex-grow: 0 !important;
        align-items: stretch;
    }}

    .home-card-grid > .gr-column,
    .home-card-grid > div {{
        min-width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        background: transparent !important;
    }}

    .home-card-column {{
        gap: 0 !important;
        border-radius: 18px;
        overflow: hidden;
        background: #1a2236 !important;
        min-width: 0 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 14px 40px rgba(0, 0, 0, 0.26);
        transform: translateY(0);
        transition:
            border-color 0.2s ease,
            box-shadow 0.2s ease,
            transform 0.2s ease;
    }}

    .home-card-column > div,
    .home-card-column .gr-block,
    .home-card-column .gr-box,
    .home-card-column .gr-group {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    .home-card-live:hover {{
        border-color: rgba(59, 130, 246, 0.5) !important;
        box-shadow:
            0 18px 40px rgba(59, 130, 246, 0.12),
            0 0 0 1px rgba(59, 130, 246, 0.18);
        transform: translateY(-3px);
    }}

    .home-card-upload:hover {{
        border-color: rgba(168, 85, 247, 0.5) !important;
        box-shadow:
            0 18px 40px rgba(168, 85, 247, 0.12),
            0 0 0 1px rgba(168, 85, 247, 0.18);
        transform: translateY(-3px);
    }}

    .home-mode-card {{
        display: flex;
        flex-direction: column;
        height: 100%;
        padding: 28px 28px 0 28px;
        border-radius: 0;
        border: none;
        background: transparent;
        box-shadow: none;
    }}

    .home-mode-card.upload-card {{
        background: transparent;
    }}

    .home-mode-card-body {{
        display: flex;
        flex-direction: column;
        gap: 0;
        height: 100%;
        min-height: 414px;
    }}

    .home-mode-icon {{
        width: 56px;
        height: 56px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 18px;
        border-radius: 14px;
        background: rgba(37, 99, 235, 0.16);
        border: 1px solid rgba(59, 130, 246, 0.24);
        color: #60a5fa;
    }}

    .upload-card .home-mode-icon {{
        background: rgba(147, 51, 234, 0.16);
        border-color: rgba(192, 132, 252, 0.24);
        color: #c084fc;
    }}

    .home-card-live:hover .home-mode-icon {{
        background: rgba(59, 130, 246, 0.20);
        border-color: rgba(59, 130, 246, 0.35);
    }}

    .home-card-upload:hover .home-mode-icon {{
        background: rgba(168, 85, 247, 0.20);
        border-color: rgba(168, 85, 247, 0.35);
    }}

    .home-mode-icon svg,
    .home-feature-icon svg {{
        width: 24px;
        height: 24px;
        stroke: currentColor;
        stroke-width: 1.9;
        fill: none;
        stroke-linecap: round;
        stroke-linejoin: round;
    }}

    .home-mode-title {{
        color: #ffffff;
        font-size: 40px;
        font-weight: 500;
        line-height: 1.2;
    }}

    .home-mode-subtitle {{
        margin-top: 6px;
        color: #94a3b8;
        font-size: 24px;
        font-weight: 400;
    }}

    .home-mode-description {{
        margin-top: 30px;
        color: #cbd5e1;
        font-size: 16px;
        line-height: 1.7;
    }}

    .home-feature-list {{
        display: flex;
        flex-direction: column;
        gap: 12px;
        margin-top: 28px;
    }}

    .home-feature-item {{
        display: flex;
        align-items: flex-start;
        gap: 12px;
    }}

    .home-feature-icon {{
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        background: rgba(37, 99, 235, 0.14);
        color: #60a5fa;
        flex-shrink: 0;
        margin-top: 2px;
    }}

    .upload-card .home-feature-icon {{
        background: rgba(147, 51, 234, 0.14);
        color: #c084fc;
    }}

    .home-feature-title {{
        color: #ffffff;
        font-size: 14px;
        font-weight: 600;
    }}

    .home-feature-desc {{
        margin-top: 2px;
        color: #64748b;
        font-size: 12px;
        line-height: 1.55;
    }}

    .home-card-cta {{
        margin-top: auto !important;
        padding: 22px 28px 28px 28px !important;
        background: transparent !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }}

    .home-card-button {{
        width: 100% !important;
        min-width: 0 !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }}

    .home-card-button > div,
    .home-card-button .gr-button-container,
    .home-card-button .wrap,
    .home-card-button .block {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }}

    #home-live-btn,
    #home-upload-btn {{
        width: 100% !important;
        min-width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    #home-live-btn button,
    #home-upload-btn button,
    #home-live-btn .gr-button,
    #home-upload-btn .gr-button,
    #home-live-btn [role="button"],
    #home-upload-btn [role="button"] {{
        width: 100% !important;
        min-width: 0 !important;
        min-height: 48px !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        line-height: 1.5 !important;
        border: none !important;
        margin: 0 !important;
        padding: 12px 18px !important;
        color: #ffffff !important;
        outline: none !important;
        opacity: 1 !important;
        background-clip: padding-box !important;
        transition:
            background 0.15s ease,
            box-shadow 0.15s ease,
            transform 0.15s ease !important;
    }}

    #home-live-btn button,
    #home-live-btn .gr-button,
    #home-live-btn [role="button"] {{
        background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%) !important;
        box-shadow: 0 10px 28px rgba(37, 99, 235, 0.28) !important;
    }}

    #home-upload-btn button,
    #home-upload-btn .gr-button,
    #home-upload-btn [role="button"] {{
        background: linear-gradient(90deg, #9333ea 0%, #c026d3 100%) !important;
        box-shadow: 0 10px 28px rgba(147, 51, 234, 0.28) !important;
    }}

    #home-live-btn button:hover,
    #home-live-btn .gr-button:hover,
    #home-live-btn [role="button"]:hover {{
        background: linear-gradient(90deg, #1d4ed8 0%, #2563eb 100%) !important;
        box-shadow: 0 14px 34px rgba(37, 99, 235, 0.34) !important;
        transform: translateY(-1px);
    }}

    #home-upload-btn button:hover,
    #home-upload-btn .gr-button:hover,
    #home-upload-btn [role="button"]:hover {{
        background: linear-gradient(90deg, #7e22ce 0%, #a21caf 100%) !important;
        box-shadow: 0 14px 34px rgba(147, 51, 234, 0.34) !important;
        transform: translateY(-1px);
    }}

    .home-footer-note {{
        margin-top: 64px;
        text-align: center;
        color: #475569;
        font-size: 14px;
        line-height: 1.4;
    }}

    .upload-shell {{
        display: grid;
        grid-template-columns: minmax(0, 1.1fr) minmax(260px, 0.9fr);
        gap: 20px;
        margin-bottom: 20px;
    }}

    .upload-feature-list {{
        display: grid;
        gap: 12px;
    }}

    .upload-feature-card {{
        padding: 18px;
        border-radius: 18px;
        border: 1px solid var(--line);
        background: rgba(255, 255, 255, 0.04);
    }}

    .feature-title {{
        color: white;
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 8px;
    }}

    .feature-desc {{
        color: #cbd5e1;
        font-size: 14px;
        line-height: 1.6;
    }}

    .upload-panel,
    .report-shell {{
        border-radius: 28px;
        border: 1px solid var(--line);
        background: rgba(18, 24, 39, 0.84);
        box-shadow: 0 22px 50px rgba(0, 0, 0, 0.22);
        padding: 22px;
    }}

    .report-shell {{
        min-height: 560px;
    }}

    .report-page-header {{
        margin-bottom: 18px;
    }}

    .report-page-body {{
        display: flex;
        flex-direction: column;
        gap: 18px;
    }}

    .report-summary-grid {{
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 12px;
    }}

    .report-stat-card,
    .report-block,
    .report-event {{
        border-radius: 18px;
        border: 1px solid var(--line);
        background: rgba(255, 255, 255, 0.04);
        padding: 18px;
    }}

    .report-stat-label {{
        color: var(--muted);
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }}

    .report-stat-value {{
        margin-top: 10px;
        color: white;
        font-size: 28px;
        font-weight: 800;
    }}

    .report-block-title {{
        color: white;
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 12px;
    }}

    .report-block-text,
    .report-list,
    .report-empty {{
        color: #dbe4f0;
        font-size: 14px;
        line-height: 1.7;
    }}

    .report-list {{
        margin: 0;
        padding-left: 18px;
    }}

    .report-events {{
        display: grid;
        gap: 10px;
    }}

    .report-event-title {{
        color: white;
        font-size: 14px;
        font-weight: 700;
    }}

    .report-event-meta {{
        margin-top: 4px;
        color: var(--muted);
        font-size: 12px;
    }}

    #stage-shell {{
        background: rgba(24, 24, 27, 0.72);
        border: 1px solid var(--line);
        border-radius: 24px;
        padding: 18px;
        box-shadow: 0 22px 50px rgba(0, 0, 0, 0.28);
    }}

    #stage-topbar {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 14px;
    }}

    .stage-topbar-actions {{
        display: flex;
        align-items: center;
        gap: 10px;
    }}

    .topbar-label {{
        color: var(--blue);
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.08em;
    }}

    .topbar-title {{
        margin-top: 4px;
        color: white;
        font-size: 20px;
        font-weight: 700;
    }}

    .topbar-badge {{
        padding: 8px 12px;
        border-radius: 999px;
        border: 1px solid rgba(96, 165, 250, 0.18);
        background: rgba(96, 165, 250, 0.1);
        color: #bfdbfe;
        font-size: 12px;
        font-weight: 700;
        white-space: nowrap;
    }}

    .report-link-btn {{
        padding: 10px 16px;
        border-radius: 999px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        background: rgba(255, 255, 255, 0.06);
        color: white;
        font-size: 13px;
        font-weight: 700;
        cursor: pointer;
    }}

    #demo-stage {{
        position: relative;
        width: 100%;
        aspect-ratio: {BG_W} / {BG_H};
        border-radius: 20px;
        overflow: hidden;
        border: 1px solid var(--line);
        background: #09090b;
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
        background: #09090b;
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
        border-radius: 0;
        box-sizing: border-box;
        z-index: 3;
    }}

    #student-cam {{
        object-fit: cover;
        transform: scaleX(-1);
        background: #0a0a0a;
        border: 3px solid rgba(34, 197, 94, 0.85);
        box-shadow: 0 18px 34px rgba(0, 0, 0, 0.34);
        z-index: 4;
    }}

    #cam-placeholder {{
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 10px;
        color: #e4e4e7;
        font-size: 13px;
        background: rgba(9, 9, 11, 0.58);
        border: 1px dashed rgba(255, 255, 255, 0.18);
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
        margin-top: 10px;
        color: var(--muted);
        font-size: 13px;
    }}

    #control-row {{
        margin-top: 12px !important;
        margin-bottom: 8px !important;
        gap: 10px;
    }}

    #debug-accordion {{
        margin-top: 8px !important;
        margin-bottom: 0 !important;
    }}

    .bridge-hidden {{
        display: none !important;
    }}

    #right-panel {{
        min-width: 0;
    }}

    .panel-shell {{
        min-height: 100%;
        display: flex;
        flex-direction: column;
        gap: 14px;
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 24px;
        padding: 18px;
        box-shadow: 0 22px 50px rgba(0, 0, 0, 0.25);
    }}

    .panel-header {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 12px;
    }}

    .panel-eyebrow {{
        color: var(--blue);
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.08em;
    }}

    .panel-title {{
        margin-top: 4px;
        color: white;
        font-size: 22px;
        font-weight: 700;
    }}

    .camera-chip {{
        padding: 8px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        border: 1px solid transparent;
        white-space: nowrap;
    }}

    .cam-on {{
        background: rgba(34, 197, 94, 0.12);
        color: #86efac;
        border-color: rgba(34, 197, 94, 0.24);
    }}

    .cam-off {{
        background: rgba(239, 68, 68, 0.12);
        color: #fca5a5;
        border-color: rgba(239, 68, 68, 0.24);
    }}

    .hero-card {{
        border-radius: 20px;
        padding: 18px;
        border: 1px solid var(--line);
    }}

    .hero-card-row {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
    }}

    .hero-label {{
        color: var(--muted);
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 8px;
    }}

    .hero-value {{
        color: white;
        font-size: 28px;
        font-weight: 800;
        line-height: 1.1;
    }}

    .hero-desc {{
        margin-top: 6px;
        color: #d4d4d8;
        font-size: 14px;
    }}

    .hero-dot {{
        width: 14px;
        height: 14px;
        border-radius: 999px;
        flex-shrink: 0;
    }}

    .status-normal {{
        background: rgba(70, 220, 70, 0.10);
        border-color: rgba(70, 220, 70, 0.20);
    }}

    .status-normal .hero-dot {{
        background: #46dc46;
    }}

    .status-drowsy {{
        background: rgba(255, 0, 0, 0.10);
        border-color: rgba(255, 0, 0, 0.20);
    }}

    .status-drowsy .hero-dot {{
        background: #ff0000;
    }}

    .status-yawn {{
        background: rgba(255, 128, 0, 0.10);
        border-color: rgba(255, 128, 0, 0.20);
    }}

    .status-yawn .hero-dot {{
        background: #ff8000;
    }}

    .status-absent {{
        background: rgba(255, 165, 0, 0.10);
        border-color: rgba(255, 165, 0, 0.20);
    }}

    .status-absent .hero-dot {{
        background: #ffa500;
    }}

    .status-unknown {{
        background: rgba(160, 160, 160, 0.10);
        border-color: rgba(160, 160, 160, 0.20);
    }}

    .status-unknown .hero-dot {{
        background: #a0a0a0;
    }}

    .info-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
    }}

    .info-card {{
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 16px;
    }}

    .compact-card {{
        min-height: 84px;
    }}

    .card-label {{
        color: var(--muted);
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 10px;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }}

    .card-value {{
        color: white;
        font-size: 16px;
        line-height: 1.5;
        word-break: keep-all;
    }}

    .report-card {{
        flex: 1;
    }}

    .report-text {{
        margin: 0;
        color: #e5e7eb;
        font-size: 14px;
        line-height: 1.6;
        white-space: pre-wrap;
        font-family: inherit;
    }}

    button.primary-btn {{
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%) !important;
        color: white !important;
        border: none !important;
    }}

    button.secondary-btn {{
        background: rgba(255, 255, 255, 0.06) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
    }}

    @media (max-width: 1100px) {{
        #content-wrap {{
            grid-template-columns: 1fr;
        }}

        #app-root {{
            padding: 0 14px;
        }}

        .home-card-grid,
        .upload-shell,
        .report-summary-grid {{
            grid-template-columns: 1fr;
        }}

        .home-shell {{
            justify-content: flex-start;
            padding: 0;
        }}

        .home-hero {{
            margin-bottom: 30px;
        }}

        .home-footer-note {{
            margin-top: 34px;
        }}
    }}

    @media (max-width: 720px) {{
        .home-hero h2,
        .upload-copy h2,
        .report-page-header h2 {{
            font-size: 44px;
        }}

        .home-view {{
            min-height: auto;
            justify-content: flex-start;
            padding: 28px 0 24px 0;
        }}

        .home-badge {{
            font-size: 13px;
            padding: 9px 14px;
        }}

        .home-hero p {{
            font-size: 16px;
        }}

        .home-mode-title {{
            font-size: 28px;
        }}

        .home-mode-subtitle {{
            font-size: 18px;
        }}

        .mode-card {{
            flex-direction: column;
        }}

        .stage-topbar-actions {{
            flex-wrap: wrap;
            justify-content: flex-end;
        }}
    }}
    """
