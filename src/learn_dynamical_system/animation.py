"""manim 側の共通設定。

matplotlib の :mod:`style` と同じ考え方で、**スライド上の表示サイズちょうど**で
動画を書き出す。こうすると図と同じく等倍で貼れて、動画内の文字サイズも
本文と揃う。

manim の座標系は「フレーム幅 = ``frame_width`` manim 単位」で、ピクセル数は
``pixel_width`` で決まる。スライド上で ``width_px`` CSS px で表示したいなら、

* ``pixel_width  = width_px * 2``（高 DPI 用に 2 倍で書き出す）
* ``frame_width  = width_px / SLIDE_PX_PER_INCH``（= matplotlib の figsize と同じ
  インチ数を manim 単位に読み替える）

と取れば、1 manim 単位 = 1 インチ = 96 CSS px になり、
:data:`~learn_dynamical_system.style.BASE_FONT_PT` と同じ pt 指定がそのまま通る。
"""

from __future__ import annotations

from pathlib import Path

from manim import config

from learn_dynamical_system import style
from learn_dynamical_system.palette import BLUE, FG, GREEN, GREY, ORANGE, RED

__all__ = [
    "OUTPUT_DIR", "SCALE", "apply", "font_size", "BLUE", "RED", "GREEN",
    "ORANGE", "GREY", "FG",
]

#: 動画の出力先。図と同じく public/ 配下に置く
OUTPUT_DIR = Path(__file__).resolve().parents[2] / "public" / "animations"

#: 高 DPI 用の書き出し倍率（図の savefig.dpi = 192 と揃える）
SCALE = 2


#: manim の ``font_size`` 1 あたりのグリフ高さ (manim 単位)。
#: ``Text("Hxq", font_size=48).height == 0.6246`` を実測して求めた。
#: ``font_size`` はピクセル数ではなく**フレーム座標**で解釈されるので、
#: :data:`SCALE` は掛けないこと（掛けると 2 倍の文字になる）。
_HEIGHT_PER_FONT_SIZE = 0.6246 / 48

#: 「H の上端から q の下端まで」が公称フォントサイズの何倍か（一般的な欧文書体の目安）
_GLYPH_SPAN_RATIO = 0.95


def font_size(pt: float) -> float:
    """matplotlib と同じ pt 指定を manim の ``font_size`` に変換する。

    1 manim 単位 = 1 インチ = ``SLIDE_PX_PER_INCH`` CSS px として書き出すので、
    pt をいったん CSS px の公称サイズに直し、実測した比率で逆算する。
    結果はおおむね ``font_size == pt`` になる。
    """
    nominal_px = pt * style.SLIDE_PX_PER_INCH / 72
    height_units = nominal_px * _GLYPH_SPAN_RATIO / style.SLIDE_PX_PER_INCH
    return height_units / _HEIGHT_PER_FONT_SIZE


def apply(width_px: float, height_px: float) -> None:
    """スライド上の表示サイズ (CSS px) を指定して manim の出力設定を行う。

    ``style.slot()`` と対になる関数。同じ ``SLOT_*`` 定数を渡すこと。
    """
    config.pixel_width = int(width_px * SCALE)
    config.pixel_height = int(height_px * SCALE)
    config.frame_width = width_px / style.SLIDE_PX_PER_INCH
    config.frame_height = height_px / style.SLIDE_PX_PER_INCH
    # スライドは dark 固定。図と同じく背景は透過にして本文に馴染ませる
    config.background_color = "#121212"
    config.media_dir = str(OUTPUT_DIR / ".manim")
    config.video_dir = str(OUTPUT_DIR)
    config.disable_caching = False
    config.verbosity = "WARNING"
    config.frame_rate = 30
