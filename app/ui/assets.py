from __future__ import annotations

import base64
import mimetypes
from pathlib import Path


def load_file_as_data_url(path: str | Path) -> str:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"파일이 없습니다: {file_path}")

    mime_type, _ = mimetypes.guess_type(str(file_path))
    if mime_type is None:
        mime_type = "image/png"

    encoded = base64.b64encode(file_path.read_bytes()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"
