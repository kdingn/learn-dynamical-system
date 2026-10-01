"""Chapter 2 figures: Invariant Manifolds and Nonlinear Analysis."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from scipy.integrate import solve_ivp

from learn_dynamical_system import style
from learn_dynamical_system.palette import (
    BLUE, FG, GREEN, GREY, LIGHT_GREY, ORANGE, PURPLE, RED,
)

# スライド上での表示サイズ (CSS px)。図はこの寸法ちょうどで作られるので、
# slides/02-manifolds.md 側の `width:` 指定をこの値と一致させること。
SLOT_CHAPTER_OVERVIEW = (820, 250)
SLOT_INVARIANT_SET = (400, 252)
SLOT_MANIFOLD_CHART = (360, 300)
SLOT_TANGENT_SPACE = (360, 400)
SLOT_TANGENT_CHART = (720, 190)
SLOT_TANGENT_SUBSPACE = (340, 240)
SLOT_EIGENSPACES = (360, 300)
SLOT_STABLE_MANIFOLD = (450, 255)
SLOT_PENDULUM_MANIFOLDS = (770, 250)
SLOT_CONNECTIONS = (740, 196)
SLOT_CONNECTION_ENERGY = (800, 200)
SLOT_CENTER_MANIFOLD = (400, 230)
SLOT_CM_EXAMPLE = (780, 292)
SLOT_CM_NONUNIQUE = (520, 220)
SLOT_PENDULUM_PERTURBATION = (560, 232)


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


def _saddle_orbits(ax, cx, cy, sx, sy, color, lw=0.6, alpha=0.45,
                   arrows=False):
    """双曲線 uv = c を (cx, cy) 中心に (sx, sy) 倍で描く（背景の流れ用）.

    ``arrows=True`` で進行方向（|u| が増える向き）の矢羽を1つ置く。
    """
    for c in (0.45, 1.5, -0.45, -1.5):
        for lo, hi in ((0.16, 3.2), (-3.2, -0.16)):
            u = np.linspace(lo, hi, 300)
            v = c / u
            m = np.abs(v) <= 2.6
            xs, ys = cx + u[m] * sx, cy + v[m] * sy
            ax.plot(xs, ys, color=color, lw=lw, alpha=alpha)
            if arrows and len(xs) > 8:
                i = len(xs) // 2
                p, q = (xs[i], ys[i]), (xs[i + 3], ys[i + 3])
                if lo < 0:      # u が負の枝では |u| が増える向きが逆
                    p, q = q, p
                _arrow(ax, p, q, color, lw=lw, alpha=alpha)


def _integrate(rhs, q0, t_end, max_r=6.0, n=4000):
    """q0 から t_end まで積分する（半径 max_r を超えたら打ち切る）."""
    def event(t, q):
        return np.hypot(q[0], q[1]) - max_r
    event.terminal = True

    sol = solve_ivp(rhs, (0.0, t_end), np.asarray(q0, dtype=float),
                    t_eval=np.linspace(0.0, t_end, n), events=event,
                    rtol=1e-10, atol=1e-13)
    return sol.y[0], sol.y[1]


# ---------------------------------------------------------------------------
# 1. Chapter overview (cover schematic)
# ---------------------------------------------------------------------------

def chapter_overview(output_dir: Path) -> None:
    """章の筋道: 固有空間 → 不変多様体 → 中心多様体上の縮約."""
    style.apply()

    fig, ax = plt.subplots(figsize=style.slot(*SLOT_CHAPTER_OVERVIEW))
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 9.2)
    _hide_axes(ax)
    fs = style.SMALL_FONT_PT
    cy = 6.0

    # --- (1) 線形: 固有空間は直線 ---
    cx = 4.6
    _saddle_orbits(ax, cx, cy, 0.85, 0.72, GREY)
    ax.plot([cx - 2.9, cx + 2.9], [cy, cy], color=RED, lw=1.8)
    ax.plot([cx, cx], [cy - 2.1, cy + 2.1], color=BLUE, lw=1.8)
    _arrow(ax, (cx + 1.5, cy), (cx + 2.8, cy), RED, lw=1.4)
    _arrow(ax, (cx - 1.5, cy), (cx - 2.8, cy), RED, lw=1.4)
    _arrow(ax, (cx, cy + 2.0), (cx, cy + 0.7), BLUE, lw=1.4)
    _arrow(ax, (cx, cy - 2.0), (cx, cy - 0.7), BLUE, lw=1.4)
    ax.plot(cx, cy, "o", color=FG, ms=7, zorder=6)
    ax.text(cx + 3.0, cy + 0.15, r"$E^u$", color=RED, fontsize=fs,
            ha="left", va="bottom")
    ax.text(cx + 0.2, cy + 2.15, r"$E^s$", color=BLUE, fontsize=fs,
            ha="left", va="bottom")
    ax.text(cx, 1.9, "Eigenspaces (linear)", ha="center", fontsize=fs, color=FG)
    ax.text(cx, 0.55, r"$E^s \oplus E^u \oplus E^c$", ha="center",
            fontsize=fs, color=GREY)

    # --- (2) 非線形: 曲がった不変多様体 ---
    cx = 14.6
    u = np.linspace(-2.9, 2.9, 300)
    ax.plot([cx - 2.9, cx + 2.9], [cy, cy], color=GREY, lw=0.8, ls="--")
    ax.plot([cx, cx], [cy - 2.1, cy + 2.1], color=GREY, lw=0.8, ls="--")
    ax.plot(cx + u, cy + 0.18 * u**2, color=RED, lw=1.8)
    v = np.linspace(-2.1, 2.1, 300)
    ax.plot(cx - 0.20 * v**2, cy + v, color=BLUE, lw=1.8)
    ax.plot(cx, cy, "o", color=FG, ms=7, zorder=6)
    ax.text(cx + 3.0, cy + 1.3, r"$W^u$", color=RED, fontsize=fs,
            ha="left", va="center")
    ax.text(cx - 1.1, cy + 2.15, r"$W^s$", color=BLUE, fontsize=fs,
            ha="center", va="bottom")
    ax.text(cx, 1.9, "Invariant manifolds", ha="center", fontsize=fs, color=FG)
    ax.text(cx, 0.55, r"tangent to $E^s, E^u, E^c$", ha="center",
            fontsize=fs, color=GREY)

    # --- (3) 中心多様体上への縮約 ---
    cx = 24.8
    u = np.linspace(-3.1, 3.1, 300)
    wc = cy - 0.13 * u**2
    ax.plot(cx + u, wc, color=GREEN, lw=2.0)
    for du in (-2.2, -1.0, 1.0, 2.2):
        y0 = cy - 0.13 * du**2
        _arrow(ax, (cx + du, y0 + 1.9), (cx + du, y0 + 0.35), ORANGE, lw=1.1)
        _arrow(ax, (cx + du, y0 - 1.9), (cx + du, y0 - 0.35), ORANGE, lw=1.1)
    _arrow(ax, (cx + 2.0, cy - 0.52), (cx + 0.8, cy - 0.08), GREEN, lw=1.5)
    _arrow(ax, (cx - 2.0, cy - 0.52), (cx - 0.8, cy - 0.08), GREEN, lw=1.5)
    ax.plot(cx, cy, "o", color=FG, ms=7, zorder=6)
    ax.text(cx + 3.2, cy - 1.2, r"$W^c$", color=GREEN, fontsize=fs,
            ha="left", va="center")
    ax.text(cx - 3.2, cy + 2.0, "fast", color=ORANGE, fontsize=fs,
            ha="left", va="center")
    ax.text(cx, 1.9, "Reduction on $W^c$", ha="center", fontsize=fs, color=FG)
    ax.text(cx, 0.55, r"$\dot{x} = Ax + N_c(x, h(x))$", ha="center",
            fontsize=fs, color=GREY)

    # --- ステージ間の矢印 ---
    for x0, x1 in ((8.2, 10.4), (18.4, 20.6)):
        _arrow(ax, (x0, cy), (x1, cy), FG, lw=1.4)

    fig.savefig(output_dir / "ch02_overview.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 2. What "invariant" means
# ---------------------------------------------------------------------------

def invariant_set(output_dir: Path) -> None:
    """不変な集合とそうでない集合の対比（サドルの流れを背景にする）."""
    style.apply()

    fig, axes = plt.subplots(1, 2, figsize=style.slot(*SLOT_INVARIANT_SET))
    fs = style.SMALL_FONT_PT

    for ax in axes:
        _saddle_orbits(ax, 0.0, 0.0, 1.0, 1.0, GREY, lw=0.7, alpha=0.5,
                       arrows=True)
        ax.plot([-2.6, 2.6], [0, 0], color=GREY, lw=0.7, alpha=0.5)
        ax.plot([0, 0], [-2.6, 2.6], color=GREY, lw=0.7, alpha=0.5)
        for sgn in (1, -1):
            _arrow(ax, (sgn * 1.1, 0), (sgn * 1.6, 0), GREY, lw=0.7,
                   alpha=0.5)
        ax.plot(0, 0, "o", color=FG, ms=6, zorder=6)
        ax.set_xlim(-2.7, 2.7)
        ax.set_ylim(-2.7, 2.7)
        ax.set_aspect("equal")
        _hide_axes(ax)

    # --- 左: 不変（安定部分空間は流れに閉じている）---
    ax = axes[0]
    ax.plot([0, 0], [-2.4, 2.4], color=GREEN, lw=2.2, zorder=5)
    _arrow(ax, (0, 2.3), (0, 0.9), GREEN, lw=1.5)
    _arrow(ax, (0, -2.3), (0, -0.9), GREEN, lw=1.5)
    ax.set_title(r"Invariant: $\phi_t(S) \subseteq S$",
                 fontsize=fs, color=GREEN)
    ax.text(0.22, 1.75, r"$S$", color=GREEN, fontsize=fs,
            ha="left", va="center")
    # キャプションは xlabel に置く（ax.text だと constrained_layout が
    # 場所を確保してくれず、下の余白に食い込む）
    ax.set_xlabel("never leaves $S$", color=GREY, fontsize=fs)

    # --- 右: 不変でない（円は流れに横切られる）---
    ax = axes[1]
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(1.5 * np.cos(th), 1.5 * np.sin(th),
            color=ORANGE, lw=2.2, zorder=5)
    # 円周上の点が外/内へ抜ける様子（サドル場 (x, -y) の速度ベクトル）
    for a in (0.35, np.pi - 0.35, np.pi + 0.35, -0.35):
        x0, y0 = 1.5 * np.cos(a), 1.5 * np.sin(a)
        vx, vy = x0, -y0
        nrm = np.hypot(vx, vy)
        _arrow(ax, (x0, y0), (x0 + 0.85 * vx / nrm, y0 + 0.85 * vy / nrm),
               RED, lw=1.5)
    ax.set_title("Not invariant", fontsize=fs, color=ORANGE)
    ax.set_xlabel("the flow crosses it", color=GREY, fontsize=fs)

    fig.savefig(output_dir / "invariant_set.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 2b. What a manifold is: local charts, dimension, tangent space
# ---------------------------------------------------------------------------

def _warp(u, v):
    """平らな格子を「曲がった面」に見せるための歪み."""
    return u + 0.24 * np.sin(2.0 * v), v + 0.34 * np.sin(1.7 * u)


def _grid_patch(ax, cx, cy, sx, sy, u0, u1, v0, v1, color, lw, warp,
                n=5, zorder=2, fill=None):
    """(u, v) ∈ [u0,u1]×[v0,v1] の格子を描く。warp=True なら歪ませる."""
    def to_xy(u, v):
        if warp:
            u, v = _warp(u, v)
        return cx + sx * u, cy + sy * v

    if fill is not None:
        e = np.linspace(0, 1, 60)
        bu = np.concatenate([u0 + (u1 - u0) * e, np.full_like(e, u1),
                             u1 - (u1 - u0) * e, np.full_like(e, u0)])
        bv = np.concatenate([np.full_like(e, v0), v0 + (v1 - v0) * e,
                             np.full_like(e, v1), v1 - (v1 - v0) * e])
        ax.fill(*to_xy(bu, bv), color=fill, alpha=0.18, lw=0,
                zorder=zorder - 1)

    for u in np.linspace(u0, u1, n):
        vv = np.linspace(v0, v1, 120)
        ax.plot(*to_xy(np.full_like(vv, u), vv), color=color, lw=lw,
                zorder=zorder)
    for v in np.linspace(v0, v1, n):
        uu = np.linspace(u0, u1, 120)
        ax.plot(*to_xy(uu, np.full_like(uu, v)), color=color, lw=lw,
                zorder=zorder)


def manifold_chart(output_dir: Path) -> None:
    """多様体 = どの点のそばも平らな R^k と同じ、を曲線と面で示す."""
    style.apply()

    fig, axes = plt.subplots(2, 1, figsize=style.slot(*SLOT_MANIFOLD_CHART))
    fs = style.SMALL_FONT_PT
    for ax in axes:
        ax.set_xlim(0, 10)
        # 行の高さ（約 114px）と幅（約 340px）の比に合わせ、図形が
        # 縦につぶれないよう ylim を取る
        ax.set_ylim(0, 3.35)
        _hide_axes(ax)

    # --- 上段: 曲線 (k = 1) -> 区間 ---
    ax = axes[0]
    t = np.linspace(0, 1, 400)
    cx = 0.4 + 3.6 * t
    cy = 1.75 + 0.95 * np.sin(3.4 * t - 0.7)
    ax.plot(cx, cy, color=GREY, lw=1.6)
    m = (t >= 0.33) & (t <= 0.67)
    ax.plot(cx[m], cy[m], color=GREEN, lw=2.6)
    i = int(np.argmin(np.abs(t - 0.5)))
    ax.plot(cx[i], cy[i], "o", color=FG, ms=5, zorder=6)
    ax.text(cx[i] + 0.14, cy[i] + 0.1, r"$p$", color=FG, fontsize=fs,
            ha="left", va="bottom")

    _arrow(ax, (4.5, 1.75), (6.0, 1.75), FG, lw=1.2)
    ax.text(5.25, 1.95, r"chart $\varphi$", color=FG, fontsize=fs,
            ha="center", va="bottom")

    ax.plot([6.5, 9.6], [1.75, 1.75], color=GREY, lw=1.6)
    ax.plot([7.5, 8.6], [1.75, 1.75], color=GREEN, lw=2.6)
    for xt in (7.5, 8.6):
        ax.plot([xt, xt], [1.62, 1.88], color=GREEN, lw=1.2)
    ax.plot(8.05, 1.75, "o", color=FG, ms=5, zorder=6)

    ax.text(2.2, 0.45, r"$M$: a curve", color=FG, fontsize=fs, ha="center")
    ax.text(8.05, 0.45, r"interval in $\mathbb{R}$", color=FG, fontsize=fs,
            ha="center")
    ax.set_title(r"$k = 1$", fontsize=fs)

    # --- 下段: 面 (k = 2) -> 円板 ---
    ax = axes[1]
    _grid_patch(ax, 2.2, 1.80, 1.35, 0.78, -1, 1, -1, 1, GREY, 0.9, True)
    _grid_patch(ax, 2.2, 1.80, 1.35, 0.78, -0.36, 0.4, -0.36, 0.4,
                GREEN, 1.6, True, n=3, zorder=4, fill=GREEN)
    px, py = _warp(0.02, 0.02)
    ax.plot(2.2 + 1.35 * px, 1.80 + 0.78 * py, "o", color=FG, ms=5, zorder=6)

    _arrow(ax, (4.5, 1.75), (6.0, 1.75), FG, lw=1.2)
    ax.text(5.25, 1.95, r"$\varphi$", color=FG, fontsize=fs,
            ha="center", va="bottom")

    _grid_patch(ax, 8.05, 1.80, 1.2, 0.78, -1, 1, -1, 1, GREY, 0.9, False)
    _grid_patch(ax, 8.05, 1.80, 1.2, 0.78, -0.36, 0.4, -0.36, 0.4,
                GREEN, 1.6, False, n=3, zorder=4, fill=GREEN)
    ax.plot(8.05 + 1.2 * 0.02, 1.80 + 0.78 * 0.02, "o", color=FG, ms=5,
            zorder=6)

    ax.text(2.2, 0.32, r"$M$: a surface", color=FG, fontsize=fs, ha="center")
    ax.text(8.05, 0.32, r"disk in $\mathbb{R}^2$", color=FG, fontsize=fs,
            ha="center")
    ax.set_title(r"$k = 2$", fontsize=fs)

    fig.savefig(output_dir / "manifold_chart.png")
    plt.close(fig)


def _parallelogram(ax, center, d1, d2, color, lw=2.0, fill_alpha=0.14,
                   zorder=3, ls="-"):
    """center を中心に d1, d2 が張る平行四辺形（= 平面の一部）を描く."""
    c, d1, d2 = np.asarray(center), np.asarray(d1), np.asarray(d2)
    pts = np.array([c + d1 + d2, c + d1 - d2, c - d1 - d2, c - d1 + d2,
                    c + d1 + d2])
    if fill_alpha:
        ax.fill(pts[:, 0], pts[:, 1], color=color, alpha=fill_alpha, lw=0,
                zorder=zorder - 1)
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, ls=ls, zorder=zorder)
    return pts


#: k = 2 の「曲がった面」の共通パラメータ（接空間まわりの図で使い回す）
_SURF = dict(sx=2.7, sy=1.15)


def _surface(cx, cy, sx, sy):
    """(u, v) -> 平面上の点。_warp で歪ませた面を返す."""
    def S(u, v):
        uu, vv = _warp(u, v)
        return np.array([cx + sx * uu, cy + sy * vv])
    return S


def tangent_space(output_dir: Path) -> None:
    """接空間が k 次元になる理由を k = 1 と k = 2 で見せる.

    上段: 道は1本でも走り方は自由なので、速度は v の定数倍を埋めつくす。
    下段: 独立な2方向が取れるので平面になる。
    """
    style.apply()

    fig, axes = plt.subplots(2, 1, figsize=style.slot(*SLOT_TANGENT_SPACE))
    fs = style.SMALL_FONT_PT
    for ax in axes:
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 4.8)
        _hide_axes(ax)

    # --- 上段: k = 1。同じ道を速さ・向きを変えて走る ---
    ax = axes[0]
    xs = np.linspace(0.6, 9.4, 400)
    ys = 1.5 + 1.3 * np.sin(np.pi * (xs - 0.6) / 8.8)
    ax.plot(xs, ys, color=GREY, lw=1.6)
    ax.text(8.6, 1.72, r"$M$", color=GREY, fontsize=fs, ha="center",
            va="top")

    xp = 2.9
    yp = 1.5 + 1.3 * np.sin(np.pi * (xp - 0.6) / 8.8)
    slope = 1.3 * (np.pi / 8.8) * np.cos(np.pi * (xp - 0.6) / 8.8)
    p1 = np.array([xp, yp])
    v = 1.55 * np.array([1.0, slope])

    ends = np.array([p1 - 1.4 * v, p1 + 2.6 * v])
    ax.plot(ends[:, 0], ends[:, 1], color=GREEN, lw=2.0, zorder=4)
    _arrow(ax, tuple(p1), tuple(p1 + v), GREEN, lw=2.0)
    # 速度の目盛: v の定数倍が「全部」現れる（0 も負も）
    for c, lab in ((-1.0, r"$-\boldsymbol{v}$"), (0.0, r"$\boldsymbol{0}$"),
                   (1.0, r"$\boldsymbol{v}$"), (2.0, r"$2\boldsymbol{v}$")):
        q = p1 + c * v
        ax.plot(*q, "o", color=GREEN, ms=5, zorder=6)
        ax.text(q[0], q[1] + 0.24, lab, color=GREEN, fontsize=fs,
                ha="center", va="bottom")
    ax.plot(*p1, "o", color=FG, ms=5, zorder=7)
    ax.text(p1[0], p1[1] - 0.3, r"$p$", color=FG, fontsize=fs,
            ha="center", va="top")
    ax.text(ends[1][0] + 0.15, ends[1][1], r"$T_pM$", color=GREEN,
            fontsize=fs, ha="left", va="center")
    ax.set_title(r"$k = 1$: any speed on one road", fontsize=fs)

    # --- 下段: k = 2。独立な2方向が取れる ---
    ax = axes[1]
    cx, cy = 4.6, 2.35
    S = _surface(cx, cy, _SURF["sx"], _SURF["sy"])
    _grid_patch(ax, cx, cy, _SURF["sx"], _SURF["sy"], -1, 1, -1, 1,
                GREY, 0.9, True)

    u0, v0 = -0.15, -0.10
    p = S(u0, v0)
    tt = np.linspace(-1, 1, 200)
    g1 = S(np.full_like(tt, u0), tt)
    g2 = S(tt, np.full_like(tt, v0))
    ax.plot(g1[0], g1[1], color=ORANGE, lw=1.8, zorder=5)
    ax.plot(g2[0], g2[1], color=ORANGE, lw=1.8, zorder=5)
    ax.text(g1[0][-1] + 0.05, g1[1][-1] + 0.15, r"$\gamma_1$", color=ORANGE,
            fontsize=fs, ha="left", va="bottom")
    ax.text(g2[0][-1] + 0.12, g2[1][-1] - 0.08, r"$\gamma_2$", color=ORANGE,
            fontsize=fs, ha="left", va="top")

    h = 1e-4
    du = (S(u0 + h, v0) - S(u0 - h, v0)) / (2 * h)
    dv = (S(u0, v0 + h) - S(u0, v0 - h)) / (2 * h)
    corners = _parallelogram(ax, p, 0.70 * du, 0.70 * dv, GREEN, lw=2.0,
                             zorder=4)
    _arrow(ax, tuple(p), tuple(p + 0.62 * du), ORANGE, lw=2.0)
    _arrow(ax, tuple(p), tuple(p + 0.62 * dv), ORANGE, lw=2.0)

    ax.plot(*p, "o", color=FG, ms=5, zorder=8)
    ax.text(p[0] - 0.15, p[1] + 0.05, r"$p$", color=FG, fontsize=fs,
            ha="right", va="bottom")
    ax.text(corners[0][0] + 0.15, corners[0][1] + 0.2, r"$T_pM$",
            color=GREEN, fontsize=fs, ha="left", va="bottom")
    ax.set_title(r"$k = 2$: two independent directions", fontsize=fs)

    fig.savefig(output_dir / "tangent_space.png")
    plt.close(fig)


def tangent_chart(output_dir: Path) -> None:
    """局所座標の直線束を M へ送ると、速度が T_pM を埋めつくす."""
    style.apply()

    fig, ax = plt.subplots(figsize=style.slot(*SLOT_TANGENT_CHART))
    fs = style.SMALL_FONT_PT
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 3.8)
    _hide_axes(ax)

    dirs = [np.array(d, dtype=float)
            for d in ((1.0, 0.0), (0.45, 1.0), (-0.55, 0.95))]

    # --- 左: 平らな局所座標。phi(p) を通るまっすぐな線 ---
    lx, ly, sx, sy = 4.0, 1.95, 2.7, 1.1
    _grid_patch(ax, lx, ly, sx, sy, -1, 1, -1, 1, GREY, 0.8, False)
    for d in dirs:
        t = np.linspace(-1, 1, 2) / max(abs(d[0]), abs(d[1]))
        ax.plot(lx + sx * t * d[0], ly + sy * t * d[1], color=ORANGE,
                lw=1.6, zorder=5)
    ax.plot(lx, ly, "o", color=FG, ms=5, zorder=8)
    ax.text(lx, ly - sy - 0.5, r"$\varphi(p) + t\boldsymbol{c}$  in  $\mathbb{R}^k$",
            color=FG, fontsize=fs, ha="center", va="center")

    # --- 矢印 ---
    _arrow(ax, (7.5, 1.95), (9.6, 1.95), FG, lw=1.4)
    ax.text(8.55, 2.15, r"$\varphi^{-1}$", color=FG, fontsize=fs,
            ha="center", va="bottom")

    # --- 右: 曲がった M 上の曲線束と、速度が張る接平面 ---
    rx, ry = 14.6, 1.95
    S = _surface(rx, ry, sx, sy)
    _grid_patch(ax, rx, ry, sx, sy, -1, 1, -1, 1, GREY, 0.8, True)
    for d in dirs:
        t = np.linspace(-1, 1, 200) / max(abs(d[0]), abs(d[1]))
        ax.plot(*S(t * d[0], t * d[1]), color=ORANGE, lw=1.6, zorder=5)

    h = 1e-4
    du = (S(h, 0) - S(-h, 0)) / (2 * h)
    dv = (S(0, h) - S(0, -h)) / (2 * h)
    p = S(0.0, 0.0)
    _parallelogram(ax, p, 0.78 * du, 0.78 * dv, GREEN, lw=2.0, zorder=4)
    ax.plot(*p, "o", color=FG, ms=5, zorder=8)
    ax.text(rx, ry - sy - 0.5, r"curves through $p$ on $M$", color=FG,
            fontsize=fs, ha="center", va="center")
    ax.text(rx + 3.1, ry + 1.05, r"$T_pM$", color=GREEN, fontsize=fs,
            ha="left", va="center")

    ax.set_title(r"straight lines in $\mathbb{R}^k$ $\to$ curves on $M$ "
                 r"$\to$ their velocities fill $T_pM$", fontsize=fs)

    fig.savefig(output_dir / "tangent_chart.png")
    plt.close(fig)


def tangent_subspace(output_dir: Path) -> None:
    """平らな部分空間は自分自身が接空間: gamma(t) = t*w の速度が w になる."""
    style.apply()

    fig, ax = plt.subplots(figsize=style.slot(*SLOT_TANGENT_SUBSPACE))
    fs = style.SMALL_FONT_PT
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    _hide_axes(ax)

    o = np.array([4.7, 2.5])
    e1, e2 = np.array([2.8, 0.58]), np.array([1.2, 1.35])
    _parallelogram(ax, o, e1, e2, BLUE, lw=3.2, zorder=3)
    _parallelogram(ax, o, e1, e2, GREEN, lw=1.3, fill_alpha=0.0, zorder=5,
                   ls="--")

    # gamma(t) = t w : 原点から w へ向かう直線と、その速度ベクトル
    w = 0.62 * e1 + 0.30 * e2
    ax.plot([o[0] - w[0], o[0] + w[0]], [o[1] - w[1], o[1] + w[1]],
            color=ORANGE, lw=1.6, zorder=6)
    _arrow(ax, tuple(o), tuple(o + w), ORANGE, lw=2.0)
    ax.text(o[0] + w[0] + 0.12, o[1] + w[1] + 0.05, r"$\boldsymbol{w}$",
            color=ORANGE, fontsize=fs, ha="left", va="bottom")
    # 直線の下側、平行四辺形の辺に触れない位置に置く
    ax.text(3.5, 1.72, r"$\gamma(t) = t\boldsymbol{w}$", color=ORANGE,
            fontsize=fs, ha="center", va="top")

    ax.plot(*o, "o", color=FG, ms=5, zorder=8)
    ax.text(o[0] + 0.05, o[1] - 0.18, r"$\boldsymbol{0}$", color=FG,
            fontsize=fs, ha="left", va="top")
    ax.text(o[0] + e1[0] + e2[0] + 0.15, o[1] + e1[1] + e2[1], r"$E$",
            color=BLUE, fontsize=fs, ha="left", va="center")
    ax.text(0.4, 4.6, r"$T_{\boldsymbol{0}}E = E$", color=GREEN, fontsize=fs,
            ha="left", va="center")
    ax.set_title(r"every $\boldsymbol{w} \in E$ is itself a velocity",
                 fontsize=fs)

    fig.savefig(output_dir / "tangent_subspace.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 3. Eigenspace decomposition of a linear system
# ---------------------------------------------------------------------------

def eigenspaces(output_dir: Path) -> None:
    """R^n = E^s + E^u + E^c の模式図（E^s を面、E^u / E^c を直線に描く）."""
    style.apply()

    fig, ax = plt.subplots(figsize=style.slot(*SLOT_EIGENSPACES))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    _hide_axes(ax)
    fs = style.SMALL_FONT_PT

    ox, oy = 5.2, 4.9
    # 面は「床」に見えるよう平たく取る。E^u / E^c はこの平行四辺形の外へ
    # 突き抜ける向きに描かないと、投影の上で面内に見えてしまう。
    a = np.array([3.0, 0.45])    # 面の第1方向
    b = np.array([-1.3, -1.05])  # 面の第2方向

    corners = [(ox, oy) + a + b, (ox, oy) + a - b,
               (ox, oy) - a - b, (ox, oy) - a + b]
    ax.add_patch(Polygon(corners, closed=True, facecolor=BLUE, alpha=0.13,
                         edgecolor=BLUE, lw=1.2))
    # 面内を原点へ向かう流れ
    for d in (a, -a, b, -b, a + b, -(a + b), a - b, b - a):
        p = np.array([ox, oy]) + 0.92 * d
        q = np.array([ox, oy]) + 0.30 * d
        _arrow(ax, tuple(p), tuple(q), BLUE, lw=1.0)

    # E^u: 鉛直方向（面を貫いて両側へ出ていく）
    ax.plot([ox, ox], [oy - 3.0, oy + 3.5], color=RED, lw=1.6)
    _arrow(ax, (ox, oy + 1.3), (ox, oy + 3.4), RED, lw=1.4)
    _arrow(ax, (ox, oy - 1.3), (ox, oy - 2.9), RED, lw=1.4)

    # E^c: 面にも E^u にも属さない向き（中立なので両向きの矢印）
    cdir = np.array([-2.0, 2.0])
    ax.plot([ox - cdir[0], ox + cdir[0]], [oy - cdir[1], oy + cdir[1]],
            color=GREEN, lw=1.6)
    for sgn in (1, -1):
        p = np.array([ox, oy]) + sgn * 0.42 * cdir
        q = np.array([ox, oy]) + sgn * 0.92 * cdir
        # 両向きの矢印にして「伸びも縮みもしない」ことを示す
        _arrow(ax, tuple(p), tuple(q), GREEN, lw=1.0, style_="<|-|>")

    ax.plot(ox, oy, "o", color=FG, ms=7, zorder=8)

    # 各空間の名前と次元を現物のそばに置く（次元は本文で説明しなくて済む）
    ax.text(ox + 0.15, oy + 3.55, r"$E^u$  ($\dim 1$)", color=RED,
            fontsize=fs, ha="left", va="bottom")
    ax.text(ox + cdir[0] - 0.1, oy + cdir[1] + 0.25, r"$E^c$  ($\dim 1$)",
            color=GREEN, fontsize=fs, ha="center", va="bottom")
    ax.text(9.9, oy + a[1] - 0.45, r"$E^s$  ($\dim 2$)", color=BLUE,
            fontsize=fs, ha="right", va="top")

    # s / u / c の由来
    ax.text(0.1, 1.45, r"$E^s$: $s$ = stable,  $\mathrm{Re}\,\lambda < 0$",
            color=BLUE, fontsize=fs, ha="left", va="center")
    ax.text(0.1, 0.88, r"$E^u$: $u$ = unstable,  $\mathrm{Re}\,\lambda > 0$",
            color=RED, fontsize=fs, ha="left", va="center")
    ax.text(0.1, 0.31, r"$E^c$: $c$ = center,  $\mathrm{Re}\,\lambda = 0$",
            color=GREEN, fontsize=fs, ha="left", va="center")
    ax.set_title(r"$\dim$ = number of such eigenvalues", fontsize=fs)

    fig.savefig(output_dir / "eigenspaces.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 4. Stable / unstable manifolds: linear vs nonlinear
# ---------------------------------------------------------------------------

#: 双曲型固定点を持つ非線形系。原点で J = diag(1, -1) なのでサドル。
#: W^u は q_2 = q_1^2/6 + ...、W^s は q_1 = -q_2^2/6 + ... と曲がる。
#: 係数を 1/2 にしてあるのは、もう一方の固定点 (-2, 2) を描画範囲から
#: 十分遠ざけるため（近いと余計な渦が写り込んで主題がぼける）。
def _saddle_nl(t, q):
    x, y = q
    return [x + 0.5 * y**2, -y + 0.5 * x**2]


def stable_manifold(output_dir: Path) -> None:
    """線形の E^s / E^u と、非線形の W^s / W^u を並べる."""
    style.apply()

    fig, axes = plt.subplots(1, 2, figsize=style.slot(*SLOT_STABLE_MANIFOLD))
    fs = style.SMALL_FONT_PT
    lim = 1.3

    grid = np.linspace(-lim, lim, 26)
    X, Y = np.meshgrid(grid, grid)

    # --- 左: 線形 ---
    ax = axes[0]
    ax.streamplot(X, Y, X, -Y, color=GREY, linewidth=0.55,
                  density=1.0, arrowsize=0.7)
    ax.plot([-lim, lim], [0, 0], color=RED, lw=2.0, zorder=5)
    ax.plot([0, 0], [-lim, lim], color=BLUE, lw=2.0, zorder=5)
    ax.text(1.18, 0.1, r"$E^u$", color=RED, fontsize=fs, ha="right",
            va="bottom")
    ax.text(0.12, 1.16, r"$E^s$", color=BLUE, fontsize=fs, ha="left",
            va="top")
    ax.set_title(r"Linear: $\dot{\xi} = J\xi$", fontsize=fs)

    # --- 右: 非線形 ---
    ax = axes[1]
    U = X + 0.5 * Y**2
    V = -Y + 0.5 * X**2
    ax.streamplot(X, Y, U, V, color=GREY, linewidth=0.55,
                  density=1.0, arrowsize=0.7)
    # 接線（= 固有空間）を破線で重ねると、接していることが読める
    ax.plot([-lim, lim], [0, 0], color=GREY, lw=0.9, ls="--", alpha=0.9)
    ax.plot([0, 0], [-lim, lim], color=GREY, lw=0.9, ls="--", alpha=0.9)

    eps = 1e-7
    for sgn in (1.0, -1.0):
        xs, ys = _integrate(_saddle_nl, (sgn * eps, 0.0), 22.0, max_r=2.0)
        ax.plot(xs, ys, color=RED, lw=2.0, zorder=5)
        xs, ys = _integrate(_saddle_nl, (0.0, sgn * eps), -22.0, max_r=2.0)
        ax.plot(xs, ys, color=BLUE, lw=2.0, zorder=5)

    ax.text(1.18, 0.40, r"$W^u$", color=RED, fontsize=fs, ha="right",
            va="bottom")
    ax.text(-0.42, 1.16, r"$W^s$", color=BLUE, fontsize=fs, ha="right",
            va="top")
    ax.set_title(r"Nonlinear: $\dot{q} = f(q)$", fontsize=fs)

    for ax in axes:
        ax.plot(0, 0, "s", color=ORANGE, ms=7, zorder=7)
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.set_xticks([-1, 0, 1])
        ax.set_yticks([-1, 0, 1])
        ax.set_xlabel(r"$q_1$")
    axes[0].set_ylabel(r"$q_2$")
    axes[1].set_yticklabels([])

    fig.savefig(output_dir / "stable_manifold.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 5. The pendulum separatrix *is* a pair of invariant manifolds
# ---------------------------------------------------------------------------

def pendulum_manifolds(output_dir: Path) -> None:
    """振り子のセパラトリクスを、2つのサドルの W^s / W^u として描き分ける.

    サドルを q_1^* (theta = -pi), q_2^* (theta = pi) と名付け、全ての枝に
    どのサドルの多様体かを書く。紫の弧は一方の W^u と他方の W^s が一致した部分。
    """
    style.apply()

    fig, ax = plt.subplots(figsize=style.slot(*SLOT_PENDULUM_MANIFOLDS))
    fs = style.SMALL_FONT_PT
    lim = 4.3
    pi = np.pi

    def sep(theta):
        return 2.0 * np.abs(np.cos(theta / 2.0))

    # 背景: 振動軌道と回転軌道（ラベルの置き場を空けるため本数を絞る）
    th = np.linspace(-lim, lim, 900)
    for H in (-0.55, 0.0):
        y2 = 2 * (H + np.cos(th))
        m = y2 > 0
        for s in (1, -1):
            yy = np.where(m, s * np.sqrt(np.maximum(y2, 0)), np.nan)
            ax.plot(th, yy, color=GREY, lw=0.6, alpha=0.55)
    for H in (4.5,):   # 弧のラベルにかからないよう十分外側の回転軌道
        y2 = 2 * (H + np.cos(th))
        for s in (1, -1):
            ax.plot(th, s * np.sqrt(y2), color=GREY, lw=0.6, alpha=0.55)

    # --- 2つのサドルを結ぶ弧（紫）: 一方の W^u = 他方の W^s ---
    thm = np.linspace(-pi, pi, 600)
    ax.plot(thm, sep(thm), color=PURPLE, lw=2.0, zorder=5)
    ax.plot(thm, -sep(thm), color=PURPLE, lw=2.0, zorder=5)
    _arrow(ax, (-0.35, sep(-0.35)), (0.35, sep(0.35)), PURPLE, lw=1.8)
    _arrow(ax, (0.35, -sep(0.35)), (-0.35, -sep(-0.35)), PURPLE, lw=1.8)
    ax.text(0.0, 2.32, r"$W^u(q_1^*) = W^s(q_2^*)$", color=PURPLE,
            fontsize=fs, ha="center", va="bottom")
    ax.text(0.0, -2.32, r"$W^u(q_2^*) = W^s(q_1^*)$", color=PURPLE,
            fontsize=fs, ha="center", va="top")

    # --- 外側の枝: 相手のサドルに届かない W^s (青) / W^u (赤) ---
    tr = np.linspace(pi, lim, 300)
    tl = np.linspace(-lim, -pi, 300)
    ax.plot(tr, sep(tr), color=RED, lw=2.0, zorder=5)      # W^u(q_2^*)
    ax.plot(tl, -sep(tl), color=RED, lw=2.0, zorder=5)     # W^u(q_1^*)
    ax.plot(tr, -sep(tr), color=BLUE, lw=2.0, zorder=5)    # W^s(q_2^*)
    ax.plot(tl, sep(tl), color=BLUE, lw=2.0, zorder=5)     # W^s(q_1^*)
    _arrow(ax, (pi + 0.25, sep(pi + 0.25)), (pi + 0.62, sep(pi + 0.62)),
           RED, lw=1.5)
    _arrow(ax, (-pi - 0.25, -sep(-pi - 0.25)),
           (-pi - 0.62, -sep(-pi - 0.62)), RED, lw=1.5)
    _arrow(ax, (pi + 0.62, -sep(pi + 0.62)), (pi + 0.25, -sep(pi + 0.25)),
           BLUE, lw=1.5)
    _arrow(ax, (-pi - 0.62, sep(-pi - 0.62)), (-pi - 0.25, sep(-pi - 0.25)),
           BLUE, lw=1.5)
    ax.text(lim - 0.05, 1.3, r"$W^u(q_2^*)$", color=RED,
            fontsize=fs, ha="right", va="bottom")
    ax.text(-lim + 0.05, -1.3, r"$W^u(q_1^*)$", color=RED,
            fontsize=fs, ha="left", va="top")
    ax.text(lim - 0.05, -1.3, r"$W^s(q_2^*)$", color=BLUE,
            fontsize=fs, ha="right", va="top")
    ax.text(-lim + 0.05, 1.3, r"$W^s(q_1^*)$", color=BLUE,
            fontsize=fs, ha="left", va="bottom")

    # 固定点
    ax.plot(0, 0, "o", color=FG, ms=6, zorder=7)
    for xs in (-pi, pi):
        ax.plot(xs, 0, "s", color=ORANGE, ms=8, zorder=7)

    # 領域のラベル（セパラトリクスが分ける 2 つの領域）
    ax.text(2.3, 3.32, "rotation", color=GREY, fontsize=fs, ha="center",
            va="center")
    ax.text(0.0, -0.52, "libration", color=GREY, fontsize=fs, ha="center",
            va="center")

    ax.set_xlim(-lim, lim)
    ax.set_ylim(-3.7, 3.7)
    ax.set_xlabel(r"$\theta$")
    ax.set_ylabel(r"$\omega$")
    ax.set_xticks([-pi, 0, pi])
    ax.set_xticklabels([r"$-\pi\ (q_1^*)$", r"$0$", r"$\pi\ (q_2^*)$"])
    ax.set_yticks([-2, 0, 2])

    fig.savefig(output_dir / "pendulum_manifolds.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 6. Homoclinic / heteroclinic connections
# ---------------------------------------------------------------------------

def connections(output_dir: Path) -> None:
    """ホモクリニック軌道とヘテロクリニック軌道の対比."""
    style.apply()

    fig, axes = plt.subplots(1, 2, figsize=style.slot(*SLOT_CONNECTIONS))
    fs = style.SMALL_FONT_PT

    # 左右の並びは connection_energy（次ページの図）と揃える: 左 = 振り子、右 = Duffing。

    # --- 右: ホモクリニック（Duffing: H = y^2/2 - x^2/2 + x^4/4 = 0）---
    # 右ループは上半分が W^u（y > 0 なので原点から離れる）、下半分が W^s。
    # 左ループはその鏡像なので、上半分が W^s、下半分が W^u になる。
    ax = axes[1]
    xr = np.linspace(0.0, np.sqrt(2.0), 500)
    env = xr * np.sqrt(np.maximum(1.0 - xr**2 / 2.0, 0.0))
    ax.plot(xr, env, color=RED, lw=2.0)        # W^u (right, upper)
    ax.plot(xr, -env, color=BLUE, lw=2.0)      # W^s (right, lower)
    ax.plot(-xr, env, color=BLUE, lw=2.0)      # W^s (left, upper)
    ax.plot(-xr, -env, color=RED, lw=2.0)      # W^u (left, lower)

    def _env(v):
        return v * np.sqrt(max(1.0 - v**2 / 2.0, 0.0))

    _arrow(ax, (0.22, _env(0.22)), (0.55, _env(0.55)), RED, lw=1.6)
    _arrow(ax, (0.55, -_env(0.55)), (0.22, -_env(0.22)), BLUE, lw=1.6)
    _arrow(ax, (-0.55, _env(0.55)), (-0.22, _env(0.22)), BLUE, lw=1.6)
    _arrow(ax, (-0.22, -_env(0.22)), (-0.55, -_env(0.55)), RED, lw=1.6)

    ax.plot(0, 0, "s", color=ORANGE, ms=8, zorder=6)
    ax.text(0.0, 0.16, r"$q^*$", color=ORANGE, fontsize=fs, ha="center",
            va="bottom")
    ax.text(1.05, 0.80, r"$W^u$", color=RED, fontsize=fs, ha="center",
            va="bottom")
    ax.text(1.05, -0.80, r"$W^s$", color=BLUE, fontsize=fs, ha="center",
            va="top")
    ax.set_title(r"Homoclinic: $W^u(q^*) \cap W^s(q^*)$", fontsize=fs)
    ax.set_xlim(-1.75, 1.75)
    ax.set_ylim(-1.3, 1.45)

    # --- 左: ヘテロクリニック（振り子型）---
    ax = axes[0]
    t = np.linspace(-np.pi, np.pi, 600)
    ax.plot(t, 2 * np.cos(t / 2), color=PURPLE, lw=2.0)
    ax.plot(t, -2 * np.cos(t / 2), color=PURPLE, lw=2.0)
    _arrow(ax, (-0.4, 2 * np.cos(-0.2)), (0.4, 2 * np.cos(0.2)),
           PURPLE, lw=1.6)
    _arrow(ax, (0.4, -2 * np.cos(0.2)), (-0.4, -2 * np.cos(-0.2)),
           PURPLE, lw=1.6)
    for xs, lab in ((-np.pi, r"$q_1^*$"), (np.pi, r"$q_2^*$")):
        ax.plot(xs, 0, "s", color=ORANGE, ms=8, zorder=6)
        ax.text(xs, -0.32, lab, color=ORANGE, fontsize=fs, ha="center",
                va="top")
    ax.text(0.0, 2.28, r"$W^u(q_1^*) = W^s(q_2^*)$", color=PURPLE,
            fontsize=fs, ha="center", va="bottom")
    ax.set_title(r"Heteroclinic: $W^u(q_1^*) \cap W^s(q_2^*)$", fontsize=fs)
    ax.set_xlim(-4.0, 4.0)
    ax.set_ylim(-2.6, 2.9)

    for ax in axes:
        _hide_axes(ax)

    fig.savefig(output_dir / "connections.png")
    plt.close(fig)


def connection_energy(output_dir: Path) -> None:
    """接続軌道 = 山の頂上と同じエネルギーの運動、をポテンシャルで描く.

    横線はエネルギー E の運動が動ける範囲 (V <= E)。山より低い = 内側、
    ちょうど同じ = 接続軌道、高い = 外側。左右の並びは connections と揃える。
    """
    style.apply()

    fig, axes = plt.subplots(1, 2, figsize=style.slot(*SLOT_CONNECTION_ENERGY))
    fs = style.SMALL_FONT_PT

    def _panel(ax, V, x_lo, x_hi, tops, bottoms, levels, title):
        x = np.linspace(x_lo, x_hi, 800)
        ax.plot(x, V(x), color=FG, lw=1.6, zorder=3)
        for (E, color, label, lx, ly) in levels:
            m = V(x) <= E + 1e-9
            ax.plot(x, np.where(m, E, np.nan), color=color, lw=2.2, zorder=4)
            ax.text(lx, ly, label, color=color, fontsize=fs, ha="center",
                    va="center")
        for xt in tops:
            ax.plot(xt, V(xt), "s", color=ORANGE, ms=7, zorder=6)
        for xb in bottoms:
            ax.plot(xb, V(xb), "o", color=FG, ms=5, zorder=6)
        ax.set_title(title, fontsize=fs)
        ax.set_xlim(x_lo, x_hi)
        _hide_axes(ax)

    # --- 左: 振り子 V = -cos(theta)。山の頂上 = サドル (theta = ±pi) ---
    pi = np.pi
    _panel(
        axes[0], lambda t: -np.cos(t), -1.3 * pi, 1.3 * pi,
        tops=(-pi, pi), bottoms=(0.0,),
        levels=(
            (-0.3, GREEN, "inside", 0.0, -0.08),
            (1.0, PURPLE, "connecting orbit", 0.0, 1.22),
            (1.75, LIGHT_GREY, "outside", 0.0, 1.97),
        ),
        title=r"Pendulum: $V = -\cos\theta$",
    )
    axes[0].set_ylim(-1.2, 2.2)

    # --- 右: Duffing V = -x^2/2 + x^4/4。山の頂上 = サドル (x = 0) ---
    _panel(
        axes[1], lambda x: -x**2 / 2 + x**4 / 4, -1.7, 1.7,
        tops=(0.0,), bottoms=(-1.0, 1.0),
        levels=(
            (-0.18, GREEN, "inside", 0.0, -0.23),
            (0.0, PURPLE, "connecting orbit", 0.0, 0.08),
            (0.42, LIGHT_GREY, "outside", 0.0, 0.5),
        ),
        title=r"Duffing: $V = -x^2/2 + x^4/4$",
    )
    axes[1].set_ylim(-0.31, 0.66)

    fig.savefig(output_dir / "connection_energy.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 7. Center manifold: fast collapse + slow dynamics
# ---------------------------------------------------------------------------

def center_manifold(output_dir: Path) -> None:
    """W^c は E^c に接し、双曲方向は指数的に潰れる（縮約の絵）."""
    style.apply()

    fig, ax = plt.subplots(figsize=style.slot(*SLOT_CENTER_MANIFOLD))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    _hide_axes(ax)
    fs = style.SMALL_FONT_PT

    ox, oy = 5.0, 6.5
    k = 0.135
    u = np.linspace(-4.1, 4.1, 300)

    # E^c（接線）と W^c（曲線）
    ax.plot([ox - 4.3, ox + 4.3], [oy, oy], color=GREY, lw=1.0, ls="--")
    ax.text(ox + 4.35, oy + 0.1, r"$E^c$", color=GREY, fontsize=fs,
            ha="left", va="bottom")
    ax.plot(ox + u, oy - k * u**2, color=GREEN, lw=2.2, zorder=5)
    ax.text(ox - 4.35, oy - k * 4.1**2 - 0.2, r"$W^c$", color=GREEN,
            fontsize=fs, ha="left", va="top")

    # 双曲方向（速い）
    for du in (-3.2, -1.9, 1.9, 3.2):
        y0 = oy - k * du**2
        _arrow(ax, (ox + du, y0 + 2.3), (ox + du, y0 + 0.45), ORANGE, lw=1.1)
        _arrow(ax, (ox + du, y0 - 1.75), (ox + du, y0 - 0.45), ORANGE, lw=1.1)
    ax.text(ox - 1.4, oy + 2.55, r"fast: $\sim e^{-at}$", color=ORANGE,
            fontsize=fs, ha="center", va="bottom")

    # W^c 上の遅い流れ
    for du in (2.9, -2.9):
        _arrow(ax, (ox + du, oy - k * du**2),
               (ox + du * 0.42, oy - k * (du * 0.42) ** 2), GREEN, lw=1.6)
    ax.plot(ox, oy, "o", color=FG, ms=7, zorder=8)
    ax.text(ox, 3.5, "slow: reduced dynamics",
            color=GREEN, fontsize=fs, ha="center", va="top")

    ax.text(5.0, 1.3, r"$\dim W^c = \dim E^c$,   tangent at $q^*$",
            color=FG, fontsize=fs, ha="center", va="center")

    fig.savefig(output_dir / "center_manifold.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 8. Worked example of a center-manifold reduction
# ---------------------------------------------------------------------------

def _cm_example(t, q):
    """dx/dt = x y, dy/dt = -y - x^2 （原点で lambda = 0, -1）."""
    x, y = q
    return [x * y, -y - x**2]


def _h(x):
    """W^c の局所展開 y = h(x) = -x^2 - 2x^4 + ...."""
    return -x**2 - 2 * x**4


def center_manifold_example(output_dir: Path) -> None:
    """例 (xy, -y-x^2): 相図と W^c、および x(t) の比較."""
    style.apply()

    fig, axes = plt.subplots(
        1, 2, figsize=style.slot(*SLOT_CM_EXAMPLE),
        width_ratios=[1.25, 1.0])
    fs = style.SMALL_FONT_PT

    # --- 左: 相図と W^c ---
    ax = axes[0]
    xl, yl = 0.62, (-0.78, 0.34)
    gx = np.linspace(-xl, xl, 30)
    gy = np.linspace(yl[0], yl[1], 30)
    X, Y = np.meshgrid(gx, gy)
    ax.streamplot(X, Y, X * Y, -Y - X**2, color=GREY, linewidth=0.55,
                  density=1.15, arrowsize=0.7)

    ax.axhline(0.0, color=ORANGE, lw=1.1, ls="--")
    ax.text(-xl + 0.03, 0.035, r"$E^c$: $y = 0$", color=ORANGE, fontsize=fs,
            ha="left", va="bottom")

    xs = np.linspace(-0.58, 0.58, 400)
    ax.plot(xs, _h(xs), color=GREEN, lw=2.2, zorder=5)
    ax.text(0.0, -0.15, r"$W^c$", color=GREEN, fontsize=fs,
            ha="center", va="top")
    for x0 in (0.46, -0.46):
        _arrow(ax, (x0, _h(x0)), (x0 * 0.66, _h(x0 * 0.66)), GREEN, lw=1.7)

    ax.plot(0, 0, "o", color=RED, ms=7, zorder=7)
    ax.set_xlim(-xl, xl)
    ax.set_ylim(*yl)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.set_xticks([-0.5, 0, 0.5])
    ax.set_yticks([-0.6, -0.3, 0])
    ax.set_title(r"$\dot{x} = xy,\;\; \dot{y} = -y - x^2$", fontsize=fs)

    # --- 右: x(t) の比較 ---
    ax = axes[1]
    x0 = 0.5
    t = np.linspace(0, 30, 600)
    sol = solve_ivp(_cm_example, (0, 30), [x0, 0.0], t_eval=t,
                    rtol=1e-10, atol=1e-13)
    ax.plot(sol.t, sol.y[0], color=BLUE, lw=1.6)
    ax.plot(t, x0 / np.sqrt(1 + 2 * x0**2 * t), color=GREEN, lw=1.4, ls="--")
    ax.axhline(x0, color=ORANGE, lw=1.2, ls=":")

    ax.text(29.0, 0.505, r"on $E^c$: $\dot{x} = 0$", color=ORANGE,
            fontsize=fs, ha="right", va="bottom")
    ax.text(16.0, 0.30, "full system", color=BLUE, fontsize=fs,
            ha="left", va="bottom")
    ax.text(12.5, 0.062, r"reduced $\dot{x} = -x^3$", color=GREEN,
            fontsize=fs, ha="left", va="top")
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 0.62)
    ax.set_xlabel(r"$t$")
    ax.set_ylabel(r"$x(t)$")
    ax.set_yticks([0, 0.25, 0.5])
    ax.set_title(r"decay from $x(0) = 0.5$", fontsize=fs)

    fig.savefig(output_dir / "center_manifold_example.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 9. Center manifolds are not unique
# ---------------------------------------------------------------------------

def center_manifold_nonuniqueness(output_dir: Path) -> None:
    """dx/dt = x^2, dy/dt = -y には中心多様体が無限個ある."""
    style.apply()

    fig, ax = plt.subplots(figsize=style.slot(*SLOT_CM_NONUNIQUE))
    fs = style.SMALL_FONT_PT

    xlim = (-2.2, 1.0)
    gx = np.linspace(*xlim, 30)
    gy = np.linspace(-1.0, 1.0, 30)
    X, Y = np.meshgrid(gx, gy)
    ax.streamplot(X, Y, X**2, -Y, color=GREY, linewidth=0.5,
                  density=0.9, arrowsize=0.7)

    xn = np.linspace(xlim[0], -1e-3, 500)
    for C in (0.78, 0.34, -0.34, -0.78):
        ax.plot(xn, C * np.exp(1.0 / xn), color=GREEN, lw=1.6, alpha=0.9)
    # y = 0（C = 0 に対応する枝）と x >= 0 側の共通部分
    ax.plot([xlim[0], xlim[1]], [0, 0], color=GREEN, lw=2.0)

    ax.plot(0, 0, "o", color=RED, ms=7, zorder=7)
    ax.text(-2.15, 0.72, r"$y = C\,e^{1/x}$   ($x < 0$)", color=GREEN,
            fontsize=fs, ha="left", va="center")
    ax.text(0.95, -0.12, r"$y = 0$   ($x \geq 0$)", color=GREEN,
            fontsize=fs, ha="right", va="top")

    ax.set_xlim(*xlim)
    ax.set_ylim(-0.85, 0.85)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.set_xticks([-2, -1, 0, 1])
    ax.set_yticks([-0.5, 0, 0.5])

    fig.savefig(output_dir / "center_manifold_nonuniqueness.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 11. A center is structurally fragile
# ---------------------------------------------------------------------------

def pendulum_perturbation(output_dir: Path) -> None:
    """減衰項 -eps*omega を入れると、センターが両側へ壊れる."""
    style.apply()

    fig, axes = plt.subplots(
        1, 3, figsize=style.slot(*SLOT_PENDULUM_PERTURBATION))
    fs = style.SMALL_FONT_PT
    lim = 1.55

    cases = [
        (-0.5, RED, "Unstable"),
        (0.0, GREEN, "Center"),
        (0.5, BLUE, "Stable"),
    ]
    grid = np.linspace(-lim, lim, 28)
    X, Y = np.meshgrid(grid, grid)

    for ax, (epsv, color, name) in zip(axes, cases):
        U = Y
        V = -np.sin(X) - epsv * Y
        ax.streamplot(X, Y, U, V, color=color, linewidth=0.6,
                      density=1.15, arrowsize=0.75)
        ax.plot(0, 0, "o", color=FG, ms=6, zorder=6)
        # タイトルは1行に収める（2行にすると図の高さが 20px 増える）
        ax.set_title(f"{name}  ($\\varepsilon = {epsv:g}$)",
                     fontsize=fs, color=color)
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.set_xticks([-1, 0, 1])
        ax.set_yticks([-1, 0, 1])
        ax.set_xlabel(r"$\theta$")

    axes[0].set_ylabel(r"$\omega$")
    for ax in axes[1:]:
        ax.set_yticklabels([])

    fig.savefig(output_dir / "pendulum_perturbation.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def generate_all(output_dir: Path) -> None:
    """Generate all Chapter 2 figures."""
    chapter_overview(output_dir)
    invariant_set(output_dir)
    manifold_chart(output_dir)
    tangent_space(output_dir)
    tangent_chart(output_dir)
    tangent_subspace(output_dir)
    eigenspaces(output_dir)
    stable_manifold(output_dir)
    pendulum_manifolds(output_dir)
    connections(output_dir)
    connection_energy(output_dir)
    center_manifold(output_dir)
    center_manifold_example(output_dir)
    center_manifold_nonuniqueness(output_dir)
    pendulum_perturbation(output_dir)
    print("  Ch.2 figures generated.")
