"""
Zoom 파이프라인 프레임 어노테이션 유틸.

한글 텍스트, 슬롯 바운딩박스, 얼굴 영역, 정보 박스를 OpenCV 캔버스에 그립니다.
시각화 스타일을 바꾸려면 이 파일만 수정하면 됩니다.
"""
import math
import os
import re
from typing import Optional

import cv2
import numpy as np

_FONT = cv2.FONT_HERSHEY_SIMPLEX

_KOREAN_FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
    "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
]
_KOREAN_FONT_PATH: Optional[str] = next(
    (p for p in _KOREAN_FONT_CANDIDATES if os.path.exists(p)), None
)

# info box 레이아웃 상수
INFO_N_LINES = 6
INFO_LINE_H  = 16
INFO_BOX_PAD = 6
INFO_BOX_H   = INFO_BOX_PAD * 2 + INFO_N_LINES * INFO_LINE_H  # 108 px

_font_cache: dict = {}


def _contains_korean(text: str) -> bool:
    return bool(re.search(r"[가-힣]", text or ""))


def _pil_font(px: int):
    from PIL import ImageFont
    if px not in _font_cache:
        if _KOREAN_FONT_PATH:
            _font_cache[px] = ImageFont.truetype(_KOREAN_FONT_PATH, px)
        else:
            _font_cache[px] = ImageFont.load_default()
    return _font_cache[px]


def draw_text_bg(
    img: np.ndarray,
    text: str,
    org: tuple,
    scale: float = 0.5,
    color: tuple = (255, 255, 255),
    bg: tuple = (0, 0, 0),
    thickness: int = 1,
    pad: int = 3,
) -> None:
    """
    한글 포함 텍스트를 배경 사각형과 함께 그립니다 (in-place).

    한글이 포함된 경우 PIL을 사용합니다.
    """
    from PIL import Image, ImageDraw

    text = str(text)
    x, y = org

    if _contains_korean(text):
        pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        d = ImageDraw.Draw(pil)
        font_px = max(14, int(scale * 28))
        font = _pil_font(font_px)
        bb = d.textbbox((x, y), text, font=font)
        d.rectangle(
            [bb[0] - pad, bb[1] - pad, bb[2] + pad, bb[3] + pad],
            fill=tuple(int(v) for v in bg[::-1]),
        )
        d.text((x, y), text, font=font, fill=tuple(int(v) for v in color[::-1]))
        img[:] = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
    else:
        (tw, th), bl = cv2.getTextSize(text, _FONT, scale, thickness)
        cv2.rectangle(img, (x - pad, y - th - pad), (x + tw + pad, y + bl + pad), bg, -1)
        cv2.putText(img, text, (x, y), _FONT, scale, color, thickness, cv2.LINE_AA)


def draw_slot_bbox(
    canvas: np.ndarray,
    slot_id: int,
    box: tuple,
    class_name: str,
    final_state: str,
    box_colors: dict,
    state_colors: dict,
    no_face: bool = False,
    is_teacher: bool = False,
) -> None:
    """
    슬롯 바운딩박스와 상태 레이블을 캔버스에 그립니다.

    Args:
        box_colors:   {"person_on": (R,G,B), ...}
        state_colors: {"NORMAL": (R,G,B), ...}
        no_face:      얼굴 완전 미검출 여부 → NOT FOUND 표시
    """
    x1, y1, x2, y2 = [int(v) for v in box]

    # 표시 상태 결정: NOT FOUND > final_state 순 우선
    # YAWN은 final_state 자체에 포함됨 (독립 상태)
    if is_teacher:
        display_state = ""
    elif no_face:
        display_state = "NOT FOUND"
    else:
        display_state = final_state

    # bbox 테두리 색 결정
    if is_teacher or display_state == "NOT FOUND":
        border_color = (120, 120, 120)   # 회색
    elif display_state in state_colors and display_state not in ("NORMAL", "IGNORE", "ABSENT"):
        border_color = state_colors[display_state]
    else:
        border_color = box_colors.get(class_name, (180, 180, 180))

    state_color = state_colors.get(display_state, (120, 120, 120))

    cv2.rectangle(canvas, (x1, y1), (x2, y2), border_color, 2)

    label = "" if is_teacher else f"ID{slot_id} {display_state}"
    if not label:
        return
    (lw, lh), _ = cv2.getTextSize(label, _FONT, 0.44, 1)
    lx = max(0, x1)
    ly = max(lh + 4, y1 - 2)
    cv2.rectangle(canvas, (lx, ly - lh - 4), (lx + lw + 6, ly + 2), state_color, -1)
    cv2.putText(canvas, label, (lx + 3, ly - 1), _FONT, 0.44, (255, 255, 255), 1, cv2.LINE_AA)


def draw_face_box(
    canvas: np.ndarray,
    thumb_origin: tuple,
    face_box: Optional[tuple],
    color: tuple = (255, 0, 255),
) -> None:
    """
    FaceMesh 얼굴 영역을 마젠타 사각형으로 표시합니다.

    Args:
        thumb_origin: 썸네일 좌상단 (ox, oy) — 캔버스 좌표계 기준
        face_box:     (x1, y1, x2, y2) 썸네일 내 상대 좌표
    """
    if face_box is None:
        return
    ox, oy = thumb_origin
    cv2.rectangle(
        canvas,
        (ox + face_box[0], oy + face_box[1]),
        (ox + face_box[2], oy + face_box[3]),
        color, 1,
    )


def draw_info_box(
    canvas: np.ndarray,
    slot,
    face_result,
    anchor: tuple,
    final_state: str,
    state_colors: dict,
    box_w: int = 336,
    is_noface: bool = False,
) -> None:
    """
    슬롯 상세 정보 박스 (EAR, MAR, pitch, 타이머 등)를 그립니다.

    anchor 위치에 box_w × INFO_BOX_H 크기의 다크 박스를 그립니다.

    Args:
        slot:        SlotState
        face_result: FaceMeshResult
        anchor:      (ix, iy) 박스 좌상단
        final_state: 최종 상태 문자열
        state_colors: {"NORMAL": (R,G,B), ...}
        box_w:       박스 너비
        is_noface:   얼굴 장기 미검출 여부 → 테두리색을 썸네일과 동일하게 맞춤
    """
    _nan = float("nan")

    def _f(v) -> str:
        return "-" if (v is None or (isinstance(v, float) and math.isnan(v))) else str(round(float(v), 3))

    if slot.is_teacher:
        return

    ear_th = slot.bl_ear * 0.75 if slot.bl_ear else 0.18
    mar_th = max(slot.bl_mar * 1.30, 0.60) if slot.bl_mar else 0.60

    if face_result.lm_ok:
        lv = "L1"
    elif face_result.face_ok:
        lv = "L2"
    else:
        lv = "NotFound"

    te      = " [T]" if slot.is_teacher else ""
    name    = slot.name_final if slot.name_final else f"slot_{slot.slot_id}"
    yawn_str = " [YAWN]" if final_state == "YAWN" else ""

    info_lines = [
        f"{name}{te}",
        f"{final_state} {lv}",
        f"EAR={_f(face_result.ear)} th={ear_th:.3f}",
        f"MAR={_f(face_result.mar)} th={mar_th:.3f}{yawn_str}",
        f"pit={_f(face_result.pitch_like)} cy={_f(face_result.face_center_y)}",
        f"eF={slot.ear_low_frames} fF={slot.face_low_frames}",
    ]

    # is_noface=True면 썸네일과 동일하게 회색 테두리 (draw_slot_bbox와 일치)
    if is_noface:
        state_color = (120, 120, 120)
    else:
        state_color = state_colors.get(final_state, (200, 200, 200))
    ix, iy = anchor
    ibox_h = INFO_BOX_H

    cv2.rectangle(canvas, (ix, iy), (ix + box_w, iy + ibox_h), (30, 30, 30), -1)
    cv2.rectangle(canvas, (ix, iy), (ix + box_w, iy + ibox_h), state_color, 1)

    # 1. 한글이 없는 줄(영문/숫자)을 OpenCV로 캔버스에 그립니다.
    for li, line in enumerate(info_lines):
        line_str = str(line)
        if not _contains_korean(line_str):
            ty = iy + INFO_BOX_PAD + (li + 1) * INFO_LINE_H - 2
            cv2.putText(
                canvas, line_str,
                (ix + INFO_BOX_PAD, ty),
                _FONT, 0.40, (220, 220, 220), 1, cv2.LINE_AA,
            )

    # 2. 영문이 다 그려진 캔버스를 가져와서, 한글이 포함된 줄만 PIL로 추가로 그립니다.
    has_korean = any(_contains_korean(str(l)) for l in info_lines)
    if has_korean:
        from PIL import Image, ImageDraw
        pil = Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))
        d = ImageDraw.Draw(pil)
        font = _pil_font(13)  # 폰트 크기 미세 조정

        for li, line in enumerate(info_lines):
            line_str = str(line)
            if _contains_korean(line_str):
                ty = iy + INFO_BOX_PAD + (li + 1) * INFO_LINE_H - 2
                # OpenCV 기준점(Baseline)과 PIL 기준점(Top-left) 차이 보정 (-11px)
                d.text((ix + INFO_BOX_PAD, ty - 11), line_str, font=font, fill=(220, 220, 220))
                
        canvas[:] = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
