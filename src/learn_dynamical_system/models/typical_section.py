"""翼断面の2自由度モデル（typical section）— フラッターの最小模型.

上下の並進（plunge）$h$ とねじれ（pitch）$\\alpha$ の2自由度を、ばねで支えた
剛体の翼断面で表す。空気力は準定常近似（揚力傾斜 $2\\pi$、空力中心は 1/4 翼弦）。
無次元化は Hodges & Pierce, *Introduction to Structural Dynamics and
Aeroelasticity* に倣い、長さを半翼弦 $b$、時間を $1/\\omega_\\alpha$ で測る。

状態は $\\boldsymbol{q} = (h/b,\\ \\alpha,\\ h'/b,\\ \\alpha')$ の4次元、
パラメータは無次元流速 $V = U / (b\\,\\omega_\\alpha)$ で、

    M q'' + (C + C_a(V)) q' + (K + K_a(V)) q = 0

を1階の系 $\\dot{\\boldsymbol{q}} = A(V)\\,\\boldsymbol{q}$ に直したものを返す。
"""

from dataclasses import dataclass

import numpy as np
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
