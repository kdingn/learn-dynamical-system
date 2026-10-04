"""翼断面の2自由度モデル（typical section）— フラッターの最小模型.

上下の並進（plunge）$h$ とねじれ（pitch）$\\alpha$ の2自由度を、ばねで支えた
剛体の翼断面で表す。空気力は準定常近似（揚力傾斜 $2\\pi$、空力中心は 1/4 翼弦）。
無次元化は Hodges & Pierce, *Introduction to Structural Dynamics and
Aeroelasticity* に倣い、長さを半翼弦 $b$、時間を $1/\\omega_\\alpha$ で測る。

状態は $\\boldsymbol{q} = (h/b,\\ \\alpha,\\ h'/b,\\ \\alpha')$ の4次元、
パラメータは無次元流速 $V = U / (b\\,\\omega_\\alpha)$ で、

    M q'' + (C + C_a(V)) q' + (K + K_a(V)) q = 0

を1階の系 $\\dot{\\boldsymbol{q}} = A(V)\\,\\boldsymbol{q}$ に直したものを返す。

非線形性はねじりばねの3次の項だけを入れる: ねじりの復元力 $r_\\alpha^2 \\alpha$ を
$r_\\alpha^2 (\\alpha + \\kappa \\alpha^3)$ にする（$\\kappa > 0$ で硬化、$\\kappa < 0$ で軟化）。
フラッターの振幅の飽和や急成長を調べる空力弾性の標準的な模型である。
"""

from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


@dataclass(frozen=True)
class TypicalSection:
    mu: float = 20.0      # 質量比 m / (pi rho b^2)
    x_alpha: float = 0.2  # 重心と弾性軸の距離 / b
    r_alpha: float = 0.5  # 弾性軸まわりの回転半径 / b
    sigma: float = 0.4    # 振動数比 omega_h / omega_alpha
    a: float = -0.4       # 弾性軸の位置 / b（翼弦中点から後ろ向き正）
    zeta: float = 0.005   # 構造減衰比（両方向とも）

    def matrix(self, V: float) -> np.ndarray:
        """流速 V での 4x4 の状態行列 A(V)."""
        ra2 = self.r_alpha**2
        M = np.array([[1.0, self.x_alpha], [self.x_alpha, ra2]])
        K = np.diag([self.sigma**2, ra2])
        C = np.diag([2 * self.zeta * self.sigma, 2 * self.zeta * ra2])
        # 揚力 L = (2/mu) (V^2 alpha + V h')、弾性軸まわりのモーメント = e L
        e = 0.5 + self.a  # 空力中心（1/4 翼弦）から弾性軸までの腕 / b
        k = 2.0 / self.mu
        Ka = k * np.array([[0.0, V**2], [0.0, -e * V**2]])
        Ca = k * np.array([[V, 0.0], [-e * V, 0.0]])
        Mi = np.linalg.inv(M)
        return np.block([
            [np.zeros((2, 2)), np.eye(2)],
            [-Mi @ (K + Ka), -Mi @ (C + Ca)],
        ])

    def growth_rate(self, V: float) -> float:
        """最も不安定な固有値の実部 max Re(lambda)."""
        return float(np.linalg.eigvals(self.matrix(V)).real.max())

    def flutter_speed(self, lo: float = 0.1, hi: float = 4.0) -> float:
        """max Re(lambda) = 0 となる流速 V_F."""
        return brentq(self.growth_rate, lo, hi)

    def response(self, V: float, q0, t: np.ndarray) -> np.ndarray:
        """線形系の解 q(t) = exp(A t) q0 を、固有値分解で評価する（shape: len(t) x 4）."""
        lam, vec = np.linalg.eig(self.matrix(V))
        c = np.linalg.solve(vec, np.asarray(q0, dtype=complex))
        return (vec @ (c[:, None] * np.exp(np.outer(lam, t)))).real.T

    # --- 非線形（ねじりばねの3次の項） ---------------------------------------

    def _cubic_direction(self) -> np.ndarray:
        """非線形項 kappa * alpha^3 * d の向き d（状態の4成分）."""
        ra2 = self.r_alpha**2
        M = np.array([[1.0, self.x_alpha], [self.x_alpha, ra2]])
        return np.concatenate([[0.0, 0.0], -np.linalg.solve(M, [0.0, ra2])])

    def simulate(self, V: float, kappa: float, q0, t: np.ndarray,
                 alpha_max: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
        """非線形系を数値積分する。|alpha| が alpha_max を超えたら打ち切る.

        返り値は (t, q)（q の shape は len(t) x 4）。打ち切った場合は短くなる。
        """
        A, d = self.matrix(V), self._cubic_direction()

        def rhs(_, x):
            return A @ x + kappa * x[1] ** 3 * d

        def blow_up(_, x):
            return abs(x[1]) - alpha_max
        blow_up.terminal = True

        sol = solve_ivp(rhs, (t[0], t[-1]), np.asarray(q0, dtype=float),
                        t_eval=t, events=blow_up, rtol=1e-9, atol=1e-11)
        return sol.t, sol.y.T

    def center_normal_form(self, V: float, kappa: float) -> dict:
        """虚軸上の固有値の対について、中心多様体上の正規形の係数を求める.

        正規形 dz/dt = i omega z + c1 |z|^2 z の Re(c1) と、状態 q = z v + conj(z v) + ...
        の対応（ねじれ角の振幅 = 2 |v_alpha| |z|）を返す。非線形項が3次だけ（2次がない）
        なので、Kuznetsov (Elements of Applied Bifurcation Theory, 3.5) の公式は
        c1 = <p, C(v, v, conj(v))> / 2 に簡約される（<p, v> = 1, A^T p = -i omega p）。
        """
        A = self.matrix(V)
        lam, vecs = np.linalg.eig(A)
        k = int(np.argmin(np.abs(lam.real) + 10.0 * (lam.imag <= 0)))
        omega, v = lam[k].imag, vecs[:, k]
        lam_t, vecs_t = np.linalg.eig(A.T)
        p = vecs_t[:, int(np.argmin(np.abs(lam_t - np.conj(lam[k]))))]
        p = p / np.conj(np.vdot(p, v))  # <p, v> = conj(p)^T v = 1
        # N(x) = kappa alpha^3 d の3重線形形式: C(x, y, z) = 6 kappa x_a y_a z_a d
        C = 6.0 * kappa * v[1] * v[1] * np.conj(v[1]) * self._cubic_direction()
        c1 = 0.5 * np.vdot(p, C)
        return {"re_c1": float(c1.real), "omega": float(omega),
                "alpha_per_z": float(2.0 * abs(v[1])),
                "other_eigenvalues": lam[np.abs(np.arange(4) - k) > 0]}
