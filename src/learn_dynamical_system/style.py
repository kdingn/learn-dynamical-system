"""Matplotlib rcParams shared configuration.

Call ``apply()`` at the top of every figure script to ensure a consistent look.

図のフォントをスライド本文と揃えるための考え方
------------------------------------------------
figsize が ``w`` インチの図を、スライド上で ``W`` CSS px 幅で表示したとき、
``F`` pt のフォントの見かけの大きさは

    displayed_px = F * W / (72 * w)

になる。ここで **1 インチ = SLIDE_PX_PER_INCH (96) CSS px で表示する**
と決めてしまえば W = 96w なので

    displayed_px = F * 96 / 72 = 1.333 * F

と figsize に依存しなくなる。本文が SLIDE_BODY_PX のとき、これと一致する
フォントサイズが BASE_FONT_PT。図のサイズは :func:`slot` で CSS px から
逆算し、スライド側は同じ px 幅で表示する。

``savefig.bbox`` に "tight" を使うと保存後の画素数が figsize とずれて
この対応が壊れるため、既定のままにして ``layout="constrained"`` で
余白を詰める。
"""

import matplotlib.pyplot as plt
import scienceplots  # noqa: F401  (registers styles on import)
from matplotlib.colors import LinearSegmentedColormap

from learn_dynamical_system.palette import FG

# --- Slidev 側の実寸（@slidev/parser: canvasWidth=980, aspectRatio=16/9、
#     @slidev/client/styles/layouts-base.css: .slidev-layout { px-14 py-10 text-[1.1rem] }）
CANVAS_W_PX = 980.0
CANVAS_H_PX = CANVAS_W_PX * 9 / 16   # 551.25
CONTENT_W_PX = CANVAS_W_PX - 2 * 56  # 868
CONTENT_H_PX = CANVAS_H_PX - 2 * 40  # 471.25

SLIDE_PX_PER_INCH = 96.0   # CSS の 1in = 96px。この比率で等倍表示する
SLIDE_BODY_PX = 17.6       # text-[1.1rem]

#: 本文と同じ見かけの大きさになるフォントサイズ (pt)
BASE_FONT_PT = SLIDE_BODY_PX * 72 / SLIDE_PX_PER_INCH  # 13.2
#: 目盛・凡例など補助テキスト（本文の 0.85 倍）
SMALL_FONT_PT = BASE_FONT_PT * 0.85

#: 図の外周に持たせる余白 (CSS px)。見出し・キャプションとの間隔になる。
#: スライド側の margin ではなく図に内包させるので、:func:`slot` に渡す寸法が
#: そのまま「スライド上で占める総量」になる。
FIGURE_PAD_PX = 20.0


def slot(width_px: float, height_px: float) -> tuple[float, float]:
    """スライド上の表示サイズ (CSS px) から figsize (inch) を求める。

    返った figsize で図を作り、スライド側は ``width_px`` で表示すること。
    """
    return (width_px / SLIDE_PX_PER_INCH, height_px / SLIDE_PX_PER_INCH)


def sequential_cmap(*colors: str) -> LinearSegmentedColormap:
    """palette の色から連続カラーマップを作る。

    matplotlib 組み込みの ``coolwarm`` などは中央付近が白に近く、明るい
    スライド背景では消えてしまう。palette の色だけで作ることで、色の
    一貫性とコントラストの両方を保つ。
    """
    return LinearSegmentedColormap.from_list("lds", list(colors))


def apply() -> None:
    """Activate the project-wide matplotlib style."""
    plt.style.use(["science", "no-latex"])
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["CMU Serif", "Computer Modern Roman", "DejaVu Serif"],
            "mathtext.fontset": "cm",
            "font.size": BASE_FONT_PT,
            "axes.labelsize": BASE_FONT_PT,
            "axes.titlesize": BASE_FONT_PT,
            "xtick.labelsize": SMALL_FONT_PT,
            "ytick.labelsize": SMALL_FONT_PT,
            "legend.fontsize": SMALL_FONT_PT,
            "figure.dpi": 96,
            # 96px/inch 表示の 2 倍で書き出す（高 DPI ディスプレイ用）
            "savefig.dpi": 192,
            # "tight" は figsize と出力画素数の対応を壊すので使わない
            "savefig.bbox": None,
            "figure.constrained_layout.use": True,
            # 図の外周に余白を持たせる。既定の 0.04167in は 4 CSS px しかなく、
            # 見出しやキャプションと図が接触して見える。スライド側に margin を
            # 足すのではなく図に内包させることで、SLOT_* の値がそのまま
            # 「スライド上で占める総量」になり、高さの計算が一段で済む。
            # constrained_layout は外周 pad を確保してからパネルを配置するので、
            # パネル側にしわ寄せが行かない。
            "figure.constrained_layout.w_pad": FIGURE_PAD_PX / SLIDE_PX_PER_INCH,
            "figure.constrained_layout.h_pad": FIGURE_PAD_PX / SLIDE_PX_PER_INCH,
            # 複数パネルの図では、どのタイトル・軸がどのパネルのものか
            # 一目で分かるようにパネル間を少し離す（既定の 0.02 は詰まりすぎ）
            "figure.constrained_layout.wspace": 0.09,
            "figure.constrained_layout.hspace": 0.09,
            # --- 暗いスライド背景に載せる: 透過 + 明るい前景色 ---
            "figure.facecolor": "none",
            "axes.facecolor": "none",
            "savefig.facecolor": "none",
            "savefig.transparent": True,
            "text.color": FG,
            "axes.labelcolor": FG,
            "axes.edgecolor": FG,
            "xtick.color": FG,
            "ytick.color": FG,
            "legend.facecolor": "none",
            "legend.edgecolor": "none",
            "legend.labelcolor": FG,
        }
    )
