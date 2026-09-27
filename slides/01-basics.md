---
theme: default
# 図は透過 PNG でテーマに追従できないため、既定の auto ではなく dark に固定する
colorSchema: dark
title: "Ch.1 力学系の基礎と線形安定性"
drawings:
  persist: false
---

# 力学系の基礎と線形安定性

Chapter 1 — Learn Dynamical Systems

<img src="/figures/chapter_overview.png" class="mx-auto mt-6" style="width: 820px" />

---

## 力学系を学ぶ背景

非線形の微分方程式は、ほとんどの場合**解析解が得られない**。
Poincaré は三体問題でこの壁に突き当たり、発想を転換した —
解の式を求めるのをやめ、**解の集合がどういう形をしているか**を調べる。
これが力学系 (dynamical systems) という枠組みの出発点である。

問いが「$t$ 秒後の値は？」から「**どこへ向かうのか、その構造は何に依存するのか**」に変わる。
固定点・周期軌道・アトラクタといった構造は、解が解けなくても調べられる。

**流体との関係**: Navier-Stokes 方程式は無限次元の力学系 $\dot{\boldsymbol{q}} = \boldsymbol{f}(\boldsymbol{q})$ であり、
層流から乱流への遷移・渦放出の発生・周期解の出現は、すべて**解の構造が定性的に変わる**現象。
データ駆動の手法（POD・DMD・Koopman・SINDy）も、結局この構造を有限次元で捉え直す道具である。
**道具を使う前に、その構造を記述するための語彙を先に身につけておきたい。**

<div class="mt-4 px-5 py-2 border-l-4 border-teal-400 bg-white bg-opacity-5">

本章のゴール: **固定点のまわりで系がどう振る舞うかを、ヤコビアンの固有値だけで判定できるようになること。**
この「固有値」は以降、Floquet 乗数（4章）・リアプノフ指数（6章）・Koopman 固有値（9章）と
形を変えて現れ、**資料全体を貫く軸**になる。

</div>

---

## この章の流れ

<div class="grid grid-cols-2 gap-x-12 gap-y-6 mt-4">
<div>

**1. 記述の枠組みを定める**

状態・ベクトル場・相空間・フロー。「解が一意に存在する」ことが、相図を描ける根拠になる。

</div>
<div>

**2. 基準点を見つける**

固定点 $\boldsymbol{f}(\boldsymbol{q}^*) = \boldsymbol{0}$。系が静止する点のまわりで、摂動が成長するのか減衰するのかを問う。

</div>
<div>

**3. 線形化して固有値に帰着させる**

摂動の発展はヤコビアン $J$ が支配し、挙動は $\lambda_k$ の実部（減衰／成長）と虚部（振動）で決まる。

</div>
<div>

**4. 線形化の適用範囲を確かめる**

Hartman-Grobman の定理が線形化を正当化する範囲と、それが破れる $\mathrm{Re}(\lambda) = 0$ の場合（→ 第2章）。

</div>
</div>

<div class="mt-8 text-center opacity-70">

$\dot{\boldsymbol{q}} = \boldsymbol{f}(\boldsymbol{q})$ → 固定点 $\boldsymbol{q}^*$ → ヤコビアン $J$ → 固有値 $\lambda$ → 定性的な振る舞い

</div>

---

## 力学系の定義

**状態** $\boldsymbol{q} \in \mathbb{R}^n$: ある時刻における系の完全な記述。$\boldsymbol{q}$ を定めれば将来の時間発展が一意に決まる。

**連続時間**（常微分方程式）: $\quad \dfrac{d\boldsymbol{q}}{dt} = \boldsymbol{f}(\boldsymbol{q}), \qquad$
**離散時間**（写像）: $\quad \boldsymbol{q}_{k+1} = \boldsymbol{F}(\boldsymbol{q}_k)$

> **ベクトル場** $\boldsymbol{f}$ は各点 $\boldsymbol{q}$ での速度（向きと大きさ）を与え、全ての軌道を決定する。

この形に収まるか否かが、以降の道具が使えるかどうかの分かれ目になる。

| この枠組みに入る | 入らない（そのままでは） |
|------------------|--------------------------|
| 振り子、Lorenz 方程式、Navier-Stokes（無限次元） | **確率微分方程式** — ノイズ項があり決定論的でない |
| ロジスティック写像、Poincaré 写像（離散時間） | **遅延微分方程式** — 未来を決めるのに過去の履歴が要る |
| 外力なしの流れ場 | **非自律系** $\boldsymbol{f}(\boldsymbol{q}, t)$ — $(\boldsymbol{q}, t)$ に拡張すれば入る |

---

## ベクトル場と解の一意性

<div class="grid grid-cols-[1fr_440px] gap-6 items-center">
<div>

**ベクトル場の例** ($n = 2$): 前ページの $\dot{\boldsymbol{q}} = \boldsymbol{f}(\boldsymbol{q})$ で

$$
\boldsymbol{q} = \begin{pmatrix} q_1 \\ q_2 \end{pmatrix}, \quad
\boldsymbol{f}(\boldsymbol{q}) = \begin{pmatrix} q_2 \\ q_1 - q_1^3 \end{pmatrix}
$$

と取った場合。右図は各点 $\boldsymbol{q}$ に $\boldsymbol{f}(\boldsymbol{q})$ を矢印で描いたもの（色は $|\boldsymbol{f}|$）。赤点は $\boldsymbol{f}(\boldsymbol{q}) = \boldsymbol{0}$ となる点 — すなわち**固定点**。

**解の一意性**: $\boldsymbol{f}$ が Lipschitz 連続ならば、Picard-Lindelöf の定理により各初期条件に対する解がただひとつ存在する。

したがって**軌道は決して交わらない** — 交点があれば、そこを初期値とする解が2本あることになり一意性に反する。この性質が、右図のように相図を1枚の絵として描けることの根拠になっている。

</div>
<img src="/figures/vector_field.png" style="width: 440px" />
</div>

---

## 相空間

**相空間** (phase space) $\mathcal{M}$: 状態 $\boldsymbol{q}$ が取りうる値の全体。

多くの場合は $\mathcal{M} = \mathbb{R}^n$ としてよいが、そうならない場合が2通りある。

| | 系 | 相空間 $\mathcal{M}$ | 理由 |
|---|----|--------------------|------|
| **(a)** 拘束がある<br>→ $\mathbb{R}^n$ の**一部** | 反応系の濃度 $c_i$ | 正象限 $\mathbb{R}^n_{\geq 0}$ | 負の濃度は取りえない |
| | 非圧縮性流れ $\boldsymbol{u}$ | $\{\boldsymbol{u} : \nabla \cdot \boldsymbol{u} = 0\}$ | 連続の式が拘束（→ 第7章） |
| **(b)** 同一視がある<br>→ $\mathbb{R}^n$ と**別の形** | 単振り子 $(\theta, \dot\theta)$ | 円筒 $S^1 \times \mathbb{R}$ | $\theta$ と $\theta + 2\pi$ が同じ物理状態 |

> (b) の円筒は $\mathbb{R}^2$ の**部分集合ではない**（$\mathbb{R}^3$ には埋め込めるが平面の一部ではない）。
> このように $\mathcal{M}$ は一般には**多様体**であり、$\mathbb{R}^n$ と書かずに $\mathcal{M}$ と書くのはそのため。

---

## フローと軌道

**フロー** $\phi_t$: $\dot{\boldsymbol{q}} = \boldsymbol{f}(\boldsymbol{q}),\; \boldsymbol{q}(0) = \boldsymbol{q}_0$ の解を時刻 $t$ で評価したもの。積分形では

$$
\phi_t(\boldsymbol{q}_0) = \boldsymbol{q}_0 + \int_0^{t} \boldsymbol{f}\bigl(\phi_\tau(\boldsymbol{q}_0)\bigr)\, d\tau
$$

**軌道** (orbit): $\gamma(\boldsymbol{q}_0) = \{\, \phi_t(\boldsymbol{q}_0) \mid t \in \mathbb{R} \,\}$ — フローが描く軌跡そのもの。$\mathcal{M}$ の外へは出ないので $\phi_t : \mathcal{M} \to \mathcal{M}$。

**群性質**: $\quad \phi_0 = \mathrm{id}, \qquad \phi_{t+s} = \phi_t \circ \phi_s$

<div class="mt-2 px-5 py-1 border-l-4 border-teal-400 bg-white bg-opacity-5">

**証明** — 積分区間を $s$ で分割するだけ:

$$
\phi_{t+s}(\boldsymbol{q}_0) = \underbrace{\Bigl(\boldsymbol{q}_0 + \int_0^{s}\! \boldsymbol{f}\, d\tau\Bigr)}_{=\; \phi_s(\boldsymbol{q}_0)} + \int_{s}^{t+s}\! \boldsymbol{f}\, d\tau
$$

第2項は $\tau = s + \sigma$ で $\int_0^{t}\! \boldsymbol{f}\, d\sigma$。**自律系**ゆえ時刻を $s$ から測り直せて $= \phi_t(\phi_s(\boldsymbol{q}_0))$。 $\blacksquare$

</div>

---

## 固定点

**定義**: $\boldsymbol{f}(\boldsymbol{q}^*) = \boldsymbol{0}$ を満たす $\boldsymbol{q}^*$ を**固定点** (equilibrium)。速度がゼロなので状態は動かない。
**基本的な問い**: 固定点のごく近くから出発したとき、軌道はどこへ向かうか？

<img src="/figures/stability_concepts.png" class="mx-auto" style="width: 790px" />

- **安定**（リアプノフ）: $\delta$ 内から出発すれば $\varepsilon$ 内に留まる。ただし**収束するとは限らない** — 周回し続けることもある
- **漸近安定**: さらに $t \to \infty$ で $\boldsymbol{q} \to \boldsymbol{q}^*$。**固定点そのもの**に収束する
- **不安定**: $\varepsilon$ の外へ出る軌道がある。行き先（別の固定点・周期軌道・無限遠）は**線形化では決まらない**

---

## 固定点まわりの線形化

固定点 $\boldsymbol{q}^*$ からのずれを $\boldsymbol{\xi}(t) := \boldsymbol{q}(t) - \boldsymbol{q}^*$ と定義する。

**① 左辺**: $\boldsymbol{q}^*$ は**定数**なので、微分すると消える:

$$
\frac{d\boldsymbol{\xi}}{dt} = \frac{d}{dt}\bigl(\boldsymbol{q} - \boldsymbol{q}^*\bigr) = \frac{d\boldsymbol{q}}{dt} = \boldsymbol{f}(\boldsymbol{q}) = \boldsymbol{f}(\boldsymbol{q}^* + \boldsymbol{\xi})
$$

つまり $\boldsymbol{\xi}$ は**もとの方程式をそのまま満たす**（座標原点を $\boldsymbol{q}^*$ に移しただけ）。

**② 右辺**: $\boldsymbol{\xi} = \boldsymbol{0}$ のまわりでテイラー展開する:

$$
\boldsymbol{f}(\boldsymbol{q}^* + \boldsymbol{\xi}) = \underbrace{\boldsymbol{f}(\boldsymbol{q}^*)}_{=\, \boldsymbol{0}\;(\text{固定点の定義})} + \underbrace{D\boldsymbol{f}(\boldsymbol{q}^*)}_{=:\, J} \, \boldsymbol{\xi} \;+\; O(|\boldsymbol{\xi}|^2)
$$

定数項が固定点の定義から消えるのが要点。$|\boldsymbol{\xi}|$ が小さければ $O(|\boldsymbol{\xi}|^2)$ を落として

$$
\frac{d\boldsymbol{\xi}}{dt} = J \, \boldsymbol{\xi}, \qquad
J = \left[\frac{\partial f_i}{\partial q_j}\right]_{\boldsymbol{q} = \boldsymbol{q}^*} \in \mathbb{R}^{n \times n} \quad (\text{ヤコビ行列})
$$

---

## 線形系の解と固有値

$$
\frac{d\boldsymbol{\xi}}{dt} = J\,\boldsymbol{\xi} \quad \Longrightarrow \quad \boldsymbol{\xi}(t) = e^{Jt}\,\boldsymbol{\xi}(0)
$$

ここで $e^{Jt} := \sum_{k=0}^{\infty} \frac{(Jt)^k}{k!}$（行列指数関数）。$J$ の固有値 $\lambda_k$ と固有ベクトル $\boldsymbol{v}_k$ を用いると:

$$
\boldsymbol{\xi}(t) = \sum_{k=1}^{n} c_k \, e^{\lambda_k t} \, \boldsymbol{v}_k
$$

各モード $e^{\lambda_k t}$ の挙動は $\lambda_k = \sigma_k + i\omega_k$ で決まる:

| 成分 | 意味 | 効果 |
|------|------|------|
| $\sigma_k = \mathrm{Re}(\lambda_k)$ | 成長率 | $\sigma_k < 0$: 指数減衰, $\sigma_k > 0$: 指数成長 |
| $\omega_k = \mathrm{Im}(\lambda_k)$ | 角振動数 | $\omega_k \neq 0$: 振動（周期 $2\pi / \lvert\omega_k\rvert$） |

---

## 固有値が決める4つの振る舞い

<img src="/figures/eigenvalue_effect.png" class="mx-auto" style="width: 680px" />

実部 $\sigma$ が包絡線（赤破線）の増減を、虚部 $\omega$ が振動の有無を決める。

---

## 安定性の判定

**定義** (リアプノフ安定性):

- 固定点 $\boldsymbol{q}^*$ が**漸近安定** $\Longleftrightarrow$ 全ての固有値について $\mathrm{Re}(\lambda_k) < 0$
- 固定点 $\boldsymbol{q}^*$ が**不安定** $\Longleftrightarrow$ ある固有値について $\mathrm{Re}(\lambda_k) > 0$

**直感**:

$$
|\boldsymbol{\xi}(t)| \sim |c_k| \, e^{\sigma_k t}
$$

- $\sigma_k < 0$ → 全モードが減衰 → 摂動が消える → **安定**
- $\sigma_k > 0$ → あるモードが成長 → 摂動が増幅 → **不安定**
- $\sigma_k = 0$ → **線形化では判定不能** → 非線形項が本質的（第2章へ）

---

## 2次元の固定点分類

プロットされている点は $J$ の**固有値**。2次元系では $J$ は $2\times 2$ で固有値は必ず2つなので、
**線で結んだ1組が1つの系**にあたる（6つの点群ではなく、6通りの「組」を1枚に重ねた図）。

<img src="/figures/eigenvalue_plane.png" class="mx-auto" style="width: 830px" />

- **実固有値は実軸上**に乗る。両方負 → Node（安定）、両方正 → Node（不安定）、**符号が逆 → Saddle**（原点を挟んで左右に1つずつ。一方向へ押し出しつつ別方向へ引き込む型で、不安定）
- **複素固有値は必ず共役対** $\sigma \pm i\omega$ なので実軸対称の2点。$\mathrm{Im} < 0$ 側は同じ組の片割れであって、別の分類ではない

---

## 相図ギャラリー — 実固有値

いずれも $\dot{\boldsymbol{q}} = A\boldsymbol{q}$、$A = \mathrm{diag}(\lambda_1, \lambda_2)$（**固有ベクトルを座標軸に取った場合**）。

<img src="/figures/phase_portraits_real.png" class="mx-auto" style="width: 790px" />

- 実固有値なので軌道は振動せず、各固有ベクトル方向に $e^{\lambda_k t}$ で伸縮する
- **サドル**: 固有値の符号が逆のとき。$\lambda_1 > 0$ の方向には押し出され、$\lambda_2 < 0$ の方向には引き込まれる。ほとんどの軌道は一度近づいてから離れていき、双曲線状になる（**不安定**）

---

## 相図ギャラリー — 複素固有値

いずれも $\dot{\boldsymbol{q}} = A\boldsymbol{q}$、$A = \begin{pmatrix} \sigma & -\omega \\ \omega & \sigma \end{pmatrix}$（$\lambda = \sigma \pm i\omega$、ここでは $\omega = 2$）。

<img src="/figures/phase_portraits_complex.png" class="mx-auto" style="width: 790px" />

- 虚部 $\omega$ が回転を生み、実部 $\sigma$ の符号が巻き込み / 巻き出しを決める
- **固有ベクトルが座標軸からずれれば、絵は傾いたり歪んだりする**（円は楕円になる）。
  ただし**分類（定性的な構造）は固有値だけで決まる** — これが固有値に注目する理由

---

## 単振り子の固定点と分類

**例**: 非減衰単振り子 $\ddot{\theta} + \sin\theta = 0$ を1階系に書き直す:

$$
\begin{cases}
\dot{\theta} = \omega \\
\dot{\omega} = -\sin\theta
\end{cases}
$$

| 固定点 | $J$ | 固有値 | 分類 |
|--------|-----|--------|------|
| $(\theta, \omega) = (2n\pi,\; 0)$ | $\begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}$ | $\lambda = \pm i$ | センター |
| $(\theta, \omega) = ((2n+1)\pi,\; 0)$ | $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ | $\lambda = \pm 1$ | サドル |

サドル（$\theta = \pm\pi$ は振り子が真上を向く位置）は $\mathrm{Re}(\lambda) \neq 0$ なので線形化の結論をそのまま使える。
一方**センターは $\mathrm{Re}(\lambda) = 0$ の境界ケース**で線形化だけでは結論できない。実際にどうなるかは次の相図で確かめる。

---

## 単振り子の相図

<img src="/figures/pendulum_phase.png" class="mx-auto" style="width: 790px" />

- **青**: 振動軌道（原点近傍の閉軌道 — エネルギーが低い）
- **赤**: **セパラトリクス** — サドルに出入りする特別な軌道で、振動と回転を分ける境界
- **灰**: 回転軌道（エネルギーが高い — 振り子が一方向に回転）

**センターは非線形系でも残る**。エネルギー $H = \frac{1}{2}\omega^2 - \cos\theta$ が保存し、軌道は $H$ が一定の曲線に沿うため、原点のまわりでは閉じたままになる（線形化では判定できなかったが、保存量があるので結論できる）。

---

## 線形化はどこまで正しいか

同じ振り子（左）を、原点で線形化した $\dot\omega = -\theta$（右）と並べる。

<img src="/figures/linearization.png" class="mx-auto" style="width: 820px" />

- **原点近傍では軌道構造が一致**する（$\sin\theta \simeq \theta$）— 線形化が有効な範囲
- 離れると破綻する。$\sin\theta$ は $\theta = \pm\pi$ でも $0$ になるため**サドル**（橙■）と**セパラトリクス**（赤）が現れるが、線形化 $-\theta$ にはこの固定点自体がなく、全域が同心円のまま
- つまり**線形化が正しいのは固定点のごく近傍だけ**。ではその「近傍」はどこまで保証されるのか？

---

## Hartman-Grobman の定理

**定理** (Hartman 1960, Grobman 1959): 固定点 $\boldsymbol{q}^*$ が**双曲型**（全ての $k$ で $\mathrm{Re}(\lambda_k) \neq 0$）ならば、
その近傍で $\dot{\boldsymbol{q}} = \boldsymbol{f}(\boldsymbol{q})$ は線形系 $\dot{\boldsymbol{\xi}} = J\boldsymbol{\xi}$ と**位相的に同値**。

<div class="grid grid-cols-[1fr_560px] gap-6 items-center">
<div>

「位相的に同値」とは、軌道の構造を保つ同相写像 $h$ が存在すること:

$$h \circ \phi_t = e^{Jt} \circ h$$

右図の**四角形が可換**、つまり「非線形のフローで進めてから $h$ で移す」のと「$h$ で移してから線形のフローで進める」のが一致する。これが、**線形化が軌道構造を正しく捉える**ことの保証になる。

</div>
<img src="/figures/topological_conjugacy.png" style="width: 560px" />
</div>

**限界**: $\mathrm{Re}(\lambda_k) = 0$ なる固有値があれば適用不能。振り子のセンター（$\lambda = \pm i$）がまさにこれで、
今回は保存量 $H$ から閉軌道と分かったが、一般には別の道具が要る → **第2章: 中心多様体定理**

---

## まとめ

**① 非線形の問題が、行列の固有値問題に帰着する。**
固定点まわりでは $\dot{\boldsymbol{\xi}} = J\boldsymbol{\xi}$ となり、解は $\sum_k c_k e^{\lambda_k t}\boldsymbol{v}_k$。$\mathrm{Re}(\lambda)$ が減衰／成長を、$\mathrm{Im}(\lambda)$ が振動を決める。

**② 定性的な振る舞いは、固有値の複素平面上の位置だけで決まる。**
固有ベクトルは絵の傾きや歪みを変えるが、分類そのものは変えない。

| | $\mathrm{Re}(\lambda) < 0$ | $\mathrm{Re}(\lambda) > 0$ | 境界 |
|---|---|---|---|
| 実固有値（振動なし） | Stable Node | Unstable Node | 符号が逆 → **Saddle** |
| 複素共役対（振動あり） | Stable Spiral | Unstable Spiral | $\mathrm{Re}(\lambda) = 0$ → **Center** |

**③ ただし線形化が正当なのは、双曲型（全ての $\mathrm{Re}(\lambda_k) \neq 0$）のときに限る。**
Hartman-Grobman の定理が、固定点の近傍で軌道構造が一致することを保証する。

**次章へ**: 保証が失われる $\mathrm{Re}(\lambda) = 0$ の場合（振り子のセンターがその例）をどう扱うか → **不変多様体と中心多様体定理**
