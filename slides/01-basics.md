---
theme: default
title: "Ch.1 力学系の基礎と線形安定性"
drawings:
  persist: false
---

# 力学系の基礎と線形安定性

Chapter 1 — Learn Dynamical Systems

<div class="abs-br mr-6 mb-6 text-sm opacity-50">
固有値の物語 (1/10): ヤコビアンの固有値 → 固定点分類
</div>

---

## 力学系の定義

**状態** $\mathbf{x} \in \mathbb{R}^n$: ある時刻における系の完全な記述。$\mathbf{x}$ を定めれば将来の時間発展が一意に決まる。

**連続時間力学系**（常微分方程式）:

$$
\frac{d\mathbf{x}}{dt} = \mathbf{f}(\mathbf{x}), \quad \mathbf{x} \in \mathbb{R}^n, \quad \mathbf{f}: \mathbb{R}^n \to \mathbb{R}^n
$$

**離散時間力学系**（写像）:

$$
\mathbf{x}_{k+1} = \mathbf{F}(\mathbf{x}_k)
$$

> **ベクトル場** $\mathbf{f}$ は各点 $\mathbf{x}$ での速度（向きと大きさ）を与え、全ての軌道を決定する。

<img src="/figures/vector_field.png" class="mx-auto h-44" />

**前提**: $\mathbf{f}$ は Lipschitz 連続 → Picard-Lindelöf の定理により解の存在と一意性が保証される。

---

## 相空間・軌道・フロー

**相空間** (phase space): 状態 $\mathbf{x}$ が取りうる全ての値の空間 $\mathcal{M} \subseteq \mathbb{R}^n$

**フロー** $\phi_t : \mathcal{M} \to \mathcal{M}$: 初期状態を時刻 $t$ 後の状態に写す写像。以下を満たす:

$$
\phi_0 = \mathrm{id}, \qquad \phi_{t+s} = \phi_t \circ \phi_s \quad (\text{群性質})
$$

**軌道** (orbit / trajectory): 初期条件 $\mathbf{x}_0$ から出発する解曲線

$$
\gamma(\mathbf{x}_0) = \{\, \phi_t(\mathbf{x}_0) \mid t \in \mathbb{R} \,\}
$$

> フローの群性質は、力学系が**決定論的**（状態が未来を一意に決める）かつ**時間的に一様**（自律系: $\mathbf{f}$ が $t$ に陽に依存しない）であることの数学的表現。
> $\phi_t$ は $(\mathbb{R}, +)$ から $\mathrm{Diff}(\mathcal{M})$（$\mathcal{M}$ 上の微分同相写像全体の群）への群準同型。

---

## 固定点

**定義**: $\mathbf{x}^* \in \mathbb{R}^n$ が**固定点** (equilibrium / stationary point) であるとは

$$
\mathbf{f}(\mathbf{x}^*) = \mathbf{0}
$$

固定点では状態が時間変化しない: $\phi_t(\mathbf{x}^*) = \mathbf{x}^*$ for all $t$.

**基本的な問い**: 固定点の近傍で、微小な摂動を加えたら系はどう振る舞うか？

- 摂動が減衰する → **安定**
- 摂動が成長する → **不安定**

これが**安定性解析**の出発点。

---

## 固定点まわりの線形化

固定点 $\mathbf{x}^*$ の近傍で $\mathbf{x} = \mathbf{x}^* + \boldsymbol{\xi}$ と置く。テイラー展開:

$$
\frac{d\boldsymbol{\xi}}{dt} = \mathbf{f}(\mathbf{x}^* + \boldsymbol{\xi}) = \underbrace{\mathbf{f}(\mathbf{x}^*)}_{= \, \mathbf{0}} + \underbrace{D\mathbf{f}(\mathbf{x}^*)}_{=:\, J} \, \boldsymbol{\xi} \;+\; O(|\boldsymbol{\xi}|^2)
$$

**ヤコビ行列** (Jacobian):

$$
J = D\mathbf{f}(\mathbf{x}^*) = \left[\frac{\partial f_i}{\partial x_j}\right]_{\mathbf{x} = \mathbf{x}^*} \in \mathbb{R}^{n \times n}
$$

微小擾乱の時間発展は線形系で近似される:

$$
\frac{d\boldsymbol{\xi}}{dt} = J \, \boldsymbol{\xi}
$$

<img src="/figures/linearization.png" class="mx-auto h-44" />

---

## 線形系の解と固有値

$$
\frac{d\boldsymbol{\xi}}{dt} = J\,\boldsymbol{\xi} \quad \Longrightarrow \quad \boldsymbol{\xi}(t) = e^{Jt}\,\boldsymbol{\xi}(0)
$$

ここで $e^{Jt} := \sum_{k=0}^{\infty} \frac{(Jt)^k}{k!}$（行列指数関数）。$J$ の固有値 $\lambda_k$ と固有ベクトル $\mathbf{v}_k$ を用いると:

$$
\boldsymbol{\xi}(t) = \sum_{k=1}^{n} c_k \, e^{\lambda_k t} \, \mathbf{v}_k
$$

各モード $e^{\lambda_k t}$ の挙動は $\lambda_k = \sigma_k + i\omega_k$ で決まる:

| 成分 | 意味 | 効果 |
|------|------|------|
| $\sigma_k = \mathrm{Re}(\lambda_k)$ | 成長率 | $\sigma_k < 0$: 指数減衰, $\sigma_k > 0$: 指数成長 |
| $\omega_k = \mathrm{Im}(\lambda_k)$ | 角振動数 | $\omega_k \neq 0$: 振動（周期 $2\pi / \lvert\omega_k\rvert$） |

<img src="/figures/eigenvalue_effect.png" class="mx-auto h-52" />

---

## 安定性の判定

**定義** (リアプノフ安定性):

- 固定点 $\mathbf{x}^*$ が**漸近安定** $\Longleftrightarrow$ 全ての固有値について $\mathrm{Re}(\lambda_k) < 0$
- 固定点 $\mathbf{x}^*$ が**不安定** $\Longleftrightarrow$ ある固有値について $\mathrm{Re}(\lambda_k) > 0$

**直感**:

$$
|\boldsymbol{\xi}(t)| \sim |c_k| \, e^{\sigma_k t}
$$

- $\sigma_k < 0$ → 全モードが減衰 → 摂動が消える → **安定**
- $\sigma_k > 0$ → あるモードが成長 → 摂動が増幅 → **不安定**
- $\sigma_k = 0$ → **線形化では判定不能** → 非線形項が本質的（第2章へ）

---

## 2次元の固定点分類

<img src="/figures/eigenvalue_plane.png" class="mx-auto h-96" />

固有値の**複素平面上の位置**が固定点の定性的振る舞いを完全に決定する。

---

## 相図ギャラリー

<img src="/figures/phase_portraits.png" class="mx-auto h-96" />

---

## 例: 単振り子

非減衰単振り子 $\ddot{\theta} + \sin\theta = 0$ を1階系に書き直す:

$$
\begin{cases}
\dot{\theta} = \omega \\
\dot{\omega} = -\sin\theta
\end{cases}
$$

固定点でのヤコビアンと固有値:

| 固定点 | $J$ | 固有値 | 分類 |
|--------|-----|--------|------|
| $(\theta, \omega) = (2n\pi,\; 0)$ | $\begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}$ | $\lambda = \pm i$ | センター |
| $(\theta, \omega) = ((2n+1)\pi,\; 0)$ | $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ | $\lambda = \pm 1$ | サドル |

**注**: センターの固有値は $\mathrm{Re}(\lambda) = 0$ → Hartman-Grobman 定理の適用外。
非線形系でもセンターであることは、ハミルトニアン $H = \frac{1}{2}\omega^2 - \cos\theta$ の保存から従う。

---

## 単振り子の相図

<img src="/figures/pendulum_phase.png" class="mx-auto h-80" />

- **青**: 振動軌道（原点近傍の閉軌道 — エネルギーが低い）
- **赤**: セパラトリクス（サドル点を通る特別な軌道 — ホモクリニック軌道）
- **灰**: 回転軌道（エネルギーが高い — 振り子が一方向に回転）

---

## Hartman-Grobman の定理

**定理** (Hartman 1960, Grobman 1959):

固定点 $\mathbf{x}^*$ が**双曲型** ($\mathrm{Re}(\lambda_k) \neq 0$ for all $k$) ならば、$\mathbf{x}^*$ の近傍で非線形系

$$\dot{\mathbf{x}} = \mathbf{f}(\mathbf{x})$$

は線形系 $\dot{\boldsymbol{\xi}} = J\boldsymbol{\xi}$ と**位相的に同値** (topologically conjugate)。

**意味**:
- 双曲型固定点の近傍では、**線形化が位相的な振る舞い（軌道構造）を正しく捉える**
- 「位相的に同値」= 軌道の構造を保つ同相写像 $h$ が存在: $h \circ \phi_t = e^{Jt} \circ h$

**限界**: $\mathrm{Re}(\lambda_k) = 0$ なる固有値があれば定理は適用不能 → **第2章: 中心多様体定理**

---

## まとめ

| 概念 | 数学 | 物理的意味 |
|------|------|-----------|
| 力学系 | $\dot{\mathbf{x}} = \mathbf{f}(\mathbf{x})$ | 状態の時間発展規則 |
| 固定点 | $\mathbf{f}(\mathbf{x}^*) = 0$ | 静止状態 |
| ヤコビアン | $J = D\mathbf{f}(\mathbf{x}^*)$ | 微小擾乱の発展を支配 |
| 固有値の実部 | $\mathrm{Re}(\lambda)$ | 減衰率 / 成長率 |
| 固有値の虚部 | $\mathrm{Im}(\lambda)$ | 振動の有無と周波数 |
| Hartman-Grobman | 双曲型 $\Rightarrow$ 線形化 OK | 線形化の妥当性保証 |

**次章予告**: $\mathrm{Re}(\lambda) = 0$ のとき何が起こるか？ → 不変多様体と非線形解析
