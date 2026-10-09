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
軟化ばねの振幅が大きいところで再び硬くなる場合を調べるため、5次の項
$\\kappa_5 \\alpha^5$ も足せるようにしてある（既定は $\\kappa_5 = 0$）。
"""

from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, fsolve


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

    def _rhs(self, V: float, kappa: float, kappa5: float = 0.0):
        """非線形系の右辺 A(V) q + (kappa alpha^3 + kappa5 alpha^5) d."""
        A, d = self.matrix(V), self._cubic_direction()

        def rhs(_, x):
            return A @ x + (kappa * x[1] ** 3 + kappa5 * x[1] ** 5) * d
        return rhs

    def simulate(self, V: float, kappa: float, q0, t: np.ndarray,
                 alpha_max: float = 1.0,
                 kappa5: float = 0.0) -> tuple[np.ndarray, np.ndarray]:
        """非線形系を数値積分する。|alpha| が alpha_max を超えたら打ち切る.

        返り値は (t, q)（q の shape は len(t) x 4）。打ち切った場合は短くなる。
        """
        rhs = self._rhs(V, kappa, kappa5)

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

    # --- 周期軌道（リミットサイクル振動, LCO） ---------------------------------

    def _monodromy(self, V: float, kappa: float, kappa5: float,
                   q0: np.ndarray, period: float) -> tuple[np.ndarray, np.ndarray]:
        """q0 から1周期積分した点 q(T) と、変分方程式によるモノドロミー行列 dq(T)/dq0."""
        A, d = self.matrix(V), self._cubic_direction()

        def rhs(_, y):
            x, Phi = y[:4], y[4:].reshape(4, 4)
            a = x[1]
            dx = A @ x + (kappa * a**3 + kappa5 * a**5) * d
            Jx = A + np.outer(d, [0.0, 3 * kappa * a**2 + 5 * kappa5 * a**4, 0.0, 0.0])
            return np.concatenate([dx, (Jx @ Phi).ravel()])

        y0 = np.concatenate([q0, np.eye(4).ravel()])
        sol = solve_ivp(rhs, (0.0, period), y0, method="DOP853",
                        rtol=1e-10, atol=1e-12)
        return sol.y[:4, -1], sol.y[4:, -1].reshape(4, 4)

    def periodic_orbit(self, amplitude: float, kappa: float, kappa5: float = 0.0,
                       guess: dict | None = None) -> dict:
        """ねじれ角の振幅が amplitude の周期軌道と、それが存在する流速 V を求める.

        振幅を固定して流速を未知数にする（振幅で枝をたどるので、枝が折り返す
        サドルノードの点でも解ける）。位相は「alpha が最大 = alpha' = 0」の点で固定し、
        未知数 (h, h', V, T) を q(T) = q(0) の4本の式で決める（射撃法）。
        guess を省くと、フラッター速度での固有ベクトルと正規形の予測から始める。

        返り値: V, period, q0（alpha 最大の点の状態）, multipliers（Floquet 乗数のうち
        自明な 1 を除いた3つ）, stable（3つとも単位円の内側か）。
        """
        if guess is None:
            v_f = self.flutter_speed()
            lam, vecs = np.linalg.eig(self.matrix(v_f))
            k = int(np.argmin(np.abs(lam.real) + 10.0 * (lam.imag <= 0)))
            q0 = (amplitude * vecs[:, k] / vecs[1, k]).real
            nf = self.center_normal_form(v_f, kappa)
            target = -nf["re_c1"] * (amplitude / nf["alpha_per_z"]) ** 2
            V = brentq(lambda s: self.growth_rate(s) - target, 0.5 * v_f, 1.5 * v_f)
            guess = {"V": V, "period": 2 * np.pi / lam[k].imag, "q0": q0}

        def residual(u):
            h, hd, V, T = u
            q0 = np.array([h, amplitude, hd, 0.0])
            qT, _ = self._monodromy(V, kappa, kappa5, q0, T)
            return qT - q0

        u0 = [guess["q0"][0], guess["q0"][2], guess["V"], guess["period"]]
        u, _, ok, msg = fsolve(residual, u0, full_output=True, xtol=1e-11)
        if ok != 1:
            raise RuntimeError(f"periodic orbit (amplitude={amplitude}) not found: {msg}")
        h, hd, V, T = u
        q0 = np.array([h, amplitude, hd, 0.0])
        _, M = self._monodromy(V, kappa, kappa5, q0, T)
        mult = np.linalg.eigvals(M)
        mult = np.delete(mult, int(np.argmin(np.abs(mult - 1.0))))
        return {"V": float(V), "period": float(T), "q0": q0,
                "multipliers": mult, "stable": bool(np.all(np.abs(mult) < 1.0))}

    def lco_branch(self, amplitudes, kappa: float, kappa5: float = 0.0) -> dict:
        """振幅の列に沿って周期軌道の枝をたどる（前の解を次の初期値にする）.

        返り値は amplitude, V, stable の配列。amplitudes は小さい順に与える。
        """
        out = {"amplitude": [], "V": [], "stable": []}
        guess = None
        for a in amplitudes:
            orb = self.periodic_orbit(float(a), kappa, kappa5, guess)
            guess = orb
            out["amplitude"].append(float(a))
            out["V"].append(orb["V"])
            out["stable"].append(orb["stable"])
        return {k: np.array(v) for k, v in out.items()}
