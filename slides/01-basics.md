---
theme: default
# 図は透過 PNG でテーマに追従できないため、既定の auto ではなく dark に固定する
colorSchema: dark
title: "Ch.1 力学系の基礎と線形安定性"
drawings:
  persist: false
# 章の見取り図（components/Roadmap.vue）と右上の現在地表示（global-top.vue）が読む
chapter: "Ch.1"
roadmap:
  - '系の状態と、その変化をどう表すか'
  - '「乱れが消える」とはどういうことか'
  - '乱れが消えるか育つかは、何で決まるか'
  - '乱れは、どんな形で消えたり育ったりするか'
  - '線形化の答えは、どこまで信用できるか'
roadmapAnswers:
  - '状態は相空間 $\mathcal{M}$ の点、変化はベクトル場 $\boldsymbol{f}$ が決めるフロー $\phi_t$。解は一意なので軌道は交わらない'
  - '固定点 $\boldsymbol{q}^*$ のまわりで、離れない（安定）・戻ってくる（漸近安定）・離れていく（不安定）の3つに分かれる'
  - 'ヤコビアン $J$ の固有値。$\mathrm{Re}(\lambda)$ が減衰／成長を、$\mathrm{Im}(\lambda)$ が振動を決める'
  - '2次元ではノード・スパイラル・サドル・センター。高次元の運動はその組み合わせ（モード）になる'
  - '双曲型（全ての $\mathrm{Re}(\lambda_k) \neq 0$）なら固定点の近くで正しい。$\mathrm{Re}(\lambda) = 0$ では決まらない'
---

# 力学系の基礎と線形安定性

Chapter 1 — Learn Dynamical Systems

<img src="/figures/ch01_overview.png" class="mx-auto mt-6" style="width: 820px" />

---

## 小さな乱れは、消えるか育つか

翼に突風が当たった後のねじれ角 $\alpha$（上）と、円柱の後流が生む揚力 $C_L$（下）。流速 $U$・レイノルズ数 $Re$ がある値を超えると、同じ小さな乱れが**減衰から成長に変わる**。

<img src="/figures/ch01_motivation.png" class="mx-auto" style="width: 820px" />

知りたいのは、定常な状態に加えた**小さな乱れが消えるのか育つのか**、そしてその境目がどこにあるかである。本章のゴールは、これを**方程式を解かずに、行列の固有値だけで判定できるようになること**。

<div class="text-sm opacity-60">翼は2自由度の翼断面モデル、後流は振幅方程式による計算（どちらもモデルで、実測ではない）</div>

---

## 方程式を解かずに判定するまでの5つの問い

非線形の微分方程式はほとんど解けない。Poincaré 以来、力学系では解の式を求める代わりに、解の振る舞いの**性質**を調べる。本章では、次の5つの問いに順に答える。

<Roadmap class="mt-4" />

<div class="mt-4">

固有値はこの資料全体の軸で、Floquet 乗数（Ch.4）・リアプノフ指数（Ch.6）・Koopman 固有値（Ch.9）と形を変えて現れる。

</div>

---
part: 1
---

## Part 1: 系の状態と、その変化をどう表すか

フラッターと円柱後流で知りたいのは、定常な状態に加えた小さな乱れが消えるか育つかだった。

<Roadmap :current="1" class="mt-4" />

<div class="mt-4">

この Part では、その問いを式で立てるための言葉 — 状態・ベクトル場・相空間・フロー — を定める。

</div>

---

## 力学系の定義

乱れの行方を調べるには、まず系の「状態」と、それが時間とともにどう変わるかを式で書く。

**状態** $\boldsymbol{q} \in \mathbb{R}^n$ は、ある時刻の系の完全な記述である。$\boldsymbol{q}$ を定めれば将来の時間発展が一意に決まる。時間変化は

$$
\frac{d\boldsymbol{q}}{dt} = \boldsymbol{f}(\boldsymbol{q}) \quad (\text{連続時間}), \qquad
\boldsymbol{q}_{k+1} = \boldsymbol{F}(\boldsymbol{q}_k) \quad (\text{離散時間})
$$

の形に書く。$\boldsymbol{f}$ を**ベクトル場**と呼ぶ。各点 $\boldsymbol{q}$ での速度（向きと大きさ）を与え、全ての軌道を決める。

<div class="grid grid-cols-[1fr_360px] gap-6 items-center">
<div>

フラッターの翼断面モデルは $n = 4$ の連続時間の系で、状態は $\boldsymbol{q} = (h, \alpha, \dot{h}, \dot{\alpha})$（上下の変位・ねじれ角とそれぞれの速度）である。流速 $U$ は $\boldsymbol{f}$ に含まれる**パラメータ**で、状態ではない。

</div>
<img src="/figures/typical_section.png" style="width: 360px" />
</div>

---

## 力学系の対象・対象外

$\dot{\boldsymbol{q}} = \boldsymbol{f}(\boldsymbol{q})$ の形に書けるかどうかが、以降の道具が使えるかどうかの分かれ目になる。

| 対象 | 対象外（そのままでは） |
|------------------|--------------------------|
| 振り子、Lorenz 方程式、Navier-Stokes（無限次元） | **確率微分方程式**: ノイズ項があり決定論的でない |
| ロジスティック写像、Poincaré 写像（離散時間） | **遅延微分方程式**: 未来を決めるのに過去の履歴が要る |
| 一定の流速で飛ぶ翼、外力なしの流れ場 | **非自律系** $\boldsymbol{f}(\boldsymbol{q}, t)$: $(\boldsymbol{q}, t)$ を状態に取れば入る |

対象外の系も、状態の取り方を変えれば対象に入ることがある。非自律系は時刻 $t$ を状態に加えればよく、遅延微分方程式は過去の履歴（関数）を丸ごと状態に取れば無限次元の力学系になる。

---

## ベクトル場を描くと、軌道の形が見える

<div class="grid grid-cols-[1fr_380px] gap-8 items-center">
<div>

ベクトル場 $\boldsymbol{f}$ は各点 $\boldsymbol{q}$ に速度を与える。$n = 2$ で

$$
\boldsymbol{f}(\boldsymbol{q}) = \begin{pmatrix} q_2 \\ q_1 - q_1^3 \end{pmatrix}
$$

と取り、各点に $\boldsymbol{f}(\boldsymbol{q})$ を矢印で描いたのが右図である（色は速さ $|\boldsymbol{f}|$）。

軌道は、この矢印をなぞる曲線になる。赤点は $\boldsymbol{f}(\boldsymbol{q}) = \boldsymbol{0}$ となる点で、速度がゼロなので状態が動かない。

</div>
<img src="/figures/vector_field.png" style="width: 380px" />
</div>

---

## 解が一意なら、軌道は交わらない

矢印をなぞる曲線が、初期値ごとに1本に決まることは自明ではない。それを保証するのが次の定理である。

<div class="mt-3 px-5 py-1 border-l-4 border-teal-400 bg-white bg-opacity-5">

**定理**（Picard-Lindelöf）: $\boldsymbol{f}$ が Lipschitz 連続ならば、各初期条件に対して解が（少なくとも短い時間は）ただひとつ存在する。

</div>

<div class="grid grid-cols-[1fr_380px] gap-8 items-center">
<div>

したがって**軌道は交わらない**。2本の軌道が点 $\boldsymbol{p}$ で交わったとすると、$\boldsymbol{p}$ を初期値とする解が2本あることになり、一意性に反する（右図）。

この性質が、相図を1枚の絵として描けることの根拠になっている。

</div>
<img src="/figures/orbits_cannot_cross.png" style="width: 380px" />
</div>

---

## 相空間

軌道は、状態 $\boldsymbol{q}$ が取りうる値の空間の中に描かれる。この空間を**相空間** (phase space) $\mathcal{M}$ と呼ぶ。

多くの場合は $\mathcal{M} = \mathbb{R}^n$ としてよいが、そうならない場合が2通りある。

| | 系 | 相空間 $\mathcal{M}$ | 理由 |
|---|----|--------------------|------|
| **(a)** 拘束がある<br>→ $\mathbb{R}^n$ の**一部** | 反応系の濃度 $c_i$ | 正象限 $\mathbb{R}^n_{\geq 0}$ | 負の濃度は取りえない |
| | 非圧縮性流れ $\boldsymbol{u}$ | $\{\boldsymbol{u} : \nabla \cdot \boldsymbol{u} = 0\}$ | 連続の式が拘束（→ 第7章） |
| **(b)** 同一視がある<br>→ $\mathbb{R}^n$ と**別の形** | 単振り子 $(\theta, \dot\theta)$ | 円筒 $S^1 \times \mathbb{R}$ | $\theta$ と $\theta + 2\pi$ が同じ物理状態 |

(b) の円筒は平面 $\mathbb{R}^2$ の一部ではない。このように $\mathcal{M}$ は一般には**多様体**なので、$\mathbb{R}^n$ ではなく $\mathcal{M}$ と書く。

---

## フローと軌道

乱れの「行方」を書くには、初期値から時間 $t$ だけ進めた先を与える写像が要る。**フロー** $\phi_t : \mathcal{M} \to \mathcal{M}$ は、$\dot{\boldsymbol{q}} = \boldsymbol{f}(\boldsymbol{q}),\; \boldsymbol{q}(0) = \boldsymbol{q}_0$ の解を時刻 $t$ で評価したもので、積分形では $\phi_t(\boldsymbol{q}_0) = \boldsymbol{q}_0 + \int_0^{t} \boldsymbol{f}\bigl(\phi_\tau(\boldsymbol{q}_0)\bigr)\, d\tau$ と書ける。

**軌道** (orbit) $\gamma(\boldsymbol{q}_0) = \{\, \phi_t(\boldsymbol{q}_0) \mid t \in \mathbb{R} \,\}$ は、$\boldsymbol{q}_0$ を通る解が描く曲線である。

**群性質**: $\quad \phi_0 = \mathrm{id}, \qquad \phi_{t+s} = \phi_t \circ \phi_s$

<div class="mt-2 px-5 py-1 border-l-4 border-teal-400 bg-white bg-opacity-5">

$$
\phi_{t+s}(\boldsymbol{q}_0) = \underbrace{\Bigl(\boldsymbol{q}_0 + \int_0^{s}\! \boldsymbol{f}\, d\tau\Bigr)}_{=\; \phi_s(\boldsymbol{q}_0)} + \int_{s}^{t+s}\! \boldsymbol{f}\, d\tau
$$

**証明**: 上のように積分区間を $s$ で分割し、第2項で $\tau = s + \sigma$ と置くと、$\boldsymbol{\psi}(\sigma) := \phi_{s+\sigma}(\boldsymbol{q}_0)$ は初期値 $\phi_s(\boldsymbol{q}_0)$ の積分方程式を満たす（**自律系**なので）。**解の一意性**から $\boldsymbol{\psi}(t) = \phi_t(\phi_s(\boldsymbol{q}_0))$。 $\blacksquare$

</div>

---
part: 2
---

## Part 2: 「乱れが消える」とはどういうことか

Part 1 で、状態は相空間の点、時間発展はフロー $\phi_t$ で書けると分かった。解が一意なので軌道は交わらない。

<Roadmap :current="2" class="mt-4" />

<div class="mt-4">

この Part では、乱れを測る基準になる点を定め、そこからのずれがどうなるかで「消える」を言い表す。

</div>

---

## 固定点

乱れは何かからの「ずれ」である。基準になるのは、時間が経っても動かない状態である。

$$
\boldsymbol{f}(\boldsymbol{q}^*) = \boldsymbol{0}
$$

を満たす $\boldsymbol{q}^*$ を**固定点** (fixed point, equilibrium) と呼ぶ。速度がゼロなので、$\boldsymbol{q}^*$ から出発した状態はそこに留まり続ける。

| 系 | 固定点 $\boldsymbol{q}^*$ | 物理的な意味 |
|----|---------------------------|--------------|
| ベクトル場の例 $\boldsymbol{f} = (q_2,\ q_1 - q_1^3)^\top$ | $(0, 0),\ (\pm 1, 0)$ | 矢印の図の3つの赤点 |
| フラッターの翼断面モデル | $\boldsymbol{0}$ | 変位も速度もない、釣り合った翼 |
| 円柱後流 | 定常な流れ場 | 渦を放出していない、左右対称の後流 |

乱れは、固定点からのずれ $\boldsymbol{\xi} := \boldsymbol{q} - \boldsymbol{q}^*$ で表す。

---

## 「乱れが消える」には段階がある

固定点の近くから出発した軌道がどうなるかで、固定点を分類する。

<img src="/figures/stability_concepts.png" class="mx-auto" style="width: 790px" />

- **安定**（リアプノフ）: どの $\varepsilon$ にも、$\delta$ 内から出発すれば $\varepsilon$ 内に留まる $\delta$ がある。**離れないだけで、戻ってくるとは限らない**
- **漸近安定**: 安定で、さらに $t \to \infty$ で $\boldsymbol{q} \to \boldsymbol{q}^*$。乱れが**本当に消える**のはこちら
- **不安定**: 安定でないこと。行き先（別の固定点・周期軌道・無限遠）はこの定義からは決まらない

---
part: 3
---

## Part 3: 乱れが消えるか育つかは、何で決まるか

Part 2 で、「乱れが消える」は固定点の**漸近安定**（戻ってくる）と言い表せると分かった。**安定**（離れない）とは区別する。

<Roadmap :current="3" class="mt-4" />

<div class="mt-4">

この Part では、安定か不安定かを、方程式を解かずに何で判定できるかを調べる。

</div>

---

## 1次元では、固定点での傾きが決める

最も簡単な $n = 1$ の $\dot{q} = f(q)$ から始める。固定点 $q^*$ からのずれ $\xi = q - q^*$ は、$q^*$ が定数なので $\dot{\xi} = \dot{q}$ を満たす。$\xi$ が小さいとき、$f(q^*) = 0$ を使ってテイラー展開すると

$$
\dot{\xi} = f(q^* + \xi) \simeq f'(q^*)\, \xi
\quad \Longrightarrow \quad
\xi(t) = \xi(0)\, e^{\lambda t}, \qquad \lambda := f'(q^*)
$$

<div class="grid grid-cols-[1fr_400px] gap-8 items-center">
<div>

- $\lambda < 0$（青）: 乱れは指数的に消える
- $\lambda > 0$（赤）: 乱れは指数的に育つ

右図は $f(q) = q - q^3$ の場合。固定点での接線の傾きが $\lambda$ で、橙の矢印が $q$ の動く向きである。

</div>
<img src="/figures/one_dim_linearization.png" style="width: 400px" />
</div>

---

## $n$ 次元では、ヤコビアンが傾きの代わりになる

1次元の傾き $f'(q^*)$ を $n$ 次元に一般化する。ずれ $\boldsymbol{\xi} = \boldsymbol{q} - \boldsymbol{q}^*$ は、$\boldsymbol{q}^*$ が定数なので

$$
\frac{d\boldsymbol{\xi}}{dt} = \frac{d\boldsymbol{q}}{dt} = \boldsymbol{f}(\boldsymbol{q}^* + \boldsymbol{\xi})
= \underbrace{\boldsymbol{f}(\boldsymbol{q}^*)}_{=\, \boldsymbol{0}\;(\text{固定点の定義})} + \underbrace{D\boldsymbol{f}(\boldsymbol{q}^*)}_{=:\, J} \, \boldsymbol{\xi} \;+\; O(|\boldsymbol{\xi}|^2)
$$

を満たす（右辺は $\boldsymbol{\xi} = \boldsymbol{0}$ のまわりのテイラー展開）。$|\boldsymbol{\xi}|$ が小さければ $O(|\boldsymbol{\xi}|^2)$ を落として

$$
\frac{d\boldsymbol{\xi}}{dt} = J \, \boldsymbol{\xi}, \qquad
J = \left[\frac{\partial f_i}{\partial q_j}\right]_{\boldsymbol{q} = \boldsymbol{q}^*} \in \mathbb{R}^{n \times n} \quad (\text{ヤコビ行列、ヤコビアン})
$$

これを固定点まわりの**線形化**と呼ぶ。1次元の $\lambda = f'(q^*)$ にあたるのが行列 $J$ である。

たとえばベクトル場の例 $\boldsymbol{f} = (q_2,\ q_1 - q_1^3)^\top$ では、固定点ごとに $J$ が違う:

$$
J = \begin{pmatrix} 0 & 1 \\ 1 - 3q_1^2 & 0 \end{pmatrix}, \qquad
J\big|_{(0,0)} = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \qquad
J\big|_{(\pm 1, 0)} = \begin{pmatrix} 0 & 1 \\ -2 & 0 \end{pmatrix}
$$

---

## 解は、固有値ごとの指数関数の和になる

1次元の $e^{\lambda t}$ が、$n$ 次元では固有ベクトルの向きごとに起きる。$J$ が対角化できるとき、初期値を固有ベクトルで $\boldsymbol{\xi}(0) = \sum_k c_k \boldsymbol{v}_k$ と展開すると、$J\boldsymbol{v}_k = \lambda_k \boldsymbol{v}_k$ なので各成分は1次元と同じ $\dot{c}_k = \lambda_k c_k$ に従う:

$$
\boldsymbol{\xi}(t) = \sum_{k=1}^{n} c_k \, e^{\lambda_k t} \, \boldsymbol{v}_k
$$

各項を**モード**と呼ぶ。モード $e^{\lambda_k t}$ の振る舞いは $\lambda_k = \sigma_k + i\omega_k$ の実部と虚部で決まる:

| 成分 | 意味 | 効果 |
|------|------|------|
| $\sigma_k = \mathrm{Re}(\lambda_k)$ | 成長率 | $\sigma_k < 0$: 指数減衰, $\sigma_k > 0$: 指数成長 |
| $\omega_k = \mathrm{Im}(\lambda_k)$ | 角振動数 | $\omega_k \neq 0$: 振動（$e^{i\omega t} = \cos\omega t + i \sin\omega t$、周期 $2\pi / \lvert\omega_k\rvert$） |

---

## 実部が包絡線を、虚部が振動を決める

モード $e^{\lambda t}$ の実部を、$\sigma, \omega$ の組み合わせごとに描く（赤破線は包絡線 $\pm e^{\sigma t}$）。

<img src="/figures/eigenvalue_effect.png" class="mx-auto" style="width: 860px" />

---

## 固有値の実部の符号で、安定性が決まる

モードごとの振る舞いをまとめると、固定点の安定性の判定になる。

<div class="mt-3 px-5 py-1 border-l-4 border-teal-400 bg-white bg-opacity-5">

**定理**（線形化による判定）: $\boldsymbol{f}$ が $C^1$ のとき、固定点 $\boldsymbol{q}^*$ のヤコビアン $J$ について

- 全ての固有値で $\mathrm{Re}(\lambda_k) < 0$ ならば、$\boldsymbol{q}^*$ は**漸近安定**
- ある固有値で $\mathrm{Re}(\lambda_k) > 0$ ならば、$\boldsymbol{q}^*$ は**不安定**

</div>

線形化で捨てた $O(|\boldsymbol{\xi}|^2)$ を戻しても結論が変わらない、というのがこの定理の中身である。

各モードの大きさは $|c_k|\, e^{\sigma_k t}$ なので、

- 全ての $\sigma_k < 0$: 全モードが減衰し、乱れが消える
- ある $\sigma_k > 0$: そのモードが育つ
- 最大の $\sigma_k$ が $0$: **線形化では判定できない**。捨てた非線形項が結論を決める（→ Part 5）

---

## 例: フラッターは、固有値が虚軸を横切ると起きる

この判定を動機のフラッターに使う。翼断面モデル（$n = 4$）の $J$ の固有値を、流速 $U$ ごとに計算する。

<img src="/figures/flutter_eigenvalues.png" class="mx-auto" style="width: 820px" />

$U$ を上げると、ねじれに近いモードの固有値が右へ動き、$U = U_F$ で虚軸を横切る。動機の2つの時系列（$0.8\,U_F$ で減衰、$1.1\,U_F$ で成長）は、この**固有値の実部の符号**で説明できる。円柱後流も同じで、$Re = Re_c$ で固有値が虚軸を横切り、$Re > Re_c$ では実部が正になる。

---
part: 4
---

## Part 4: 乱れは、どんな形で消えたり育ったりするか

Part 3 で、固定点の安定性は $J$ の固有値の実部の符号で決まると分かった。フラッターの発生も、固有値が虚軸を横切ることとして読めた。

<Roadmap :current="4" class="mt-4" />

<div class="mt-4">

この Part では、安定・不安定よりも細かく、固定点のまわりの軌道の**形**が固有値でどう分類されるかを見る。

</div>

---

## 2次元では、固有値の組で6通りに分かれる

$n = 2$ では固有値は2つある。$J$ は実行列なので、2つとも実数か、互いに共役な複素数の対かのどちらかになる。

<img src="/figures/eigenvalue_plane.png" class="mx-auto" style="width: 830px" />

線で結んだ2点が、1つの系の固有値の組である。実固有値なら**ノード**（同符号）か**サドル**（異符号）、複素共役対なら**スパイラル**になり、実部が $0$ のときは**センター**と呼ぶ。

---

## 実固有値: 固有ベクトルの向きに伸び縮みする

固有値と固有ベクトルを指定した $J$ で $\dot{\boldsymbol{\xi}} = J\boldsymbol{\xi}$ の軌道を描く。橙・緑の直線が固有ベクトル $\boldsymbol{v}_1, \boldsymbol{v}_2$ の向き。

<img src="/figures/phase_portraits_real.png" class="mx-auto" style="width: 680px" />

固有ベクトルの向きでは1次元と同じく $e^{\lambda_k t}$ 倍に伸び縮みし、それ以外の点の軌道はその合成になる。**サドル**では $\boldsymbol{v}_1$ の向き（$\lambda_1 > 0$）に押し出され、$\boldsymbol{v}_2$ の向き（$\lambda_2 < 0$）に引き込まれる。

---

## 複素固有値: 回りながら縮む・広がる

固有値 $\lambda = \sigma \pm i\omega$ をもつ $J$ で、同じように軌道を描く（$\omega = 2$）。

<img src="/figures/phase_portraits_complex.png" class="mx-auto" style="width: 680px" />

虚部 $\omega$ が回転を、実部 $\sigma$ の符号が巻き込み／巻き出しを決める。固有ベクトルは渦巻きを傾け、円を楕円に歪めるが、**どの型になるかは固有値だけで決まる**。

---

## 例: 旅客機の運動は、固有値の組ごとのモードに分かれる

旅客機（B747、マッハ 0.8 巡航）の縦の運動を、釣り合い飛行のまわりで線形化すると $n = 4$ の $\dot{\boldsymbol{\xi}} = J\boldsymbol{\xi}$ になる（$\boldsymbol{\xi}$ = 前進速度・上下速度・ピッチ角速度・ピッチ角のずれ）。

<img src="/figures/aircraft_modes.png" class="mx-auto" style="width: 840px" />

固有値は共役対2組に分かれ、それぞれが2次元の安定スパイラルとして振る舞う。迎角を 1° 乱すと、速く強く減衰する**短周期モード**（周期 7 秒）と、ゆっくり弱く減衰する**フゴイド**（周期 93 秒、速度と高度の交換）が同時に現れる。

<div class="text-sm opacity-60">状態行列: MIT 16.333 Aircraft Stability and Control (Fall 2004), Lecture 6</div>

---

## 非線形系では、固定点ごとに分類する

ここまでの例は固定点が1つの線形系だった。非線形系には固定点が複数ありうるので、固定点ごとに $J$ を計算して分類する。非減衰単振り子 $\ddot{\theta} + \sin\theta = 0$ は、$\boldsymbol{q} = (\theta, \omega)$ と取ると $\dot{\theta} = \omega,\ \dot{\omega} = -\sin\theta$ になる。

| 固定点 | $J$ | 固有値 | 分類 |
|--------|-----|--------|------|
| $(\theta, \omega) = (2n\pi,\; 0)$ | $\begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}$ | $\lambda = \pm i$ | センター |
| $(\theta, \omega) = ((2n+1)\pi,\; 0)$ | $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ | $\lambda = \pm 1$ | サドル |

サドル（振り子が真上で静止）は $\mathrm{Re}(\lambda) \neq 0$ なので、線形化の結論をそのまま使える。センター（真下で静止）は $\mathrm{Re}(\lambda) = 0$ の境界の場合で、線形化だけでは結論できない（→ Part 5）。

---

## 固定点ごとの分類が、相図の骨組みになる

単振り子の固定点ごとの分類をつなぐと、相図全体の形が見えてくる。

<img src="/figures/pendulum_phase.png" class="mx-auto" style="width: 790px" />

- **青**: 振動。センター（青●）のまわりを回る閉じた軌道（エネルギー $H = \tfrac12\omega^2 - \cos\theta$ が保存し、軌道はその等高線に沿う）
- **赤**: **セパラトリクス**。サドル（赤■）に出入りする軌道で、振動と回転を分ける境界
- **灰**: 回転。エネルギーが高く、振り子が一方向に回り続ける

---
part: 5
---

## Part 5: 線形化の答えは、どこまで信用できるか

Part 4 で、2次元の固定点はノード・スパイラル・サドル・センターに分類され、高次元の運動はその組み合わせ（モード）になると分かった。

<Roadmap :current="5" class="mt-4" />

<div class="mt-4">

ただし、どれも線形化した系 $\dot{\boldsymbol{\xi}} = J\boldsymbol{\xi}$ の話である。この Part では、その結論がもとの非線形系でどこまで成り立つかを調べる。

</div>

---

## 線形化が正しいのは、固定点の近くだけ

線形化した系の相図が、もとの非線形系とどこまで合うかを、単振り子（左）と原点で線形化した系（右）で比べる。

<img src="/figures/linearization.png" class="mx-auto" style="width: 820px" />

- **原点の近くでは軌道の形が一致**する（$\sin\theta \simeq \theta$）
- 離れると食い違う。$\sin\theta$ は $\theta = \pm\pi$ でも $0$ になるため**サドル**（橙■）と**セパラトリクス**（赤）が現れるが、線形化 $-\theta$ にはこの固定点自体がなく、全域が同心円のまま
- では、固定点の近くで「一致する」とはどういう意味で、いつ保証されるか

---

## Hartman-Grobman の定理

固定点の近くで線形化が正しいことを保証するのが、次の定理である。

<div class="mt-3 px-5 py-1 border-l-4 border-teal-400 bg-white bg-opacity-5">

**定理** (Hartman 1960, Grobman 1959): $\boldsymbol{f}$ が $C^1$ で、固定点 $\boldsymbol{q}^*$ が**双曲型**（全ての $k$ で $\mathrm{Re}(\lambda_k) \neq 0$）ならば、その近傍で $\dot{\boldsymbol{q}} = \boldsymbol{f}(\boldsymbol{q})$ は線形系 $\dot{\boldsymbol{\xi}} = J\boldsymbol{\xi}$ と**位相的に同値**である。

</div>

<div class="grid grid-cols-[1fr_560px] gap-6 items-center">
<div>

**位相的** (topological) **に同値**: 連続で逆も連続な1対1の写像（同相写像）$h$ で、軌道を軌道に移せること:

$$h \circ \phi_t = e^{Jt} \circ h$$

右図の**四角形が可換**で、「非線形のフローで進めてから $h$ で移す」のと「$h$ で移してから線形のフローで進める」が一致する。

</div>
<img src="/figures/topological_conjugacy.png" style="width: 560px" />
</div>

---

## $\mathrm{Re}(\lambda) = 0$ では、線形化で決まらない

双曲型でない固定点では、定理の保証がない。実際に何が起きるかを、$a$ だけが違う次の3つの系で見る:

$$
\dot{q}_1 = -q_2 + a\, q_1 r^2, \qquad \dot{q}_2 = q_1 + a\, q_2 r^2 \qquad (r^2 = q_1^2 + q_2^2)
$$

<img src="/figures/center_ambiguity.png" class="mx-auto" style="width: 560px" />

原点の $J$ はどれも同じ（$\lambda = \pm i$、センター）だが、極座標で書くと $\dot{r} = a r^3$ となり、捨てた非線形項の符号だけで、巻き込む・閉じる・巻き出すが分かれる。

---
part: 0
---

## まとめ: 5つの問いへの答え

章の見取り図の問いに、答えを書き込む。

<Roadmap answers class="mt-4" />

---

## まとめ

<div class="flex flex-col gap-6 mt-2">
<div>

**① 固定点のまわりの乱れの行方は、ヤコビアンの固有値で決まる。** 実部が減衰／成長を、虚部が振動を決める。フラッターは固有値が虚軸を横切って起きる。

</div>
<div>

**② 軌道の形は、固有値の複素平面上の位置だけで決まる。** 高次元の運動は、固有値の組ごとのモードに分かれる。

</div>
<div>

| | $\mathrm{Re}(\lambda) < 0$ | $\mathrm{Re}(\lambda) > 0$ | 境界 |
|---|---|---|---|
| 実固有値（振動なし） | Stable Node | Unstable Node | 符号が逆 → **Saddle** |
| 複素共役対（振動あり） | Stable Spiral | Unstable Spiral | $\mathrm{Re}(\lambda) = 0$ → **Center** |

</div>
<div>

**③ ただし保証されるのは、双曲型の固定点の近くだけである。** $\mathrm{Re}(\lambda) = 0$ では、捨てた非線形項が結論を決める。

</div>
</div>

---

## 次章へ: 線形化では答えられなかったこと

本章の道具では答えられなかった問いが2つ残っている。どちらも、線形化で捨てた非線形項を扱う道具が要る。

<div class="grid grid-cols-2 gap-8 mt-6">
<div class="px-5 py-2 border-l-4 border-gray-500 bg-white bg-opacity-5">

**$\mathrm{Re}(\lambda) = 0$ のとき、安定性はどう決まるか**

単振り子のセンターは、エネルギー $H$ が保存するので閉軌道と分かった。一般の系には保存量がない。

→ **第2章** 不変多様体と非線形解析

</div>
<div class="px-5 py-2 border-l-4 border-gray-500 bg-white bg-opacity-5">

**固有値が虚軸を横切った後、乱れはどうなるか**

円柱後流の揚力は、育った後に一定の振幅に落ち着いた。固有値の実部は正のままなので、線形化の $e^{\sigma t}$ では説明できない。

→ **第3章** 分岐理論

</div>
</div>
