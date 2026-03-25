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
        overflow-x: hidden;
    }}

    body {{
        background: linear-gradient(180deg, #09090b 0%, #111827 100%);
    }}

    .gradio-container {{
        background: linear-gradient(180deg, #09090b 0%, #111827 100%);
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
    }}

    #app-root {{
        width: 100%;
        max-width: 100%;
        padding: 16px 20px 12px 20px;
        box-sizing: border-box;
    }}

    #app-header {{
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 0 4px 16px 4px;
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
        background: rgba(34, 197, 94, 0.10);
        border-color: rgba(34, 197, 94, 0.20);
    }}

    .status-normal .hero-dot {{
        background: #22c55e;
    }}

    .status-drowsy {{
        background: rgba(245, 158, 11, 0.10);
        border-color: rgba(245, 158, 11, 0.20);
    }}

    .status-drowsy .hero-dot {{
        background: #f59e0b;
    }}

    .status-absent {{
        background: rgba(239, 68, 68, 0.10);
        border-color: rgba(239, 68, 68, 0.20);
    }}

    .status-absent .hero-dot {{
        background: #ef4444;
    }}

    .status-unknown {{
        background: rgba(113, 113, 122, 0.10);
        border-color: rgba(113, 113, 122, 0.20);
    }}

    .status-unknown .hero-dot {{
        background: #a1a1aa;
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
            padding: 14px;
        }}
    }}
    """
