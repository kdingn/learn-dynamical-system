---
theme: default
# 図は透過 PNG でテーマに追従できないため、既定の auto ではなく dark に固定する
colorSchema: dark
title: "Ch.2 不変多様体と非線形解析"
drawings:
  persist: false
---

# 不変多様体と非線形解析

Chapter 2 — Learn Dynamical Systems

<img src="/figures/ch02_overview.png" class="mx-auto mt-6" style="width: 820px" />

---

## 線形化の限界

固定点まわりの振る舞いは、線形化するとヤコビアン $J$ の固有値に帰着する。ただし Hartman-Grobman の定理が保証するのは、**双曲型**（全ての $\mathrm{Re}(\lambda_k) \neq 0$）の固定点の**近傍**だけである。そのため、次の2つは線形化では扱えない。

**① 固定点の近傍の外。** 振り子のセパラトリクスはサドルの近くから出て相空間を横断し、隣のサドルに達する。この軌道は固定点の近傍だけを見ても捉えられない。固有空間 $E^s, E^u$ は線形系に対して定義されたものなので、**非線形系で対応する集合を定義し直す**必要がある。

**② $\mathrm{Re}(\lambda_k) = 0$ の場合。** 線形化では安定性が決まらない。振り子のセンターはエネルギー保存から閉軌道だと分かるが、一般の系にはそのような保存量がない。

どちらも、**固定点に出入りする軌道がなす集合**を調べることで扱える。この集合が本章の主題、不変多様体である。

<div class="mt-4 px-5 py-2 border-l-4 border-teal-400 bg-white bg-opacity-5">

本章のゴール: 不変多様体を用いて ① 固定点の近傍の外の軌道構造を記述し、② $\mathrm{Re}(\lambda) = 0$ の固定点の安定性を**中心多様体上の低次元の方程式**から判定できるようになること。

</div>

---

## この章の流れ

<div class="grid grid-cols-2 gap-x-12 gap-y-6 mt-4">
<div>

**1. 不変集合**

フローで閉じた集合。固定点・周期軌道・セパラトリクスはいずれもこれに含まれる。

</div>
<div>

**2. 多様体と固有空間**

多様体の**次元・接空間**と、固有空間分解 $\mathbb{R}^n = E^s \oplus E^u \oplus E^c$。接空間も固有空間も $\mathbb{R}^n$ の線形部分空間なので、比較できる。

</div>
<div>

**3. 安定・不安定多様体**

$E^s, E^u$ を「収束する点の集合」として非線形系へ拡張し、双曲型なら $E^s, E^u$ に**接する同じ次元の多様体**になることを示す（安定多様体定理）。

</div>
<div>

**4. 中心多様体と正規形**

中心多様体定理と縮約原理で $\mathrm{Re}(\lambda) = 0$ の方向に次元を落とし、正規形で非線形項を簡約する。

</div>
</div>

<div class="mt-8 text-center opacity-70">

$E^s \oplus E^u \oplus E^c$ → $W^s,\, W^u,\, W^c$ → $W^c$ 上へ縮約 → 正規形 → 安定性

</div>

---

## 不変集合と不変多様体

<div class="grid grid-cols-[1fr_400px] gap-8 items-center">
<div>

**定義**: 集合 $S \subseteq \mathcal{M}$ が**不変** (invariant) とは、全ての $t$ で $\phi_t(S) \subseteq S$ となること。$S$ の点は $S$ の外へ出ない。

解の一意性から、**任意の軌道は不変集合**である。固定点・周期軌道・セパラトリクスはいずれも不変集合である。

**不変多様体** (invariant manifold): 不変集合のうち、それ自体が多様体であるもの。

多様体であれば**次元**と**接空間**が定まり、線形系の固有空間と比較できる。以下でこの2つを定義する。

</div>
<img src="/figures/invariant_set.png" style="width: 400px" />
</div>

---

## 多様体と次元

<div class="grid grid-cols-[1fr_360px] gap-8 items-center">
<div>

以下、**一般の多様体を $M$ と書く**（相空間 $\mathcal{M}$ も、この章で扱う不変多様体も、その一例）。

**多様体** (manifold): 各点の近傍が $\mathbb{R}^k$ の開集合と1対1に対応し、その対応と逆がともに滑らかであるような集合。この対応 $\varphi$ を**局所座標**（チャート）と呼ぶ。

全体は曲がっていてよいが、各点の近傍は $\mathbb{R}^k$ と同じ構造をもつ。折れ目では滑らかさが、分岐・自己交差では1対1が崩れるので、その点で局所座標が取れない。

**次元** $k$: 局所座標の成分数（独立に動かせるパラメータの数）。連結な多様体では点によらず一定で、これを $\dim M$ と書く。

</div>
<img src="/figures/manifold_chart.png" style="width: 360px" />
</div>

---

## 接空間

<div class="grid grid-cols-[1fr_360px] gap-8 items-center">
<div>

**接空間** $T_pM$: $p$ を通る $M$ 上の滑らかな曲線 $\gamma(t)$（$\gamma(0) = p$）すべてについて、速度 $\dot{\gamma}(0)$ を集めたもの。$\gamma$ は力学系の軌道でなくてよい。

**$k = 1$**（上図）: 曲線の像は $M$ に限られるが、速さと向きは自由に選べる。$\gamma(2t)$ なら $2\boldsymbol{v}$、$\gamma(-t)$ なら $-\boldsymbol{v}$、定数曲線なら $\boldsymbol{0}$。現れる速度は $\boldsymbol{v}$ の定数倍の全体で、**直線**になる。

**$k = 2$**（下図）: $p$ から独立な2方向に曲線を引けるので、$\dot{\gamma}_1(0)$, $\dot{\gamma}_2(0)$ の一次結合が全て現れ、**平面**になる。

</div>
<img src="/figures/tangent_space.png" style="width: 360px" />
</div>

---

## 接空間の次元

局所座標 $\varphi$ を使うと $T_pM$ を具体的に書ける。座標側で $\varphi(p)$ を通る直線を引き、$M$ へ写す:

$$
\gamma_{\boldsymbol{c}}(t) = \varphi^{-1}\bigl(\varphi(p) + t\boldsymbol{c}\bigr),
\qquad
\dot{\gamma}_{\boldsymbol{c}}(0) = D\varphi^{-1}\bigl(\varphi(p)\bigr)\,\boldsymbol{c}
$$

任意の曲線 $\gamma$ の速度は $\boldsymbol{c} = (\varphi \circ \gamma)'(0)$ と取れば現れるので、**$T_pM$ はヤコビ行列 $D\varphi^{-1}$ の像**に等しい。したがって $T_pM$ は線形部分空間であり、$D\varphi^{-1}$ の階数が $k$ なので $\dim T_pM = k$ である。$k = 1$ の直線、$k = 2$ の平面はその特別な場合。

<img src="/figures/tangent_chart.png" class="mx-auto" style="width: 720px" />

---

## 接空間は $\mathbb{R}^n$ の部分空間

<div class="grid grid-cols-[1fr_340px] gap-8 items-center">
<div>

$T_pM$ の要素は**点ではなく速度ベクトル**で、$T_pM$ は**原点を通る** $\mathbb{R}^n$ の $k$ 次元部分空間である（定数曲線 $\gamma(t) = p$ の速度 $\boldsymbol{0}$ を含む）。図の接平面は、これを $p$ へ平行移動した $p + T_pM$ である。

$E$ が $\mathbb{R}^n$ の線形部分空間なら、$\boldsymbol{w} \in E$ に対して $\gamma(t) = t\boldsymbol{w}$ は $E$ 上の曲線で、速度は $\boldsymbol{w}$。よって $T_{\boldsymbol{0}}E = E$ である。

曲がった不変多様体と平らな固有空間はそのままでは比較できないが、接空間を取れば**どちらも $\mathbb{R}^n$ の部分空間**になり、等号で比較できる。一致するのは次元だけでなく、$\mathbb{R}^n$ の中での向きも含む。

</div>
<img src="/figures/tangent_subspace.png" style="width: 340px" />
</div>

---

## 線形系の固有空間分解

<div class="grid grid-cols-[1fr_360px] gap-8 items-center">
<div>

$\dot{\boldsymbol{\xi}} = J\boldsymbol{\xi}$ の固有ベクトル $\boldsymbol{v}_k$ を固有値 $\lambda_k$ の実部の符号で3組に分け、それぞれが張る部分空間を定める:

$$E^s = \operatorname{span}\bigl\{\, \boldsymbol{v}_k \;\bigm|\; \mathrm{Re}(\lambda_k) < 0 \,\bigr\}$$

$E^u,\ E^c$ も $> 0$、$= 0$ で同様に定めると $\mathbb{R}^n = E^s \oplus E^u \oplus E^c$（複素共役対は実部と虚部、重複固有値は一般化固有空間 $\ker(J - \lambda_k I)^m$ を取る）。

$E^s$ 上の解は指数的に $\boldsymbol{0}$ へ減衰し、$E^u, E^c$ の成分をもつ解は減衰しない。したがって $E^s$ は**収束する初期値の集合**として書ける:

$$E^s = \bigl\{\, \boldsymbol{\xi} \;\bigm|\; e^{Jt}\boldsymbol{\xi} \to \boldsymbol{0}\ \ (t \to \infty) \,\bigr\}$$

$E^u$ は $t \to -\infty$ で同様。**双曲型**とは $E^c = \{\boldsymbol{0}\}$ のことである。

</div>
<img src="/figures/eigenspaces.png" style="width: 360px" />
</div>

---

## 安定集合と不安定集合

線形系の固有空間は $E^s = \{\boldsymbol{\xi} \mid e^{Jt}\boldsymbol{\xi} \to \boldsymbol{0}\}$ と、$J$ を使わず「解が収束するか」だけで書けた。そこで非線形系の固定点 $\boldsymbol{q}^*$ に対しても、同じ形で定義する:

$$
W^s(\boldsymbol{q}^*) = \bigl\{\, \boldsymbol{q} \;\bigm|\; \phi_t(\boldsymbol{q}) \to \boldsymbol{q}^*\ (t \to \infty) \,\bigr\},
\qquad
W^u(\boldsymbol{q}^*) = \bigl\{\, \boldsymbol{q} \;\bigm|\; \phi_t(\boldsymbol{q}) \to \boldsymbol{q}^*\ (t \to -\infty) \,\bigr\}
$$

それぞれ**安定集合**・**不安定集合**と呼ぶ。$\boldsymbol{q}$ が $\boldsymbol{q}^*$ に収束するなら $\phi_s(\boldsymbol{q})$ も収束するので、どちらも不変集合である。

線形系なら $W^s = E^s$ で、平らな部分空間だった。非線形系では定義だけからは形が分からない。$E^s$ と比べて知りたいのは次の3点である:

- **形**: $W^s$ は多様体か（$E^s$ は部分空間なので多様体）
- **次元**: $\dim W^s = \dim E^s$ か
- **向き**: $\boldsymbol{q}^*$ での接空間が $E^s$ に一致するか（$T_{\boldsymbol{q}^*}W^s = E^s$ か）

---

## サドルの安定集合と不安定集合

左は線形化 $\dot{\boldsymbol{\xi}} = J\boldsymbol{\xi}$、右は非線形 $\dot{q}_1 = q_1 + q_2^2/2,\ \ \dot{q}_2 = -q_2 + q_1^2/2$（どちらも原点はサドル）。

<img src="/figures/stable_manifold.png" class="mx-auto" style="width: 450px" />

- 右図の**灰色の破線が固有空間** $E^s, E^u$（左図の実線）。$W^s, W^u$ は**曲がる**が、原点ではこの破線に**接する**（$W^u: q_2 = q_1^2/6 + \cdots$、$W^s: q_1 = -q_2^2/6 + \cdots$）
- 形・次元・向きの3点は、この例ではすべて成り立つ（1次元の多様体で、原点で $E^s, E^u$ に接する）。一般に成り立つことを保証するのが安定多様体定理

---

## 安定多様体定理

サドルの例で見た3点は、双曲型（全ての $\mathrm{Re}(\lambda_k) \neq 0$）の固定点なら一般に成り立つ。ただし保証されるのは $\boldsymbol{q}^*$ の近傍の中だけなので、近傍 $U$ から出ない点に限った**局所安定集合**で述べる（$t \to -\infty$ に取り替えたものが $W^u_{\mathrm{loc}}$）:

$$
W^s_{\mathrm{loc}}(\boldsymbol{q}^*) = \bigl\{\, \boldsymbol{q} \in U \;\bigm|\; \phi_t(\boldsymbol{q}) \to \boldsymbol{q}^*\ (t \to \infty),\ \ \phi_t(\boldsymbol{q}) \in U\ \ \forall\, t \geq 0 \,\bigr\}
$$

**定理** (Hadamard 1901, Perron 1928): $\boldsymbol{f}$ が $C^r$ ($r \geq 1$) で $\boldsymbol{q}^*$ が**双曲型**ならば、$U$ を十分小さく取ると

| 問い | 答え |
|---|---|
| 形 | $W^s_{\mathrm{loc}}$ は $C^r$ 級の多様体 |
| 次元 | $\dim W^s_{\mathrm{loc}} = \dim E^s$ |
| 向き | $T_{\boldsymbol{q}^*}W^s_{\mathrm{loc}} = E^s$（$\boldsymbol{q}^*$ で $E^s$ に接する） |

$W^u_{\mathrm{loc}}$ も同様。多様体であることが保証されたので、以下 $W^s, W^u$ を**安定多様体・不安定多様体**と呼ぶ。

---

## 双曲型という仮定の役割

定理は $\boldsymbol{q}^*$ が**双曲型**、つまり**どの方向にも $0$ でない伸び縮みの率がある**ことを仮定している。この仮定が要る理由を見るため、ずれ $\boldsymbol{\xi} = \boldsymbol{q} - \boldsymbol{q}^*$ で書く:

$$
\dot{\boldsymbol{\xi}} = J\boldsymbol{\xi} + \boldsymbol{N}(\boldsymbol{\xi}), \qquad |\boldsymbol{N}(\boldsymbol{\xi})| \leq \varepsilon\,|\boldsymbol{\xi}| \quad (|\boldsymbol{\xi}| < \delta)
$$

$\boldsymbol{N}$ は2次以上なので、近傍を小さくする（$\delta \to 0$）ほど $\varepsilon$ も小さくでき、非線形項が伸び縮みの率を変える量は高々 $\varepsilon$ 程度になる。双曲型なら $\mathbb{R}^n = E^s \oplus E^u$ で、線形部の率は固有値の実部で決まる:

- **$E^s$ 方向**: 縮む率 $a = \min_{\mathrm{Re}\,\lambda_k < 0} (-\mathrm{Re}\,\lambda_k) > 0$。$\varepsilon < a$ なら非線形項があっても縮む
- **$E^u$ 方向**: 伸びる率 $b = \min_{\mathrm{Re}\,\lambda_k > 0} \mathrm{Re}\,\lambda_k > 0$。$\varepsilon < b$ なら伸びる

近傍を小さくして $\varepsilon < a, b$ にすれば、縮む方向と伸びる方向の区別が保たれ、$W^s$ は $E^s$ を少し曲げた形で残る（厳密には Lyapunov-Perron 法で構成する）。

**双曲型でない場合**は $E^c \neq \{\boldsymbol{0}\}$ で、その方向の率は $0$ である。どんなに小さい $\varepsilon$ でも縮むか伸びるかは非線形項で決まり、この議論が使えない。これが後半の中心多様体の問題である。

---

## 振り子のセパラトリクス

振り子のサドル $\boldsymbol{q}_1^*, \boldsymbol{q}_2^*$（$\lambda = \pm 1$）は双曲型なので、定理から1次元の $W^s, W^u$ をもつ。線形化では「不安定」までしか言えないが、これらを軌道に沿って延ばすと、相図を仕切るセパラトリクスが得られる:

<img src="/figures/pendulum_manifolds.png" class="mx-auto" style="width: 770px" />

- 紫の弧は $\boldsymbol{q}_1^*$ を出て（$W^u(\boldsymbol{q}_1^*)$）$\boldsymbol{q}_2^*$ に入る（$W^s(\boldsymbol{q}_2^*)$）軌道で、両方の多様体を兼ねる
- 他の軌道はこれらを**横切れない**（解の一意性）ので、振動域 (libration) と回転域 (rotation) が仕切られる

---

## ホモクリニック軌道とヘテロクリニック軌道

振り子の上側の紫の弧 $W^u(\boldsymbol{q}_1^*) = W^s(\boldsymbol{q}_2^*)$ の点は、時間を戻すと $\boldsymbol{q}_1^*$ へ、進めると $\boldsymbol{q}_2^*$ へ近づく。一般に $\boldsymbol{q} \in W^u(\boldsymbol{q}_1^*) \cap W^s(\boldsymbol{q}_2^*)$ なら、その軌道は $t \to -\infty$ で $\boldsymbol{q}_1^*$ に、$t \to \infty$ で $\boldsymbol{q}_2^*$ に近づく。このように固定点どうしを結ぶ軌道を**接続軌道** (connecting orbit) と呼ぶ。

<img src="/figures/connections.png" class="mx-auto" style="width: 740px" />

- 左: $\boldsymbol{q}_1^* \neq \boldsymbol{q}_2^*$（別の固定点へ移る）なら**ヘテロクリニック軌道**。振り子の紫はこちら（$\theta$ と $\theta + 2\pi$ を同一視する円筒上では $\pm\pi$ が同じ点なので、ホモクリニックになる）
- 右: $\boldsymbol{q}_1^* = \boldsymbol{q}_2^*$（出発した固定点に戻る）なら**ホモクリニック軌道**。図は Duffing 振動子 $\ddot{x} = x - x^3$ で、ループは $W^u$ でも $W^s$ でもある（赤 = 出る側、青 = 入る側）

---

## 接続軌道が意味すること

どちらの例も、ポテンシャル $V$ の谷を玉が転がる運動として見られる。エネルギー $E$ は保存し、玉は $V \leq E$ の範囲（横線）しか動けない:

<img src="/figures/connection_energy.png" class="mx-auto" style="width: 800px" />

- **内側**（緑、相図ではループの内側）: 山を越えられず、谷の中で往復する（Duffing は片方の谷だけ）
- **外側**（灰）: 山を越える。振り子は回り続け、Duffing は両方の谷をまたいで往復する
- **接続軌道**（紫）: $E$ が山の頂上（サドル）とちょうど同じ。今回のケースでは、エネルギーがわずかに多ければ頂上を越え、少なければ手前で戻る。ちょうど同じときだけ、近づくほど遅くなって**有限の時間では着かない**。内側と外側の境目である

---

## 接続は構造的に脆い

振り子と Duffing 振動子で $W^u$ と $W^s$ がぴったり一致しているのは、エネルギーが保存され、両方が同じ等高線の上に乗っているからである。

減衰などの一般の摂動を加えると保存量がなくなり、$W^u$ と $W^s$ はずれて接続は消える。わずかな摂動で消えてしまうこの性質を**構造的に脆い**という（第3章で定式化する）。

接続が壊れる・残ることは、後の章で次の形で効いてくる:

- **カオス**（第5・6章）: 時間周期的な摂動を加えた系（のポアンカレ写像）では、ずれた $W^u$ と $W^s$ が**横断的に交わり**うる。交点の像も交点なので交点は無限個あり、$W^u$ は激しく折り畳まれる
- **流体**（第7章）: 定常流の剥離点と再付着点を結ぶ流線はヘテロクリニック接続で、**剥離領域の境界**を与える

---

## 双曲型の固定点でわかること

全ての $\mathrm{Re}(\lambda_k) \neq 0$ のとき、わかることは次の3段に積み上がる:

| 知りたいこと | 道具 | 答え |
|---|---|---|
| 安定か不安定か | 線形化・Hartman-Grobman の定理 | 固有値の実部の符号で決まる |
| 安定集合 $W^s$ はどんな形か | 安定多様体定理 | 近傍では $E^s$ に接する、同じ次元の多様体 |
| 近傍の外の構造 | $W^s, W^u$ を軌道に沿って延ばす | セパラトリクス・接続軌道が相空間を仕切る |

どの段も、固有値の実部が $0$ でないことを使っている。**$\mathrm{Re}(\lambda_k) = 0$ の方向（$E^c$）があると、最初の段の安定性から線形化では決まらない**。以下ではこの場合を扱う。

---

## 非双曲型の固定点

$E^c \neq \{\boldsymbol{0}\}$ の場合。座標を $E^c$ 方向 $\boldsymbol{x}$ と双曲方向 $\boldsymbol{y}$ に分けて書き直すと

$$
\begin{cases}
\dot{\boldsymbol{x}} = A\boldsymbol{x} + \boldsymbol{f}(\boldsymbol{x}, \boldsymbol{y}), & \boldsymbol{x} \in \mathbb{R}^{c}, \quad A \text{ の固有値は } \mathrm{Re}(\lambda) = 0 \\[2pt]
\dot{\boldsymbol{y}} = B\boldsymbol{y} + \boldsymbol{g}(\boldsymbol{x}, \boldsymbol{y}), & \boldsymbol{y} \in \mathbb{R}^{s}, \quad B \text{ の固有値は } \mathrm{Re}(\lambda) < 0
\end{cases}
$$

ここで $\boldsymbol{f}, \boldsymbol{g}$ は2次以上（$\boldsymbol{f}(\boldsymbol{0},\boldsymbol{0}) = \boldsymbol{0}$, $D\boldsymbol{f}(\boldsymbol{0},\boldsymbol{0}) = 0$、$\boldsymbol{g}$ も同様）。

**$E^u$ は除いてよい**: $E^u \neq \{\boldsymbol{0}\}$ なら $W^u$ に沿って離れる軌道が存在するので、不安定である。安定性が問題になるのは $\mathbb{R}^n = E^s \oplus E^c$ の場合だけである。

$\boldsymbol{y}$ 方向は指数的に減衰するので、$\boldsymbol{x}$ の方程式だけを調べればよいと考えられる。ただし **$\boldsymbol{y} = \boldsymbol{0}$ と置いて $\boldsymbol{y}$ を消すことはできない**。$\boldsymbol{y} = \boldsymbol{0}$ の上でも $\dot{\boldsymbol{y}} = \boldsymbol{g}(\boldsymbol{x}, \boldsymbol{0}) \neq \boldsymbol{0}$ となりうるので、$E^c$ は**不変ではない**。$\boldsymbol{y}$ の正しい消し方を与えるのが中心多様体定理である。

---

## 中心多様体定理

<div class="grid grid-cols-[1fr_400px] gap-8 items-center">
<div>

**定理** (Pliss 1964, Kelley 1967): $\boldsymbol{x}, \boldsymbol{y}$ に分けた系で $\boldsymbol{f}, \boldsymbol{g}$ が $C^r$ ($r \geq 2$) ならば、原点の近傍に

$$\boldsymbol{y} = \boldsymbol{h}(\boldsymbol{x}), \qquad \boldsymbol{h}(\boldsymbol{0}) = \boldsymbol{0}, \quad D\boldsymbol{h}(\boldsymbol{0}) = 0$$

のグラフとして表される $C^r$ 級の**中心多様体** $W^c$ が存在し、局所不変である。$\dim W^c = \dim E^c$ で、原点で $E^c$ に**接する**。

$\boldsymbol{h}(\boldsymbol{0}) = \boldsymbol{0}$ が「原点を通る」、$D\boldsymbol{h}(\boldsymbol{0}) = 0$ が「$E^c$ に接する」に対応する。

**局所不変**とは、軌道が $|\boldsymbol{x}| < \delta$ にいる間は $W^c$ 上に留まるという意味（外へ出た先は保証しない）。

</div>
<img src="/figures/center_manifold.png" style="width: 400px" />
</div>

---

## 縮約原理

**定理** (Shoshitaishvili 1975): $B$ の固有値が全て $\mathrm{Re}(\lambda) < 0$ のとき、原点の近傍で元の系は $\dot{\boldsymbol{x}} = A\boldsymbol{x} + \boldsymbol{f}(\boldsymbol{x}, \boldsymbol{h}(\boldsymbol{x}))$ と $\dot{\boldsymbol{y}} = -\boldsymbol{y}$ の**直積に位相的に同値**である。左が $W^c$ 上へ制限した**縮約系**、右は双曲方向の指数減衰を表す。

したがって、**原点の安定性は縮約系の安定性と一致する**。Hartman-Grobman の定理は「双曲型なら**線形系**に帰着する」と述べ、縮約原理は「非双曲型なら**低次元の非線形系**に帰着する」と述べている。

| | 縮約前 | 縮約後 |
|---|---|---|
| 次元 | $n = c + s$ | $c = \dim E^c$ |
| 線形部の固有値 | $\mathrm{Re}(\lambda) = 0$ と $\mathrm{Re}(\lambda) < 0$ が混在 | $\mathrm{Re}(\lambda) = 0$ のみ |
| 安定性 | 線形化では判定できない | 非線形項が決める |

---

## 中心多様体の方程式

**例**: $\boldsymbol{x}, \boldsymbol{y}$ に分けた形で $c = s = 1$、$A = 0$, $B = -1$ と取った場合。

$$\dot{x} = x y, \qquad \dot{y} = -y - x^2 \qquad\Longrightarrow\qquad J = \begin{pmatrix} 0 & 0 \\ 0 & -1 \end{pmatrix}, \quad \lambda = 0,\, -1$$

$E^c$ は $x$ 軸、$E^s$ は $y$ 軸。$W^c$ を $y = h(x)$, $h(0) = h'(0) = 0$ と置く。$W^c$ が不変であることは、**$W^c$ 上の $\dot{y}$ を2通りに計算した結果が一致すること**と同値である:

$$
\underbrace{h'(x)\,\dot{x}}_{\text{曲線に沿った微分}} \;=\; \underbrace{-h(x) - x^2}_{\text{方程式の右辺}},
\qquad \dot{x} = x\,h(x)
$$

$\dot{x} = x\,h(x)$ を代入すると、$h$ だけの方程式になる。

---

## 中心多様体の級数展開

$h(x) = a_2 x^2 + a_3 x^3 + a_4 x^4 + \cdots$ を代入し、次数ごとに係数を比べる:

| 次数 | 左辺 $h'(x)\,x\,h(x)$ | 右辺 $-h(x) - x^2$ | 結果 |
|---|---|---|---|
| $x^2$ | $0$ | $-a_2 - 1$ | $a_2 = -1$ |
| $x^3$ | $0$ | $-a_3$ | $a_3 = 0$ |
| $x^4$ | $2a_2^2 = 2$ | $-a_4$ | $a_4 = -2$ |

$$h(x) = -x^2 - 2x^4 + O(x^6) \qquad\Longrightarrow\qquad \dot{x} = x\,h(x) = -x^3 - 2x^5 + \cdots$$

主要項は $\dot{x} = -x^3$ なので**漸近安定**。ただし収束は指数的ではなく、$|x| \sim (2t)^{-1/2}$ と代数的に遅い。

---

## 数値解と縮約系の比較

<img src="/figures/center_manifold_example.png" class="mx-auto" style="width: 780px" />

- 左: 軌道はまず**緑の $W^c$ へ速く近づき**、その後 $W^c$ に沿ってゆっくり原点へ向かう
- **橙の破線 $E^c$ ($y = 0$) は不変ではない**。その上でも $\dot{y} = -x^2 \neq 0$ なので軌道は離れる。$y = 0$ と置くと $\dot{x} = 0$ となり、安定性を誤って判定する
- 右: $x(0) = 0.5$ からの $x(t)$ は、速い過渡のあと縮約系 $\dot{x} = -x^3$（緑破線）に重なる

---

## 中心多様体は一意でない

$$\dot{x} = x^2, \qquad \dot{y} = -y \qquad (\lambda = 0,\, -1)$$

軌道は $dy/dx = -y/x^2$ を解いて $y = Ce^{1/x}$。$x < 0$ の枝と $x \geq 0$ の $y = 0$ をつなぐと、**どの $C$ でも**不変な $C^\infty$ 曲線になる。

<img src="/figures/center_manifold_nonuniqueness.png" class="mx-auto" style="width: 520px" />

- $x \to 0^-$ で $e^{1/x}$ の**全ての階数の微分が $0$ に収束する**ので、どの曲線も $E^c$ に無限次まで接する
- 一意に決まるのは $\boldsymbol{h}$ の**テイラー係数**で、縮約系の展開も一致する。どの $W^c$ を選んでも安定性の結論は同じ

---

## 正規形

縮約系にはまだ非線形項が残っている。座標変換によって、これをできるだけ少ない項にするのが正規形理論である。$\dot{\boldsymbol{x}} = J\boldsymbol{x} + \sum_{k \geq 2} \boldsymbol{F}_k(\boldsymbol{x})$（$\boldsymbol{F}_k$ は $k$ 次の同次項）に、恒等写像に近い変換 $\boldsymbol{x} = \boldsymbol{y} + \boldsymbol{h}_k(\boldsymbol{y})$ を施すと

$$
\dot{\boldsymbol{y}} = J\boldsymbol{y} + \boldsymbol{F}_k(\boldsymbol{y}) - L_J\boldsymbol{h}_k(\boldsymbol{y}) + O(|\boldsymbol{y}|^{k+1}),
\qquad L_J \boldsymbol{h} := D\boldsymbol{h}(\boldsymbol{y})\,J\boldsymbol{y} - J\boldsymbol{h}(\boldsymbol{y})
$$

<img src="/figures/normal_form.png" class="mx-auto" style="width: 740px" />

$L_J$（**ホモロジー作用素**）は $k$ 次の同次ベクトル場の空間 $H_k$ 上の線形写像。$\boldsymbol{F}_k \in \mathrm{Im}\,L_J$ ならば、$\boldsymbol{h}_k$ を選んで $k$ 次の項を消せる。残るのは $\mathrm{Im}\,L_J$ の補空間にある成分だけである。

---

## 共鳴条件

$J = \mathrm{diag}(\lambda_1, \dots, \lambda_n)$ と対角化できる場合、単項式のベクトル場 $\boldsymbol{y}^{\boldsymbol{m}}\boldsymbol{e}_i$（$\boldsymbol{y}^{\boldsymbol{m}} = y_1^{m_1}\cdots y_n^{m_n}$, $|\boldsymbol{m}| = k$）は $L_J$ の固有ベクトルになる:

$$
L_J\bigl(\boldsymbol{y}^{\boldsymbol{m}}\boldsymbol{e}_i\bigr)
= \Bigl(\langle \boldsymbol{m}, \boldsymbol{\lambda}\rangle - \lambda_i\Bigr)\, \boldsymbol{y}^{\boldsymbol{m}}\boldsymbol{e}_i,
\qquad \langle \boldsymbol{m}, \boldsymbol{\lambda}\rangle = \sum_j m_j \lambda_j
$$

固有値 $\langle \boldsymbol{m}, \boldsymbol{\lambda}\rangle - \lambda_i$ が $0$ でなければ、その単項式は座標変換で消せる。$0$ になる場合を**共鳴** (resonance) と呼ぶ:

$$
\lambda_i = \sum_j m_j \lambda_j, \qquad m_j \geq 0, \quad \sum_j m_j \geq 2
$$

- **共鳴がなければ、任意の有限次数までの非線形項を消して $\dot{\boldsymbol{y}} = J\boldsymbol{y}$ にできる**（Poincaré）。位相的な同値を与える Hartman-Grobman と違い、こちらは多項式の座標変換による線形化である
- **$\mathrm{Re}(\lambda) = 0$ では共鳴が避けられない。** $\lambda = \pm i\omega$ なら $\lambda_1 = 2\lambda_1 + \lambda_2$（$2i\omega - i\omega = i\omega$）が常に成り立つ。そのため中心多様体上では、共鳴項が座標変換で消えずに残る

---

## センターの正規形

$\dim E^c = 2$, $\lambda = \pm i\omega$ の場合。2次の項は全て消え、3次で残る共鳴項は $|z|^2 z$ だけなので、複素座標 $z = y_1 + i y_2$ で正規形は

$$\dot{z} = i\omega z + c_1 |z|^2 z + O(|z|^5)$$

極座標 $z = re^{i\theta}$ を代入し（$\dot{z} = (\dot{r} + i r\dot{\theta})e^{i\theta}$）、実部と虚部を比べると

$$\dot{r} = \mathrm{Re}(c_1)\, r^3 + \cdots, \qquad \dot{\theta} = \omega + \mathrm{Im}(c_1)\, r^2 + \cdots$$

- **$\mathrm{Re}(c_1) \neq 0$ なら、安定性はその符号で決まる。** $\mathrm{Re}(c_1) < 0$ なら漸近安定（ただし $r \sim t^{-1/2}$ と遅い）、$\mathrm{Re}(c_1) > 0$ なら不安定
- $\mathrm{Re}(c_1)$ は**第1リアプノフ係数**と呼ばれる。$\mathrm{Im}(c_1)$ は振動数が振幅に依存すること（非線形の周波数ずれ）を表す
- 振り子のような保存系では $\mathrm{Re}(c_1) = 0$ となる（高次の項も同様で、閉軌道が保たれる）

---

## センターは構造的に脆い

振り子のセンターが閉軌道になるのは $\mathrm{Re}(c_1) = 0$、すなわち**保存系である**ためである。減衰 $-\varepsilon\omega$ を加えると $\dot{\omega} = -\sin\theta - \varepsilon\omega$ となり、$\lambda = (-\varepsilon \pm \sqrt{\varepsilon^2 - 4})/2$。

<img src="/figures/pendulum_perturbation.png" class="mx-auto" style="width: 560px" />

- $\varepsilon \neq 0$ なら固有値の実部は $0$ でなくなり**双曲型**になるので、線形化で判定できる（$\varepsilon > 0$ で安定、$\varepsilon < 0$ で不安定）
- $\mathrm{Re}(\lambda) = 0$ は、パラメータ空間で安定と不安定を分ける**境界**にあたる。中心多様体は、**この境界で起きる定性的な変化を記述する道具**にもなる

---

## まとめ

**① 双曲型の固定点では、固有空間 $E^s, E^u$ に接する不変多様体 $W^s, W^u$ が存在する。** 振り子のセパラトリクスは、サドルの $W^s \cup W^u$ である。

**② $\mathrm{Re}(\lambda) = 0$ の安定性は、中心多様体の上で決まる。** $E^c$ に制限する（$\boldsymbol{y} = \boldsymbol{0}$ と置く）のは誤りで、$\boldsymbol{h}$ の曲がりが結論を変える。

**③ 縮約した系は、共鳴項だけを残した正規形にできる。** センターでは $|z|^2 z$ が残り、その係数の実部が安定性を決める。

| | 線形（固有空間） | 非線形（不変多様体） | 安定性の決まり方 |
|---|---|---|---|
| $\mathrm{Re}(\lambda) \neq 0$ | $E^s,\ E^u$ | $W^s,\ W^u$（接する、同次元） | 指数的に減衰／成長 |
| $\mathrm{Re}(\lambda) = 0$ | $E^c$ | $W^c$（一意でない、局所不変） | 縮約系／正規形の係数 |

**次章へ**: センターの正規形にパラメータを入れた $\dot{z} = (\mu + i\omega)z + c_1|z|^2 z$ が Stuart-Landau 方程式で、$\mu$ が $0$ を**横切る瞬間**に何が起きるかが**分岐**の話になる → **第3章 分岐理論**
