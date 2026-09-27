"""Chapter 1 figures: Basics and Linear Stability."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

from learn_dynamical_system import style
from learn_dynamical_system.palette import (
    BLUE, FG, GREEN, GREY, ORANGE, PURPLE, RED,
)

# スライド上での表示サイズ (CSS px)。図はこの寸法ちょうどで作られるので、
# slides/01-basics.md 側の `width:` 指定をこの値と一致させること
# （ずらすと拡大縮小がかかり、フォントが本文と合わなくなる）。
SLOT_PHASE_PORTRAITS = (790, 268)
SLOT_EIGENVALUE_PLANE = (830, 262)
SLOT_PENDULUM = (790, 245)
SLOT_VECTOR_FIELD = (440, 400)
SLOT_LINEARIZATION = (820, 250)
SLOT_EIGENVALUE_EFFECT = (680, 372)
SLOT_STABILITY_CONCEPTS = (790, 236)
SLOT_CHAPTER_OVERVIEW = (820, 250)
SLOT_CONJUGACY = (560, 210)


# ---------------------------------------------------------------------------
# 1. Phase portraits for six types of 2D linear fixed points
# ---------------------------------------------------------------------------

#: 実固有値の3種類 / 複素固有値の3種類。パネルは正方形固定で大きさが
#: 「行の高さ」だけで決まるため、2 段 (118px) ではなく 1 段 (214px) に分けて
#: 2 枚のスライドに載せる。
PHASE_PORTRAIT_GROUPS = {
    "phase_portraits_real": [
        (np.array([[-2.0, 0], [0, -1.0]]),
         "Stable Node  $\\lambda = -2,\\, -1$"),
        (np.array([[2.0, 0], [0, 1.0]]),
         "Unstable Node  $\\lambda = 2,\\, 1$"),
        (np.array([[1.0, 0], [0, -1.0]]),
         "Saddle  $\\lambda = 1,\\, -1$"),
    ],
    "phase_portraits_complex": [
        (np.array([[-0.3, -2], [2, -0.3]]),
         "Stable Spiral  $\\lambda = -0.3 \\pm 2i$"),
        (np.array([[0.3, -2], [2, 0.3]]),
         "Unstable Spiral  $\\lambda = 0.3 \\pm 2i$"),
        (np.array([[0.0, -2], [2, 0.0]]),
         "Center  $\\lambda = \\pm 2i$"),
    ],
}


def phase_portraits(output_dir: Path) -> None:
    """Generate 1x3 phase-portrait strips, one per eigenvalue family."""
    style.apply()

    for name, cases in PHASE_PORTRAIT_GROUPS.items():
        fig, axes = plt.subplots(
            1, len(cases), figsize=style.slot(*SLOT_PHASE_PORTRAITS))

        for ax, (A, title) in zip(axes, cases):
            xx = np.linspace(-2.5, 2.5, 20)
            yy = np.linspace(-2.5, 2.5, 20)
            X, Y = np.meshgrid(xx, yy)
            U = A[0, 0] * X + A[0, 1] * Y
            V = A[1, 0] * X + A[1, 1] * Y
            ax.streamplot(X, Y, U, V, color=BLUE, linewidth=0.7,
                          density=1.3, arrowsize=0.9)
            ax.plot(0, 0, "o", color=RED, markersize=6, zorder=5)
            ax.set_xlim(-2.5, 2.5)
            ax.set_ylim(-2.5, 2.5)
            ax.set_aspect("equal")
            ax.set_title(title, fontsize=style.SMALL_FONT_PT)
            ax.set_xticks([-2, 0, 2])
            ax.set_yticks([-2, 0, 2])
            ax.set_xlabel(r"$q_1$")

        # 3 枚とも同じ縦軸なので、ラベルは左端だけに出す
        for ax in axes[1:]:
            ax.set_yticklabels([])
        axes[0].set_ylabel(r"$q_2$")

        fig.savefig(output_dir / f"{name}.png")
        plt.close(fig)


# ---------------------------------------------------------------------------
# 2. Eigenvalue classification diagram in the complex plane
# ---------------------------------------------------------------------------

def eigenvalue_plane(output_dir: Path) -> None:
    """Classification of 2D fixed points by the *pair* of eigenvalues of J.

    2 次元系の J は固有値を2つ持つ。図の要点は「線で結んだ1組が1つの系」で
    あることなので、各ケースをペアとして描き、条件式を添える。
    """
    style.apply()

    fig, ax = plt.subplots(figsize=style.slot(*SLOT_EIGENVALUE_PLANE))
    fs = style.SMALL_FONT_PT

    # 安定（左半平面）/ 不安定（右半平面）
    ax.axvspan(-4.8, 0, alpha=0.10, color=BLUE)
    ax.axvspan(0, 4.8, alpha=0.10, color=RED)

    # 座標軸
    ax.annotate("", xy=(4.6, 0), xytext=(-4.6, 0),
                arrowprops=dict(arrowstyle="->", color=FG, lw=0.9))
    ax.annotate("", xy=(0, 2.45), xytext=(0, -2.5),
                arrowprops=dict(arrowstyle="->", color=FG, lw=0.9))
    ax.text(4.55, -0.25, r"$\mathrm{Re}(\lambda)$", fontsize=fs,
            ha="right", va="top")
    # Center のラベルが軸の真上に来るので、Im 軸ラベルは軸から離して右下に置く
    ax.text(0.22, 1.95, r"$\mathrm{Im}(\lambda)$", fontsize=fs,
            ha="left", va="center")

    def real_pair(x0, x1, color, marker, name, cond):
        """実固有値の組: 実軸上の2点を下向きの弧で結び、下にラベルを置く."""
        ax.plot([x0, x1], [0, 0], marker, color=color, ms=7, zorder=6)
        xs = np.linspace(x0, x1, 80)
        ys = -0.34 * np.sin(np.pi * (xs - x0) / (x1 - x0))
        ax.plot(xs, ys, color=color, lw=1.0, alpha=0.8)
        mx = (x0 + x1) / 2
        ax.text(mx, -0.72, name, fontsize=fs, ha="center", va="top",
                color=color, weight="bold")
        ax.text(mx, -1.22, cond, fontsize=fs, ha="center", va="top",
                color=color, alpha=0.85)

    def conjugate_pair(x, y, color, marker, label):
        """複素固有値の組: 実軸対称の2点を破線で結び、上にラベルを置く."""
        ax.plot([x, x], [y, -y], marker, color=color, ms=7, zorder=6)
        ax.plot([x, x], [y, -y], color=color, lw=0.9, ls="--", alpha=0.6)
        ax.text(x, y + 0.3, label, fontsize=fs, ha="center", va="bottom",
                color=color, weight="bold")

    # --- 実固有値の3ケース（実軸上に乗る。ラベルは軸の下）---
    real_pair(-4.05, -3.15, BLUE, "o", "Stable Node",
              r"$\lambda_2 \leq \lambda_1 < 0$")
    real_pair(-0.6, 0.6, ORANGE, "^", "Saddle",
              r"$\lambda_2 < 0 < \lambda_1$")
    real_pair(3.15, 4.05, RED, "o", "Unstable Node",
              r"$0 < \lambda_1 \leq \lambda_2$")

    # --- 複素固有値の3ケース（必ず共役対。ラベルは軸の上）---
    conjugate_pair(-2.0, 1.35, BLUE, "D", r"Stable Spiral  ($\sigma < 0$)")
    conjugate_pair(2.0, 1.35, RED, "D", r"Unstable Spiral  ($\sigma > 0$)")
    conjugate_pair(0.0, 2.15, GREEN, "s", r"Center  ($\sigma = 0$)")

    # 半平面の意味
    ax.text(-3.6, -2.15, "Stable", fontsize=style.BASE_FONT_PT * 1.15,
            ha="center", color=BLUE, alpha=0.45, weight="bold")
    ax.text(3.6, -2.15, "Unstable", fontsize=style.BASE_FONT_PT * 1.15,
            ha="center", color=RED, alpha=0.45, weight="bold")

    ax.set_xlim(-4.8, 4.8)
    ax.set_ylim(-2.6, 3.1)
    # 模式図なので等方性は不要（掛けると横長スロットに内部余白ができる）
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

    fig.savefig(output_dir / "eigenvalue_plane.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 3. Pendulum phase portrait — a nonlinear example
# ---------------------------------------------------------------------------

def pendulum_phase_portrait(output_dir: Path) -> None:
    """Phase portrait for the simple pendulum dx/dt=y, dy/dt=-sin(x)."""
    style.apply()

    fig, ax = plt.subplots(figsize=style.slot(*SLOT_PENDULUM))
    x_grid = np.linspace(-2 * np.pi, 2 * np.pi, 500)

    # Closed orbits (libration, H < 1)
    for H in [-0.5, 0.0, 0.5, 0.8]:
        y_sq = 2 * (H + np.cos(x_grid))
        mask = y_sq > 0
        y_pos = np.where(mask, np.sqrt(np.maximum(y_sq, 0)), np.nan)
        y_neg = np.where(mask, -np.sqrt(np.maximum(y_sq, 0)), np.nan)
        ax.plot(x_grid, y_pos, color=BLUE, linewidth=0.7, alpha=0.7)
        ax.plot(x_grid, y_neg, color=BLUE, linewidth=0.7, alpha=0.7)

    # Separatrix (H = 1)
    y_sq = 2 * (1.0 + np.cos(x_grid))
    mask = y_sq >= 0
    y_pos = np.where(mask, np.sqrt(np.maximum(y_sq, 0)), np.nan)
    y_neg = np.where(mask, -np.sqrt(np.maximum(y_sq, 0)), np.nan)
    ax.plot(x_grid, y_pos, color=RED, linewidth=1.5, alpha=0.9)
    ax.plot(x_grid, y_neg, color=RED, linewidth=1.5, alpha=0.9)

    # Rotation orbits (H > 1)
    for H in [1.5, 2.5]:
        y_sq = 2 * (H + np.cos(x_grid))
        ax.plot(x_grid, np.sqrt(y_sq), color=GREY, linewidth=0.7, alpha=0.7)
        ax.plot(x_grid, -np.sqrt(y_sq), color=GREY, linewidth=0.7, alpha=0.7)

    # Fixed points
    for xc in [0, -2 * np.pi, 2 * np.pi]:
        ax.plot(xc, 0, "o", color=BLUE, markersize=6, zorder=5)
    for xs in [-np.pi, np.pi]:
        ax.plot(xs, 0, "s", color=RED, markersize=6, zorder=5)

    ax.set_xlim(-2 * np.pi, 2 * np.pi)
    ax.set_ylim(-4, 4)
    ax.set_xlabel(r"$\theta$")
    ax.set_ylabel(r"$\dot{\theta}$")
    ax.set_xticks([-2 * np.pi, -np.pi, 0, np.pi, 2 * np.pi])
    ax.set_xticklabels([r"$-2\pi$", r"$-\pi$", r"$0$", r"$\pi$", r"$2\pi$"])

    legend_elements = [
        Line2D([0], [0], color=BLUE, lw=1, label="Libration"),
        Line2D([0], [0], color=RED, lw=1.5, label="Separatrix"),
        Line2D([0], [0], color=GREY, lw=1, label="Rotation"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor=BLUE,
               markeredgecolor=BLUE, ms=6, label="Center"),
        Line2D([0], [0], marker="s", color="none", markerfacecolor=RED,
               markeredgecolor=RED, ms=6, label="Saddle"),
    ]
    # 枠色・背景色は style.apply() の rcParams（透過）に任せる
    ax.legend(handles=legend_elements, loc="upper right",
              fontsize=style.SMALL_FONT_PT, ncol=2)

    fig.savefig(output_dir / "pendulum_phase.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 4. Vector field quiver plot
# ---------------------------------------------------------------------------

def vector_field(output_dir: Path) -> None:
    """Quiver plot of a 2D vector field: dq1=q2, dq2=q1-q1^3."""
    style.apply()

    fig, ax = plt.subplots(figsize=style.slot(*SLOT_VECTOR_FIELD))
    xx = np.linspace(-2.0, 2.0, 20)
    yy = np.linspace(-2.0, 2.0, 20)
    X, Y = np.meshgrid(xx, yy)
    U = Y
    V = X - X**3
    speed = np.sqrt(U**2 + V**2)
    speed[speed == 0] = 1.0  # avoid division by zero

    ax.quiver(X, Y, U / speed, V / speed, speed,
              cmap=style.sequential_cmap(BLUE, PURPLE, RED),
              scale=25, width=0.006)
    # Mark fixed points: (0,0), (1,0), (-1,0)
    for xf in [-1.0, 0.0, 1.0]:
        ax.plot(xf, 0, "o", color=RED, markersize=7, zorder=5)
    ax.set_xlim(-2.0, 2.0)
    ax.set_ylim(-2.0, 2.0)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$q_1$")
    ax.set_ylabel(r"$q_2$")
    ax.set_xticks([-2, -1, 0, 1, 2])
    ax.set_yticks([-2, -1, 0, 1, 2])

    fig.savefig(output_dir / "vector_field.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 5. Linearization comparison: nonlinear vs linear
# ---------------------------------------------------------------------------

def linearization(output_dir: Path) -> None:
    """Side-by-side streamplots: nonlinear pendulum vs its linearization."""
    style.apply()

    fig, axes = plt.subplots(1, 2, figsize=style.slot(*SLOT_LINEARIZATION))
    # サドル点 theta = +-pi を含む範囲を取らないとセパラトリクスが現れず、
    # 「線形化が破れる場所」を図で示せない
    lim = 4.0
    xx = np.linspace(-lim, lim, 40)
    yy = np.linspace(-2.6, 2.6, 30)
    X, Y = np.meshgrid(xx, yy)

    # Left: nonlinear (pendulum)
    U_nl = Y
    V_nl = -np.sin(X)
    axes[0].streamplot(X, Y, U_nl, V_nl, color=BLUE, linewidth=0.6,
                       density=1.2, arrowsize=0.8)
    # セパラトリクス H = 1 を強調
    x_fine = np.linspace(-lim, lim, 800)
    sep = np.sqrt(np.maximum(2 * (1.0 + np.cos(x_fine)), 0))
    axes[0].plot(x_fine, sep, color=RED, lw=1.6)
    axes[0].plot(x_fine, -sep, color=RED, lw=1.6)
    axes[0].plot(0, 0, "o", color=RED, markersize=6, zorder=5)
    # サドル点
    for xs in (-np.pi, np.pi):
        axes[0].plot(xs, 0, "s", color=ORANGE, markersize=7, zorder=6)
    axes[0].set_title("Nonlinear: $\\dot{\\omega} = -\\sin\\theta$")

    # Right: linearized
    U_l = Y
    V_l = -X
    axes[1].streamplot(X, Y, U_l, V_l, color=ORANGE, linewidth=0.6,
                       density=1.2, arrowsize=0.8)
    axes[1].plot(0, 0, "o", color=RED, markersize=6, zorder=5)
    axes[1].set_title("Linearized: $\\dot{\\omega} = -\\theta$")

    for ax in axes:
        ax.set_xlabel(r"$\theta$")
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-2.6, 2.6)
        ax.set_aspect("equal")
        ax.set_xticks([-np.pi, 0, np.pi])
        ax.set_xticklabels([r"$-\pi$", r"$0$", r"$\pi$"])
    axes[0].set_ylabel(r"$\omega$")
    axes[1].set_yticklabels([])

    fig.savefig(output_dir / "linearization.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 6. Eigenvalue effect: real/imaginary parts on time evolution
# ---------------------------------------------------------------------------

def eigenvalue_effect(output_dir: Path) -> None:
    """2x2 panel showing how sigma and omega affect time evolution."""
    style.apply()

    t = np.linspace(0, 6, 300)
    cases = [
        (-0.5, 0.0, r"$\sigma < 0,\; \omega = 0$" + "\nExponential decay"),
        (0.3, 0.0, r"$\sigma > 0,\; \omega = 0$" + "\nExponential growth"),
        (-0.5, 5.0, r"$\sigma < 0,\; \omega \neq 0$" + "\nDamped oscillation"),
        (0.0, 5.0, r"$\sigma = 0,\; \omega \neq 0$" + "\nPure oscillation"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=style.slot(*SLOT_EIGENVALUE_EFFECT))
    for ax, (sigma, omega, label) in zip(axes.flat, cases):
        y = np.exp(sigma * t) * np.cos(omega * t)
        ax.plot(t, y, color=BLUE, linewidth=1.2)
        # Envelope
        envelope = np.exp(sigma * t)
        if sigma != 0:
            ax.plot(t, envelope, "--", color=RED, linewidth=0.8, alpha=0.7)
            ax.plot(t, -envelope, "--", color=RED, linewidth=0.8, alpha=0.7)
        ax.axhline(0, color=GREY, linewidth=0.5, alpha=0.5)
        ax.set_title(label, fontsize=style.SMALL_FONT_PT)
        ax.set_xlim(0, 6)

    for ax in axes[-1, :]:
        ax.set_xlabel(r"$t$")
    for ax in axes[:, 0]:
        ax.set_ylabel(r"$e^{\lambda t}$")

    fig.savefig(output_dir / "eigenvalue_effect.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 7. Lyapunov / asymptotic stability / instability — the epsilon-delta picture
# ---------------------------------------------------------------------------

def stability_concepts(output_dir: Path) -> None:
    """Three panels contrasting Lyapunov stable, asymptotically stable, unstable."""
    style.apply()

    eps, delta = 1.0, 0.45

    fig, axes = plt.subplots(1, 3, figsize=style.slot(*SLOT_STABILITY_CONCEPTS))
    titles = ["Stable (Lyapunov)", "Asymptotically stable", "Unstable"]
    # sigma = 0 で閉軌道、sigma < 0 で収束、sigma > 0 で発散。
    # t_max はパネルごとに切る（伸ばしすぎると軌道が枠外にはみ出す）
    sigmas = [0.0, -0.16, 0.13]
    t_maxes = [3.4, 14.0, 9.7]

    for ax, title, sigma, t_max in zip(axes, titles, sigmas, t_maxes):
        t = np.linspace(0, t_max, 1200)
        # epsilon / delta の同心円
        theta = np.linspace(0, 2 * np.pi, 200)
        ax.plot(eps * np.cos(theta), eps * np.sin(theta),
                color=GREY, lw=1.0, ls="--")
        ax.plot(delta * np.cos(theta), delta * np.sin(theta),
                color=GREY, lw=1.0, ls=":")
        ax.text(0, eps + 0.09, r"$\varepsilon$", color=GREY,
                ha="center", va="bottom", fontsize=style.SMALL_FONT_PT)
        ax.text(delta * 0.72, delta * 0.72, r"$\delta$", color=GREY,
                ha="left", va="bottom", fontsize=style.SMALL_FONT_PT)

        # delta 円内から出発する軌道
        r = delta * 0.8 * np.exp(sigma * t)
        ax.plot(r * np.cos(2.0 * t), r * np.sin(2.0 * t),
                color=BLUE, lw=1.1)
        ax.plot(delta * 0.8, 0, "o", color=BLUE, ms=5, zorder=5)
        ax.plot(0, 0, "o", color=RED, ms=7, zorder=6)

        ax.set_title(title, fontsize=style.SMALL_FONT_PT)
        ax.set_xlim(-1.45, 1.45)
        ax.set_ylim(-1.45, 1.45)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

    fig.savefig(output_dir / "stability_concepts.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 8. Concept diagrams (schematics, not data plots)
# ---------------------------------------------------------------------------

def _hide_axes(ax) -> None:
    """概念図用: 軸・目盛・枠をすべて消す."""
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


def chapter_overview(output_dir: Path) -> None:
    """本章の筋道を1枚にした概念図: 非線形の流れ → 線形化 → 固有値."""
    style.apply()

    fig, ax = plt.subplots(figsize=style.slot(*SLOT_CHAPTER_OVERVIEW))
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 10)
    _hide_axes(ax)
    fs = style.SMALL_FONT_PT

    # --- ① 非線形の流れ場: 固定点へ巻き込む螺旋 ---
    cx, cy = 5.0, 5.8
    for phase in np.linspace(0, 2 * np.pi, 5, endpoint=False):
        th = np.linspace(0, 3.2 * np.pi, 300)
        r = 3.1 * np.exp(-0.18 * th)
        ax.plot(cx + r * np.cos(th + phase), cy + r * np.sin(th + phase) * 0.85,
                color=BLUE, lw=1.0, alpha=0.9)
    ax.plot(cx, cy, "o", color=RED, ms=8, zorder=5)
    ax.text(cx, 1.6, "Nonlinear flow", ha="center", fontsize=fs, color=FG)
    ax.text(cx, 0.4, r"$\dot{q} = f(q)$", ha="center", fontsize=fs, color=GREY)

    # --- ② 線形化: 原点へ向かう直線的な場 ---
    lx, ly = 15.0, 5.8
    for ang in np.linspace(0, 2 * np.pi, 12, endpoint=False):
        dx, dy = np.cos(ang), np.sin(ang) * 0.85
        ax.annotate("", xy=(lx + 0.9 * dx, ly + 0.9 * dy),
                    xytext=(lx + 3.1 * dx, ly + 3.1 * dy),
                    arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.0))
    ax.plot(lx, ly, "o", color=RED, ms=8, zorder=5)
    ax.text(lx, 1.6, "Linearization", ha="center", fontsize=fs, color=FG)
    ax.text(lx, 0.4, r"$\dot{\xi} = J\xi$", ha="center", fontsize=fs, color=GREY)

    # --- ③ 複素平面上の固有値 ---
    ex, ey = 25.5, 5.8
    ax.axvspan(ex - 3.4, ex, ymin=0.27, ymax=0.93, alpha=0.12, color=BLUE)
    ax.axvspan(ex, ex + 3.4, ymin=0.27, ymax=0.93, alpha=0.12, color=RED)
    ax.annotate("", xy=(ex + 3.4, ey), xytext=(ex - 3.4, ey),
                arrowprops=dict(arrowstyle="->", color=FG, lw=0.8))
    ax.annotate("", xy=(ex, ey + 3.1), xytext=(ex, ey - 3.1),
                arrowprops=dict(arrowstyle="->", color=FG, lw=0.8))
    ax.plot([ex - 1.7, ex - 1.7], [ey + 1.5, ey - 1.5], "D", color=BLUE, ms=6)
    ax.plot(ex + 1.9, ey, "o", color=RED, ms=7)
    ax.text(ex, 1.6, "Eigenvalues of $J$", ha="center", fontsize=fs, color=FG)
    ax.text(ex, 0.4, r"$\lambda = \sigma + i\omega$", ha="center",
            fontsize=fs, color=GREY)

    # --- ステージ間の矢印 ---
    for x0, x1 in ((8.8, 11.2), (18.8, 21.2)):
        ax.annotate("", xy=(x1, ey), xytext=(x0, ey),
                    arrowprops=dict(arrowstyle="-|>", color=FG, lw=1.4))

    fig.savefig(output_dir / "chapter_overview.png")
    plt.close(fig)


def topological_conjugacy(output_dir: Path) -> None:
    """Hartman-Grobman の可換図式 h . phi_t = e^{Jt} . h."""
    style.apply()

    fig, ax = plt.subplots(figsize=style.slot(*SLOT_CONJUGACY))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    _hide_axes(ax)
    fs = style.SMALL_FONT_PT

    nodes = {
        "tl": (2.6, 7.4, r"$q$"),
        "tr": (7.4, 7.4, r"$\phi_t(q)$"),
        "bl": (2.6, 2.6, r"$h(q)$"),
        "br": (7.4, 2.6, r"$e^{Jt}h(q)$"),
    }
    for x, y, label in nodes.values():
        ax.text(x, y, label, ha="center", va="center",
                fontsize=style.BASE_FONT_PT, color=FG)

    def arrow(p0, p1, label, color, offset, ha="center", va="center"):
        ax.annotate("", xy=p1, xytext=p0,
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=1.2))
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        ax.text(mx + offset[0], my + offset[1], label, color=color,
                fontsize=fs, ha=ha, va=va)

    # 上段: 非線形のフロー / 下段: 線形のフロー
    arrow((3.7, 7.4), (6.0, 7.4), r"$\phi_t$", BLUE, (0, 0.55))
    arrow((3.7, 2.6), (5.9, 2.6), r"$e^{Jt}$", ORANGE, (0, -0.75))
    # 縦: 同相写像 h
    arrow((2.6, 6.7), (2.6, 3.4), r"$h$", GREEN, (-0.5, 0), ha="right")
    arrow((7.4, 6.7), (7.4, 3.4), r"$h$", GREEN, (0.5, 0), ha="left")

    ax.text(0.2, 7.4, "Nonlinear", color=BLUE, fontsize=fs,
            ha="left", va="center", weight="bold")
    ax.text(0.2, 2.6, "Linear", color=ORANGE, fontsize=fs,
            ha="left", va="center", weight="bold")
    ax.text(5.0, 0.5, "the square commutes", color=GREY,
            fontsize=fs, ha="center", va="center")

    fig.savefig(output_dir / "topological_conjugacy.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def generate_all(output_dir: Path) -> None:
    """Generate all Chapter 1 figures."""
    phase_portraits(output_dir)
    eigenvalue_plane(output_dir)
    pendulum_phase_portrait(output_dir)
    vector_field(output_dir)
    linearization(output_dir)
    eigenvalue_effect(output_dir)
    stability_concepts(output_dir)
    chapter_overview(output_dir)
    topological_conjugacy(output_dir)
    print("  Ch.1 figures generated.")
