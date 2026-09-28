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

## 線形化が答えなかった2つのこと

Ch.1 で、固定点まわりの振る舞いは $J$ の固有値に帰着した。ただし Hartman-Grobman の定理が保証するのは、**双曲型**（全ての $\mathrm{Re}(\lambda_k) \neq 0$）の固定点の、**ごく近傍だけ**である。残された問いは2つあり、どちらも「固定点1点の情報では足りない」という同じ形をしている。

**① 近傍の外はどうなるか。** 振り子のセパラトリクスは、サドルのそばから出発して相空間を横断し、隣のサドルまで届いていた。こうした軌道は固定点の近傍だけを見ても掴めない。固有空間 $E^s, E^u$ は線形系にしか定義されていないので、**非線形系の上に「固有空間にあたる集合」を定義し直す**必要がある。

**② $\mathrm{Re}(\lambda_k) = 0$ のときはどうするか。** 線形化が定性的な情報を失う場合。振り子のセンターがその例で、Ch.1 ではエネルギー保存という特殊事情に頼って閉軌道だと結論した。一般の系にそんな保存量はない。

どちらに対しても、Poincaré 以降の答えは共通している —— **固定点ではなく、そこへ出入りする「面」を主役にする**。その面が本章の主題、不変多様体である。

<div class="mt-4 px-5 py-2 border-l-4 border-teal-400 bg-white bg-opacity-5">

本章のゴール: 不変多様体の言葉で ① 大域的な軌道構造を記述し、② $\mathrm{Re}(\lambda) = 0$ の安定性を**中心多様体上に縮約した低次元の方程式**として判定できるようになること。

</div>

---

## この章の流れ

<div class="grid grid-cols-2 gap-x-12 gap-y-6 mt-4">
<div>

**1. 不変性を定義する**

流れに対して閉じた集合とは何か。固定点・周期軌道・セパラトリクスを同じ言葉で扱えるようになる。

</div>
<div>

**2. 比べる道具をそろえる**

多様体の**次元・接空間**と、線形側の固有空間 $\mathbb{R}^n = E^s \oplus E^u \oplus E^c$。どちらも $\mathbb{R}^n$ の線形部分空間になる。

</div>
<div>

**3. 非線形へ持ち上げる**

安定多様体定理。双曲型なら $W^s, W^u$ が $E^s, E^u$ に**接して同じ次元で**存在する。

</div>
<div>

**4. 中立方向だけを残す**

中心多様体定理と縮約原理。$\mathrm{Re}(\lambda) = 0$ の方向へ次元を落とし、正規形で最簡形にする。

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

軌道の一意性（Ch.1）から**任意の軌道は不変集合**である。固定点・周期軌道・セパラトリクスは、この意味では同じ種類のものになる。

**不変多様体** (invariant manifold): 不変集合のうち、それ自体が多様体（局所的に $\mathbb{R}^k$ と同相）であるもの。

なぜ多様体であることを要求するのか。**次元**と**接空間**が定まり、線形側（固有空間）と直接比べられるようになるからである。次の3ページでこの2つを押さえる。

</div>
<img src="/figures/invariant_set.png" style="width: 400px" />
</div>

---

## 多様体と次元

<div class="grid grid-cols-[1fr_360px] gap-8 items-center">
<div>

Ch.1 では相空間 $\mathcal{M}$ を「多様体」と呼んだだけで定義を与えていなかった。以下、**一般の多様体を $M$ と書く**（相空間 $\mathcal{M}$ も、この章で作る不変多様体も、その一例）。

**多様体** (manifold): どの点のまわりを見ても $\mathbb{R}^k$ の開集合と1対1に対応づけられる集合。この対応を**局所座標**（チャート）$\varphi$ と呼ぶ。

要点は「全体は曲がっていてよいが、**どの点のそばも平らな $\mathbb{R}^k$ と同じ**」であること。折れ目・分岐・自己交差があると、その点で座標が入らず多様体にならない。

**次元** $k$: 局所座標の個数、つまり「何個のパラメータで動けるか」。連結なら点のとり方によらず一定で、これを $\dim M$ と書く。

</div>
<img src="/figures/manifold_chart.png" style="width: 360px" />
</div>

---

## 接空間 —— $p$ で許される速度の全体

<div class="grid grid-cols-[1fr_360px] gap-8 items-center">
<div>

**接空間** $T_pM$: $p$ を通って $M$ 上を走る滑らかな曲線 $\gamma(t)$（$\gamma(0) = p$）を**すべて**考え、その速度 $\dot{\gamma}(0)$ として現れうるベクトルを集めたもの。$\gamma$ は力学系の軌道でなくてよい。

**$k = 1$**（上図）: 道は $M$ 一本きりだが、走り方は自由。$\gamma(2t)$ なら $2\boldsymbol{v}$、$\gamma(-t)$ なら $-\boldsymbol{v}$、止まったままなら $\boldsymbol{0}$。現れる速度は**ちょうど $\boldsymbol{v}$ の定数倍の全体**で、これは**直線**。

**$k = 2$**（下図）: $p$ から**独立な2方向**へ出られるので、$\dot{\gamma}_1(0)$, $\dot{\gamma}_2(0)$ とその一次結合が現れて**平面**になる。

</div>
<img src="/figures/tangent_space.png" style="width: 360px" />
</div>

---

## なぜ $k$ 次元の「空間」になるのか

「速度が無数にある」だけでは空間になりません（向きだけ集めれば円周で、足し算に閉じない）。効いているのは**局所座標**で、平らな側で $\varphi(p)$ を通るまっすぐな線を引き、$M$ へ送り返します:

$$
\gamma_{\boldsymbol{c}}(t) = \varphi^{-1}\bigl(\varphi(p) + t\boldsymbol{c}\bigr),
\qquad
\dot{\gamma}_{\boldsymbol{c}}(0) = D\varphi^{-1}\bigl(\varphi(p)\bigr)\,\boldsymbol{c}
$$

$\boldsymbol{c} \in \mathbb{R}^k$ を動かせば速度は出尽くす。つまり **$T_pM$ はヤコビ行列 $D\varphi^{-1}$ の像**で、像だから定数倍にも足し算にも自動で閉じ、階数が $k$ なので次元も $k$ になる。$k = 1$ も $k = 2$ も、この一つの構成の特殊化である。

<img src="/figures/tangent_chart.png" class="mx-auto" style="width: 720px" />

---

## 接空間は原点を通る —— 線形側と比べる準備

<div class="grid grid-cols-[1fr_340px] gap-8 items-center">
<div>

$T_pM$ の要素は**点ではなく速度ベクトル**である。止まったままの曲線 $\gamma(t) = p$ の速度は $\boldsymbol{0}$ なので $\boldsymbol{0} \in T_pM$。つまり $T_pM$ は**原点を通る** $\mathbb{R}^n$ の $k$ 次元部分空間（図の接平面は、それを $p$ に生やした $p + T_pM$ のほう）。

$E$ 自身が原点を通る平面なら、$\boldsymbol{w} \in E$ ごとに $\gamma(t) = t\boldsymbol{w}$ が $E$ 上の曲線でその速度は $\boldsymbol{w}$。だから $T_{\boldsymbol{0}}E = E$ —— 平らなものの1次近似は自分自身。

**これで比べる準備ができた。** 非線形の不変多様体は曲がり、線形の固有空間は平らで、そのままでは比べようがない。接空間を取れば**どちらも同じ $\mathbb{R}^n$ の中の平らな部分空間**になり、等号で結べる（$\mathbb{R}^k$ と同型なだけでは足りず、$\mathbb{R}^n$ の中でどちらを向いているかまで込みだから意味がある）。次ページで線形側を用意する。

</div>
<img src="/figures/tangent_subspace.png" style="width: 340px" />
</div>

---

## 線形系の固有空間分解

<div class="grid grid-cols-[1fr_360px] gap-8 items-center">
<div>

比べる相手はこちら。$\dot{\boldsymbol{\xi}} = J\boldsymbol{\xi}$ の固有値 $\lambda_k$ と固有ベクトル $\boldsymbol{v}_k$ を、実部の符号で3組に分けて張る:

$$E^s = \operatorname{span}\bigl\{\, \boldsymbol{v}_k \;\bigm|\; \mathrm{Re}(\lambda_k) < 0 \,\bigr\}$$

$E^u,\ E^c$ も $> 0$、$= 0$ で同様に定めると $\mathbb{R}^n = E^s \oplus E^u \oplus E^c$（複素共役対は実部と虚部、重複固有値は一般化固有空間 $\ker(J - \lambda_k I)^m$ を取る）。

**$E^s$ は不変**: $JE^s \subseteq E^s$ なので $e^{Jt}$ も $E^s$ を保つ。しかも $E^s$ 上の解は**前向きの時間で指数的に $\boldsymbol{0}$ へ減衰する** —— ある $a > 0$ で $|e^{Jt}\boldsymbol{\xi}| \leq Ce^{-at}|\boldsymbol{\xi}|\ (t \geq 0)$。

$E^u$ は逆で、**後ろ向きの時間で**同じ形に減衰する（前向きには発散）。$E^c$ ではどちら向きにもこの評価が取れず、そこが本章の焦点。**双曲型**とは $E^c = \{\boldsymbol{0}\}$ のことである。

</div>
<img src="/figures/eigenspaces.png" style="width: 360px" />
</div>

---

## 安定多様体定理

固定点 $\boldsymbol{q}^*$ の近傍 $U$ に対し、**局所安定多様体**を次で定める（$t \to -\infty$ に取り替えたものが $W^u_{\mathrm{loc}}$）:

$$
W^s_{\mathrm{loc}}(\boldsymbol{q}^*) = \bigl\{\, \boldsymbol{q} \in U \;\bigm|\; \phi_t(\boldsymbol{q}) \to \boldsymbol{q}^*\ (t \to \infty),\ \ \phi_t(\boldsymbol{q}) \in U\ \ \forall\, t \geq 0 \,\bigr\}
$$

**定理** (Hadamard 1901, Perron 1928): $\boldsymbol{f}$ が $C^r$ ($r \geq 1$) で $\boldsymbol{q}^*$ が**双曲型**ならば、$U$ を十分小さく取ると $W^s_{\mathrm{loc}}$ は $C^r$ 級の多様体であり、$\dim W^s_{\mathrm{loc}} = \dim E^s$ で、$\boldsymbol{q}^*$ において $E^s$ に**接する**（接空間の言葉で書けば $T_{\boldsymbol{q}^*}W^s_{\mathrm{loc}} = E^s$）。$W^u_{\mathrm{loc}}$ も同様。

<div class="mt-3 px-5 py-1 border-l-4 border-teal-400 bg-white bg-opacity-5">

**証明の筋** —— Lyapunov-Perron の積分方程式（$P_s, P_u$ は $E^s, E^u$ への射影、$\boldsymbol{N} = O(|\boldsymbol{\xi}|^2)$ は非線形項）

$$
\boldsymbol{\xi}(t) = e^{Jt}P_s\boldsymbol{\xi}(0) + \int_0^{t} \!\! e^{J(t-\tau)}P_s\boldsymbol{N}\,d\tau \;-\; \int_t^{\infty} \!\! e^{J(t-\tau)}P_u\boldsymbol{N}\,d\tau
$$

の右辺を「指数減衰する有界な解」の空間上の写像と見ると、**双曲性が与える減衰率の隙間**と $\boldsymbol{N}$ の2次性から縮小写像になる。その不動点が $W^s$ 上の解を与える。 $\blacksquare$

</div>

---

## 固有空間から不変多様体へ

左は線形化 $\dot{\boldsymbol{\xi}} = J\boldsymbol{\xi}$、右は非線形 $\dot{q}_1 = q_1 + q_2^2/2,\ \ \dot{q}_2 = -q_2 + q_1^2/2$（どちらも原点はサドル）。

<img src="/figures/stable_manifold.png" class="mx-auto" style="width: 450px" />

- 右図の**灰色の破線が固有空間** $E^s, E^u$（左図で実線で描いたもの）。非線形では多様体が**曲がる**が、原点では $W^s, W^u$ がこの破線に**接して**いる（$W^u: q_2 = q_1^2/6 + \cdots$、$W^s: q_1 = -q_2^2/6 + \cdots$）
- 次元も本数も線形と同じ。双曲型なら $\dim W^s + \dim W^u = n$ で、近傍のどの方向も収束か発散のどちらかに属する

---

## 局所から大域へ —— セパラトリクスの正体

$W^s_{\mathrm{loc}}$ は固定点のそばでしか定義されていないが、不変性から**フローで流せば延ばせる**: $W^s(\boldsymbol{q}^*) = \bigcup_{t \leq 0} \phi_t(W^s_{\mathrm{loc}})$、$W^u(\boldsymbol{q}^*) = \bigcup_{t \geq 0} \phi_t(W^u_{\mathrm{loc}})$。

<img src="/figures/pendulum_manifolds.png" class="mx-auto" style="width: 770px" />

- **青 = $W^s$、赤 = $W^u$**（$\theta = \pm\pi$ のサドルのもの）、**紫は両方を兼ねる部分**（次ページ）。Ch.1 の**セパラトリクス**の正体はこの $W^s \cup W^u$ だった
- $W^s$ は不変なので他の軌道はこれを**横切れない**（軌道の一意性）。だから振動域 (libration) と回転域 (rotation) を分ける境界になる

---

## ホモクリニック接続とヘテロクリニック接続

$W^u$ と $W^s$ が交わると、両端で固定点に漸近する軌道ができる。同じ固定点なら**ホモクリニック軌道**、異なる固定点どうしなら**ヘテロクリニック軌道**。振り子の紫の枝は後者だった。

<img src="/figures/connections.png" class="mx-auto" style="width: 740px" />

- 接続は**構造的に脆い**。上の例では保存量のおかげで $W^u$ と $W^s$ が一本に重なる（色は役割の違い）が、摂動を加えるとずれる
- ずれた $W^u$ と $W^s$ が**横断的に交わる**と、交点の軌道全体が交点になるため交わりは無限に続き、$W^u$ が激しく折り畳まれる。これがカオスの発生機構のひとつ（→ 第5・6章）
- 流体では、定常流の剥離点と再付着点を結ぶ流線がヘテロクリニック接続で、**剥離領域の境界**を与える（→ 第7章）

---

## 非双曲型の固定点 —— 問題を切り分ける

$E^c \neq \{\boldsymbol{0}\}$ の場合。座標を $E^c$ 方向 $\boldsymbol{x}$ と双曲方向 $\boldsymbol{y}$ に分けて書き直すと

$$
\begin{cases}
\dot{\boldsymbol{x}} = A\boldsymbol{x} + \boldsymbol{f}(\boldsymbol{x}, \boldsymbol{y}), & \boldsymbol{x} \in \mathbb{R}^{c}, \quad A \text{ の固有値は } \mathrm{Re}(\lambda) = 0 \\[2pt]
\dot{\boldsymbol{y}} = B\boldsymbol{y} + \boldsymbol{g}(\boldsymbol{x}, \boldsymbol{y}), & \boldsymbol{y} \in \mathbb{R}^{s}, \quad B \text{ の固有値は } \mathrm{Re}(\lambda) < 0
\end{cases}
$$

ここで $\boldsymbol{f}, \boldsymbol{g}$ は2次以上（$\boldsymbol{f}(\boldsymbol{0},\boldsymbol{0}) = \boldsymbol{0}$, $D\boldsymbol{f}(\boldsymbol{0},\boldsymbol{0}) = 0$、$\boldsymbol{g}$ も同様）。

**$E^u$ を外してよい理由**: $E^u \neq \{\boldsymbol{0}\}$ なら $W^u$ に沿って離れる軌道が実際に存在するので、その時点で不安定と結論できる。安定性が非自明なのは $\mathbb{R}^n = E^s \oplus E^c$ の場合だけである。

**問い**: $\boldsymbol{y}$ 方向は $e^{-at}$ で潰れるので、残るのは $\boldsymbol{x}$ の方程式。ではそこから $\boldsymbol{y}$ をどう消すか。**$\boldsymbol{y} = \boldsymbol{0}$ と置くのは誤り**である。$\boldsymbol{y} = \boldsymbol{0}$ の上でも $\dot{\boldsymbol{y}} = \boldsymbol{g}(\boldsymbol{x}, \boldsymbol{0}) \neq \boldsymbol{0}$ となりうるので、$E^c$ は**不変ではない**。正しい消し方を与えるのが次の定理になる。

---

## 中心多様体定理

<div class="grid grid-cols-[1fr_400px] gap-8 items-center">
<div>

**定理** (Pliss 1964, Kelley 1967): 前ページの系で $\boldsymbol{f}, \boldsymbol{g}$ が $C^r$ ($r \geq 2$) ならば、原点の近傍に

$$\boldsymbol{y} = \boldsymbol{h}(\boldsymbol{x}), \qquad \boldsymbol{h}(\boldsymbol{0}) = \boldsymbol{0}, \quad D\boldsymbol{h}(\boldsymbol{0}) = 0$$

のグラフとして表される $C^r$ 級の**中心多様体** $W^c$ が存在し、局所不変である。$\dim W^c = \dim E^c$ で、原点で $E^c$ に**接する**。

$\boldsymbol{h}(\boldsymbol{0}) = \boldsymbol{0}$ が「原点を通る」、$D\boldsymbol{h}(\boldsymbol{0}) = 0$ が「$E^c$ に接する」に対応する。

**局所不変**とは、軌道が $|\boldsymbol{x}| < \delta$ にいる間は $W^c$ 上に留まるという意味（外へ出た先は保証しない）。

</div>
<img src="/figures/center_manifold.png" style="width: 400px" />
</div>

---

## 縮約原理

**定理** (Shoshitaishvili 1975): $B$ の固有値が全て $\mathrm{Re}(\lambda) < 0$ のとき、原点の近傍で元の系は$\dot{\boldsymbol{x}} = A\boldsymbol{x} + \boldsymbol{f}(\boldsymbol{x}, \boldsymbol{h}(\boldsymbol{x}))$ と $\dot{\boldsymbol{y}} = -\boldsymbol{y}$ の**直積に位相的に同値**である。左が $W^c$ 上へ制限した**縮約系**、右は双曲方向の指数減衰を表す。

つまり $\boldsymbol{y}$ 方向には「素直に潰れる」以上のことは起きず、**原点の安定性は縮約系の安定性と一致する**。Hartman-Grobman が「双曲型なら**線形系**に帰着する」と言ったのに対し、縮約原理は「非双曲型なら**低次元の非線形系**に帰着する」と言っている。

| | 縮約前 | 縮約後 |
|---|---|---|
| 次元 | $n = c + s$ | $c = \dim E^c$ |
| 線形部の固有値 | $\mathrm{Re}(\lambda) = 0$ と $\mathrm{Re}(\lambda) < 0$ が混在 | $\mathrm{Re}(\lambda) = 0$ のみ |
| 安定性 | 線形化では判定できない | 非線形項が決める |

---

## 中心多様体を求める —— 不変性の方程式

**例**: 前ページの形で $c = s = 1$、$A = 0$, $B = -1$ と取った場合。

$$\dot{x} = x y, \qquad \dot{y} = -y - x^2 \qquad\Longrightarrow\qquad J = \begin{pmatrix} 0 & 0 \\ 0 & -1 \end{pmatrix}, \quad \lambda = 0,\, -1$$

$E^c$ は $x$ 軸、$E^s$ は $y$ 軸。$W^c$ を $y = h(x)$, $h(0) = h'(0) = 0$ と置くと、**不変性は「$\dot{y}$ を2通りに計算して一致させること」と書ける**:

$$
\underbrace{h'(x)\,\dot{x}}_{\text{曲線に沿った微分}} \;=\; \underbrace{-h(x) - x^2}_{\text{方程式の右辺}},
\qquad \dot{x} = x\,h(x)
$$

左辺の $\dot{x}$ に縮約系そのものが入るのがこの方程式の特徴で、$h$ について閉じた関係になっている。

---

## 中心多様体を求める —— 係数を次数ごとに決める

$h(x) = a_2 x^2 + a_3 x^3 + a_4 x^4 + \cdots$ を代入し、次数ごとに係数を比べる:

| 次数 | 左辺 $h'(x)\,x\,h(x)$ | 右辺 $-h(x) - x^2$ | 結果 |
|---|---|---|---|
| $x^2$ | $0$ | $-a_2 - 1$ | $a_2 = -1$ |
| $x^3$ | $0$ | $-a_3$ | $a_3 = 0$ |
| $x^4$ | $2a_2^2 = 2$ | $-a_4$ | $a_4 = -2$ |

$$h(x) = -x^2 - 2x^4 + O(x^6) \qquad\Longrightarrow\qquad \dot{x} = x\,h(x) = -x^3 - 2x^5 + \cdots$$

主要項は $\dot{x} = -x^3$ なので**漸近安定**。ただし収束は指数的でなく $|x| \sim (2t)^{-1/2}$ と代数的で、中心方向が「遅い」のはこのためである。

---

## 縮約が効いていることを確かめる

<img src="/figures/center_manifold_example.png" class="mx-auto" style="width: 780px" />

- 左: 軌道はまず**緑の $W^c$ へ速く落ち**、そのあと $W^c$ に沿ってゆっくり原点へ向かう
- **橙の破線 $E^c$ ($y = 0$) は不変でない** —— その上でも $\dot{y} = -x^2 \neq 0$ なので軌道はすぐ外れる。ここで $y = 0$ と置いて $\dot{x} = x\cdot 0 = 0$、ゆえに中立と結論するのが典型的な誤り
- 右: $x(0) = 0.5$ からの $x(t)$ は、速い過渡のあと縮約系 $\dot{x} = -x^3$（緑破線）に重なる

---

## 中心多様体は一意でない

$$\dot{x} = x^2, \qquad \dot{y} = -y \qquad (\lambda = 0,\, -1)$$

軌道は $dy/dx = -y/x^2$ を解いて $y = Ce^{1/x}$。$x < 0$ の枝と $x \geq 0$ の $y = 0$ をつなぐと、**どの $C$ でも**不変な $C^\infty$ 曲線になる。

<img src="/figures/center_manifold_nonuniqueness.png" class="mx-auto" style="width: 520px" />

- $x \to 0^-$ で $e^{1/x}$ は**全ての階数の微分が $0$** なので、どの曲線も $E^c$ に無限次まで接する。一意なのは $\boldsymbol{h}$ の**テイラー係数**のほうで、曲線どうしの差はどんな多項式よりも小さい「平坦な」項だけ
- **困らない理由**: どの $W^c$ を選んでも縮約系は（座標変換を除いて）一致し、安定性の結論は変わらない

---

## 正規形 —— 非線形項をどこまで消せるか

縮約で次元は落ちたが、$W^c$ 上の方程式には非線形項が残っている。これを座標変換で**最も簡単な形**にするのが正規形理論である。$\dot{\boldsymbol{x}} = J\boldsymbol{x} + \sum_{k \geq 2} \boldsymbol{F}_k(\boldsymbol{x})$（$\boldsymbol{F}_k$ は $k$ 次の同次項）に、恒等写像に近い変換 $\boldsymbol{x} = \boldsymbol{y} + \boldsymbol{h}_k(\boldsymbol{y})$ を施すと

$$
\dot{\boldsymbol{y}} = J\boldsymbol{y} + \boldsymbol{F}_k(\boldsymbol{y}) - L_J\boldsymbol{h}_k(\boldsymbol{y}) + O(|\boldsymbol{y}|^{k+1}),
\qquad L_J \boldsymbol{h} := D\boldsymbol{h}(\boldsymbol{y})\,J\boldsymbol{y} - J\boldsymbol{h}(\boldsymbol{y})
$$

<img src="/figures/normal_form.png" class="mx-auto" style="width: 740px" />

$L_J$（**ホモロジー作用素**）は $k$ 次の同次ベクトル場の空間 $H_k$ 上の線形写像。$\boldsymbol{F}_k \in \mathrm{Im}\,L_J$ ならば $\boldsymbol{h}_k$ を選んで $k$ 次の項を丸ごと消せる。残るのは $\mathrm{Im}\,L_J$ の補空間にある成分だけである。

---

## 共鳴条件

$J = \mathrm{diag}(\lambda_1, \dots, \lambda_n)$ と対角化できる場合、単項式のベクトル場$\boldsymbol{y}^{\boldsymbol{m}}\boldsymbol{e}_i$（$\boldsymbol{y}^{\boldsymbol{m}} = y_1^{m_1}\cdots y_n^{m_n}$, $|\boldsymbol{m}| = k$）は $L_J$ の固有ベクトルになる:

$$
L_J\bigl(\boldsymbol{y}^{\boldsymbol{m}}\boldsymbol{e}_i\bigr)
= \Bigl(\langle \boldsymbol{m}, \boldsymbol{\lambda}\rangle - \lambda_i\Bigr)\, \boldsymbol{y}^{\boldsymbol{m}}\boldsymbol{e}_i,
\qquad \langle \boldsymbol{m}, \boldsymbol{\lambda}\rangle = \sum_j m_j \lambda_j
$$

固有値 $\langle \boldsymbol{m}, \boldsymbol{\lambda}\rangle - \lambda_i$ が $0$ でなければ、その単項式は座標変換で消せる。$0$ になる場合を**共鳴** (resonance) と呼ぶ:

$$
\lambda_i = \sum_j m_j \lambda_j, \qquad m_j \geq 0, \quad \sum_j m_j \geq 2
$$

- **双曲型で共鳴がなければ、全ての非線形項が消えて $\dot{\boldsymbol{y}} = J\boldsymbol{y}$ になる**（Poincaré の定理）。位相的な同値しか主張しない Hartman-Grobman と違い、こちらは解析的な変換による線形化である
- **$\mathrm{Re}(\lambda) = 0$ では共鳴が避けられない。** $\lambda = \pm i\omega$ なら $\lambda_1 = 2\lambda_1 + \lambda_2$（$2i\omega - i\omega = i\omega$）が恒等的に成り立つ。中心多様体上に非線形項が残るのは、偶然ではなく構造的な事情による

---

## センターの安定性を決めるもの

$\dim E^c = 2$, $\lambda = \pm i\omega$ の場合。共鳴条件を満たす3次の項は $|z|^2 z$ の形に限られるので、複素座標 $z = y_1 + i y_2$ で正規形は

$$\dot{z} = i\omega z + c_1 |z|^2 z + O(|z|^5)$$

極座標 $z = re^{i\theta}$ を代入し（$\dot{z} = (\dot{r} + i r\dot{\theta})e^{i\theta}$）、実部と虚部を比べると

$$\dot{r} = \mathrm{Re}(c_1)\, r^3 + \cdots, \qquad \dot{\theta} = \omega + \mathrm{Im}(c_1)\, r^2 + \cdots$$

- **線形化では決まらなかった安定性が、3次の係数ひとつで決まる。** $\mathrm{Re}(c_1) < 0$ なら漸近安定（ただし $r \sim t^{-1/2}$ と遅い）、$\mathrm{Re}(c_1) > 0$ なら不安定
- $\mathrm{Re}(c_1)$ は**第1リアプノフ係数**と呼ばれる。$\mathrm{Im}(c_1)$ のほうは振動数が振幅に依存すること（非線形の周波数ずれ）を表す
- 保存系では $\mathrm{Re}(c_1) = 0$ になり、振幅が変化しない。振り子のセンターがその場合である

---

## センターは構造的に脆い

Ch.1 の宿題への答え。振り子のセンターが閉軌道のままだったのは $\mathrm{Re}(c_1) = 0$、すなわち**保存系という特殊事情**による。減衰 $-\varepsilon\omega$ を加えると $\dot{\omega} = -\sin\theta - \varepsilon\omega$ となり、$\lambda = (-\varepsilon \pm \sqrt{\varepsilon^2 - 4})/2$。

<img src="/figures/pendulum_perturbation.png" class="mx-auto" style="width: 560px" />

- $\varepsilon \neq 0$ にした瞬間 $\mathrm{Re}(\lambda) = -\varepsilon/2 \neq 0$ で**双曲型**になり、Ch.1 の判定がそのまま効く。符号だけで安定と不安定が入れ替わる
- つまり $\mathrm{Re}(\lambda) = 0$ はパラメータ空間の中では**境界**でしかない。中心多様体は、**パラメータを動かしたとき定性が変わる場所を記述する道具**でもある

---

## まとめ

**① 線形の固有空間は、非線形系では不変多様体になる。** Ch.1 のセパラトリクスは、サドルの $W^s \cup W^u$ だった。

**② $\mathrm{Re}(\lambda) = 0$ の安定性は、中心多様体の上で決まる。** $E^c$ に制限する（$\boldsymbol{y} = \boldsymbol{0}$ と置く）のは誤りで、$\boldsymbol{h}$ の曲がりが結論を変える。

**③ 縮約した系は、共鳴項だけを残した正規形にできる。** センターでは $|z|^2 z$ が残り、その係数の実部が安定性を決める。

| | 線形（固有空間） | 非線形（不変多様体） | 安定性の決まり方 |
|---|---|---|---|
| $\mathrm{Re}(\lambda) \neq 0$ | $E^s,\ E^u$ | $W^s,\ W^u$（接する、同次元） | 指数的に減衰／成長 |
| $\mathrm{Re}(\lambda) = 0$ | $E^c$ | $W^c$（一意でない、局所不変） | 縮約系／正規形の係数 |

**次章へ**: センターの正規形にパラメータを入れた $\dot{z} = (\mu + i\omega)z + c_1|z|^2 z$ が Stuart-Landau 方程式で、$\mu$ が $0$ を**横切る瞬間**に何が起きるかが**分岐**の話になる → **第3章 分岐理論**
