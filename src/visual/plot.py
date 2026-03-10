import platform
import random
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import warnings
from matplotlib import font_manager, rc
from PIL import Image
warnings.filterwarnings('ignore')

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


def count_plot(df, col, ax=None, figsize=(10, 6), palette="Blues_r", rotation=None, title=None, xlabel=None, ylabel=None, order='desc', orient='v', top_n=None, show=True):
    """
    order: 'desc'(내림차순), 'asc'(오름차순), None(정렬 안 함)
    orient: 'v'(세로, 기본값), 'h'(가로)
    top_n: 상위 N개만 표시 (None이면 전체)
    """
    if ax is None:
        plt.figure(figsize=figsize)
        ax = plt.gca()

    # 정렬 순서 결정
    if order == 'desc':
        order_list = df[col].value_counts().index.tolist()
    elif order == 'asc':
        order_list = df[col].value_counts(ascending=True).index.tolist()
    else:
        order_list = df[col].value_counts().index.tolist()

    # top_n 적용
    if top_n is not None:
        order_list = order_list[:top_n]
        df = df[df[col].isin(order_list)]

    # 방향에 따라 x/y 설정
    if orient == 'h':
        sns.countplot(data=df, y=col, palette=palette, ax=ax, order=order_list)
        ax.set_ylabel(ylabel if ylabel is not None else col)
        ax.set_xlabel(xlabel if xlabel is not None else 'Count')
    else:
        sns.countplot(data=df, x=col, palette=palette, ax=ax, order=order_list)
        ax.set_xlabel(xlabel if xlabel is not None else col)
        ax.set_ylabel(ylabel if ylabel is not None else 'Count')

    ax.set_title(title if title else f'{col} Count')
    if rotation:
        ax.tick_params(axis='x' if orient == 'v' else 'y', rotation=rotation)

    if show:
        plt.tight_layout()
        plt.show()
    return ax


def bar_plot(df, x_col, y_col, ax=None, figsize=(10, 6), hue=None, palette="Blues_r", rotation=None, title=None, xlabel=None, ylabel=None, show=True):
    if ax is None:
        plt.figure(figsize=figsize)
        ax = plt.gca()

    if hue:
        sns.barplot(x=x_col, y=y_col, hue=hue, data=df, palette=palette, ax=ax)
    else:
        sns.barplot(x=x_col, y=y_col, data=df, palette=palette, ax=ax)

    if rotation:
        ax.tick_params(axis='x', rotation=rotation)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if show:
        plt.tight_layout()
        plt.show()
    return ax


def line_plot(df, x_col, y_col, hue=None, ax=None, figsize=(12, 6), color=None, palette='tab10', marker=None, linewidth=1, rotation=None, title=None, xlabel=None, ylabel=None, show=True):
    if ax is None:
        plt.figure(figsize=figsize)
        ax = plt.gca()

    if hue:
        sns.lineplot(data=df, x=x_col, y=y_col, hue=hue, palette=palette, linewidth=linewidth, marker=marker, ax=ax)
    else:
        sns.lineplot(data=df, x=x_col, y=y_col, color=color, linewidth=linewidth, marker=marker, ax=ax)

    if rotation:
        ax.tick_params(axis='x', rotation=rotation)
    ax.set_title(title if title else f'{y_col} by {x_col}')
    ax.set_xlabel(xlabel if xlabel else x_col)
    ax.set_ylabel(ylabel if ylabel else y_col)
    ax.grid(True)

    if show:
        plt.tight_layout()
        plt.show()
    return ax


def box_plot(df, col, hue=None, ax=None, figsize=(8, 6), palette=None, title=None, show=True):
    """
    단일 boxplot 또는 hue로 그룹 비교
    - hue: 그룹 비교할 컬럼명 (예: 'completed')
    - palette: 색상 리스트 (예: ['salmon', 'skyblue'])
    """
    if ax is None:
        plt.figure(figsize=figsize)
        ax = plt.gca()

    if palette is None:
        palette = ['skyblue', 'salmon']

    if hue:
        sns.boxplot(data=df, x=hue, y=col, palette=palette, ax=ax)
        ax.set_title(title if title else f'{col} by {hue}')
    else:
        sns.boxplot(y=df[col], color=palette[0], ax=ax)
        ax.set_title(title if title else f'{col} (Box Plot)')

    ax.set_ylabel(col)

    if show:
        plt.tight_layout()
        plt.show()
    return ax


def hist_plot(df, col, ax=None, figsize=(10, 6), bins='auto', color='steelblue', kde=False, stat='count', title=None, xlabel=None, ylabel=None, show=True):
    """
    히스토그램 시각화
    - bins: 구간 수 ('auto', 정수, 리스트 등)
    - kde: True면 KDE 곡선 함께 표시
    - stat: 'count', 'density', 'probability', 'frequency' 등
    """
    if ax is None:
        plt.figure(figsize=figsize)
        ax = plt.gca()

    sns.histplot(data=df, x=col, bins=bins, color=color, kde=kde, stat=stat, ax=ax)

    ax.set_title(title if title else f'{col} Distribution')
    ax.set_xlabel(xlabel if xlabel else col)
    ax.set_ylabel(ylabel if ylabel else stat.capitalize())

    if show:
        plt.tight_layout()
        plt.show()
    return ax


def kde_plot(df, col, ax=None, figsize=(10, 6), color='steelblue', fill=True, alpha=0.3, linewidth=2, hue=None, palette='Blues', title=None, xlabel=None, ylabel=None, show=True):
    """
    KDE(커널 밀도 추정) 시각화
    - fill: True면 곡선 아래 영역 채움
    - alpha: 채움 투명도 (0~1)
    - hue: 그룹별 비교할 컬럼명
    - palette: hue 사용 시 색상 팔레트
    """
    if ax is None:
        plt.figure(figsize=figsize)
        ax = plt.gca()

    if hue:
        sns.kdeplot(data=df, x=col, hue=hue, fill=fill, alpha=alpha, linewidth=linewidth, palette=palette, ax=ax)
    else:
        sns.kdeplot(data=df, x=col, color=color, fill=fill, alpha=alpha, linewidth=linewidth, ax=ax)

    ax.set_title(title if title else f'{col} KDE')
    ax.set_xlabel(xlabel if xlabel else col)
    ax.set_ylabel(ylabel if ylabel else 'Density')

    if show:
        plt.tight_layout()
        plt.show()
    return ax


def heatmap_plot(data, ax=None, figsize=(12, 8), cmap='Blues', annot=True, fmt='d', linewidths=0.5, cbar=True, title=None, xlabel=None, ylabel=None, rotation_x=45, rotation_y=0, show=True):
    """
    히트맵 시각화 (crosstab, pivot table, correlation matrix 등에 사용)
    - data: 2D 데이터 (DataFrame, crosstab 결과 등)
    - cmap: 색상맵 ('Blues', 'Reds', 'YlGnBu', 'coolwarm' 등)
    - annot: True면 셀에 값 표시
    - fmt: annot 포맷 ('d'=정수, '.2f'=소수점 2자리 등)
    - linewidths: 셀 간 선 두께
    - cbar: True면 컬러바 표시
    - rotation_x, rotation_y: x축, y축 레이블 회전 각도
    """
    if ax is None:
        plt.figure(figsize=figsize)
        ax = plt.gca()

    sns.heatmap(data, annot=annot, fmt=fmt, cmap=cmap, linewidths=linewidths, cbar=cbar, ax=ax)

    ax.set_title(title if title else 'Heatmap')
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)

    if rotation_x:
        ax.tick_params(axis='x', rotation=rotation_x)
    if rotation_y:
        ax.tick_params(axis='y', rotation=rotation_y)

    if show:
        plt.tight_layout()
        plt.show()
    return ax


def sample_images_plot(dataset_path, n: int = 16, cols: int = 8, figsize_per_img: tuple = (2.5, 2.5), seed: int = None, show: bool = True):
    """
    dataset_path 하위의 이미지를 n장 랜덤 샘플링해서 시각화
    - dataset_path: 이미지 파일 또는 클래스 폴더가 담긴 루트 경로 (str or Path)
    - n: 샘플링할 이미지 수
    - cols: 한 행에 표시할 이미지 수
    - figsize_per_img: 이미지 한 장당 figsize 크기
    - seed: 랜덤 시드
    """
    dataset_path = Path(dataset_path)
    exts = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    all_imgs = [p for p in dataset_path.rglob('*') if p.suffix.lower() in exts]

    if not all_imgs:
        raise FileNotFoundError(f"이미지 파일 없음: {dataset_path}")

    random.seed(seed)
    sampled = random.sample(all_imgs, min(n, len(all_imgs)))

    cols = min(cols, len(sampled))
    rows = (len(sampled) + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(cols * figsize_per_img[0], rows * figsize_per_img[1]))
    axes = np.array(axes).flatten()

    for ax, img_path in zip(axes, sampled):
        img = Image.open(img_path)
        label = img_path.parent.name
        ax.imshow(img, cmap='gray' if img.mode == 'L' else None)
        ax.set_title(label, fontsize=7)
        ax.axis('off')

    for ax in axes[len(sampled):]:
        ax.axis('off')

    plt.suptitle(f"{dataset_path.name}  |  샘플 {len(sampled)}장", fontsize=11)
    plt.tight_layout()

    if show:
        plt.show()
        return None
    return fig