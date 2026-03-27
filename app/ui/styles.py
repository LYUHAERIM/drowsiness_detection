from app.config import BG_H, BG_W, SLOT_H, SLOT_W, SLOT_X, SLOT_Y


def build_css() -> str:
    return f"""
    :root {{
        --bg-app: #0a0e1a;
        --bg-card: #151b2e;
        --bg-card-soft: rgba(21, 27, 46, 0.82);
        --bg-card-muted: rgba(15, 23, 42, 0.58);
        --bg-panel: rgba(10, 14, 26, 0.72);
        --line: rgba(148, 163, 184, 0.14);
        --line-strong: rgba(148, 163, 184, 0.28);
        --text: #f8fafc;
        --text-soft: #cbd5e1;
        --text-muted: #94a3b8;
        --text-faint: #64748b;
        --blue: #3b82f6;
        --blue-soft: rgba(59, 130, 246, 0.16);
        --purple: #a855f7;
        --purple-soft: rgba(168, 85, 247, 0.16);
        --emerald: #34d399;
        --amber: #f59e0b;
        --red: #ef4444;
        --shadow-card: 0 22px 50px rgba(2, 6, 23, 0.34);
        --radius-lg: 28px;
        --radius-md: 20px;
        --radius-sm: 14px;
    }}

    html, body {{
        margin: 0;
        padding: 0;
        height: 100%;
        overflow-x: hidden;
        background: var(--bg-app);
    }}

    body {{
        background:
            radial-gradient(circle at 50% 0%, rgba(17, 24, 39, 0.45), transparent 35%),
            var(--bg-app);
    }}

    .gradio-container {{
        min-height: 100vh;
        margin: 0 !important;
        padding: 0 !important;
        color: var(--text);
        background: transparent !important;
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
        max-width: 1240px;
        margin: 0 auto;
        padding: 0 16px 40px;
        box-sizing: border-box;
    }}

    .view-shell {{
        padding: 0 !important;
        margin: 0 !important;
        background: transparent !important;
    }}

    .page-view {{
        padding-top: 18px !important;
    }}

    .top-header,
    #app-header {{
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 16px;
        padding: 8px 4px 24px;
    }}

    .brand-wrap {{
        display: flex;
        align-items: center;
        gap: 14px;
    }}

    .brand-mark {{
        width: 52px;
        height: 52px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 16px;
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
        color: white;
        font-size: 20px;
        font-weight: 800;
        box-shadow: 0 14px 30px rgba(37, 99, 235, 0.28);
    }}

    .brand-copy h1 {{
        margin: 0;
        font-size: 22px;
        line-height: 1.2;
        font-weight: 700;
        color: var(--text);
    }}

    .brand-copy p {{
        margin: 4px 0 0;
        color: var(--text-muted);
        font-size: 13px;
    }}

    .page-heading {{
        display: flex;
        flex-direction: column;
        gap: 6px;
        text-align: right;
    }}

    .page-heading-top {{
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 10px;
    }}

    .page-heading h2 {{
        margin: 0;
        font-size: 22px;
        font-weight: 700;
        color: var(--text);
    }}

    .page-heading p {{
        margin: 0;
        color: var(--text-faint);
        font-size: 13px;
    }}

    .page-status-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 7px 11px;
        border-radius: 999px;
        border: 1px solid rgba(59, 130, 246, 0.24);
        background: rgba(59, 130, 246, 0.10);
        color: #bfdbfe;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.08em;
    }}

    .home-view {{
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 48px 0 36px !important;
    }}

    .section-badge {{
        display: inline-flex;
        align-items: center;
        padding: 8px 14px;
        border-radius: 999px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        background: rgba(59, 130, 246, 0.1);
        color: #93c5fd;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }}

    .home-shell {{
        position: relative;
        width: 100%;
        overflow: hidden;
    }}

    .home-bg-glow {{
        position: absolute;
        inset: -140px 0 auto;
        height: 420px;
        background: radial-gradient(circle at 50% 50%, rgba(17, 24, 39, 0.55), transparent 50%);
        pointer-events: none;
    }}

    .home-hero {{
        position: relative;
        z-index: 1;
        max-width: 1152px;
        margin: 0 auto 56px;
        text-align: center;
    }}

    .home-badge-wrap {{
        display: inline-flex;
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
    }}

    .home-badge-icon,
    .home-badge-icon svg,
    .home-mode-icon svg,
    .home-feature-icon svg,
    .feature-icon svg,
    .upload-drop-icon svg {{
        width: 20px;
        height: 20px;
        stroke: currentColor;
        stroke-width: 1.9;
        fill: none;
        stroke-linecap: round;
        stroke-linejoin: round;
    }}

    .home-hero h2,
    .upload-copy h2,
    .report-page-header h2 {{
        margin: 0 0 14px;
        color: var(--text);
        font-size: 58px;
        line-height: 1.04;
        letter-spacing: -0.03em;
        font-weight: 500;
    }}

    .home-hero p,
    .upload-copy p,
    .report-page-header p {{
        margin: 0;
        color: var(--text-muted);
        font-size: 18px;
        line-height: 1.65;
    }}

    .home-card-grid {{
        width: 100%;
        max-width: 1024px;
        display: grid !important;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 24px;
        margin: 0 auto !important;
        padding: 0 !important;
    }}

    .home-card-column,
    .home-card-column > div,
    .home-card-column .gr-block,
    .home-card-column .gr-box,
    .home-card-column .gr-group {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }}

    .home-card-column {{
        border-radius: 22px;
        overflow: hidden;
        background: var(--bg-card) !important;
        border: 1px solid rgba(30, 41, 59, 0.9) !important;
        box-shadow: var(--shadow-card);
        transform: translateY(0);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }}

    .home-card-live:hover {{
        transform: translateY(-4px);
        border-color: rgba(59, 130, 246, 0.52) !important;
        box-shadow: 0 24px 54px rgba(37, 99, 235, 0.22);
    }}

    .home-card-upload:hover {{
        transform: translateY(-4px);
        border-color: rgba(168, 85, 247, 0.52) !important;
        box-shadow: 0 24px 54px rgba(168, 85, 247, 0.18);
    }}

    .home-mode-card {{
        display: flex;
        flex-direction: column;
        min-height: 420px;
        padding: 28px 28px 0;
    }}

    .home-mode-card-body {{
        display: flex;
        flex-direction: column;
        height: 100%;
    }}

    .home-mode-icon {{
        width: 56px;
        height: 56px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 18px;
        border-radius: 14px;
        background: rgba(59, 130, 246, 0.12);
        border: 1px solid rgba(59, 130, 246, 0.24);
        color: #60a5fa;
    }}

    .upload-card .home-mode-icon {{
        background: rgba(168, 85, 247, 0.12);
        border-color: rgba(168, 85, 247, 0.24);
        color: #c084fc;
    }}

    .home-mode-title {{
        font-size: 38px;
        font-weight: 500;
        line-height: 1.18;
        color: var(--text);
    }}

    .home-mode-subtitle {{
        margin-top: 6px;
        font-size: 24px;
        color: var(--text-muted);
    }}

    .home-mode-description {{
        margin-top: 28px;
        color: var(--text-soft);
        font-size: 16px;
        line-height: 1.75;
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
        background: rgba(59, 130, 246, 0.12);
        color: #60a5fa;
        flex-shrink: 0;
    }}

    .upload-card .home-feature-icon {{
        background: rgba(168, 85, 247, 0.12);
        color: #c084fc;
    }}

    .home-feature-title {{
        color: var(--text);
        font-size: 14px;
        font-weight: 600;
    }}

    .home-feature-desc {{
        margin-top: 2px;
        color: var(--text-faint);
        font-size: 12px;
        line-height: 1.6;
    }}

    .home-card-cta {{
        width: 100% !important;
        margin-top: auto !important;
        padding: 22px 28px 28px !important;
        background: transparent !important;
    }}

    .home-card-button,
    .home-card-button > div,
    .home-card-button .gr-button-container,
    .home-card-button .wrap,
    .home-card-button .block,
    #home-live-btn,
    #home-upload-btn {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }}

    #home-live-btn button,
    #home-upload-btn button,
    #home-live-btn .gr-button,
    #home-upload-btn .gr-button,
    #home-live-btn [role="button"],
    #home-upload-btn [role="button"] {{
        width: 100% !important;
        min-height: 52px !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 14px 18px !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease !important;
    }}

    #home-live-btn button,
    #home-live-btn .gr-button,
    #home-live-btn [role="button"] {{
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%) !important;
        box-shadow: 0 14px 28px rgba(37, 99, 235, 0.28) !important;
    }}

    #home-upload-btn button,
    #home-upload-btn .gr-button,
    #home-upload-btn [role="button"] {{
        background: linear-gradient(135deg, #9333ea 0%, #a855f7 100%) !important;
        box-shadow: 0 14px 28px rgba(168, 85, 247, 0.24) !important;
    }}

    #home-live-btn button:hover,
    #home-upload-btn button:hover,
    #home-live-btn .gr-button:hover,
    #home-upload-btn .gr-button:hover {{
        transform: translateY(-1px);
    }}

    .home-footer-note {{
        margin-top: 60px;
        text-align: center;
        color: #475569;
        font-size: 14px;
    }}

    #content-wrap {{
        display: grid;
        grid-template-columns: minmax(0, 1.7fr) minmax(360px, 0.86fr);
        gap: 24px;
        align-items: start;
        margin: 0 !important;
    }}

    #stage-shell,
    .upload-card-shell,
    .report-shell {{
        background: var(--bg-card-soft);
        border: 1px solid rgba(30, 41, 59, 0.9);
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-card);
    }}

    #stage-shell {{
        padding: 18px;
    }}

    #stage-topbar {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        margin-bottom: 14px;
    }}

    .topbar-label,
    .live-panel-eyebrow {{
        color: #93c5fd;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }}

    .topbar-title,
    .live-panel-title {{
        margin-top: 4px;
        color: var(--text);
        font-size: 20px;
        font-weight: 700;
    }}

    .stage-topbar-actions {{
        display: flex;
        align-items: center;
        gap: 10px;
    }}

    .topbar-badge {{
        padding: 8px 12px;
        border-radius: 999px;
        border: 1px solid rgba(59, 130, 246, 0.18);
        background: rgba(59, 130, 246, 0.1);
        color: #bfdbfe;
        font-size: 12px;
        font-weight: 700;
    }}

    .report-link-btn {{
        padding: 10px 16px;
        border-radius: 12px;
        border: 1px solid rgba(59, 130, 246, 0.24);
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
        color: white;
        font-size: 13px;
        font-weight: 700;
        cursor: pointer;
        box-shadow: 0 12px 24px rgba(37, 99, 235, 0.22);
    }}

    #demo-stage {{
        position: relative;
        width: 100%;
        aspect-ratio: {BG_W} / {BG_H};
        overflow: hidden;
        border-radius: 22px;
        border: 1px solid rgba(30, 41, 59, 0.9);
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
        z-index: 3;
        box-sizing: border-box;
    }}

    #student-cam {{
        object-fit: cover;
        transform: scaleX(-1);
        border: 3px solid rgba(52, 211, 153, 0.82);
        box-shadow: 0 18px 36px rgba(2, 6, 23, 0.38);
        z-index: 4;
    }}

    #cam-placeholder {{
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 10px;
        text-align: center;
        font-size: 13px;
        color: var(--text-soft);
        background: rgba(9, 9, 11, 0.52);
        border: 1px dashed rgba(148, 163, 184, 0.28);
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
        color: var(--text-muted);
        font-size: 13px;
    }}

    .bridge-hidden {{
        display: none !important;
    }}

    .live-panel-shell {{
        display: flex;
        flex-direction: column;
        gap: 16px;
    }}

    .live-panel-card {{
        padding: 18px;
        border-radius: 22px;
        border: 1px solid rgba(30, 41, 59, 0.9);
        background: var(--bg-card-soft);
        box-shadow: var(--shadow-card);
    }}

    .live-panel-card-head {{
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 12px;
    }}

    .live-control-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin-top: 16px;
    }}

    .panel-action {{
        min-height: 48px;
        border: none;
        border-radius: 14px;
        color: white;
        font-size: 15px;
        font-weight: 700;
        cursor: pointer;
        transition: transform 0.15s ease, opacity 0.15s ease;
    }}

    .panel-action.primary {{
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
    }}

    .panel-action.secondary {{
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(148, 163, 184, 0.2);
    }}

    .panel-action.is-disabled {{
        opacity: 0.45;
        cursor: not-allowed;
    }}

    .live-panel-status {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        border-radius: 999px;
        background: rgba(59, 130, 246, 0.10);
        border: 1px solid rgba(59, 130, 246, 0.22);
        color: #bfdbfe;
        font-size: 12px;
        font-weight: 700;
    }}

    .live-panel-status.idle {{
        background: rgba(148, 163, 184, 0.08);
        border-color: rgba(148, 163, 184, 0.18);
        color: var(--text-muted);
    }}

    .live-panel-status .dot {{
        width: 8px;
        height: 8px;
        border-radius: 999px;
        background: currentColor;
    }}

    .status-card {{
        background: linear-gradient(180deg, var(--status-bg), rgba(21, 27, 46, 0.82));
    }}

    .status-orb {{
        width: 42px;
        height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 14px;
        background: var(--status-bg);
        color: var(--status-color);
        font-size: 22px;
        font-weight: 800;
    }}

    .status-hero {{
        margin-top: 18px;
        color: var(--status-color);
        font-size: 34px;
        font-weight: 800;
        line-height: 1.1;
    }}

    .status-description {{
        margin-top: 8px;
        color: var(--text-soft);
        font-size: 14px;
    }}

    .status-chip-row {{
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 16px;
    }}

    .status-chip {{
        display: inline-flex;
        align-items: center;
        padding: 8px 12px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid var(--line);
        color: var(--text-muted);
        font-size: 12px;
        font-weight: 600;
    }}

    .participant-list,
    .alert-list {{
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin-top: 16px;
        max-height: 360px;
        overflow-y: auto;
    }}

    .participant-row,
    .alert-row {{
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 12px;
        padding: 14px;
        border-radius: 16px;
        border: 1px solid var(--line);
        background: rgba(15, 23, 42, 0.45);
    }}

    .participant-main,
    .alert-copy {{
        display: flex;
        align-items: flex-start;
        gap: 10px;
        flex: 1;
    }}

    .participant-dot {{
        width: 10px;
        height: 10px;
        border-radius: 999px;
        margin-top: 6px;
        flex-shrink: 0;
    }}

    .participant-name,
    .alert-title {{
        color: var(--text);
        font-size: 14px;
        font-weight: 600;
    }}

    .participant-copy,
    .alert-time {{
        margin-top: 3px;
        color: var(--text-faint);
        font-size: 12px;
        line-height: 1.5;
    }}

    .participant-state {{
        font-size: 13px;
        font-weight: 700;
        white-space: nowrap;
    }}

    .alert-icon {{
        font-size: 11px;
        line-height: 1;
        margin-top: 4px;
    }}

    .empty-block {{
        padding: 26px 12px;
        text-align: center;
        color: var(--text-faint);
        font-size: 14px;
    }}

    .upload-shell {{
        display: grid;
        grid-template-columns: minmax(0, 1.12fr) minmax(280px, 0.88fr);
        gap: 20px;
        margin-bottom: 20px;
    }}

    .upload-hero-card {{
        padding: 28px;
        border-radius: var(--radius-lg);
        border: 1px solid rgba(30, 41, 59, 0.9);
        background: linear-gradient(180deg, rgba(21, 27, 46, 0.9), rgba(15, 23, 42, 0.75));
        box-shadow: var(--shadow-card);
    }}

    .upload-step-list {{
        display: grid;
        gap: 12px;
        margin-top: 24px;
    }}

    .upload-step-item {{
        display: flex;
        gap: 12px;
        align-items: flex-start;
    }}

    .upload-step-number {{
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        background: rgba(168, 85, 247, 0.14);
        border: 1px solid rgba(168, 85, 247, 0.24);
        color: #d8b4fe;
        font-size: 13px;
        font-weight: 800;
        flex-shrink: 0;
    }}

    .upload-step-title,
    .feature-title,
    .upload-card-title {{
        color: var(--text);
        font-size: 15px;
        font-weight: 700;
    }}

    .upload-step-desc,
    .feature-desc,
    .upload-card-subtitle,
    .upload-tip-item {{
        color: var(--text-muted);
        font-size: 13px;
        line-height: 1.65;
    }}

    .upload-feature-list {{
        display: grid;
        gap: 12px;
    }}

    .upload-feature-card {{
        padding: 20px;
        border-radius: 22px;
        border: 1px solid rgba(30, 41, 59, 0.9);
        background: var(--bg-card-soft);
        box-shadow: var(--shadow-card);
    }}

    .feature-icon,
    .upload-drop-icon {{
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 16px;
        margin-bottom: 14px;
    }}

    .feature-icon.emerald {{
        background: rgba(52, 211, 153, 0.10);
        border: 1px solid rgba(52, 211, 153, 0.24);
        color: #6ee7b7;
    }}

    .feature-icon.amber {{
        background: rgba(245, 158, 11, 0.10);
        border: 1px solid rgba(245, 158, 11, 0.24);
        color: #fbbf24;
    }}

    .feature-icon.red {{
        background: rgba(239, 68, 68, 0.10);
        border: 1px solid rgba(239, 68, 68, 0.24);
        color: #f87171;
    }}

    .upload-layout {{
        display: grid !important;
        grid-template-columns: minmax(0, 1.06fr) minmax(320px, 0.94fr);
        gap: 22px;
        margin: 0 !important;
    }}

    .upload-main-column,
    .upload-side-column {{
        gap: 16px !important;
    }}

    .upload-card-shell {{
        padding: 22px;
    }}

    .upload-card-subtitle {{
        margin-top: 8px;
        margin-bottom: 18px;
    }}

    .upload-dropzone {{
        display: flex;
        align-items: flex-start;
        gap: 16px;
        padding: 22px;
        border-radius: 22px;
        border: 2px dashed rgba(100, 116, 139, 0.38);
        background: rgba(15, 23, 42, 0.42);
        transition: border-color 0.2s ease, background 0.2s ease;
    }}

    .upload-dropzone.ready {{
        border-color: rgba(168, 85, 247, 0.42);
        background: rgba(168, 85, 247, 0.08);
    }}

    .upload-drop-icon {{
        margin-bottom: 0;
        background: rgba(168, 85, 247, 0.10);
        border: 1px solid rgba(168, 85, 247, 0.22);
        color: #d8b4fe;
        flex-shrink: 0;
    }}

    .upload-drop-copy {{
        display: flex;
        flex-direction: column;
        gap: 6px;
    }}

    .upload-drop-state {{
        color: #c084fc;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }}

    .upload-drop-title {{
        color: var(--text);
        font-size: 20px;
        font-weight: 700;
    }}

    .upload-drop-meta,
    .upload-drop-help {{
        color: var(--text-muted);
        font-size: 13px;
        line-height: 1.6;
    }}

    .upload-file-input {{
        margin-top: 16px !important;
    }}

    .upload-file-input .wrap,
    .upload-file-input .gr-box,
    .upload-file-input .gr-input {{
        background: rgba(15, 23, 42, 0.42) !important;
        border-radius: 16px !important;
        border-color: rgba(100, 116, 139, 0.24) !important;
    }}

    .upload-file-input button {{
        border-radius: 12px !important;
        background: rgba(168, 85, 247, 0.14) !important;
        border: 1px solid rgba(168, 85, 247, 0.24) !important;
        color: #e9d5ff !important;
    }}

    .upload-status-box textarea,
    .upload-status-box input {{
        background: rgba(15, 23, 42, 0.42) !important;
        border: 1px solid rgba(100, 116, 139, 0.24) !important;
        color: var(--text-soft) !important;
        border-radius: 16px !important;
    }}

    .upload-form-card input,
    .upload-form-card textarea {{
        background: rgba(15, 23, 42, 0.42) !important;
        border: 1px solid rgba(100, 116, 139, 0.24) !important;
        color: var(--text) !important;
        border-radius: 14px !important;
    }}

    .upload-form-card label {{
        color: var(--text-soft) !important;
        font-weight: 600 !important;
    }}

    .upload-tip-card {{
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.10), rgba(59, 130, 246, 0.08));
        border-color: rgba(168, 85, 247, 0.24);
    }}

    .upload-tip-list {{
        display: grid;
        gap: 10px;
        margin-top: 14px;
    }}

    .action-btn button,
    button.primary-btn,
    button.secondary-btn {{
        min-height: 48px !important;
        border-radius: 14px !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        padding: 12px 16px !important;
    }}

    button.primary-btn {{
        background: linear-gradient(135deg, #9333ea 0%, #a855f7 100%) !important;
        border: none !important;
        color: white !important;
        box-shadow: 0 14px 28px rgba(168, 85, 247, 0.22);
    }}

    button.secondary-btn {{
        background: rgba(255, 255, 255, 0.06) !important;
        color: white !important;
        border: 1px solid rgba(148, 163, 184, 0.18) !important;
    }}

    .report-shell {{
        min-height: 560px;
        padding: 24px;
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
    .report-event,
    .report-recommendation {{
        padding: 18px;
        border-radius: 20px;
        border: 1px solid var(--line);
        background: rgba(15, 23, 42, 0.42);
    }}

    .report-stat-label {{
        color: var(--text-faint);
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }}

    .report-stat-value {{
        margin-top: 10px;
        color: var(--text);
        font-size: 30px;
        font-weight: 800;
        line-height: 1.1;
    }}

    .report-stat-value-sm {{
        font-size: 20px;
    }}

    .accent-purple {{
        color: #d8b4fe;
    }}

    .report-two-column {{
        display: grid;
        grid-template-columns: 1.1fr 0.9fr;
        gap: 18px;
    }}

    .report-block-title,
    .report-recommendation-title {{
        color: var(--text);
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 12px;
    }}

    .report-block-text,
    .report-empty,
    .report-event-meta,
    .report-helper-note,
    .report-recommendation-text {{
        color: var(--text-soft);
        font-size: 14px;
        line-height: 1.7;
    }}

    .report-event-title,
    .participant-summary-name {{
        color: var(--text);
        font-size: 14px;
        font-weight: 700;
    }}

    .report-events,
    .report-recommendation-grid {{
        display: grid;
        gap: 10px;
    }}

    .participant-summary-row {{
        padding: 14px;
        border-radius: 16px;
        border: 1px solid var(--line);
        background: rgba(255, 255, 255, 0.03);
    }}

    .participant-summary-top {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
    }}

    .participant-summary-rate,
    .participant-summary-meta {{
        color: var(--text-faint);
        font-size: 12px;
    }}

    .participant-bar {{
        display: flex;
        gap: 1px;
        height: 8px;
        border-radius: 999px;
        overflow: hidden;
        background: rgba(15, 23, 42, 0.75);
        margin: 10px 0 8px;
    }}

    .participant-bar span {{
        display: block;
        height: 100%;
    }}

    .bar-normal {{ background: var(--emerald); }}
    .bar-drowsy {{ background: var(--amber); }}
    .bar-absent {{ background: var(--red); }}

    .tone-blue {{
        background: rgba(59, 130, 246, 0.08);
        border-color: rgba(59, 130, 246, 0.2);
    }}

    .tone-purple {{
        background: rgba(168, 85, 247, 0.08);
        border-color: rgba(168, 85, 247, 0.2);
    }}

    .report-action-row {{
        gap: 12px !important;
        margin-top: 16px !important;
    }}

    #debug-accordion {{
        margin-top: 8px !important;
    }}

    @media (max-width: 1100px) {{
        #content-wrap,
        .upload-layout,
        .upload-shell,
        .report-two-column,
        .report-summary-grid,
        .home-card-grid {{
            grid-template-columns: 1fr !important;
        }}

        #app-root {{
            padding: 0 14px 28px;
        }}

        .top-header,
        #app-header {{
            flex-direction: column;
            align-items: flex-start;
        }}

        .page-heading {{
            text-align: left;
        }}

        .page-heading-top {{
            justify-content: flex-start;
        }}
    }}

    @media (max-width: 720px) {{
        .home-hero h2,
        .upload-copy h2,
        .report-page-header h2 {{
            font-size: 42px;
        }}

        .home-mode-title {{
            font-size: 28px;
        }}

        .home-mode-subtitle {{
            font-size: 18px;
        }}

        .stage-topbar-actions {{
            flex-wrap: wrap;
            justify-content: flex-end;
        }}

        .report-action-row {{
            flex-direction: column;
        }}
    }}
    """
