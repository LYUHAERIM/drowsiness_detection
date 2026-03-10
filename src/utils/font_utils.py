import platform

import matplotlib.pyplot as plt
from matplotlib import font_manager, rc


def set_korean_font(verbose: bool = False) -> bool:
    """한글 폰트 설정. Mac, Windows, Linux 지원. verbose=True면 메시지 출력."""
    system = platform.system()
    success = False
    font_name = None

    # OS별 한글 폰트 후보 목록
    font_candidates = {
        'Darwin': ['Arial Unicode MS', 'AppleGothic', 'Apple SD Gothic Neo'],
        'Windows': ['Malgun Gothic', 'NanumGothic', 'Gulim', 'Dotum'],
        'Linux': ['Noto Sans CJK KR', 'NanumGothic', 'NanumBarunGothic', 'UnDotum', 'DejaVu Sans'],
    }

    # 시스템에 설치된 폰트 목록
    available_fonts = {f.name for f in font_manager.fontManager.ttflist}

    # 해당 OS의 폰트 후보에서 사용 가능한 폰트 찾기
    candidates = font_candidates.get(system, font_candidates['Linux'])

    for font in candidates:
        if font in available_fonts:
            font_name = font
            break

    if font_name:
        rc('font', family=font_name)
        success = True
        if verbose:
            print(f'[font] Using Korean font: {font_name}')
    else:
        if verbose:
            print(f'[font] No Korean font found for {system}. Tried: {candidates}')
        success = False

    plt.rcParams['axes.unicode_minus'] = False
    return success
