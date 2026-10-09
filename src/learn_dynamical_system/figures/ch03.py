"""Chapter 3 figures: Bifurcation Theory."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

from learn_dynamical_system import style
from learn_dynamical_system.models.typical_section import TypicalSection
from learn_dynamical_system.palette import (
    BLUE, FG, GREEN, GREY, ORANGE, PURPLE, RED,
)

# スライド上での表示サイズ (CSS px)。図はこの寸法ちょうどで作られるので、
# slides/03-bifurcation.md 側の `width:` 指定をこの値と一致させること。
SLOT_CHAPTER_OVERVIEW = (820, 250)
SLOT_MOTIVATION = (820, 222)
SLOT_EIGENVALUE_CROSSING = (720, 200)
SLOT_SINGULAR_J = (760, 180)
SLOT_PERTURBATION_DECOMP = (380, 310)
SLOT_SURFACES_3D = (840, 245)
SLOT_SADDLE_CONNECTION = (780, 200)
SLOT_ROBUST_HYPERBOLIC = (840, 220)
SLOT_LOCAL_FRAGILE = (840, 220)
SLOT_GLOBAL_FRAGILE = (840, 220)
SLOT_CODIMENSION = (360, 300)
SLOT_SADDLE_NODE = (360, 300)
SLOT_TC_PITCHFORK = (820, 280)
SLOT_HYSTERESIS = (380, 290)
SLOT_IMPERFECT = (780, 220)
SLOT_HOPF = (820, 240)
SLOT_HOPF_EXAMPLE = (760, 260)
SLOT_FLUTTER_HOPF = (820, 240)

#: 安定な枝は実線、不安定な枝は破線（全ての分岐図で共通）
STABLE = dict(color=BLUE, lw=2.0, ls="-")
UNSTABLE = dict(color=RED, lw=1.8, ls="--")


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _hide_axes(ax) -> None:
    """概念図用: 軸・目盛・枠をすべて消す."""
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


def _arrow(ax, p0, p1, color, lw=1.2, style_="-|>", alpha=1.0):
    ax.annotate("", xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle=style_, color=color, lw=lw,
                                alpha=alpha, shrinkA=0, shrinkB=0))


def _plot_branch(ax, mu, x, stable_mask) -> None:
    """固定点の枝を安定（実線）／不安定（破線）に塗り分けて描く."""
    ax.plot(mu, np.where(stable_mask, x, np.nan), **STABLE)
    ax.plot(mu, np.where(~stable_mask, x, np.nan), **UNSTABLE)


def _phase_arrows(ax, mu, g, xlim, n=9, color=GREY, length=0.16):
    """縦の相直線: μ を止めたときの dx/dt の符号を矢印で描く.

    固定点の枝の上にはかからないよう、矢印は固定点から離れた点に置く。
    """
    fine = np.linspace(xlim[0] - 0.5, xlim[1] + 0.5, 4001)
    gv = g(fine, mu)
    roots = fine[:-1][np.sign(gv[:-1]) != np.sign(gv[1:])]
    xs = np.linspace(xlim[0], xlim[1], n)
    for x in xs:
        v = g(x, mu)
        if abs(v) < 1e-3 or np.any(np.abs(roots - x) < 0.2):
            continue
        d = np.sign(v) * length
        _arrow(ax, (mu, x - d / 2), (mu, x + d / 2), color, lw=1.0)


def _bif_axes(ax, xlabel=r"$\mu$", ylabel=r"$x^*$") -> None:
    """分岐図の軸: 原点を通る細い補助線と、端に置いた軸ラベル."""
    ax.axhline(0, color=GREY, lw=0.6, alpha=0.6, zorder=0)
    ax.axvline(0, color=GREY, lw=0.6, alpha=0.6, zorder=0)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


# ---------------------------------------------------------------------------
# 1. Chapter overview (cover schematic)
# ---------------------------------------------------------------------------

def chapter_overview(output_dir: Path) -> None:
    """章の筋道: 固有値が虚軸を横切る → 相図が変わる → 分岐図."""
    style.apply()

    fig, ax = plt.subplots(figsize=style.slot(*SLOT_CHAPTER_OVERVIEW))
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 9.2)
    _hide_axes(ax)
    fs = style.SMALL_FONT_PT
    cy = 5.9

    # --- (1) 固有値が虚軸を横切る ---
    cx = 4.6
    ax.plot([cx - 3.0, cx + 3.0], [cy, cy], color=GREY, lw=0.9)
    ax.plot([cx, cx], [cy - 2.6, cy + 2.6], color=GREY, lw=0.9)
    for s in (1, -1):
        ax.plot(cx - 1.6, cy + s * 1.6, "x", color=BLUE, ms=8, mew=2)
        ax.plot(cx + 1.6, cy + s * 1.6, "x", color=RED, ms=8, mew=2)
        _arrow(ax, (cx - 1.25, cy + s * 1.6), (cx + 1.25, cy + s * 1.6),
               FG, lw=1.3)
    ax.text(cx + 0.15, cy + 2.6, r"Im $\lambda$", color=GREY, fontsize=fs,
            ha="left", va="top")
    ax.text(cx + 3.0, cy - 0.2, r"Re $\lambda$", color=GREY, fontsize=fs,
            ha="right", va="top")
    ax.text(cx, 1.9, r"$\lambda(\mu)$ crosses Re $\lambda = 0$", ha="center",
            fontsize=fs, color=FG)
    ax.text(cx, 0.55, r"at $\mu = \mu_0$", ha="center", fontsize=fs,
            color=GREY)

    # --- (2) 相図が変わる: 渦が吸い込む → 周期軌道 ---
    cx = 14.6
    th = np.linspace(0, 6 * np.pi, 500)
    r = 2.2 * np.exp(-0.09 * th)
    ax.plot(cx - 1.5 + 0.55 * r * np.cos(th), cy + 0.55 * r * np.sin(th),
            color=BLUE, lw=1.3)
    ax.plot(cx - 1.5, cy, "o", color=FG, ms=5, zorder=6)
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(cx + 1.6 + 1.05 * np.cos(th), cy + 1.05 * np.sin(th),
            color=GREEN, lw=2.0)
    ax.plot(cx + 1.6, cy, "o", color=FG, ms=5, zorder=6, mfc="none")
    ax.text(cx - 1.5, cy - 1.75, r"$\mu < \mu_0$", color=GREY, fontsize=fs,
            ha="center", va="top")
    ax.text(cx + 1.6, cy - 1.75, r"$\mu > \mu_0$", color=GREY, fontsize=fs,
            ha="center", va="top")
    ax.text(cx, 1.9, "Phase portrait changes", ha="center", fontsize=fs,
            color=FG)
    ax.text(cx, 0.55, "not structurally stable at $\\mu_0$", ha="center",
            fontsize=fs, color=GREY)

    # --- (3) 分岐図 ---
    cx = 24.8
    mu = np.linspace(0, 3.0, 200)
    ax.plot([cx - 3.0, cx], [cy - 0.9, cy - 0.9], **STABLE)
    ax.plot([cx, cx + 3.0], [cy - 0.9, cy - 0.9], **UNSTABLE)
    ax.plot(cx + mu, cy - 0.9 + 1.5 * np.sqrt(mu), color=GREEN, lw=2.0)
    ax.text(cx + 3.05, cy - 0.9 + 1.5 * np.sqrt(3.0), r"$\sqrt{\mu - \mu_0}$",
            color=GREEN, fontsize=fs, ha="left", va="center")
    ax.text(cx + 3.05, cy - 0.9, r"$\mu$", color=GREY, fontsize=fs,
            ha="left", va="center")
    ax.text(cx, 1.9, "Normal form", ha="center", fontsize=fs, color=FG)
    ax.text(cx, 0.55, r"$\dot{z} = (\mu + i\omega)z + c_1|z|^2 z$",
            ha="center", fontsize=fs, color=GREY)

    for x0, x1 in ((8.4, 10.4), (18.6, 20.6)):
        _arrow(ax, (x0, cy), (x1, cy), FG, lw=1.4)

    fig.savefig(output_dir / "ch03_overview.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 2. Two ways for an eigenvalue to reach the imaginary axis
# ---------------------------------------------------------------------------

def eigenvalue_crossing(output_dir: Path) -> None:
    """実固有値が 0 を通る場合と、複素共役対が虚軸を横切る場合."""
    style.apply()

    fig, axes = plt.subplots(1, 2, figsize=style.slot(*SLOT_EIGENVALUE_CROSSING))
    fs = style.SMALL_FONT_PT

    for ax in axes:
        ax.set_xlim(-3.2, 3.2)
        ax.set_ylim(-2.2, 2.2)
        _hide_axes(ax)
        # 安定側（左半平面）を薄く塗る
        ax.fill_between([-3.2, 0], -2.2, 2.2, color=BLUE, alpha=0.08, lw=0)
        ax.plot([-3.0, 3.0], [0, 0], color=GREY, lw=0.9)
        ax.plot([0, 0], [-2.0, 2.0], color=GREEN, lw=1.6)
        ax.text(3.0, -0.15, r"Re", color=GREY, fontsize=fs, ha="right",
                va="top")
        ax.text(-0.12, 2.0, r"Im", color=GREY, fontsize=fs, ha="right",
                va="top")
        ax.text(-1.6, -1.75, "stable", color=BLUE, fontsize=fs, ha="center")
        ax.text(1.6, -1.75, "unstable", color=RED, fontsize=fs, ha="center")

    # --- 左: 実固有値が 0 を通る ---
    ax = axes[0]
    ax.plot(-1.4, 0, "x", color=BLUE, ms=9, mew=2, zorder=5)
    ax.plot(1.4, 0, "x", color=RED, ms=9, mew=2, zorder=5)
    _arrow(ax, (-1.1, 0.35), (1.1, 0.35), FG, lw=1.4)
    ax.plot(0, 0, "o", color=GREEN, ms=7, zorder=6)
    ax.text(0.15, 0.55, r"$\lambda = 0$", color=GREEN, fontsize=fs,
            ha="left", va="bottom")
    ax.set_title(r"real $\lambda$ passes through $0$", fontsize=fs)

    # --- 右: 複素共役対が虚軸を横切る ---
    ax = axes[1]
    for s in (1, -1):
        ax.plot(-1.4, s * 1.1, "x", color=BLUE, ms=9, mew=2, zorder=5)
        ax.plot(1.4, s * 1.1, "x", color=RED, ms=9, mew=2, zorder=5)
        _arrow(ax, (-1.1, s * 1.1), (1.1, s * 1.1), FG, lw=1.4)
        ax.plot(0, s * 1.1, "o", color=GREEN, ms=7, zorder=6)
    ax.text(0.15, 0.9, r"$i\omega$", color=GREEN, fontsize=fs,
            ha="left", va="top")
    ax.text(0.15, -0.9, r"$-i\omega$", color=GREEN, fontsize=fs,
            ha="left", va="bottom")
    ax.set_title(r"complex pair crosses the imaginary axis", fontsize=fs)

    fig.savefig(output_dir / "eigenvalue_crossing.png")
    plt.close(fig)


def singular_jacobian(output_dir: Path) -> None:
    """固定点 = グラフと x 軸の交点。傾き (= λ) が 0 だと、ずらすと交点が 2 つか 0 個."""
    style.apply()

    fig, axes = plt.subplots(1, 2, figsize=style.slot(*SLOT_SINGULAR_J))
    fs = style.SMALL_FONT_PT
    x = np.linspace(-1.3, 1.3, 300)
    # μ の符号に意味はない。着目する値 μ0 から上下どちらにずらすかだけを示す
    shifts = ((0.35, GREEN, r"$\mu_0 + \delta$"), (0.0, FG, r"$\mu_0$"),
              (-0.35, ORANGE, r"$\mu_0 - \delta$"))

    for ax, kind in zip(axes, ("transversal", "tangent")):
        ax.axhline(0, color=GREY, lw=1.0)
        ax.text(1.3, -0.06, r"$x$", color=GREY, fontsize=fs, ha="right",
                va="top")
        for c, color, label in shifts:
            if kind == "transversal":
                # 傾き 0.6 の直線。上下にずらしても交点は1つのまま
                y = 0.6 * x + c
                zeros = [-c / 0.6]
                y_end = 0.6 * 1.3 + c
            else:
                y = c - x**2
                zeros = [np.sqrt(c), -np.sqrt(c)] if c > 0 else (
                    [0.0] if c == 0 else [])
                y_end = c - 1.3**2
            lw = 2.0 if c == 0 else 1.6
            ax.plot(x, y, color=color, lw=lw)
            for z in zeros:
                # 傾き（= 固有値）が負なら安定（塗り）、正なら不安定（白抜き）
                slope = 0.6 if kind == "transversal" else -2 * z
                filled = slope < 0
                ax.plot(z, 0, "o", color=color, ms=7, zorder=6, mew=1.6,
                        mfc=color if filled else "none")
            ax.text(1.36, y_end, label, color=color, fontsize=fs,
                    ha="left", va="center")
        ax.set_xlim(-1.3, 2.15)
        _hide_axes(ax)

    axes[0].set_ylim(-1.25, 1.25)
    axes[1].set_ylim(-2.05, 0.6)
    axes[0].set_title(r"slope $\lambda \neq 0$: one zero persists",
                      fontsize=fs)
    axes[1].set_title(r"slope $\lambda = 0$: two zeros or none", fontsize=fs)

    fig.savefig(output_dir / "singular_jacobian.png")
    plt.close(fig)


def perturbation_decomposition(output_dir: Path) -> None:
    """摂動 ξ を固有ベクトル成分に分け、各成分がどう動くかを軌道で見せる.

    例 dx/dt = mu - x^2, dy/dt = -y の mu = mu0 (= 0)。v2 (y) 成分は e^{-t} で
    速く消え、v1 (x) 成分は線形では変わらず x^2 の項でゆっくり動く。
    """
    style.apply()

    fig, ax = plt.subplots(figsize=style.slot(*SLOT_PERTURBATION_DECOMP))
    fs = style.SMALL_FONT_PT
    # 概念図なので縦横比は揃えない（x 方向を引き伸ばして原点付近を見やすくする）
    ax.set_xlim(-0.2, 0.62)
    ax.set_ylim(-0.36, 1.22)
    _hide_axes(ax)

    # 固有ベクトルの向き（原点を通る直線）
    ax.plot([-0.18, 0.6], [0, 0], color=GREEN, lw=1.4, zorder=2)
    ax.plot([0, 0], [-0.32, 1.18], color=BLUE, lw=1.4, zorder=2)
    ax.text(0.6, 0.03, r"$v_1$ ($\lambda_1 = 0$)", color=GREEN, fontsize=fs,
            ha="right", va="bottom")
    ax.text(0.012, 1.2, r"$v_2$ ($\lambda_2 = -1$)", color=BLUE, fontsize=fs,
            ha="left", va="top")

    # 摂動 ξ とその分解 s1 v1 + s2 v2
    p = np.array([0.4, 1.0])
    ax.plot([p[0], p[0]], [0, p[1]], color=GREEN, lw=0.9, ls=":")
    ax.plot([0, p[0]], [p[1], p[1]], color=BLUE, lw=0.9, ls=":")
    _arrow(ax, (0, 0), (p[0], 0), GREEN, lw=2.2)
    _arrow(ax, (0, 0), (0, p[1]), BLUE, lw=2.2)
    _arrow(ax, (0, 0), tuple(p), FG, lw=1.8)
    ax.text(0.3, 0.03, r"$s_1 v_1$", color=GREEN, fontsize=fs,
            ha="center", va="bottom")
    ax.text(-0.012, 0.5, r"$s_2 v_2$", color=BLUE, fontsize=fs,
            ha="right", va="center")
    ax.text(0.17, 0.55, r"$\xi$", color=FG, fontsize=style.BASE_FONT_PT,
            ha="right", va="bottom")

    # ξ から出発した軌道（mu = mu0 = 0）と、等時間間隔の点
    t = np.linspace(0, 10, 600)
    ax.plot(p[0] / (1 + p[0] * t), p[1] * np.exp(-t), color=ORANGE, lw=1.8,
            zorder=4)
    tk = np.arange(0, 10.01, 1.0)
    ax.plot(p[0] / (1 + p[0] * tk), p[1] * np.exp(-tk), "o", color=ORANGE,
            ms=4.5, zorder=5)
    ax.plot(0, 0, "o", color=FG, ms=7, zorder=6)
    ax.text(0.425, 0.62, "1. fast\n" + r"$s_2 \propto e^{-t}$", color=BLUE,
            fontsize=fs, ha="left", va="center")
    ax.text(0.01, -0.06, "2. slow along $v_1$\n" + r"($x^2$ term)",
            color=GREEN, fontsize=fs, ha="left", va="top")
    ax.set_title(r"orbit from $q^* + \xi$ (dots every $\Delta t = 1$)",
                 fontsize=fs)

    fig.savefig(output_dir / "perturbation_decomposition.png")
    plt.close(fig)


def surfaces_3d(output_dir: Path) -> None:
    """f の各成分を面で描く: z = f1 (v1 方向) と z = f2 (v2 方向)、および z = 0.

    例 dx/dt = mu - x^2, dy/dt = -y。f2 = -y は z = 0 を斜めに横切る面
    （λ2 = -1）、f1 = mu - x^2 は z = 0 に接する放物柱面（λ1 = 0）で、mu で
    上下に動く。各面が z = 0 と交わる線の交わりが固定点。
    """
    style.apply()

    fig = plt.figure(figsize=style.slot(*SLOT_SURFACES_3D))
    fs = style.SMALL_FONT_PT
    d = 0.36
    u = np.linspace(-1.2, 1.2, 40)
    U, V = np.meshgrid(u, u)

    cases = ((-d, r"$\mu_0 - \delta$: 0 fixed points"),
             (0.0, r"$\mu_0$: 1"),
             (d, r"$\mu_0 + \delta$: 2"))
    for i, (mu, title) in enumerate(cases):
        ax = fig.add_subplot(1, 3, i + 1, projection="3d")
        ax.set_proj_type("ortho")
        ax.view_init(elev=24, azim=-58)
        # 3D 軸は既定で内側に大きな余白を取るので、拡大して詰める
        ax.set_box_aspect(None, zoom=1.12)

        # z = 0 の面（枠だけ）
        e = 1.2
        ax.plot([-e, e, e, -e, -e], [-e, -e, e, e, -e], [0] * 5, color=GREY,
                lw=0.8)
        # z = f1 = mu - x^2（v1 方向）と z = f2 = -y（v2 方向）
        ax.plot_surface(U, V, mu - U**2, color=GREEN, alpha=0.28, lw=0,
                        shade=False)
        ax.plot_surface(U, V, -V, color=BLUE, alpha=0.32, lw=0,
                        shade=False)
        # 各面が z = 0 と交わる線
        ax.plot([-e, e], [0, 0], [0, 0], color=BLUE, lw=2.0)
        zeros = [] if mu < 0 else ([0.0] if mu == 0 else
                                   [-np.sqrt(mu), np.sqrt(mu)])
        for z in zeros:
            ax.plot([z, z], [-e, e], [0, 0], color=GREEN, lw=2.0)
            ax.scatter([z], [0], [0], color=FG, s=30, depthshade=False,
                       zorder=10)

        ax.set_xlim(-e, e)
        ax.set_ylim(-e, e)
        ax.set_zlim(-1.65, 0.9)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
            axis.set_pane_color((0, 0, 0, 0))
            axis.line.set_color(GREY)
        ax.grid(False)
        ax.set_xlabel(r"$v_1$", labelpad=-12)
        ax.set_ylabel(r"$v_2$", labelpad=-12)
        ax.set_zlabel(r"$f$", labelpad=-12)
        # 3D 軸のタイトルは既定だと面から離れすぎるので、下げて近づける
        ax.set_title(title, fontsize=fs, y=0.9)

    fig.savefig(output_dir / "surfaces_3d.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 3. Structural stability: what survives a small perturbation and what does not
# ---------------------------------------------------------------------------

def _frame(ax):
    """軸・目盛を消し、枠だけ薄く残す（小さなパネルの区切り用）."""
    _hide_axes(ax)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color(GREY)
        spine.set_linewidth(0.6)


def _stream(ax, f, lim, density=0.6):
    """[-lim, lim]^2 に f(X, Y) -> (U, V) の流線を薄く描き、枠を整える."""
    g = np.linspace(-lim, lim, 60)
    X, Y = np.meshgrid(g, g)
    U, V = f(X, Y)
    ax.streamplot(X, Y, U, V, color=GREY, linewidth=0.5, density=density,
                  arrowsize=0.6)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    _frame(ax)


def _pair_axes(fig):
    """2 つずつ組になった 4 パネル。組の間に細い空き列を挟んで区切る."""
    gs = fig.add_gridspec(1, 5, width_ratios=[1, 1, 0.18, 1, 1])
    axes = [fig.add_subplot(gs[0, i]) for i in (0, 1, 3, 4)]
    return axes


def robust_hyperbolic(output_dir: Path) -> None:
    """双曲型のノードとサドルは、少しずらしても同じ型のまま（構造安定）."""
    style.apply()

    fig = plt.figure(figsize=style.slot(*SLOT_ROBUST_HYPERBOLIC))
    axes = _pair_axes(fig)
    fs = style.SMALL_FONT_PT
    lim = 1.2

    panels = (
        (r"node: $f$", lambda X, Y: (-X, -2 * Y), True),
        (r"node: $f + \varepsilon g$",
         lambda X, Y: (-X + 0.5 * Y + 0.4 * X**2, -2 * Y + 0.4 * X), True),
        (r"saddle: $f$", lambda X, Y: (X, -Y), False),
        (r"saddle: $f + \varepsilon g$",
         lambda X, Y: (X + 0.4 * Y + 0.3 * Y**2, -Y + 0.4 * X), False),
    )
    for ax, (title, field, filled) in zip(axes, panels):
        _stream(ax, field, lim)
        ax.plot(0, 0, "o", color=FG, ms=7, zorder=6, mew=1.6,
                mfc=FG if filled else "none")
        ax.set_title(title, fontsize=fs, color=GREEN)

    fig.savefig(output_dir / "robust_hyperbolic.png")
    plt.close(fig)


def local_fragile(output_dir: Path) -> None:
    """固定点が非双曲だと、少しずらすだけで型が変わる（構造不安定）."""
    style.apply()

    fig = plt.figure(figsize=style.slot(*SLOT_LOCAL_FRAGILE))
    axes = _pair_axes(fig)
    fs = style.SMALL_FONT_PT
    lim = 1.2

    # --- 実固有値が 0: サドルノードの瞬間 ---
    _stream(axes[0], lambda X, Y: (-X**2, -Y), lim)
    axes[0].plot(0, 0, "o", color=FG, ms=7, zorder=6, mfc="none", mew=1.6)
    axes[0].set_title(r"$\lambda = 0$: one point", fontsize=fs, color=RED)
    _stream(axes[1], lambda X, Y: (0.25 - X**2, -Y), lim)
    axes[1].plot(0.5, 0, "o", color=FG, ms=7, zorder=6)
    axes[1].plot(-0.5, 0, "o", color=FG, ms=7, zorder=6, mfc="none",
                 mew=1.6)
    axes[1].set_title(r"shifted: two (or none)", fontsize=fs)

    # --- 複素共役対が虚軸上: センター ---
    _stream(axes[2], lambda X, Y: (Y, -X), lim)
    axes[2].plot(0, 0, "o", color=FG, ms=7, zorder=6)
    axes[2].set_title(r"$\lambda = \pm i\omega$: center", fontsize=fs,
                      color=RED)
    _stream(axes[3], lambda X, Y: (Y, -X - 0.3 * Y), lim)
    axes[3].plot(0, 0, "o", color=FG, ms=7, zorder=6)
    axes[3].set_title("shifted: spiral", fontsize=fs)

    fig.savefig(output_dir / "local_fragile.png")
    plt.close(fig)


def _wrapped(ax, th1, th2, color, lw):
    """トーラス（単位正方形の両端を同一視）上の軌道を、折り返しで切って描く."""
    a, b = np.mod(th1, 1.0), np.mod(th2, 1.0)
    jump = (np.abs(np.diff(a)) > 0.5) | (np.abs(np.diff(b)) > 0.5)
    cut = np.where(jump)[0] + 1
    for sa, sb in zip(np.split(a, cut), np.split(b, cut)):
        ax.plot(sa, sb, color=color, lw=lw)


def global_fragile(output_dir: Path) -> None:
    """固定点の近くでは見えない構造不安定: 非双曲な周期軌道と、稠密な軌道.

    左の組: 半安定な周期軌道 dr/dt = (r - 1)^2 - eps。ずらすと 2 つ（または 0）。
    右の組: トーラス上の無理数回転（軌道が稠密）。ずらすと周期軌道に引き込まれる。
    サドル接続は saddle_connection の図で別に示す。
    """
    style.apply()

    fig = plt.figure(figsize=style.slot(*SLOT_GLOBAL_FRAGILE))
    axes = _pair_axes(fig)
    fs = style.SMALL_FONT_PT

    # --- 非双曲な周期軌道 ---
    th = np.linspace(0, 2 * np.pi, 200)
    for ax, eps in ((axes[0], 0.0), (axes[1], 0.06)):
        def rhs(t, s, eps=eps):
            r, _ = s
            return [(r - 1) ** 2 - eps, 1.0]
        for r0, t_end in ((0.45, 14.0), (1.12, 5.0)):
            sol = solve_ivp(rhs, (0, t_end), [r0, 0.0], max_step=0.02)
            r, ang = sol.y
            keep = r < 1.55
            ax.plot(r[keep] * np.cos(ang[keep]), r[keep] * np.sin(ang[keep]),
                    color=GREY, lw=0.8)
        if eps == 0:
            ax.plot(np.cos(th), np.sin(th), color=PURPLE, lw=2.0)
        else:
            rs, ru = 1 - np.sqrt(eps), 1 + np.sqrt(eps)
            ax.plot(rs * np.cos(th), rs * np.sin(th), color=GREEN, lw=2.0)
            ax.plot(ru * np.cos(th), ru * np.sin(th), color=GREEN, lw=1.5,
                    ls="--")
        ax.plot(0, 0, "o", color=FG, ms=4, zorder=6, mfc="none", mew=1.2)
        ax.set_xlim(-1.6, 1.6)
        ax.set_ylim(-1.6, 1.6)
        ax.set_aspect("equal")
        _frame(ax)
    axes[0].set_title("semi-stable cycle", fontsize=fs, color=RED)
    axes[1].set_title("shifted: two (or none)", fontsize=fs)

    # --- トーラス上の無理数回転と、その引き込み ---
    alpha = (np.sqrt(5) - 1) / 2
    t = np.linspace(0, 24, 6000)
    _wrapped(axes[2], t, alpha * t + 0.1, GREY, 0.7)

    def rhs(tt, s):
        th1, th2 = s
        return [1.0, alpha - 0.2 * np.sin(2 * np.pi * (2 * th2 - th1))]
    for th20 in (0.05, 0.4, 0.75):
        sol = solve_ivp(rhs, (0, 10), [0.0, th20], max_step=0.01)
        _wrapped(axes[3], sol.y[0], sol.y[1], GREY, 0.8)
    # 引き込み先の周期軌道（2 th2 - th1 = 一定、傾き 1/2）
    phi = np.arcsin((2 * alpha - 1) / 0.4) / (2 * np.pi)
    s1 = np.linspace(0, 2, 400)
    _wrapped(axes[3], s1, (s1 + phi) / 2, GREEN, 2.0)
    for ax in axes[2:]:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal")
        _frame(ax)
    axes[2].set_title("dense orbit on a torus", fontsize=fs, color=RED)
    axes[3].set_title("shifted: periodic", fontsize=fs)

    fig.savefig(output_dir / "global_fragile.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 3. Global bifurcation: a saddle connection breaks
# ---------------------------------------------------------------------------

def _pendulum(eps):
    def rhs(t, q):
        return [q[1], -np.sin(q[0]) - eps * q[1]]
    return rhs


def _branch(rhs, q0, t_end, box):
    """q0 から積分し、box = (xmin, xmax, ymin, ymax) を出たら止める."""
    def leave(t, q):
        x, y = q
        return min(x - box[0], box[1] - x, y - box[2], box[3] - y)
    leave.terminal = True
    sol = solve_ivp(rhs, (0.0, t_end), q0, events=leave, max_step=0.02,
                    rtol=1e-10, atol=1e-12)
    return sol.y


def saddle_connection(output_dir: Path) -> None:
    """減衰 eps を入れた振り子: 上側の接続 W^u(q1) = W^s(q2) がずれる."""
    style.apply()

    fig, axes = plt.subplots(1, 3, figsize=style.slot(*SLOT_SADDLE_CONNECTION))
    fs = style.SMALL_FONT_PT
    pi = np.pi
    box = (-pi - 0.05, pi + 0.05, -0.2, 2.9)
    d = 1e-6

    cases = [(-0.12, r"$\varepsilon < 0$"), (0.0, r"$\varepsilon = 0$"),
             (0.12, r"$\varepsilon > 0$")]
    for ax, (eps, title) in zip(axes, cases):
        rhs = _pendulum(eps)
        # サドル (±pi, 0) の固有値: lambda^2 + eps*lambda - 1 = 0
        lu = (-eps + np.sqrt(eps**2 + 4)) / 2
        ls = (-eps - np.sqrt(eps**2 + 4)) / 2
        # W^u(q1*): (-pi, 0) から (1, lu) 方向へ、時間を進める
        wu = _branch(rhs, [-pi + d, d * lu], 60.0, box)
        # W^s(q2*): (pi, 0) から (-1, -ls) 方向へ、時間を戻す
        ws = _branch(lambda t, q: [-v for v in rhs(t, q)],
                     [pi - d, -d * ls], 60.0, box)
        if eps == 0:
            # 一致している: 第2章と同じく紫で描く
            ax.plot(wu[0], wu[1], color=PURPLE, lw=2.0, zorder=5)
            arrows = ((wu, PURPLE),)
        else:
            ax.plot(wu[0], wu[1], color=RED, lw=2.0, zorder=5)
            ax.plot(ws[0], ws[1], color=BLUE, lw=2.0, zorder=4)
            # ws は時間を戻して積分したので、配列の逆順が進む向き
            arrows = ((wu, RED), (ws[:, ::-1], BLUE))
        for br, c in arrows:
            i = int(np.argmin(np.abs(br[0] + 1.2) + 10 * (br[1] < 0.5)))
            _arrow(ax, (br[0][i], br[1][i]), (br[0][i + 15], br[1][i + 15]),
                   c, lw=1.5)
        for xs in (-pi, pi):
            ax.plot(xs, 0, "s", color=ORANGE, ms=7, zorder=7)
        ax.text(-pi, -0.25, r"$q_1^*$", color=ORANGE, fontsize=fs,
                ha="center", va="top")
        ax.text(pi, -0.25, r"$q_2^*$", color=ORANGE, fontsize=fs,
                ha="center", va="top")
        ax.set_title(title, fontsize=fs)
        ax.set_xlim(-pi - 0.5, pi + 0.5)
        ax.set_ylim(-0.75, 3.0)
        _hide_axes(ax)

    for ax, top, bottom in ((axes[0], (RED, "u", 1), (BLUE, "s", 2)),
                            (axes[2], (BLUE, "s", 2), (RED, "u", 1))):
        c, k, i = top
        ax.text(0.0, 2.45, f"$W^{k}(q_{i}^*)$", color=c, fontsize=fs,
                ha="center", va="bottom")
        c, k, i = bottom
        ax.text(0.0, 1.4, f"$W^{k}(q_{i}^*)$", color=c, fontsize=fs,
                ha="center", va="top")
    axes[1].text(0.0, 2.2, "connected", color=PURPLE, fontsize=fs,
                 ha="center", va="bottom")

    fig.savefig(output_dir / "saddle_connection.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 4. Codimension: a generic 1-parameter path meets only codim-1 sets
# ---------------------------------------------------------------------------

def codimension(output_dir: Path) -> None:
    """減衰振動子 x'' + c x' + k x = 0 の (k, c) 平面: 分岐集合と経路の当たり方.

    J = [[0, 1], [-k, -c]] なので det J = k, tr J = -c。
    k = 0（実固有値 0）は直線、c = 0 かつ k > 0（純虚数の対）は半直線で余次元1、
    原点（2つの固有値が同時に 0）は点で余次元2。
    """
    style.apply()

    fig, ax = plt.subplots(figsize=style.slot(*SLOT_CODIMENSION))
    fs = style.SMALL_FONT_PT
    kl, cl = (-1.0, 1.3), (-1.0, 1.0)
    ax.set_xlim(*kl)
    ax.set_ylim(cl[0], cl[1] + 0.12)
    _hide_axes(ax)

    # 座標軸（k: ばね定数、c: 減衰係数）
    _arrow(ax, (kl[0], cl[0]), (kl[1], cl[0]), GREY, lw=0.9)
    _arrow(ax, (kl[0], cl[0]), (kl[0], cl[1]), GREY, lw=0.9)
    ax.text(kl[1], cl[0] + 0.04, r"$k$", color=GREY, fontsize=fs,
            ha="right", va="bottom")
    ax.text(kl[0] + 0.04, cl[1], r"$c$", color=GREY, fontsize=fs,
            ha="left", va="top")

    # 領域ごとの固定点の型
    ax.text(-0.55, 0.45, "saddle", color=GREY, fontsize=fs, ha="center")
    ax.text(1.0, 0.55, "stable", color=GREY, fontsize=fs, ha="center")
    ax.text(1.0, -0.75, "unstable", color=GREY, fontsize=fs, ha="center")

    # 分岐集合: k = 0（緑）、c = 0 かつ k > 0（橙）、原点（紫）
    ax.plot([0, 0], [cl[0], cl[1]], color=GREEN, lw=2.2)
    ax.text(-0.04, 0.95, r"$\lambda = 0$", color=GREEN, fontsize=fs,
            ha="right", va="top")
    ax.plot([0, kl[1]], [0, 0], color=ORANGE, lw=2.2)
    ax.text(1.27, 0.04, r"$\lambda = \pm i\omega$", color=ORANGE,
            fontsize=fs, ha="right", va="bottom")
    ax.plot(0, 0, "o", color=PURPLE, ms=9, zorder=7)
    ax.text(-0.06, 0.06, "codim 2", color=PURPLE, fontsize=fs,
            ha="right", va="bottom")

    # 経路 A: k > 0 のまま c を下げる（フラッター型）。ずらしても橙を横切る
    for dk, alpha in ((0.0, 1.0), (0.12, 0.4)):
        _arrow(ax, (0.62 + dk, 0.8), (0.62 + dk, -0.55), FG, lw=1.5,
               alpha=alpha)
    ax.text(0.58, 0.8, "A", color=FG, fontsize=fs, ha="right", va="center")

    # 経路 B: 原点を通る。ずらすと外れる
    for dk, alpha in ((0.0, 1.0), (0.14, 0.4)):
        _arrow(ax, (-0.55 + dk, -0.75), (0.45 + dk, 0.6), FG, lw=1.5,
               alpha=alpha)
    ax.text(-0.6, -0.75, "B", color=FG, fontsize=fs, ha="right",
            va="center")
    ax.set_title("faint: slightly shifted path", fontsize=fs)

    fig.savefig(output_dir / "codimension.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 5. Saddle-node bifurcation
# ---------------------------------------------------------------------------

def saddle_node(output_dir: Path) -> None:
    """dx/dt = mu - x^2 の分岐図と、mu を止めたときの相直線."""
    style.apply()

    fig, ax = plt.subplots(figsize=style.slot(*SLOT_SADDLE_NODE))
    fs = style.SMALL_FONT_PT

    def g(x, mu):
        return mu - x**2

    mu = np.linspace(0, 1.6, 300)
    ax.plot(mu, np.sqrt(mu), **STABLE)
    ax.plot(mu, -np.sqrt(mu), **UNSTABLE)
    for m in (-0.6, 0.45):
        _phase_arrows(ax, m, g, (-1.15, 1.15), n=11)
    ax.plot(0, 0, "o", color=GREEN, ms=7, zorder=6)

    ax.text(0.75, 0.62, "stable", color=BLUE, fontsize=fs,
            ha="left", va="top")
    ax.text(0.75, -0.62, "unstable", color=RED, fontsize=fs,
            ha="left", va="bottom")
    ax.text(-0.6, 1.3, "no fixed point", color=GREY, fontsize=fs,
            ha="center", va="bottom")
    ax.set_xlim(-1.1, 1.6)
    ax.set_ylim(-1.35, 1.75)
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    _bif_axes(ax)
    ax.set_title(r"$\dot{x} = \mu - x^2$", fontsize=fs)

    fig.savefig(output_dir / "saddle_node.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 6. Transcritical and pitchfork
# ---------------------------------------------------------------------------

def tc_pitchfork(output_dir: Path) -> None:
    """トランスクリティカル・超臨界ピッチフォーク・亜臨界ピッチフォーク."""
    style.apply()

    fig, axes = plt.subplots(1, 3, figsize=style.slot(*SLOT_TC_PITCHFORK))
    fs = style.SMALL_FONT_PT
    mu = np.linspace(-1.2, 1.2, 400)
    xl = (-1.1, 1.1)

    # --- トランスクリティカル: x = 0 と x = mu が安定性を交換 ---
    ax = axes[0]
    _plot_branch(ax, mu, np.zeros_like(mu), mu < 0)
    _plot_branch(ax, mu, mu, mu > 0)
    for m in (-0.8, 0.8):
        _phase_arrows(ax, m, lambda x, u: u * x - x**2, xl, n=9)
    ax.set_title(r"$\dot{x} = \mu x - x^2$", fontsize=fs)

    # --- 超臨界ピッチフォーク ---
    ax = axes[1]
    _plot_branch(ax, mu, np.zeros_like(mu), mu < 0)
    mp = mu[mu >= 0]
    ax.plot(mp, np.sqrt(mp), **STABLE)
    ax.plot(mp, -np.sqrt(mp), **STABLE)
    for m in (-0.8, 0.8):
        _phase_arrows(ax, m, lambda x, u: u * x - x**3, xl, n=9)
    ax.set_title(r"$\dot{x} = \mu x - x^3$  (super)", fontsize=fs)

    # --- 亜臨界ピッチフォーク ---
    ax = axes[2]
    _plot_branch(ax, mu, np.zeros_like(mu), mu < 0)
    mn = mu[mu <= 0]
    ax.plot(mn, np.sqrt(-mn), **UNSTABLE)
    ax.plot(mn, -np.sqrt(-mn), **UNSTABLE)
    for m in (-0.8, 0.8):
        _phase_arrows(ax, m, lambda x, u: u * x + x**3, xl, n=9)
    ax.set_title(r"$\dot{x} = \mu x + x^3$  (sub)", fontsize=fs)

    for ax in axes:
        ax.plot(0, 0, "o", color=GREEN, ms=6, zorder=6)
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.25, 1.25)
        ax.set_xticks([-1, 0, 1])
        ax.set_yticks([-1, 0, 1])
        _bif_axes(ax)
    for ax in axes[1:]:
        ax.set_ylabel("")
        ax.set_yticklabels([])

    fig.savefig(output_dir / "tc_pitchfork.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 7. Subcritical pitchfork with quintic saturation: hysteresis
# ---------------------------------------------------------------------------

def hysteresis(output_dir: Path) -> None:
    """dx/dt = mu x + x^3 - x^5: 双安定とヒステリシス."""
    style.apply()

    fig, ax = plt.subplots(figsize=style.slot(*SLOT_HYSTERESIS))
    fs = style.SMALL_FONT_PT

    mu = np.linspace(-0.5, 0.35, 500)
    _plot_branch(ax, mu, np.zeros_like(mu), mu < 0)
    # 外側の枝 x^2 = (1 + sqrt(1+4mu))/2（安定）と内側の枝（不安定）
    m = mu[mu >= -0.25]
    xo = np.sqrt((1 + np.sqrt(1 + 4 * m)) / 2)
    mi = m[m <= 0]
    xi = np.sqrt((1 - np.sqrt(1 + 4 * mi)) / 2)
    for s in (1, -1):
        ax.plot(m, s * xo, **STABLE)
        ax.plot(mi, s * xi, **UNSTABLE)
    sn = np.sqrt(0.5)
    for s in (1, -1):
        ax.plot(-0.25, s * sn, "o", color=GREEN, ms=6, zorder=6)
    ax.plot(0, 0, "o", color=GREEN, ms=6, zorder=6)

    # 履歴: mu を増やすと 0 で跳び上がり、減らすと -1/4 で落ちる
    up = np.sqrt((1 + np.sqrt(1.0)) / 2)
    _arrow(ax, (0.0, 0.06), (0.0, up - 0.06), ORANGE, lw=1.8)
    _arrow(ax, (-0.25, sn - 0.06), (-0.25, 0.06), ORANGE, lw=1.8)
    _arrow(ax, (-0.42, -0.07), (-0.08, -0.07), ORANGE, lw=1.4)
    xo_at = lambda u: np.sqrt((1 + np.sqrt(1 + 4 * u)) / 2)  # noqa: E731
    _arrow(ax, (0.25, xo_at(0.25) + 0.13), (-0.17, xo_at(-0.17) + 0.13),
           ORANGE, lw=1.4)

    ax.axvspan(-0.25, 0.0, color=PURPLE, alpha=0.12, lw=0)
    ax.text(-0.125, -1.18, "bistable", color=PURPLE, fontsize=fs,
            ha="center", va="center")
    ax.text(-0.27, sn + 0.12, r"$-\frac{1}{4}$", color=GREEN, fontsize=fs,
            ha="right", va="bottom")

    ax.set_xlim(-0.5, 0.35)
    ax.set_ylim(-1.32, 1.35)
    ax.set_xticks([-0.5, -0.25, 0, 0.25])
    ax.set_yticks([-1, 0, 1])
    _bif_axes(ax)
    ax.set_title(r"$\dot{x} = \mu x + x^3 - x^5$", fontsize=fs)

    fig.savefig(output_dir / "hysteresis.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 8. Imperfect pitchfork
# ---------------------------------------------------------------------------

def imperfect(output_dir: Path) -> None:
    """dx/dt = h + mu x - x^3: 対称性を崩すとピッチフォークが分かれる."""
    style.apply()

    fig, axes = plt.subplots(1, 3, figsize=style.slot(*SLOT_IMPERFECT))
    fs = style.SMALL_FONT_PT

    for ax, h in zip(axes, (-0.12, 0.0, 0.12)):
        if h == 0:
            mu = np.linspace(-1.0, 1.2, 400)
            _plot_branch(ax, mu, np.zeros_like(mu), mu < 0)
            mp = mu[mu >= 0]
            ax.plot(mp, np.sqrt(mp), **STABLE)
            ax.plot(mp, -np.sqrt(mp), **STABLE)
            ax.plot(0, 0, "o", color=GREEN, ms=6, zorder=6)
        else:
            # 固定点の集合を x でパラメータ表示: mu = x^2 - h/x
            for xs in (np.linspace(-1.3, -1e-3, 2000),
                       np.linspace(1e-3, 1.3, 2000)):
                mu = xs**2 - h / xs
                keep = (mu > -1.0) & (mu < 1.2)
                _plot_branch(ax, np.where(keep, mu, np.nan), xs,
                             mu - 3 * xs**2 < 0)
            x_sn = -np.cbrt(h / 2)
            ax.plot(x_sn**2 - h / x_sn, x_sn, "o", color=GREEN, ms=6,
                    zorder=6)
        ax.set_title(f"$h = {h:g}$", fontsize=fs)
        ax.set_xlim(-1.0, 1.2)
        ax.set_ylim(-1.25, 1.25)
        ax.set_xticks([-1, 0, 1])
        ax.set_yticks([-1, 0, 1])
        _bif_axes(ax)
    for ax in axes[1:]:
        ax.set_ylabel("")
        ax.set_yticklabels([])

    fig.savefig(output_dir / "imperfect.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 9. Hopf bifurcation of the Stuart-Landau equation
# ---------------------------------------------------------------------------

def _stuart_landau(mu, ell, omega=1.0):
    def rhs(t, q):
        x, y = q
        r2 = x * x + y * y
        return [mu * x - omega * y + ell * r2 * x,
                omega * x + mu * y + ell * r2 * y]
    return rhs


def hopf(output_dir: Path) -> None:
    """超臨界ホップ: mu < 0 は渦が吸い込み、mu > 0 は周期軌道。右は振幅."""
    style.apply()

    fig, axes = plt.subplots(
        1, 3, figsize=style.slot(*SLOT_HOPF), width_ratios=[1, 1, 1.35])
    fs = style.SMALL_FONT_PT
    lim = 1.25

    for ax, mu, title in ((axes[0], -0.15, r"$\mu < 0$"),
                          (axes[1], 0.5, r"$\mu > 0$")):
        rhs = _stuart_landau(mu, -1.0)
        for q0 in ((1.15, 0.0), (0.05, 0.0)):
            if mu < 0 and q0[0] < 0.1:
                continue
            sol = solve_ivp(rhs, (0, 40), q0, max_step=0.02)
            ax.plot(sol.y[0], sol.y[1], color=GREY, lw=0.8)
        if mu > 0:
            th = np.linspace(0, 2 * np.pi, 300)
            r = np.sqrt(mu)
            ax.plot(r * np.cos(th), r * np.sin(th), color=GREEN, lw=2.2,
                    zorder=5)
            ax.plot(0, 0, "o", color=RED, ms=6, zorder=6, mfc="none",
                    mew=1.6)
        else:
            ax.plot(0, 0, "o", color=BLUE, ms=6, zorder=6)
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title, fontsize=fs)
        ax.set_xlabel(r"$\mathrm{Re}\,z$")
    axes[0].set_ylabel(r"$\mathrm{Im}\,z$")
    axes[1].text(0.0, np.sqrt(0.5) + 0.08, r"$r = \sqrt{\mu/|\ell|}$",
                 color=GREEN, fontsize=fs, ha="center", va="bottom")

    # --- 右: 振幅の分岐図（超臨界と亜臨界）---
    ax = axes[2]
    mu = np.linspace(-1.0, 1.0, 300)
    ax.plot(mu[mu < 0], 0 * mu[mu < 0], **STABLE)
    ax.plot(mu[mu >= 0], 0 * mu[mu >= 0], **UNSTABLE)
    mp = mu[mu >= 0]
    ax.plot(mp, np.sqrt(mp), color=GREEN, lw=2.0)
    mn = mu[mu <= 0]
    ax.plot(mn, np.sqrt(-mn), color=ORANGE, lw=1.8, ls="--")
    ax.text(0.92, 0.45, r"$\ell < 0$" + "\nstable", color=GREEN,
            fontsize=fs, ha="right", va="top")
    ax.text(-0.92, 0.45, r"$\ell > 0$" + "\nunstable", color=ORANGE,
            fontsize=fs, ha="left", va="top")
    ax.plot(0, 0, "o", color=FG, ms=5, zorder=6)
    ax.set_xlim(-1.0, 1.0)
    ax.set_ylim(-0.08, 1.12)
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([0, 0.5, 1])
    ax.set_xlabel(r"$\mu$")
    ax.set_ylabel(r"$r$")
    ax.set_title("amplitude of the cycle", fontsize=fs)

    fig.savefig(output_dir / "hopf.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 10. A Hopf bifurcation decided by quadratic terms alone
# ---------------------------------------------------------------------------

def _hopf_example(mu):
    """dx1 = mu x1 - x2 + x1^2, dx2 = x1 + mu x2 + x1^2（l = -1/4）."""
    def rhs(t, q):
        x1, x2 = q
        return [mu * x1 - x2 + x1**2, x1 + mu * x2 + x1**2]
    return rhs


def _settled_cycle(mu, t_settle=2500.0, t_rec=60.0):
    sol = solve_ivp(_hopf_example(mu), (0, t_settle + t_rec), [0.01, 0.0],
                    t_eval=np.linspace(t_settle, t_settle + t_rec, 4000),
                    rtol=1e-10, atol=1e-12)
    return sol.y


def hopf_example(output_dir: Path) -> None:
    """2次の項だけの例: 周期軌道と、その平均半径 vs 2 sqrt(mu)."""
    style.apply()

    fig, axes = plt.subplots(
        1, 2, figsize=style.slot(*SLOT_HOPF_EXAMPLE), width_ratios=[1, 1.35])
    fs = style.SMALL_FONT_PT

    # --- 左: いくつかの mu での周期軌道 ---
    ax = axes[0]
    colors = (BLUE, GREEN, ORANGE)
    for mu, c in zip((0.01, 0.03, 0.06), colors):
        y = _settled_cycle(mu)
        ax.plot(y[0], y[1], color=c, lw=1.8, label=f"$\\mu = {mu:g}$")
    ax.plot(0, 0, "o", color=FG, ms=4, zorder=6)
    ax.set_xlim(-0.75, 0.75)
    ax.set_ylim(-0.75, 0.75)
    ax.set_aspect("equal")
    ax.set_xticks([-0.5, 0, 0.5])
    ax.set_yticks([-0.5, 0, 0.5])
    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    # 周期軌道と重ならないよう、凡例は軸の外（右）に出す
    ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), handlelength=1.0,
              borderpad=0.1, labelspacing=0.3)

    # --- 右: 平均半径 vs 2 sqrt(mu) ---
    ax = axes[1]
    mus = np.array([0.002, 0.005, 0.01, 0.02, 0.03, 0.045, 0.06])
    rbar = [np.hypot(*_settled_cycle(m)).mean() for m in mus]
    mm = np.linspace(0, 0.065, 200)
    ax.plot(mm, 2 * np.sqrt(mm), color=GREEN, lw=1.6, ls="--")
    ax.plot(mus, rbar, "o", color=BLUE, ms=6, zorder=5)
    ax.text(0.003, 0.47, r"$\sqrt{\mu/|\ell|} = 2\sqrt{\mu}$", color=GREEN,
            fontsize=fs, ha="left", va="bottom")
    ax.text(0.034, 0.25, "mean radius\n(numerical)", color=BLUE, fontsize=fs,
            ha="left", va="top")
    ax.set_xlim(0, 0.065)
    ax.set_ylim(0, 0.56)
    ax.set_xticks([0, 0.02, 0.04, 0.06])
    ax.set_yticks([0, 0.25, 0.5])
    ax.set_xlabel(r"$\mu$")
    ax.set_ylabel(r"$\bar{r}$")

    fig.savefig(output_dir / "hopf_example.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 動機と Part 5 の例: 翼断面モデルのフラッター — 振動の振幅が流速でどう変わるか
# ---------------------------------------------------------------------------

#: ねじりばねの非線形係数 (kappa, kappa5) と図での色・説明。
#: 硬化ばねは Ch.2 と同じ kappa = +1。軟化ばねは Ch.2 の kappa = -1 に、
#: 振幅が大きいところで再び硬くなる 5次の項を足して振動が飽和するようにした
FLUTTER_SPRINGS = (
    ((+1.0, 0.0), "hardening spring"),
    ((-1.0, 2.5), "softening spring"),
)
#: 流速の範囲 U / U_F と、掃引の刻み
FLUTTER_U_RANGE = (0.9, 1.1)
FLUTTER_U_STEP = 0.01
FLUTTER_AMP_MAX = 0.95

_LCO_CACHE: dict = {}


def _lco_branch(model, kappa, kappa5):
    """周期軌道の枝（振幅 → 流速と安定性）。2つの図で使うので一度だけ計算する."""
    key = (kappa, kappa5)
    if key not in _LCO_CACHE:
        amps = np.linspace(0.01, 0.9, 90)
        _LCO_CACHE[key] = model.lco_branch(amps, kappa, kappa5)
    return _LCO_CACHE[key]


def _sweep(model, v_f, kappa, kappa5):
    """流速をゆっくり上げる・下げるときに落ち着く振幅（準静的な掃引）.

    U < U_F の釣り合い（振幅 0）は安定、U > U_F では不安定。周期軌道の枝のうち
    安定な部分を流速の関数として補間し、上げるときは U_F を超えるまで 0 に留まり、
    下げるときは安定な周期軌道がある限りそれに乗り続ける。
    """
    b = _lco_branch(model, kappa, kappa5)
    st = b["stable"]
    v_st, a_st = b["V"][st] / v_f, b["amplitude"][st]
    order = np.argsort(v_st)
    v_st, a_st = v_st[order], a_st[order]
    lo, hi = FLUTTER_U_RANGE
    u = np.round(np.arange(lo, hi + 1e-9, FLUTTER_U_STEP), 4)
    on_lco = (u >= v_st.min()) & (u <= v_st.max())
    a_lco = np.interp(u, v_st, a_st)
    up = np.where(u > 1.0, a_lco, 0.0)
    down = np.where(on_lco, a_lco, 0.0)
    return u, up, down


def motivation(output_dir: Path) -> None:
    """流速を上げ下げしたときの、落ち着いた振動の振幅（硬化ばね / 軟化ばね）."""
    style.apply()

    model = TypicalSection()
    v_f = model.flutter_speed()
    fs = style.SMALL_FONT_PT

    fig, axes = plt.subplots(1, 2, figsize=style.slot(*SLOT_MOTIVATION),
                             sharey=True)
    titles = ("hardening spring: grows continuously",
              "softening spring: jumps, with hysteresis")
    for ax, ((kappa, kappa5), _), title in zip(axes, FLUTTER_SPRINGS, titles):
        u, up, down = _sweep(model, v_f, kappa, kappa5)
        ax.axvline(1.0, color=GREY, lw=0.8, ls=":", zorder=0)
        ax.plot(u, up, "^", color=ORANGE, ms=5, zorder=4)
        ax.plot(u, down, "v", color=BLUE, ms=6, mfc="none", mew=1.1, zorder=5)
        ax.set_title(title, fontsize=fs)
        ax.set_xlim(FLUTTER_U_RANGE[0] - 0.005, FLUTTER_U_RANGE[1] + 0.005)
        ax.set_ylim(-0.05, FLUTTER_AMP_MAX)
        ax.set_xticks([0.9, 0.95, 1.0, 1.05, 1.1])
        ax.set_yticks([0, 0.4, 0.8])
        ax.set_xlabel(r"$U / U_F$")

    ax = axes[0]
    ax.set_ylabel(r"$\hat{\alpha}$")
    ax.text(0.915, 0.10, r"$U$ up ($\blacktriangle$)", color=ORANGE,
            fontsize=fs, ha="left", va="bottom")
    ax.text(0.915, 0.24, r"$U$ down ($\triangledown$)", color=BLUE,
            fontsize=fs, ha="left", va="bottom")
    ax.text(1.003, 0.80, r"$U_F$", color=GREY, fontsize=fs, ha="left")

    # 軟化ばね: U_F で跳び上がり、下げると U_F より手前で落ちる
    ax = axes[1]
    u, up, down = _sweep(model, v_f, *FLUTTER_SPRINGS[1][0])
    jump = up[np.argmax(up > 0)]
    _arrow(ax, (1.005, 0.05), (1.005, jump - 0.06), ORANGE, lw=1.6)
    i_drop = np.argmax(down > 0)
    _arrow(ax, (u[i_drop] - 0.004, down[i_drop] - 0.06), (u[i_drop] - 0.004, 0.05),
           BLUE, lw=1.6)
    ax.text(1.003, 0.80, r"$U_F$", color=GREY, fontsize=fs, ha="left")

    fig.savefig(output_dir / "ch03_motivation.png")
    plt.close(fig)


def flutter_hopf(output_dir: Path) -> None:
    """周期軌道の枝（安定 / 不安定）と、正規形 r = sqrt(-sigma / l) の予測."""
    style.apply()

    model = TypicalSection()
    v_f = model.flutter_speed()
    fs = style.SMALL_FONT_PT

    fig, axes = plt.subplots(1, 2, figsize=style.slot(*SLOT_FLUTTER_HOPF),
                             sharey=True)
    lo, hi = FLUTTER_U_RANGE
    uu = np.linspace(lo, hi, 400)
    sigma = np.array([model.growth_rate(s * v_f) for s in uu])
    for ax, ((kappa, kappa5), name) in zip(axes, FLUTTER_SPRINGS):
        # 釣り合い（振幅 0）: U < U_F で安定、U > U_F で不安定
        ax.plot([lo, 1.0], [0, 0], **STABLE)
        ax.plot([1.0, hi], [0, 0], **UNSTABLE)
        b = _lco_branch(model, kappa, kappa5)
        u_b, a_b, st = b["V"] / v_f, b["amplitude"], b["stable"]
        ax.plot(u_b, np.where(st, a_b, np.nan), **STABLE)
        # 安定と不安定の境目で線が途切れないよう、不安定側に1点重ねる
        unst = ~st | np.r_[False, ~st[:-1]]
        ax.plot(u_b, np.where(unst, a_b, np.nan), **UNSTABLE)

        nf = model.center_normal_form(v_f, kappa)
        ell = nf["re_c1"]
        r2 = -sigma / ell
        ok = r2 >= 0
        ax.plot(uu[ok], nf["alpha_per_z"] * np.sqrt(r2[ok]), color=ORANGE,
                lw=1.6, ls=":", zorder=6)
        sign = "<" if ell < 0 else ">"
        ax.set_title(rf"{name}: $\ell {sign} 0$", fontsize=fs)
        ax.set_xlim(lo - 0.005, hi + 0.005)
        ax.set_ylim(-0.05, FLUTTER_AMP_MAX)
        ax.set_xticks([0.9, 0.95, 1.0, 1.05, 1.1])
        ax.set_yticks([0, 0.4, 0.8])
        ax.set_xlabel(r"$U / U_F$")

    ax = axes[0]
    ax.set_ylabel(r"$\hat{\alpha}$")
    ax.text(1.06, 0.32, "stable LCO", color=BLUE, fontsize=fs, ha="left",
            va="top")
    ax.text(0.905, 0.52, r"normal form" "\n" r"$\hat{\alpha} \propto \sqrt{-\sigma(U)/\ell}$",
            color=ORANGE, fontsize=fs, ha="left", va="bottom")

    ax = axes[1]
    b = _lco_branch(model, *FLUTTER_SPRINGS[1][0])
    i_fold = int(np.argmin(b["V"]))
    ax.plot(b["V"][i_fold] / v_f, b["amplitude"][i_fold], "o", color=GREEN,
            ms=6, zorder=7)
    ax.text(b["V"][i_fold] / v_f - 0.004, b["amplitude"][i_fold], "fold",
            color=GREEN, fontsize=fs, ha="right", va="center")
    ax.text(1.04, 0.66, "stable LCO", color=BLUE, fontsize=fs, ha="left",
            va="top")
    ax.text(1.006, 0.13, "unstable LCO", color=RED, fontsize=fs, ha="left",
            va="bottom")

    fig.savefig(output_dir / "flutter_hopf.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def generate_all(output_dir: Path) -> None:
    """Generate all Chapter 3 figures."""
    chapter_overview(output_dir)
    motivation(output_dir)
    eigenvalue_crossing(output_dir)
    singular_jacobian(output_dir)
    perturbation_decomposition(output_dir)
    surfaces_3d(output_dir)
    saddle_connection(output_dir)
    robust_hyperbolic(output_dir)
    local_fragile(output_dir)
    global_fragile(output_dir)
    codimension(output_dir)
    saddle_node(output_dir)
    tc_pitchfork(output_dir)
    hysteresis(output_dir)
    imperfect(output_dir)
    hopf(output_dir)
    hopf_example(output_dir)
    flutter_hopf(output_dir)
    print("  Ch.3 figures generated.")
