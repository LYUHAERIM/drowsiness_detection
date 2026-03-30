from app.ui.styles.base import build_base_css
from app.ui.styles.home import build_home_css
from app.ui.styles.live import build_live_css
from app.ui.styles.report import build_report_css
from app.ui.styles.tokens import build_tokens_css
from app.ui.styles.upload import build_upload_css


def build_css() -> str:
    return "\n".join(
        [
            build_tokens_css(),
            build_base_css(),
            build_home_css(),
            build_live_css(),
            build_upload_css(),
            build_report_css(),
        ]
    )
