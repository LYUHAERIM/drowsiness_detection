from pathlib import Path

from app.inference.live_engine import get_device_summary
from app.ui.build import create_demo


print(f"[gradio_app] Starting demo on {get_device_summary()}")

demo = create_demo()


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        allowed_paths=[str(Path("assets").resolve())],
        css=getattr(demo, "demo_css", None),
        head=getattr(demo, "demo_head", None),
    )
