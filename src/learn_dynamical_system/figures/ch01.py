"""Chapter 1 figures: Basics and Linear Stability."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

from learn_dynamical_system import style
from learn_dynamical_system.models.typical_section import TypicalSection
from learn_dynamical_system.palette import (
    BG, BLUE, FG, GREEN, GREY, ORANGE, PURPLE, RED,
)

# スライド上での表示サイズ (CSS px)。図はこの寸法ちょうどで作られるので、
# slides/01-basics.md 側の `width:` 指定をこの値と一致させること
# （ずらすと拡大縮小がかかり、フォントが本文と合わなくなる）。
SLOT_CHAPTER_OVERVIEW = (820, 250)
SLOT_MOTIVATION = (820, 215)
SLOT_TYPICAL_SECTION = (360, 180)
SLOT_VECTOR_FIELD = (380, 350)
SLOT_NO_CROSSING = (380, 230)
SLOT_STABILITY_CONCEPTS = (790, 236)
SLOT_ONE_DIM = (400, 250)
SLOT_EIGENVALUE_EFFECT = (860, 340)
SLOT_FLUTTER_EIGENVALUES = (820, 250)
SLOT_EIGENVALUE_PLANE = (830, 262)
SLOT_PHASE_PORTRAITS = (680, 250)
SLOT_AIRCRAFT_MODES = (840, 220)
SLOT_PENDULUM = (790, 245)
SLOT_LINEARIZATION = (820, 250)
SLOT_CONJUGACY = (560, 210)
SLOT_CENTER_AMBIGUITY = (560, 225)

#: 動機とフラッターの固有値の図で使う流速（フラッター速度 V_F に対する比）
FLUTTER_SPEEDS = (0.8, 1.1)


def _hide_axes(ax) -> None:
    """概念図用: 軸・目盛・枠をすべて消す."""
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


# ---------------------------------------------------------------------------
# 表紙: 本章の筋道を1枚にした概念図
# ---------------------------------------------------------------------------

def chapter_overview(output_dir: Path) -> None:
    """非線形の流れ → 線形化 → 固有値."""
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
    ax.text(cx, 0.4, r"$\dot{\boldsymbol{q}} = \boldsymbol{f}(\boldsymbol{q})$", ha="center",
            fontsize=fs, color=GREY)

    # --- ② 線形化: 原点へ向かう直線的な場 ---
    lx, ly = 15.0, 5.8
    for ang in np.linspace(0, 2 * np.pi, 12, endpoint=False):
        dx, dy = np.cos(ang), np.sin(ang) * 0.85
        ax.annotate("", xy=(lx + 0.9 * dx, ly + 0.9 * dy),
                    xytext=(lx + 3.1 * dx, ly + 3.1 * dy),
                    arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.0))
    ax.plot(lx, ly, "o", color=RED, ms=8, zorder=5)
    ax.text(lx, 1.6, "Linearization", ha="center", fontsize=fs, color=FG)
    ax.text(lx, 0.4, r"$\dot{\boldsymbol{\xi}} = J\boldsymbol{\xi}$", ha="center",
            fontsize=fs, color=GREY)

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

    for x0, x1 in ((8.8, 11.2), (18.8, 21.2)):
        ax.annotate("", xy=(x1, ey), xytext=(x0, ey),
                    arrowprops=dict(arrowstyle="-|>", color=FG, lw=1.4))

    fig.savefig(output_dir / "ch01_overview.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 動機: フラッターと円柱後流 — 乱れが消えるか育つか
# ---------------------------------------------------------------------------

def _wake_lift(growth: float, t: np.ndarray, a0: float = 0.02) -> np.ndarray:
    """円柱後流の揚力の振幅方程式 dA/dt = (s + i)A - (1 + i)|A|^2 A の Re(A).

    臨界レイノルズ数の近くで後流の振幅が従う式（Ch.3 で導く Stuart-Landau 方程式）。
    s < 0 なら乱れは減衰し、s > 0 なら成長してから一定の振幅に落ち着く。
    """
    def rhs(_, y):
        A = y[0] + 1j * y[1]
        dA = (growth + 1j) * A - (1 + 1j) * abs(A) ** 2 * A
        return [dA.real, dA.imag]

    sol = solve_ivp(rhs, (t[0], t[-1]), [a0, 0.0], t_eval=t,
                    rtol=1e-8, atol=1e-10)
    return sol.y[0]


def motivation(output_dir: Path) -> None:
    """2x2: 行 = 現象（フラッター / 円柱後流）、列 = パラメータが臨界値の手前 / 先."""
    style.apply()

    model = TypicalSection()
    v_f = model.flutter_speed()
    t = np.linspace(0, 150, 3000)

    fig, axes = plt.subplots(2, 2, figsize=style.slot(*SLOT_MOTIVATION),
                             sharex=True)
    lo, hi = FLUTTER_SPEEDS

    # 上段: 突風でねじれ角 alpha を乱したあとの応答
    for ax, ratio, color, label in (
        (axes[0, 0], lo, BLUE, rf"Flutter, $U = {lo}\,U_F$: decays"),
        (axes[0, 1], hi, RED, rf"Flutter, $U = {hi}\,U_F$: grows"),
    ):
        q = model.response(ratio * v_f, [0.0, 1.0, 0.0, 0.0], t)
        ax.plot(t, q[:, 1], color=color, lw=0.8)
        ax.set_title(label, fontsize=style.SMALL_FONT_PT)

    # 下段: 後流の揚力（臨界レイノルズ数 Re_c の手前 / 先）
    for ax, growth, color, label in (
        (axes[1, 0], -0.03, BLUE, r"Cylinder wake, $Re < Re_c$: decays"),
        (axes[1, 1], 0.03, RED, r"Cylinder wake, $Re > Re_c$: grows"),
    ):
        ax.plot(t, _wake_lift(growth, t), color=color, lw=0.8)
        ax.set_title(label, fontsize=style.SMALL_FONT_PT)

    # 振幅の絶対値には意味がない（乱れの大きさで変わる）ので目盛は出さず、
    # 同じ行の2枚で縦軸を揃えて「減衰 / 成長」を比べられるようにする
    for row, ylabel in zip(axes, (r"$\alpha$", r"$C_L$")):
        ymax = max(abs(np.array(ax.get_ylim())).max() for ax in row)
        for ax in row:
            ax.set_ylim(-ymax, ymax)
            ax.set_yticks([])
            ax.axhline(0, color=GREY, lw=0.5, alpha=0.5)
        row[0].set_ylabel(ylabel)
    for ax in axes[1]:
        ax.set_xlabel(r"$t$")
        ax.set_xticks([])
    ax.set_xlim(t[0], t[-1])

    fig.savefig(output_dir / "ch01_motivation.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Part 1: 翼断面モデルの模式図 — 状態 (h, alpha, h', alpha') が何を指すか
# ---------------------------------------------------------------------------

def typical_section_schematic(output_dir: Path) -> None:
    """ばねで支えた翼断面: 上下の変位 h とねじれ角 alpha、流速 U."""
    style.apply()

    fig, ax = plt.subplots(figsize=style.slot(*SLOT_TYPICAL_SECTION))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 10)
    _hide_axes(ax)
    fs = style.SMALL_FONT_PT

    # NACA 0012 の外形を、弾性軸 (ex, ey) まわりに alpha だけ機首上げに回す
    c, x0, ex, ey, alpha = 9.0, 5.0, 8.6, 5.6, np.deg2rad(10)
    s = np.linspace(0, 1, 120)
    t = 0.6 * (0.2969 * np.sqrt(s) - 0.126 * s - 0.3516 * s**2
               + 0.2843 * s**3 - 0.1015 * s**4)
    xs = np.concatenate([s, s[::-1]]) * c + x0
    ys = np.concatenate([t, -t[::-1]]) * c + ey
    rot = np.array([[np.cos(alpha), -np.sin(alpha)],
                    [np.sin(alpha), np.cos(alpha)]])
    # 機首上げ = 前縁（左）が上がる向き
    pts = rot.T @ np.vstack([xs - ex, ys - ey])
    ax.fill(pts[0] + ex, pts[1] + ey, color=BLUE, alpha=0.35, lw=0)
    ax.plot(pts[0] + ex, pts[1] + ey, color=BLUE, lw=1.2)

    # 釣り合いの位置（翼弦線）
    ax.plot([x0 - 0.3, x0 + c + 0.3], [ey, ey], color=GREY, lw=0.9, ls="--")

    # 上下のばね k_h（地面から弾性軸まで）
    zz_y = np.linspace(1.0, ey - 0.4, 12)
    zz_x = ex + np.where(np.arange(12) % 2 == 0, -0.35, 0.35)
    zz_x[0] = zz_x[-1] = ex
    ax.plot(zz_x, zz_y, color=FG, lw=1.0)
    ax.plot([ex - 1.0, ex + 1.0], [1.0, 1.0], color=FG, lw=1.2)
    for hx in np.linspace(ex - 0.9, ex + 0.9, 6):
        ax.plot([hx, hx - 0.3], [1.0, 0.6], color=FG, lw=0.8)
    ax.text(ex + 0.6, 2.6, r"$k_h$", color=FG, fontsize=fs, ha="left")
    ax.plot(ex, ey, "o", color=FG, ms=4, zorder=5)

    # 状態の成分: h（上下）と alpha（ねじれ）
    ax.annotate("", xy=(16.0, ey - 1.6), xytext=(16.0, ey + 1.6),
                arrowprops=dict(arrowstyle="<|-|>", color=ORANGE, lw=1.3))
    ax.text(16.4, ey, r"$h$", color=ORANGE, fontsize=style.BASE_FONT_PT,
            va="center")
    th = np.linspace(np.pi * 0.62, np.pi * 0.95, 40)
    ax.plot(ex + 3.2 * np.cos(th), ey + 3.2 * np.sin(th), color=GREEN, lw=1.3)
    ax.annotate("", xy=(ex + 3.2 * np.cos(th[0]), ey + 3.2 * np.sin(th[0])),
                xytext=(ex + 3.2 * np.cos(th[3]), ey + 3.2 * np.sin(th[3])),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.3))
    ax.text(ex - 2.6, ey + 3.0, r"$\alpha$", color=GREEN,
            fontsize=style.BASE_FONT_PT, ha="center")

    # 流れ
    for yy in (ey - 1.2, ey + 1.2):
        ax.annotate("", xy=(3.6, yy), xytext=(0.6, yy),
                    arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.1))
    ax.text(2.1, ey, r"$U$", color=GREY, fontsize=style.BASE_FONT_PT,
            ha="center", va="center")

    fig.savefig(output_dir / "typical_section.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Part 1: ベクトル場
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
# Part 1: 解の一意性 — 軌道が交わると、交点から出る解が2本になる
# ---------------------------------------------------------------------------

def orbits_cannot_cross(output_dir: Path) -> None:
    """交わる2本の軌道（ありえない）の概念図."""
    style.apply()

    fig, ax = plt.subplots(figsize=style.slot(*SLOT_NO_CROSSING))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    _hide_axes(ax)
    fs = style.SMALL_FONT_PT

    x = np.linspace(0.6, 9.4, 200)
    s = (x - 5.0) / 4.4
    for sign, color in ((1, BLUE), (-1, ORANGE)):
        y = 3.7 + sign * 1.5 * np.tanh(1.6 * s)
        ax.plot(x, y, color=color, lw=1.6)
        # 時間の向き（交点の手前と先に1つずつ）
        for i in (45, 160):
            ax.annotate("", xy=(x[i + 3], y[i + 3]), xytext=(x[i], y[i]),
                        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6))

    ax.plot(5.0, 3.7, "o", color=RED, ms=9, zorder=5)
    ax.text(5.0, 4.15, r"$\boldsymbol{p}$", color=RED, ha="center", va="bottom",
            fontsize=style.BASE_FONT_PT)
    ax.text(5.0, 0.1, r"two solutions would start from $\boldsymbol{p}$"
            "\n" r"$\Rightarrow$ impossible", color=RED, ha="center", va="bottom",
            fontsize=fs)

    fig.savefig(output_dir / "orbits_cannot_cross.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Part 2: 安定 / 漸近安定 / 不安定 — epsilon-delta の絵
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
        theta = np.linspace(0, 2 * np.pi, 200)
        ax.plot(eps * np.cos(theta), eps * np.sin(theta),
                color=GREY, lw=1.0, ls="--")
        ax.plot(delta * np.cos(theta), delta * np.sin(theta),
                color=GREY, lw=1.0, ls=":")
        ax.text(0, eps + 0.09, r"$\varepsilon$", color=GREY,
                ha="center", va="bottom", fontsize=style.SMALL_FONT_PT)
        ax.text(delta * 0.72, delta * 0.72, r"$\delta$", color=GREY,
                ha="left", va="bottom", fontsize=style.SMALL_FONT_PT)

        r = delta * 0.8 * np.exp(sigma * t)
        ax.plot(r * np.cos(2.0 * t), r * np.sin(2.0 * t),
                color=BLUE, lw=1.1)
        ax.plot(delta * 0.8, 0, "o", color=BLUE, ms=5, zorder=5)
        ax.plot(0, 0, "o", color=RED, ms=7, zorder=6)

        ax.set_title(title, fontsize=style.SMALL_FONT_PT)
        ax.set_xlim(-1.45, 1.45)
        ax.set_ylim(-1.45, 1.45)
        ax.set_aspect("equal")
        _hide_axes(ax)

    fig.savefig(output_dir / "stability_concepts.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Part 3: 1次元の線形化 — 傾きの符号で決まる
# ---------------------------------------------------------------------------

def one_dim_linearization(output_dir: Path) -> None:
    """f(q) = q - q^3 のグラフ、固定点での接線、q 軸上の流れの向き."""
    style.apply()

    fig, ax = plt.subplots(figsize=style.slot(*SLOT_ONE_DIM))
    q = np.linspace(-1.55, 1.55, 400)
    ax.plot(q, q - q**3, color=FG, lw=1.3)
    ax.axhline(0, color=GREY, lw=0.8)

    # 固定点ごとの接線（傾き = lambda）
    for qs, lam, color in ((-1.0, -2.0, BLUE), (0.0, 1.0, RED), (1.0, -2.0, BLUE)):
        dq = np.linspace(-0.32, 0.32, 2)
        ax.plot(qs + dq, lam * dq, color=color, lw=2.0, alpha=0.75)
        ax.plot(qs, 0, "o", color=color, ms=7, zorder=5)
    ax.text(-1.0, 0.82, r"$\lambda = -2$", color=BLUE, ha="center",
            fontsize=style.SMALL_FONT_PT)
    ax.text(1.0, -1.0, r"$\lambda = -2$", color=BLUE, ha="center",
            fontsize=style.SMALL_FONT_PT)
    ax.text(0.12, 0.62, r"$\lambda = 1$", color=RED, ha="left",
            fontsize=style.SMALL_FONT_PT)

    # q 軸上の流れの向き（f > 0 なら右、f < 0 なら左）
    for x0, sgn in ((-1.45, 1), (-0.55, -1), (0.55, 1), (1.45, -1)):
        ax.annotate("", xy=(x0 + 0.22 * sgn, 0), xytext=(x0 - 0.0 * sgn, 0),
                    arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.6))

    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.25, 1.25)
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax.set_xlabel(r"$q$")
    ax.set_ylabel(r"$f(q)$")

    fig.savefig(output_dir / "one_dim_linearization.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Part 3: 固有値の実部・虚部と時間発展
# ---------------------------------------------------------------------------

def eigenvalue_effect(output_dir: Path) -> None:
    """2x2 panel showing how sigma and omega affect time evolution."""
    style.apply()

    t = np.linspace(0, 6, 300)
    cases = [
        (-0.5, 0.0, r"$\sigma < 0,\; \omega = 0$: decay"),
        (0.3, 0.0, r"$\sigma > 0,\; \omega = 0$: growth"),
        (-0.5, 5.0, r"$\sigma < 0,\; \omega \neq 0$: damped oscillation"),
        (0.0, 5.0, r"$\sigma = 0,\; \omega \neq 0$: pure oscillation"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=style.slot(*SLOT_EIGENVALUE_EFFECT),
                             sharex=True)
    for ax, (sigma, omega, label) in zip(axes.flat, cases):
        y = np.exp(sigma * t) * np.cos(omega * t)
        ax.plot(t, y, color=BLUE, linewidth=1.2)
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
        ax.set_ylabel(r"$\mathrm{Re}\,e^{\lambda t}$")

    fig.savefig(output_dir / "eigenvalue_effect.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Part 3: 動機への回答 — フラッターの固有値が虚軸を横切る
# ---------------------------------------------------------------------------

def flutter_eigenvalues(output_dir: Path) -> None:
    """左: 流速を上げたときの固有値の軌跡 / 右: 最大の実部と流速."""
    style.apply()

    model = TypicalSection()
    v_f = model.flutter_speed()
    ratios = np.linspace(0.05, 1.35, 400)
    lams = np.array([np.linalg.eigvals(model.matrix(r * v_f)) for r in ratios])

    fig, (ax0, ax1) = plt.subplots(
        1, 2, figsize=style.slot(*SLOT_FLUTTER_EIGENVALUES),
        gridspec_kw=dict(width_ratios=[1.0, 1.15]))

    # 上半平面だけを描く（実行列なので下半平面は共役で同じ形）。
    # 固有値の並び順は流速で入れ替わりうるので、虚部の大小で2本に分ける
    upper = np.sort_complex(np.where(lams.imag > 0, lams, np.nan))
    pitch = np.array([row[~np.isnan(row)][np.argmax(row[~np.isnan(row)].imag)]
                      for row in upper])
    plunge = np.array([row[~np.isnan(row)][np.argmin(row[~np.isnan(row)].imag)]
                       for row in upper])

    ax0.axvspan(0, 0.25, color=RED, alpha=0.10, lw=0)
    ax0.axvline(0, color=GREY, lw=0.8)
    ax0.text(0.04, 0.3, "unstable", color=RED, ha="center",
             fontsize=style.SMALL_FONT_PT)
    # 低速側は固有値がほとんど動かず、軌跡が小さく巻いて読みにくいので、
    # 左のパネルは 0.4 U_F から描く（右のパネルは全域）
    shown = ratios >= 0.4
    ax0.plot(pitch[shown].real, pitch[shown].imag, color=PURPLE, lw=1.4)
    ax0.plot(plunge[shown].real, plunge[shown].imag, color=GREY, lw=1.4)
    # 流速を上げる向き（軌跡上の2つの流速の間に矢印を置く）
    for path, (r0, r1), color in ((pitch, (1.15, 1.3), PURPLE),
                                  (plunge, (0.6, 0.9), GREY)):
        i0, i1 = np.searchsorted(ratios, (r0, r1))
        ax0.annotate("", xy=(path[i1].real, path[i1].imag),
                     xytext=(path[i0].real, path[i0].imag),
                     arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6))
    ax0.text(-0.03, 1.1, "torsion-like", color=PURPLE, ha="right",
             fontsize=style.SMALL_FONT_PT)
    ax0.text(-0.03, 0.37, "bending-like", color=GREY, ha="right", va="top",
             fontsize=style.SMALL_FONT_PT)

    # 低速側の点のラベルは左下（右上は軌跡の始まりと重なる）
    for ratio, color, (dx, dy, ha, va) in zip(
            FLUTTER_SPEEDS, (BLUE, RED),
            ((-0.012, -0.05, "right", "top"), (0.012, 0.04, "left", "bottom"))):
        lam = np.linalg.eigvals(model.matrix(ratio * v_f))
        top = lam[np.argmax(lam.imag)]
        ax0.plot(top.real, top.imag, "o", color=color, ms=7, zorder=5)
        ax0.text(top.real + dx, top.imag + dy, rf"${ratio}\,U_F$",
                 color=color, ha=ha, va=va, fontsize=style.SMALL_FONT_PT)

    ax0.set_xlim(-0.2, 0.08)
    ax0.set_ylim(0.2, 1.25)
    ax0.set_xticks([-0.1, 0])
    ax0.set_xlabel(r"$\mathrm{Re}(\lambda)$")
    ax0.set_ylabel(r"$\mathrm{Im}(\lambda)$")
    ax0.set_title("Eigenvalues as $U$ increases", fontsize=style.SMALL_FONT_PT)

    # 右: 最大の実部
    growth = lams.real.max(axis=1)
    ax1.axhline(0, color=GREY, lw=0.8)
    ax1.plot(ratios, growth, color=PURPLE, lw=1.4)
    for ratio, color in zip(FLUTTER_SPEEDS, (BLUE, RED)):
        ax1.plot(ratio, model.growth_rate(ratio * v_f), "o", color=color,
                 ms=7, zorder=5)
    ax1.axvline(1.0, color=GREY, lw=0.8, ls="--")
    ax1.text(1.02, -0.045, r"$U_F$", color=GREY, fontsize=style.SMALL_FONT_PT)
    ax1.text(0.08, 0.01, "grows", color=RED, fontsize=style.SMALL_FONT_PT)
    ax1.text(0.08, -0.03, "decays", color=BLUE, fontsize=style.SMALL_FONT_PT)
    ax1.set_xlim(0, 1.35)
    ax1.set_ylim(-0.05, 0.05)
    ax1.set_yticks([-0.04, 0, 0.04])
    ax1.set_xlabel(r"$U / U_F$")
    ax1.set_ylabel(r"$\max\,\mathrm{Re}(\lambda)$")
    ax1.set_title("Largest real part", fontsize=style.SMALL_FONT_PT)

    fig.savefig(output_dir / "flutter_eigenvalues.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Part 4: 2次元の固定点の分類（複素平面）
# ---------------------------------------------------------------------------

def eigenvalue_plane(output_dir: Path) -> None:
    """Classification of 2D fixed points by the *pair* of eigenvalues of J.

    2 次元系の J は固有値を2つ持つ。図の要点は「線で結んだ1組が1つの系」で
    あることなので、各ケースをペアとして描き、条件式を添える。
    """
    style.apply()

    fig, ax = plt.subplots(figsize=style.slot(*SLOT_EIGENVALUE_PLANE))
    fs = style.SMALL_FONT_PT

    ax.axvspan(-4.8, 0, alpha=0.10, color=BLUE)
    ax.axvspan(0, 4.8, alpha=0.10, color=RED)

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

    real_pair(-4.05, -3.15, BLUE, "o", "Stable Node",
              r"$\lambda_2 \leq \lambda_1 < 0$")
    real_pair(-0.6, 0.6, ORANGE, "^", "Saddle",
              r"$\lambda_2 < 0 < \lambda_1$")
    real_pair(3.15, 4.05, RED, "o", "Unstable Node",
              r"$0 < \lambda_1 \leq \lambda_2$")

    conjugate_pair(-2.0, 1.35, BLUE, "D", r"Stable Spiral  ($\sigma < 0$)")
    conjugate_pair(2.0, 1.35, RED, "D", r"Unstable Spiral  ($\sigma > 0$)")
    conjugate_pair(0.0, 2.15, GREEN, "s", r"Center  ($\sigma = 0$)")

    ax.text(-3.6, -2.15, "Stable", fontsize=style.BASE_FONT_PT * 1.15,
            ha="center", color=BLUE, alpha=0.45, weight="bold")
    ax.text(3.6, -2.15, "Unstable", fontsize=style.BASE_FONT_PT * 1.15,
            ha="center", color=RED, alpha=0.45, weight="bold")

    ax.set_xlim(-4.8, 4.8)
    ax.set_ylim(-2.6, 3.1)
    # 模式図なので等方性は不要（掛けると横長スロットに内部余白ができる）
    _hide_axes(ax)

    fig.savefig(output_dir / "eigenvalue_plane.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Part 4: 2次元の相図（固有ベクトルは座標軸と一致させない）
# ---------------------------------------------------------------------------

#: 固有ベクトルを座標軸からずらすための基底。対角行列の例だと
#: 「軌道が座標軸に沿う」という特別な性質を本質と取り違えやすい
_P_REAL = np.array([[1.0, 0.45], [0.35, 1.0]])
_P_COMPLEX = np.array([[1.0, 0.6], [0.0, 0.7]])


def _real_case(l1: float, l2: float) -> np.ndarray:
    """固有値 l1, l2、固有ベクトル = _P_REAL の列 となる行列."""
    return _P_REAL @ np.diag([l1, l2]) @ np.linalg.inv(_P_REAL)


def _complex_case(sigma: float, omega: float) -> np.ndarray:
    """固有値 sigma +- i omega の行列（回転の標準形を _P_COMPLEX で傾けたもの）."""
    R = np.array([[sigma, -omega], [omega, sigma]])
    return _P_COMPLEX @ R @ np.linalg.inv(_P_COMPLEX)


PHASE_PORTRAIT_GROUPS = {
    "phase_portraits_real": [
        (_real_case(-2.0, -0.7), "Stable Node  $\\lambda = -2,\\, -0.7$"),
        (_real_case(2.0, 0.7), "Unstable Node  $\\lambda = 2,\\, 0.7$"),
        (_real_case(1.0, -1.0), "Saddle  $\\lambda = 1,\\, -1$"),
    ],
    "phase_portraits_complex": [
        (_complex_case(-0.3, 2.0), "Stable Spiral  $\\lambda = -0.3 \\pm 2i$"),
        (_complex_case(0.3, 2.0), "Unstable Spiral  $\\lambda = 0.3 \\pm 2i$"),
        (_complex_case(0.0, 2.0), "Center  $\\lambda = \\pm 2i$"),
    ],
}


def phase_portraits(output_dir: Path) -> None:
    """Generate 1x3 phase-portrait strips, one per eigenvalue family."""
    style.apply()

    lim = 2.5
    for name, cases in PHASE_PORTRAIT_GROUPS.items():
        fig, axes = plt.subplots(
            1, len(cases), figsize=style.slot(*SLOT_PHASE_PORTRAITS))

        for ax, (A, title) in zip(axes, cases):
            xx = np.linspace(-lim, lim, 24)
            X, Y = np.meshgrid(xx, xx)
            U = A[0, 0] * X + A[0, 1] * Y
            V = A[1, 0] * X + A[1, 1] * Y
            ax.streamplot(X, Y, U, V, color=BLUE, linewidth=0.7,
                          density=1.0, arrowsize=0.9)
            if name == "phase_portraits_real":
                # 固有ベクトルの向き: 軌道はこの直線に沿って伸び縮みする
                for k, color in ((0, ORANGE), (1, GREEN)):
                    v = _P_REAL[:, k] / np.linalg.norm(_P_REAL[:, k])
                    ax.plot([-3 * v[0], 3 * v[0]], [-3 * v[1], 3 * v[1]],
                            color=color, lw=1.6, alpha=0.9)
                    # 流線の上に置くので、背景色の下敷きを敷いて読めるようにする
                    s = 1.9 if k == 0 else 1.75
                    ax.text(s * v[0], s * v[1], rf"$\boldsymbol{{v}}_{k + 1}$",
                            color=color, ha="center", va="center",
                            fontsize=style.BASE_FONT_PT, zorder=6,
                            bbox=dict(boxstyle="round,pad=0.15", fc=BG,
                                      ec="none"))
            ax.plot(0, 0, "o", color=RED, markersize=6, zorder=5)
            ax.set_xlim(-lim, lim)
            ax.set_ylim(-lim, lim)
            ax.set_aspect("equal")
            ax.set_title(title, fontsize=style.SMALL_FONT_PT)
            ax.set_xticks([-2, 0, 2])
            ax.set_yticks([-2, 0, 2])
            ax.set_xlabel(r"$\xi_1$")

        for ax in axes[1:]:
            ax.set_yticklabels([])
        axes[0].set_ylabel(r"$\xi_2$")

        fig.savefig(output_dir / f"{name}.png")
        plt.close(fig)


# ---------------------------------------------------------------------------
# Part 4: 高次元の例 — 旅客機の縦の運動のモード
# ---------------------------------------------------------------------------

#: B747 の縦の運動（M = 0.8 巡航）の状態行列。状態は (u, w, q, theta) =
#: (前進速度の変化 [m/s], 上下速度の変化 [m/s], ピッチ角速度 [rad/s], ピッチ角 [rad])。
#: 出典: MIT 16.333 Aircraft Stability and Control (Fall 2004), Lecture 6。
#: 固有値は短周期 -0.372 +- 0.887i、フゴイド -0.0033 +- 0.067i（同資料の値と一致）。
B747_LONGITUDINAL = np.array([
    [-0.0069, 0.0139, 0.0, -9.81],
    [-0.0905, -0.3149, 235.8928, 0.0],
    [0.0004, -0.0034, -0.4282, 0.0],
    [0.0, 0.0, 1.0, 0.0],
])
B747_U0 = 235.9  # 巡航速度 [m/s]


def aircraft_modes(output_dir: Path) -> None:
    """左: 4つの固有値 / 中: 迎角の応答（短周期）/ 右: 速度の応答（フゴイド）."""
    style.apply()

    A = B747_LONGITUDINAL
    lam, vec = np.linalg.eig(A)
    # 迎角を 1 度乱した初期状態（上向きの突風）: w = U0 * alpha
    q0 = np.array([0.0, B747_U0 * np.deg2rad(1.0), 0.0, 0.0])
    c = np.linalg.solve(vec, q0.astype(complex))

    def response(t):
        return (vec @ (c[:, None] * np.exp(np.outer(lam, t)))).real

    fig, axes = plt.subplots(
        1, 3, figsize=style.slot(*SLOT_AIRCRAFT_MODES),
        gridspec_kw=dict(width_ratios=[0.8, 1.0, 1.0]))

    # --- 固有値 ---
    ax = axes[0]
    ax.axvline(0, color=GREY, lw=0.8)
    ax.axhline(0, color=GREY, lw=0.8)
    short = lam[np.abs(lam.imag) > 0.5]
    phug = lam[np.abs(lam.imag) < 0.5]
    ax.plot(short.real, short.imag, "D", color=ORANGE, ms=6)
    ax.plot(phug.real, phug.imag, "D", color=GREEN, ms=6)
    ax.text(-0.36, 0.62, "short\nperiod", color=ORANGE, ha="center",
            va="top", fontsize=style.SMALL_FONT_PT)
    ax.annotate("phugoid", xy=(phug.real[0], abs(phug.imag[0])),
                xytext=(-0.33, -0.55), color=GREEN, ha="center",
                fontsize=style.SMALL_FONT_PT,
                arrowprops=dict(arrowstyle="-", color=GREEN, lw=0.8))
    ax.set_xlim(-0.5, 0.12)
    ax.set_ylim(-1.1, 1.1)
    ax.set_xticks([-0.4, 0])
    ax.set_yticks([-1, 0, 1])
    ax.set_xlabel(r"$\mathrm{Re}(\lambda)$")
    ax.set_ylabel(r"$\mathrm{Im}(\lambda)$")
    ax.set_title("Eigenvalues", fontsize=style.SMALL_FONT_PT)

    # --- 短周期: 迎角 alpha = w / U0 ---
    t = np.linspace(0, 20, 600)
    alpha = np.rad2deg(response(t)[1] / B747_U0)
    axes[1].plot(t, alpha, color=ORANGE, lw=1.2)
    axes[1].axhline(0, color=GREY, lw=0.5, alpha=0.5)
    axes[1].set_xlabel(r"$t$ [s]")
    axes[1].set_ylabel(r"$\alpha$ [deg]")
    axes[1].set_title("Short period: angle of attack",
                      fontsize=style.SMALL_FONT_PT)

    # --- フゴイド: 前進速度 u ---
    t = np.linspace(0, 600, 1200)
    u = response(t)[0]
    axes[2].plot(t, u, color=GREEN, lw=1.2)
    axes[2].axhline(0, color=GREY, lw=0.5, alpha=0.5)
    axes[2].set_xlabel(r"$t$ [s]")
    axes[2].set_ylabel(r"$u$ [m/s]")
    axes[2].set_title("Phugoid: forward speed", fontsize=style.SMALL_FONT_PT)

    fig.savefig(output_dir / "aircraft_modes.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Part 4: 単振り子の相図
# ---------------------------------------------------------------------------

def pendulum_phase_portrait(output_dir: Path) -> None:
    """Phase portrait for the simple pendulum dtheta=omega, domega=-sin(theta)."""
    style.apply()

    fig, ax = plt.subplots(figsize=style.slot(*SLOT_PENDULUM))
    x_grid = np.linspace(-2 * np.pi, 2 * np.pi, 500)

    for H in [-0.5, 0.0, 0.5, 0.8]:
        y_sq = 2 * (H + np.cos(x_grid))
        mask = y_sq > 0
        y_pos = np.where(mask, np.sqrt(np.maximum(y_sq, 0)), np.nan)
        ax.plot(x_grid, y_pos, color=BLUE, linewidth=0.7, alpha=0.7)
        ax.plot(x_grid, -y_pos, color=BLUE, linewidth=0.7, alpha=0.7)

    y_sep = np.sqrt(np.maximum(2 * (1.0 + np.cos(x_grid)), 0))
    ax.plot(x_grid, y_sep, color=RED, linewidth=1.5, alpha=0.9)
    ax.plot(x_grid, -y_sep, color=RED, linewidth=1.5, alpha=0.9)

    for H in [1.5, 2.5]:
        y_sq = 2 * (H + np.cos(x_grid))
        ax.plot(x_grid, np.sqrt(y_sq), color=GREY, linewidth=0.7, alpha=0.7)
        ax.plot(x_grid, -np.sqrt(y_sq), color=GREY, linewidth=0.7, alpha=0.7)

    for xc in [0, -2 * np.pi, 2 * np.pi]:
        ax.plot(xc, 0, "o", color=BLUE, markersize=6, zorder=5)
    for xs in [-np.pi, np.pi]:
        ax.plot(xs, 0, "s", color=RED, markersize=6, zorder=5)

    ax.set_xlim(-2 * np.pi, 2 * np.pi)
    ax.set_ylim(-4, 4)
    ax.set_xlabel(r"$\theta$")
    ax.set_ylabel(r"$\omega$")
    ax.set_xticks([-2 * np.pi, -np.pi, 0, np.pi, 2 * np.pi])
    ax.set_xticklabels([r"$-2\pi$", r"$-\pi$", r"$0$", r"$\pi$", r"$2\pi$"])

    # 凡例は曲線に重なって読めないので置かない。色と記号の対応はスライド本文で示す

    fig.savefig(output_dir / "pendulum_phase.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Part 5: 線形化はどこまで正しいか
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

    axes[0].streamplot(X, Y, Y, -np.sin(X), color=BLUE, linewidth=0.6,
                       density=1.2, arrowsize=0.8)
    x_fine = np.linspace(-lim, lim, 800)
    sep = np.sqrt(np.maximum(2 * (1.0 + np.cos(x_fine)), 0))
    axes[0].plot(x_fine, sep, color=RED, lw=1.6)
    axes[0].plot(x_fine, -sep, color=RED, lw=1.6)
    axes[0].plot(0, 0, "o", color=RED, markersize=6, zorder=5)
    for xs in (-np.pi, np.pi):
        axes[0].plot(xs, 0, "s", color=ORANGE, markersize=7, zorder=6)
    axes[0].set_title("Nonlinear: $\\dot{\\omega} = -\\sin\\theta$")

    axes[1].streamplot(X, Y, Y, -X, color=ORANGE, linewidth=0.6,
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


def topological_conjugacy(output_dir: Path) -> None:
    """Hartman-Grobman の可換図式 h . phi_t = e^{Jt} . h."""
    style.apply()

    fig, ax = plt.subplots(figsize=style.slot(*SLOT_CONJUGACY))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    _hide_axes(ax)
    fs = style.SMALL_FONT_PT

    nodes = {
        "tl": (2.6, 7.4, r"$\boldsymbol{q}$"),
        "tr": (7.4, 7.4, r"$\phi_t(\boldsymbol{q})$"),
        "bl": (2.6, 2.6, r"$h(\boldsymbol{q})$"),
        "br": (7.4, 2.6, r"$e^{Jt}h(\boldsymbol{q})$"),
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

    arrow((3.7, 7.4), (6.0, 7.4), r"$\phi_t$", BLUE, (0, 0.55))
    arrow((3.7, 2.6), (5.9, 2.6), r"$e^{Jt}$", ORANGE, (0, -0.75))
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
# Part 5: Re(lambda) = 0 では線形化で決まらない
# ---------------------------------------------------------------------------

def center_ambiguity(output_dir: Path) -> None:
    """同じ線形化 (lambda = +-i) をもつ3つの系: a < 0 / a = 0 / a > 0."""
    style.apply()

    fig, axes = plt.subplots(1, 3, figsize=style.slot(*SLOT_CENTER_AMBIGUITY))
    lim = 1.5
    xx = np.linspace(-lim, lim, 30)
    X, Y = np.meshgrid(xx, xx)
    R2 = X**2 + Y**2

    for ax, a, title, color in (
        (axes[0], -1.0, r"$a < 0$: spiral in", BLUE),
        (axes[1], 0.0, r"$a = 0$: closed", GREEN),
        (axes[2], 1.0, r"$a > 0$: spiral out", RED),
    ):
        U = -Y + a * X * R2
        V = X + a * Y * R2
        ax.streamplot(X, Y, U, V, color=color, linewidth=0.7, density=0.9,
                      arrowsize=0.8)
        ax.plot(0, 0, "o", color=FG, ms=5, zorder=5)
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.set_title(title, fontsize=style.SMALL_FONT_PT)
        _hide_axes(ax)
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color(GREY)

    fig.savefig(output_dir / "center_ambiguity.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def generate_all(output_dir: Path) -> None:
    """Generate all Chapter 1 figures."""
    chapter_overview(output_dir)
    motivation(output_dir)
    typical_section_schematic(output_dir)
    vector_field(output_dir)
    orbits_cannot_cross(output_dir)
    stability_concepts(output_dir)
    one_dim_linearization(output_dir)
    eigenvalue_effect(output_dir)
    flutter_eigenvalues(output_dir)
    eigenvalue_plane(output_dir)
    phase_portraits(output_dir)
    aircraft_modes(output_dir)
    pendulum_phase_portrait(output_dir)
    linearization(output_dir)
    topological_conjugacy(output_dir)
    center_ambiguity(output_dir)
    print("  Ch.1 figures generated.")
