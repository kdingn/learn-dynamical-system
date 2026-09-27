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
SLOT_PHASE_PORTRAITS = (868, 340)
SLOT_EIGENVALUE_PLANE = (830, 392)
SLOT_PENDULUM = (770, 300)
SLOT_VECTOR_FIELD = (440, 400)
SLOT_LINEARIZATION = (770, 300)
SLOT_EIGENVALUE_EFFECT = (680, 372)


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
    """Classification of 2D fixed points by eigenvalue location."""
    style.apply()

    fig, ax = plt.subplots(figsize=style.slot(*SLOT_EIGENVALUE_PLANE))

    # Background shading: stable (left) / unstable (right)
    # xlim いっぱいまで塗る（半平面を表すので途中で切れていると意図が伝わらない）
    ax.axvspan(-3.9, 0, alpha=0.12, color=BLUE)
    ax.axvspan(0, 3.9, alpha=0.12, color=RED)

    # Coordinate arrows
    ax.annotate("", xy=(3.3, 0), xytext=(-3.3, 0),
                arrowprops=dict(arrowstyle="->", color=FG, lw=0.8))
    ax.annotate("", xy=(0, 3.3), xytext=(0, -3.3),
                arrowprops=dict(arrowstyle="->", color=FG, lw=0.8))
    ax.axvline(0, color=FG, linewidth=0.8, linestyle="--", alpha=0.3)

    ax.text(3.4, -0.25, r"$\mathrm{Re}(\lambda)$")
    ax.text(0.15, 3.15, r"$\mathrm{Im}(\lambda)$")

    fs = style.SMALL_FONT_PT

    # --- Stable node ---
    ax.plot([-2.5, -1.2], [0, 0], "o", color=BLUE, ms=6, zorder=5)
    ax.text(-1.85, 0.4, "Stable Node", fontsize=fs, ha="center",
            color=BLUE, weight="bold")

    # --- Unstable node ---
    ax.plot([1.2, 2.5], [0, 0], "o", color=RED, ms=6, zorder=5)
    ax.text(1.85, 0.4, "Unstable Node", fontsize=fs, ha="center",
            color=RED, weight="bold")

    # --- Stable spiral ---
    ax.plot(-1.2, 1.8, "D", color=BLUE, ms=5, zorder=5)
    ax.plot(-1.2, -1.8, "D", color=BLUE, ms=5, zorder=5)
    ax.text(-2.3, 2.2, "Stable\nSpiral", fontsize=fs, ha="center",
            color=BLUE, weight="bold")

    # --- Unstable spiral ---
    ax.plot(1.2, 1.8, "D", color=RED, ms=5, zorder=5)
    ax.plot(1.2, -1.8, "D", color=RED, ms=5, zorder=5)
    ax.text(2.3, 2.2, "Unstable\nSpiral", fontsize=fs, ha="center",
            color=RED, weight="bold")

    # --- Center ---
    ax.plot(0, 2.5, "s", color=GREEN, ms=5, zorder=5)
    ax.plot(0, -2.5, "s", color=GREEN, ms=5, zorder=5)
    # 虚軸上の点なので、ラベルは軸の左に寄せて "Unstable Spiral" から離す
    ax.text(-0.3, 2.5, "Center", fontsize=fs, ha="right", va="center",
            color=GREEN, weight="bold")

    # --- Saddle ---
    ax.plot(-2.0, 0, "^", color=ORANGE, ms=7, zorder=6)
    ax.plot(2.0, 0, "^", color=ORANGE, ms=7, zorder=6)
    ax.annotate("Saddle", xy=(2.0, 0), xytext=(2.5, -1.0),
                fontsize=fs, ha="center", color=ORANGE, weight="bold",
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=0.8))
    ax.annotate("", xy=(-2.0, 0), xytext=(-1.5, -1.0),
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=0.8))
    # 虚軸に重ならないよう "Saddle" の真下に置く
    ax.text(2.5, -1.7, r"$\lambda_1 > 0 > \lambda_2$",
            fontsize=fs, ha="center", color=ORANGE)

    # Watermark-style stability labels
    ax.text(-2.8, -2.8, "Stable", fontsize=style.BASE_FONT_PT * 1.2, ha="center",
            color=BLUE, alpha=0.45, weight="bold")
    ax.text(2.8, -2.8, "Unstable", fontsize=style.BASE_FONT_PT * 1.2, ha="center",
            color=RED, alpha=0.45, weight="bold")

    ax.set_xlim(-3.9, 3.9)
    ax.set_ylim(-3.3, 3.5)
    # ラベル付きの模式図であり、等方性に依存した主張はしていない。
    # set_aspect("equal") を掛けると正方形の軸が強制され、横長のスロットの
    # 左右に大きな内部余白ができてしまうので掛けない。
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
    xx = np.linspace(-2, 2, 25)
    yy = np.linspace(-2, 2, 25)
    X, Y = np.meshgrid(xx, yy)

    # Left: nonlinear (pendulum)
    U_nl = Y
    V_nl = -np.sin(X)
    axes[0].streamplot(X, Y, U_nl, V_nl, color=BLUE, linewidth=0.6,
                       density=1.3, arrowsize=0.8)
    axes[0].plot(0, 0, "o", color=RED, markersize=6, zorder=5)
    axes[0].set_title("Nonlinear: $\\dot{\\omega} = -\\sin\\theta$", fontsize=11)
    axes[0].set_xlabel(r"$\theta$")
    axes[0].set_ylabel(r"$\omega$")
    axes[0].set_xlim(-2, 2)
    axes[0].set_ylim(-2, 2)
    axes[0].set_aspect("equal")

    # Right: linearized
    U_l = Y
    V_l = -X
    axes[1].streamplot(X, Y, U_l, V_l, color=ORANGE, linewidth=0.6,
                       density=1.3, arrowsize=0.8)
    axes[1].plot(0, 0, "o", color=RED, markersize=6, zorder=5)
    axes[1].set_title("Linearized: $\\dot{\\omega} = -\\theta$", fontsize=11)
    axes[1].set_xlabel(r"$\theta$")
    axes[1].set_ylabel(r"$\omega$")
    axes[1].set_xlim(-2, 2)
    axes[1].set_ylim(-2, 2)
    axes[1].set_aspect("equal")

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
    print("  Ch.1 figures generated.")
