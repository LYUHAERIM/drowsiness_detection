from textwrap import dedent


def build_tokens_css() -> str:
    return dedent(
        f"""
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
        """
    )
