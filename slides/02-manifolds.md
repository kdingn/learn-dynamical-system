---
theme: default
# 図は透過 PNG でテーマに追従できないため、既定の auto ではなく dark に固定する
colorSchema: dark
title: "Ch.2 不変多様体と非線形解析"
drawings:
  persist: false
# 章の見取り図（components/Roadmap.vue）と右上の現在地表示（global-top.vue）が読む
chapter: "Ch.2"
roadmap:
  - '固有空間に当たるものは、非線形系では何か'
  - '双曲型なら、それはどんな形か'
  - 'その多様体は、固定点から遠くで何をするか'
  - '固有値の実部が 0 の方向では、何が安定性を決めるか'
  - '残った非線形項は、どこまで簡単にできるか'
roadmapAnswers:
  - '不変多様体。$E^s$ を「収束する初期値の集合」と言い直し、同じ形で安定集合 $W^s$ を定義する'
  - '$E^s, E^u$ に固定点で接する、同じ次元の多様体 $W^s, W^u$（安定多様体定理）'
  - '軌道に沿って延び、相空間を仕切る（セパラトリクス・接続軌道）。接続は摂動で壊れやすい'
  - '中心多様体 $W^c$ 上の低次元の方程式（縮約系）。$E^c$ に制限するのは誤り'
  - '共鳴項だけが残る正規形。センターでは $\mathrm{Re}(c_1)$ の符号が安定性を決める'
---

# 不変多様体と非線形解析

Chapter 2 — Learn Dynamical Systems

<img src="/figures/ch02_overview.png" class="mx-auto mt-6" style="width: 820px" />

---

## 線形化が「中立」と言うとき、乱れはどうなるか

Ch.1 の翼断面モデルを、流速がちょうどフラッター速度 $U_F$ のときで計算する。固有値は虚軸の上にあり（$\mathrm{Re}(\lambda) = 0$）、線形化は乱れの振幅が変わらない（破線）と予測する。

<img src="/figures/ch02_motivation.png" class="mx-auto" style="width: 820px" />

実際には、ねじりばねが振幅とともに硬くなるか（硬化）柔らかくなるか（軟化）だけで、乱れは**消えるか育つかに分かれる**。知りたいのは、**線形化で決まらないとき、何が乱れの行方を決めるか**である。本章のゴールは、これを**4次元の系を2次元に縮めた方程式の係数1つで判定できるようになること**。

<div class="text-sm opacity-60">

Ch.1 と同じ翼断面モデルに、ねじりばねの3次の項 $\kappa\alpha^3$ を加えた計算（実測ではない）

</div>

---

## 線形化の外側を調べるための5つの問い

Ch.1 の線形化が使えるのは、双曲型の固定点の近くだけだった。その外側、つまり**固定点から遠く**と**固有値の実部が $0$ の方向**を扱うために、固有空間を非線形系へ持ち上げる。

<Roadmap class="mt-4" />

<div class="mt-4">

固有値の物語では、固有値の実部が $0$ の方向の上で、非線形項まで含めたダイナミクスを調べる章にあたる。

</div>

---
part: 1
---

## Part 1: 固有空間に当たるものは、非線形系では何か

Ch.1 で、固定点のまわりの振る舞いは $J$ の固有値と固有ベクトルで分類でき、それが保証されるのは双曲型の固定点の近くだけだと分かった。

<Roadmap :current="1" class="mt-4" />

<div class="mt-4">

この Part では、固有ベクトルが張る空間（固有空間）に当たるものを、非線形系で定義する。

</div>

---

## 不変集合と不変多様体

<div class="grid grid-cols-[1fr_400px] gap-8 items-center">
<div>

固有空間には「その上から出発した解は、その上に留まる」という性質がある。この性質を非線形系に持ち込む。

**定義**: 集合 $S \subseteq \mathcal{M}$ が**不変** (invariant) とは、全ての $t$ で $\phi_t(S) \subseteq S$ となること。

解の一意性から、**任意の軌道は不変集合**である。固定点・周期軌道・セパラトリクスもそう。

**不変多様体**: 不変集合のうち、それ自体が多様体であるもの。多様体なら**次元**と**接空間**が定まり、固有空間と比べられる。以下でこの2つを定義する。

</div>
<img src="/figures/invariant_set.png" style="width: 400px" />
</div>

---

## 多様体と次元

<div class="grid grid-cols-[1fr_360px] gap-8 items-center">
<div>

以下、**一般の多様体を $M$ と書く**（相空間 $\mathcal{M}$ も、この章で扱う不変多様体も、その一例）。

**多様体** (manifold): 各点の近傍が $\mathbb{R}^k$ の開集合と1対1に対応し、その対応と逆がともに滑らかであるような集合。この対応 $\varphi$ を**局所座標**（チャート）と呼ぶ。

全体は曲がっていてよいが、各点の近傍は $\mathbb{R}^k$ と同じ構造をもつ。折れ目では滑らかさが、枝分かれ・自己交差では1対1が崩れるので、局所座標が取れない。

**次元** $k$: 局所座標の成分数。連結な多様体では点によらず一定で、$\dim M$ と書く。

</div>
<img src="/figures/manifold_chart.png" style="width: 360px" />
</div>

---

## 接空間

<div class="grid grid-cols-[1fr_360px] gap-8 items-center">
<div>

次元の次は、多様体の「向き」を表す接空間を定める。

**接空間** $T_pM$: $p$ を通る $M$ 上の滑らかな曲線 $\gamma(t)$（$\gamma(0) = p$）すべてについて、速度 $\dot{\gamma}(0)$ を集めたもの。$\gamma$ は軌道でなくてよい。

**$k = 1$**（上図）: 速さと向きは自由に選べる。$\gamma(2t)$ なら $2\boldsymbol{v}$、$\gamma(-t)$ なら $-\boldsymbol{v}$、定数曲線なら $\boldsymbol{0}$ で、全体は**直線**になる。

**$k = 2$**（下図）: 独立な2方向の速度の一次結合が全て現れ、**平面**になる。

</div>
<img src="/figures/tangent_space.png" style="width: 360px" />
</div>

---

## 接空間の次元

$k = 1, 2$ で見たことは、局所座標 $\varphi$ を使うと一般に示せる。座標側で $\varphi(p)$ を通る直線を引き、$M$ へ写す:

$$
\gamma_{\boldsymbol{c}}(t) = \varphi^{-1}\bigl(\varphi(p) + t\boldsymbol{c}\bigr),
\qquad
\dot{\gamma}_{\boldsymbol{c}}(0) = D\varphi^{-1}\bigl(\varphi(p)\bigr)\,\boldsymbol{c}
$$

任意の曲線の速度は $\boldsymbol{c} = (\varphi \circ \gamma)'(0)$ と取れば現れるので、**$T_pM$ はヤコビ行列 $D\varphi^{-1}$ の像**である。したがって $T_pM$ は線形部分空間で、$\dim T_pM = k$。

<img src="/figures/tangent_chart.png" class="mx-auto" style="width: 720px" />

---

## 接空間は $\mathbb{R}^n$ の部分空間

<div class="grid grid-cols-[1fr_340px] gap-8 items-center">
<div>

接空間を取る目的は、曲がった多様体を固有空間と比べることだった。

$T_pM$ の要素は**点ではなく速度ベクトル**で、$T_pM$ は**原点を通る** $\mathbb{R}^n$ の $k$ 次元部分空間である。図の接平面は、それを $p$ へ平行移動した $p + T_pM$ である。

$E$ が線形部分空間なら、$\boldsymbol{w} \in E$ に対して $\gamma(t) = t\boldsymbol{w}$ の速度は $\boldsymbol{w}$ なので、$T_{\boldsymbol{0}}E = E$。

接空間を取れば、曲がった不変多様体も平らな固有空間も**どちらも $\mathbb{R}^n$ の部分空間**になり、次元と向きを等号で比べられる。

</div>
<img src="/figures/tangent_subspace.png" style="width: 340px" />
</div>

---

## 線形系の固有空間分解

<div class="grid grid-cols-[1fr_360px] gap-8 items-center">
<div>

比べる相手の固有空間を、固有値の実部の符号で3つに分ける:

$$E^s = \operatorname{span}\bigl\{\, \boldsymbol{v}_k \;\bigm|\; \mathrm{Re}(\lambda_k) < 0 \,\bigr\}$$

$E^u,\ E^c$ も $> 0$、$= 0$ で同様に定めると $\mathbb{R}^n = E^s \oplus E^u \oplus E^c$（複素共役対は実部と虚部、重複固有値は一般化固有空間を取る）。

$E^s$ 上の解だけが $\boldsymbol{0}$ へ減衰するので、$E^s$ は**収束する初期値の集合**とも書ける:

$$E^s = \bigl\{\, \boldsymbol{\xi} \;\bigm|\; e^{Jt}\boldsymbol{\xi} \to \boldsymbol{0}\ \ (t \to \infty) \,\bigr\}$$

**双曲型**とは $E^c = \{\boldsymbol{0}\}$ のことである。

</div>
<img src="/figures/eigenspaces.png" style="width: 360px" />
</div>

---

## 安定集合と不安定集合

固有空間は $E^s = \{\boldsymbol{\xi} \mid e^{Jt}\boldsymbol{\xi} \to \boldsymbol{0}\}$ と、$J$ を使わず「解が収束するか」だけで書けた。そこで非線形系の固定点 $\boldsymbol{q}^*$ に対しても、同じ形で定義する:

$$
W^s(\boldsymbol{q}^*) = \bigl\{\, \boldsymbol{q} \;\bigm|\; \phi_t(\boldsymbol{q}) \to \boldsymbol{q}^*\ (t \to \infty) \,\bigr\},
\qquad
W^u(\boldsymbol{q}^*) = \bigl\{\, \boldsymbol{q} \;\bigm|\; \phi_t(\boldsymbol{q}) \to \boldsymbol{q}^*\ (t \to -\infty) \,\bigr\}
$$

それぞれ**安定集合**・**不安定集合**と呼ぶ。どちらも不変集合である。線形系なら $W^s = E^s$ だが、非線形系では定義だけからは形が分からない。$E^s$ と比べて知りたいのは次の3点である:

| 知りたいこと | 線形系の $E^s$ では |
|---|---|
| **形**: $W^s$ は多様体か | 部分空間なので多様体 |
| **次元**: $\dim W^s = \dim E^s$ か | 当然一致 |
| **向き**: $T_{\boldsymbol{q}^*}W^s = E^s$ か | 当然一致 |

---
part: 2
---

## Part 2: 双曲型なら、それはどんな形か

Part 1 で、固有空間 $E^s$ を「収束する初期値の集合」と言い直し、同じ形で非線形系の安定集合 $W^s$ を定義した。

<Roadmap :current="2" class="mt-4" />

<div class="mt-4">

この Part では、$W^s$ が $E^s$ と同じ形・次元・向きをもつかを調べる。

</div>

---

## サドルの安定集合と不安定集合

形・次元・向きの3点を、具体例で確かめる。左は線形化 $\dot{\boldsymbol{\xi}} = J\boldsymbol{\xi}$、右は非線形 $\dot{q}_1 = q_1 + q_2^2/2,\ \dot{q}_2 = -q_2 + q_1^2/2$（どちらも原点はサドル）。

<img src="/figures/stable_manifold.png" class="mx-auto" style="width: 450px" />

- 右図の**灰色の破線が固有空間** $E^s, E^u$。$W^s, W^u$ は**曲がる**が、原点ではこの破線に**接する**（$W^u: q_2 = q_1^2/6 + \cdots$）
- この例では3点とも成り立つ。一般に成り立つことを保証するのが安定多様体定理

---

## 安定多様体定理

サドルの例で見た3点は、双曲型の固定点なら一般に成り立つ。ただし保証されるのは $\boldsymbol{q}^*$ の近傍 $U$ の中だけなので、$U$ から出ない点に限った**局所安定集合**で述べる:

$$
W^s_{\mathrm{loc}}(\boldsymbol{q}^*) = \bigl\{\, \boldsymbol{q} \in U \;\bigm|\; \phi_t(\boldsymbol{q}) \to \boldsymbol{q}^*\ (t \to \infty),\ \ \phi_t(\boldsymbol{q}) \in U\ \ \forall\, t \geq 0 \,\bigr\}
$$

<div class="mt-3 px-5 py-1 border-l-4 border-teal-400 bg-white bg-opacity-5">

**定理** (Hadamard 1901, Perron 1928): $\boldsymbol{f}$ が $C^r$ ($r \geq 1$) で $\boldsymbol{q}^*$ が**双曲型**ならば、$U$ を十分小さく取ると、$W^s_{\mathrm{loc}}$ は $C^r$ 級の多様体で（**形**）、$\dim W^s_{\mathrm{loc}} = \dim E^s$（**次元**）、$\boldsymbol{q}^*$ で $E^s$ に接する（**向き**）。$W^u_{\mathrm{loc}}$ も同様。

</div>

多様体であることが保証されたので、以下 $W^s, W^u$ を**安定多様体・不安定多様体**と呼ぶ。

---

## 双曲型という仮定の役割

定理は、**どの方向の成長率（固有値の実部）も $0$ でない**ことを仮定している。この仮定が要る理由を見るため、ずれ $\boldsymbol{\xi} = \boldsymbol{q} - \boldsymbol{q}^*$ で書く:

$$
\dot{\boldsymbol{\xi}} = J\boldsymbol{\xi} + \boldsymbol{N}(\boldsymbol{\xi}), \qquad |\boldsymbol{N}(\boldsymbol{\xi})| \leq \varepsilon\,|\boldsymbol{\xi}| \quad (|\boldsymbol{\xi}| < \delta)
$$

$\boldsymbol{N}$ は2次以上なので、近傍を小さくするほど $\varepsilon$ も小さくできる。

- **$E^s$ 方向**: 減衰率 $a = \min (-\mathrm{Re}\,\lambda_k) > 0$。$\varepsilon < a$ なら非線形項があっても縮む
- **$E^u$ 方向**: 成長率 $b = \min \mathrm{Re}\,\lambda_k > 0$。$\varepsilon < b$ なら伸びる

縮む方向と伸びる方向の区別が保たれるので、$W^s$ は $E^s$ を少し曲げた形で残る。**$E^c$ 方向**は成長率が $0$ なので、縮むか伸びるかは非線形項で決まり、この議論が使えない。

---
part: 3
---

## Part 3: その多様体は、固定点から遠くで何をするか

Part 2 で、双曲型の固定点なら $W^s, W^u$ は $E^s, E^u$ に接する同じ次元の多様体だと分かった（安定多様体定理）。

<Roadmap :current="3" class="mt-4" />

<div class="mt-4">

定理が保証するのは固定点の近くだけである。この Part では、それを軌道に沿って延ばしたときに何が見えるかを調べる。

</div>

---

## 振り子のセパラトリクス

振り子のサドル $\boldsymbol{q}_1^*, \boldsymbol{q}_2^*$（$\lambda = \pm 1$）は双曲型なので、1次元の $W^s, W^u$ をもつ。線形化では「不安定」までしか言えないが、これらを軌道に沿って延ばすと、相図を仕切るセパラトリクスが得られる:

<img src="/figures/pendulum_manifolds.png" class="mx-auto" style="width: 770px" />

- 紫の弧は $\boldsymbol{q}_1^*$ を出て（$W^u(\boldsymbol{q}_1^*)$）$\boldsymbol{q}_2^*$ に入る（$W^s(\boldsymbol{q}_2^*)$）軌道で、両方の多様体を兼ねる
- 他の軌道はこれらを**横切れない**（解の一意性）ので、振動域と回転域が仕切られる

---

## ホモクリニック軌道とヘテロクリニック軌道

紫の弧のように、ある固定点の $W^u$ と別の（または同じ）固定点の $W^s$ に同時に乗る軌道は、$t \to -\infty$ で $\boldsymbol{q}_1^*$ に、$t \to \infty$ で $\boldsymbol{q}_2^*$ に近づく。このように固定点どうしを結ぶ軌道を**接続軌道** (connecting orbit) と呼ぶ。

<img src="/figures/connections.png" class="mx-auto" style="width: 740px" />

- 左: 別の固定点へ移る（$\boldsymbol{q}_1^* \neq \boldsymbol{q}_2^*$）なら**ヘテロクリニック軌道**。振り子の紫はこちら（$\theta$ を円周とみなす円筒上では、ホモクリニックになる）
- 右: 出発した固定点に戻るなら**ホモクリニック軌道**。図は Duffing 振動子 $\ddot{x} = x - x^3$（赤 = 出る側、青 = 入る側）

---

## 接続軌道が意味すること

接続軌道が何の境目かは、ポテンシャル $V$ の谷を玉が転がる運動として見ると分かる。エネルギー $E$ は保存し、玉は $V \leq E$ の範囲（横線）しか動けない:

<img src="/figures/connection_energy.png" class="mx-auto" style="width: 800px" />

- **内側**（緑）: 山を越えられず、谷の中で往復する
- **外側**（灰）: 山を越える。振り子は回り続け、Duffing は両方の谷をまたぐ
- **接続軌道**（紫）: $E$ が山の頂上（サドル）と同じ。近づくほど遅くなり**有限時間では着かない**。内側と外側の境目である

---

## 接続は構造的に脆い

振り子と Duffing 振動子で $W^u$ と $W^s$ がぴったり一致しているのは、エネルギーが保存され、両方が同じ等高線の上に乗っているからである。

<div class="flex flex-col gap-6 mt-4">
<div>

減衰などの一般の摂動を加えると保存量がなくなり、$W^u$ と $W^s$ はずれて接続は消える。わずかな摂動で消えてしまうこの性質を**構造的に脆い**という（第3章で定式化する）。

</div>
<div>

接続が壊れる・残ることは、後で次の形で効いてくる:

</div>
<div>

| 場面 | 何が起きるか |
|---|---|
| **カオス** | ずれた $W^u$ と $W^s$ が横断的に交わり、$W^u$ が激しく折り畳まれる（第5・6章） |
| **流体** | 剥離点と再付着点を結ぶ流線はヘテロクリニック接続で、剥離領域の境界を与える |

</div>
</div>

---

## 双曲型の固定点で分かったこと

Part 1〜3 をまとめると、全ての $\mathrm{Re}(\lambda_k) \neq 0$ のとき、分かることは次の3段に積み上がる:

| 知りたいこと | 道具 | 答え |
|---|---|---|
| 安定か不安定か | 線形化（Hartman-Grobman） | 固有値の実部の符号で決まる |
| $W^s$ はどんな形か | 安定多様体定理 | $E^s$ に接する、同じ次元の多様体 |
| 固定点から遠くの構造 | $W^s, W^u$ を延ばす | セパラトリクス・接続軌道が相空間を仕切る |

どの段も、固有値の実部が $0$ でないことを使っている。**$\mathrm{Re}(\lambda_k) = 0$ の方向（$E^c$）があると、最初の段の安定性から線形化では決まらない**。動機のフラッター速度での翼がこの場合である。

---
part: 4
---

## Part 4: 固有値の実部が 0 の方向では、何が安定性を決めるか

Part 3 までで、双曲型の固定点のまわりの構造は、固有値の実部の符号と $W^s, W^u$ で決まると分かった。

<Roadmap :current="4" class="mt-4" />

<div class="mt-4">

この Part では、固有値の実部が $0$ の方向があるとき、何が安定性を決めるかを調べる。

</div>

---

## 中心方向と双曲方向に分ける

$E^c \neq \{\boldsymbol{0}\}$ の場合を調べる。固定点からのずれを $E^c$ 方向 $\boldsymbol{x}$ と双曲方向 $\boldsymbol{y}$ に分けて書き直すと

$$
\begin{cases}
\dot{\boldsymbol{x}} = A\boldsymbol{x} + \boldsymbol{N}_c(\boldsymbol{x}, \boldsymbol{y}), & A \text{ の固有値は } \mathrm{Re}(\lambda) = 0 \\[2pt]
\dot{\boldsymbol{y}} = B\boldsymbol{y} + \boldsymbol{N}_s(\boldsymbol{x}, \boldsymbol{y}), & B \text{ の固有値は } \mathrm{Re}(\lambda) < 0
\end{cases}
$$

$\boldsymbol{N}_c, \boldsymbol{N}_s$ は非線形項で2次以上。動機の翼断面モデルなら、$\boldsymbol{x}$ は虚軸上の固有値 $\pm i\omega$ をもつ2次元（ねじれに近いモード）、$\boldsymbol{y}$ は減衰する残りの2次元である。

**$E^u$ は除いてよい**: $E^u \neq \{\boldsymbol{0}\}$ なら $W^u$ に沿って離れる軌道があるので不安定。安定性が問題になるのは $\mathbb{R}^n = E^s \oplus E^c$ の場合だけである。

---

## $\boldsymbol{y} = \boldsymbol{0}$ と置いてはいけない

$\boldsymbol{y}$ 方向は指数的に減衰するので、安定性は $\boldsymbol{x}$ の振る舞いで決まるはずで、$\boldsymbol{x}$ だけの方程式にして調べたい。

<div class="flex flex-col gap-6 mt-4">
<div>

ところが **$\boldsymbol{y} = \boldsymbol{0}$（$E^c$）と置くことはできない**。$E^c$ の上でも $\dot{\boldsymbol{y}} = \boldsymbol{N}_s(\boldsymbol{x}, \boldsymbol{0}) \neq \boldsymbol{0}$ となりうるので、$E^c$ は**不変ではない**。そこから出発した軌道は $E^c$ を離れてしまう。

</div>
<div>

$\boldsymbol{x}$ だけの方程式にするには、$E^c$ の代わりに、**$\boldsymbol{y}$ が $\boldsymbol{x}$ で決まる不変な曲面** $\boldsymbol{y} = \boldsymbol{h}(\boldsymbol{x})$ が要る。不変なので、その上から出発した軌道には $\boldsymbol{y} = \boldsymbol{h}(\boldsymbol{x})$ を代入し続けてよい。

</div>
<div>

これが $E^c$ に対応する不変多様体 $W^c$ で、$E^s, E^u$ に $W^s, W^u$ が対応したのと同じ関係にある。

</div>
</div>

---

## $W^s, W^u$ と $W^c$ の違い

$W^s, W^u$ は「収束する点の集合」として先に定義でき、示すべきはその形だけだった。$E^c$ の方向は成長率が $0$ で収束も発散もしないため、$W^c$ は同じようには定義できず、**存在から**示す必要がある。それが中心多様体定理である。

| | $W^s, W^u$ | $W^c$ |
|---|---|---|
| 定義 | 収束する点の集合として先に決まる | 収束では定義できない |
| 主張 | その集合は $E^s, E^u$ に接する多様体 | $E^c$ に接する局所不変な多様体が存在する |
| 一意性 | 一意 | 一意とは限らない |
| 役割 | 相空間を仕切る | 線形化で決まらない安定性を低次元で判定する |

---

## 中心多様体定理

$W^c$ の存在を保証するのが、次の定理である。

<div class="mt-3 px-5 py-1 border-l-4 border-teal-400 bg-white bg-opacity-5">

**定理** (Pliss 1964, Kelley 1967): $\boldsymbol{N}_c, \boldsymbol{N}_s$ が $C^r$ ($r \geq 2$) ならば、原点の近傍に、グラフ $\boldsymbol{y} = \boldsymbol{h}(\boldsymbol{x})$（$\boldsymbol{h}(\boldsymbol{0}) = \boldsymbol{0}$, $D\boldsymbol{h}(\boldsymbol{0}) = 0$）で表される $C^r$ 級の**中心多様体** $W^c$ が存在する。$W^c$ は局所不変で、$\dim W^c = \dim E^c$、原点で $E^c$ に接する。

</div>

<div class="grid grid-cols-[1fr_400px] gap-8 items-center">
<div>

右図の橙は速く縮む $\boldsymbol{y}$ 方向、緑は $W^c$ に沿う遅い運動。

$W^c$ が決めるのは軌道が**どこを通るか**で、**どちら向きに動くか**は $W^c$ 上の運動で決まる（$\dot{x} = \mp x^3$ のどちらでも $W^c$ は存在する）。

</div>
<img src="/figures/center_manifold.png" style="width: 400px" />
</div>

---

## $\boldsymbol{y}$ が $\boldsymbol{x}$ の関数になる理由

定理の直観を、いちばん単純な $\dot{y} = -y + g(x)$（$x$ はゆっくり動く）で見る。

1. **$x$ を止めると**: $y$ は $g(x)$ へ指数的に引き寄せられ、$y \approx g(x)$ に落ち着く
2. **$x$ がゆっくり動くと**: 行き先 $g(x)$ も動くが、$y$ はすぐ追いつくので、いつ見ても $y \approx g(x)$ になる
3. **式で見ると**: 解は $\;y(t) = e^{-t}\,y(0) + \int_0^t e^{-(t-\tau)}\, g\bigl(x(\tau)\bigr)\, d\tau$。初期値の項は消え、効くのは直近の $x$ だけなので、$y = h(x)$ と書ける

**$y$ の緩和が速いことが要る**。遅ければ $y$ は過去の $x$ を覚えていて、同じ $x$ でも $y$ が異なる。中心多様体は、この近似を $x$ が動く分の補正まで含めて正確にしたものである。

---

## 縮約原理

$W^c$ 上では $\boldsymbol{y} = \boldsymbol{h}(\boldsymbol{x})$ なので、代入すると $\boldsymbol{x}$ だけの方程式が閉じる。これを**縮約系**と呼ぶ:

$$\dot{\boldsymbol{x}} = A\boldsymbol{x} + \boldsymbol{N}_c\bigl(\boldsymbol{x}, \boldsymbol{h}(\boldsymbol{x})\bigr) \qquad (\dim E^c \text{ 次元})$$

<div class="my-8 px-5 py-1 border-l-4 border-teal-400 bg-white bg-opacity-5">

**定理** (Pliss 1964, Shoshitaishvili 1972): $E^u = \{\boldsymbol{0}\}$ のとき、原点の近傍で元の系は、縮約系と $\dot{\boldsymbol{y}} = -\boldsymbol{y}$ を並べた系と**位相的に同値**である。特に、原点の安定性は縮約系の安定性と一致する。

</div>

- $W^c$ へ近づく運動が $\dot{\boldsymbol{y}} = -\boldsymbol{y}$、$W^c$ に沿う運動が縮約系にあたる
- 収束か発散かは保たれるが、速さは保たれない（Hartman-Grobman の定理と同じ意味）
- $W^c$ の外の軌道も、$\boldsymbol{y}$ と $\boldsymbol{h}(\boldsymbol{x})$ のずれが指数的に消えて $W^c$ 上の軌道に追従する

---

## 中心多様体の方程式

縮約系を実際に求める。$\boldsymbol{x}, \boldsymbol{y}$ に分けた形で $\dim E^c = \dim E^s = 1$、$A = 0$, $B = -1$ と取った場合:

<div class="flex flex-col gap-6 mt-4">
<div>

$$\dot{x} = x y, \qquad \dot{y} = -y - x^2 \qquad\Longrightarrow\qquad J = \begin{pmatrix} 0 & 0 \\ 0 & -1 \end{pmatrix}, \quad \lambda = 0,\, -1$$

</div>
<div>

$E^c$ は $x$ 軸、$E^s$ は $y$ 軸。$W^c$ を $y = h(x)$, $h(0) = h'(0) = 0$ と置く。$W^c$ が不変であることは、**$W^c$ 上の $\dot{y}$ を2通りに計算した結果が一致すること**と同値である:

</div>
<div>

$$
\underbrace{h'(x)\,\dot{x}}_{\text{曲線に沿った微分}} \;=\; \underbrace{-h(x) - x^2}_{\text{方程式の右辺}},
\qquad \dot{x} = x\,h(x)
$$

</div>
<div>

$\dot{x} = x\,h(x)$ を代入すると、$h$ だけの方程式になる。

</div>
</div>

---

## 中心多様体の級数展開

$h$ だけの方程式は、$h(x) = a_2 x^2 + a_3 x^3 + a_4 x^4 + \cdots$ を代入し、次数ごとに係数を比べて解く:

<div class="flex flex-col gap-6 mt-4">
<div>

| 次数 | 左辺 $h'(x)\,x\,h(x)$ | 右辺 $-h(x) - x^2$ | 結果 |
|---|---|---|---|
| $x^2$ | $0$ | $-a_2 - 1$ | $a_2 = -1$ |
| $x^3$ | $0$ | $-a_3$ | $a_3 = 0$ |
| $x^4$ | $2a_2^2 = 2$ | $-a_4$ | $a_4 = -2$ |

</div>
<div>

$$h(x) = -x^2 - 2x^4 + O(x^6) \qquad\Longrightarrow\qquad \dot{x} = x\,h(x) = -x^3 - 2x^5 + \cdots$$

</div>
<div>

主要項は $\dot{x} = -x^3$ なので**漸近安定**。ただし収束は指数的ではなく、$|x| \sim (2t)^{-1/2}$ と代数的に遅い。

</div>
</div>

---

## 数値解と縮約系の比較

縮約系の結論を、元の2次元の系の数値解で確かめる。

<img src="/figures/center_manifold_example.png" class="mx-auto" style="width: 780px" />

- 左: 軌道はまず**緑の $W^c$ へ速く近づき**、その後 $W^c$ に沿ってゆっくり原点へ向かう
- **橙の破線 $E^c$ は不変ではない**。$y = 0$ と置くと $\dot{x} = 0$ となり、安定性を誤って判定する
- 右: $x(t)$ は、速い過渡のあと縮約系 $\dot{x} = -x^3$（緑破線）に重なる

---

## 中心多様体は一意でない

定理は存在を保証するが、一意性は保証しない。次の系がその例である:

$$\dot{x} = x^2, \qquad \dot{y} = -y \qquad (\lambda = 0,\, -1)$$

軌道は $y = Ce^{1/x}$。$x < 0$ の枝と $x \geq 0$ の $y = 0$ をつなぐと、**どの $C$ でも**不変な $C^\infty$ 曲線になる。

<img src="/figures/center_manifold_nonuniqueness.png" class="mx-auto" style="width: 520px" />

- $x \to 0^-$ で $e^{1/x}$ の全ての階数の微分が $0$ に収束するので、どの曲線も $E^c$ に無限次まで接する
- 一意に決まるのは $\boldsymbol{h}$ の**テイラー係数**で、どの $W^c$ を選んでも安定性の結論は同じ

---
part: 5
---

## Part 5: 残った非線形項は、どこまで簡単にできるか

Part 4 で、固有値の実部が $0$ のときの安定性は、中心多様体の上の縮約系で決まると分かった。

<Roadmap :current="5" class="mt-4" />

<div class="mt-4">

縮約系にもまだ多くの非線形項が残る。この Part では、座標の取り替えでどこまで簡単にできるかを調べ、動機のフラッターに答えを出す。

</div>

---

## 正規形の考え方

縮約系 $\dot{\boldsymbol{x}} = A\boldsymbol{x} + (\text{2次以上の項})$ には、一般に多くの非線形項がある。恒等写像に近い座標変換をしても軌道の形は変わらないが、項の係数は変わり、消せる項がある。**消せる項を全部消した形**を正規形と呼ぶ。

1次元の $\dot{x} = \lambda x + \alpha x^2$ で、新しい座標 $u$ を $x = u + \beta u^2$ と取る。両辺をそれぞれ $u$ で書くと

$$
\dot{x} = (1 + 2\beta u)\,\dot{u}, \qquad \lambda x + \alpha x^2 = \lambda u + (\lambda \beta + \alpha)\, u^2 + O(u^3)
$$

$$
\Longrightarrow\quad \dot{u} = \lambda u + (\alpha - \lambda \beta)\, u^2 + O(u^3)
$$

- $\lambda \neq 0$ なら $\beta = \alpha/\lambda$ と選べば $u^2$ の項が消える
- $\lambda = 0$（非双曲型）だと $u^2$ の係数は $\alpha$ のまま変わらず、どう選んでも消せない。この場合を**共鳴**と呼ぶ

---

## 共鳴という名前の由来

1次元の例で消せなかった理由を、振動の言葉で言い直す。

線形部だけなら $u \sim e^{\lambda t}$ なので、$u^2$ の項は $e^{2\lambda t}$ で変化する外力のように働く。その指数が $u$ 自身の $e^{\lambda t}$ と一致する（$2\lambda = \lambda$）と、固有振動数で揺らされた振動子と同じく応答が育ち、座標変換では吸収できない。

多変数でも同じで、線形部が $A = \mathrm{diag}(\lambda_1, \dots, \lambda_n)$ のとき、第 $i$ 成分の単項式 $u_1^{m_1} \cdots u_n^{m_n}$ が消せないのは次の場合である:

$$
\lambda_i = \sum_j m_j \lambda_j, \qquad m_j \geq 0, \quad \sum_j m_j \geq 2
$$

これを**共鳴** (resonance) と呼ぶ（1次元の例は $m = 2$ で $\lambda = 2\lambda$）。

---

## 共鳴が避けられない場合

共鳴条件から、正規形にどの項が残るかが分かる。

| 固有値 | 共鳴 | 正規形 |
|---|---|---|
| 共鳴条件を満たさない | なし | 任意の有限次数まで非線形項を消して $\dot{\boldsymbol{u}} = A\boldsymbol{u}$ にできる（Poincaré） |
| $\pm i\omega$（センター） | 必ず | $2i\omega - i\omega = i\omega$ なので $\lambda_1 = 2\lambda_1 + \lambda_2$ が常に成り立ち、共鳴項が残る |
| $\lambda_2 = 2\lambda_1$ など | あり | 項は残るが、双曲型なら安定性は線形部で決まり、結論に影響しない |

固有値の実部が $0$ の中心多様体の上では、共鳴項が座標変換で消えずに残る。それが安定性を決める。

---

## センターの正規形

$\dim E^c = 2$, $\lambda = \pm i\omega$ の場合。2次の項は全て消え、3次で残る共鳴項は $|z|^2 z$ だけなので、複素座標 $z = u_1 + i u_2$ で正規形は

$$\dot{z} = i\omega z + c_1 |z|^2 z + O(|z|^5)$$

$c_1$ は元の系の2次と3次の係数で決まる（2次の項を消す変換が新たな3次の項を生むため）。極座標 $z = re^{i\theta}$ を代入して実部と虚部を比べると

$$\dot{r} = \mathrm{Re}(c_1)\, r^3 + \cdots, \qquad \dot{\theta} = \omega + \mathrm{Im}(c_1)\, r^2 + \cdots$$

- **$\mathrm{Re}(c_1) \neq 0$ なら、安定性はその符号で決まる**。$\mathrm{Re}(c_1) < 0$ なら漸近安定（ただし $r \sim t^{-1/2}$ と遅い）、$\mathrm{Re}(c_1) > 0$ なら不安定
- $\mathrm{Re}(c_1)$ を**第1リアプノフ係数**と呼ぶ。$\mathrm{Im}(c_1)$ は振動数が振幅に依存すること（非線形の周波数ずれ）を表す

---

## 単振り子のセンターが閉軌道のまま残る理由

Ch.1 では、単振り子のセンターが閉軌道になることをエネルギー保存から結論した。正規形で見ると、保存系では $\mathrm{Re}(c_1) = 0$（高次の項も同様）で、$\dot{r} = 0$ が保たれるからである。

減衰 $-\varepsilon\omega$ を加えると $\dot{\omega} = -\sin\theta - \varepsilon\omega$ となり、$\lambda = (-\varepsilon \pm \sqrt{\varepsilon^2 - 4})/2$。

<img src="/figures/pendulum_perturbation.png" class="mx-auto" style="width: 620px" />

- $\varepsilon \neq 0$ なら**双曲型**になり、線形化で判定できる（$\varepsilon > 0$ で安定、$\varepsilon < 0$ で不安定）
- $\mathrm{Re}(\lambda) = 0$ は、パラメータ空間で安定と不安定を分ける**境界**にあたる

---

## 例: フラッター速度での乱れは、$\mathrm{Re}(c_1)$ の符号で決まる

動機の翼断面モデル（$n = 4$）に戻る。$U = U_F$ では固有値 $\pm i\omega$ の対が1つあり、残りの対は減衰する。中心多様体（2次元）へ縮約して正規形にし、$\mathrm{Re}(c_1)$ を計算した:

<img src="/figures/flutter_normal_form.png" class="mx-auto" style="width: 820px" />

硬化ばねで $\mathrm{Re}(c_1) < 0$（消える）、軟化ばねで $\mathrm{Re}(c_1) > 0$（育つ）。縮約した2次元の式 $\dot{r} = \mathrm{Re}(c_1) r^3$ の予測（破線）は、4次元の数値解と振幅が小さいうちは重なる。大きくなると、捨てた $O(r^5)$ の項が効いて離れる。

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

**① 双曲型の固定点では、固有空間 $E^s, E^u$ に接する不変多様体 $W^s, W^u$ が存在する。** 延ばすと相空間を仕切り、振り子のセパラトリクスはサドルの $W^s \cup W^u$ である。

</div>
<div>

**② 固有値の実部が $0$ のときの安定性は、中心多様体の上で決まる。** $E^c$ に制限する（$\boldsymbol{y} = \boldsymbol{0}$ と置く）のは誤りである。

</div>
<div>

| | 線形（固有空間） | 非線形（不変多様体） | 安定性の決まり方 |
|---|---|---|---|
| $\mathrm{Re}(\lambda) \neq 0$ | $E^s,\ E^u$ | $W^s,\ W^u$（接する、同次元） | 指数的に減衰／成長 |
| $\mathrm{Re}(\lambda) = 0$ | $E^c$ | $W^c$（一意でない、局所不変） | 縮約系／正規形の係数 |

</div>
<div>

**③ 縮約した系は、共鳴項だけを残した正規形にできる。** センターでは $|z|^2 z$ が残り、$\mathrm{Re}(c_1)$ の符号が安定性を決める。

</div>
</div>

---

## 次章へ: 境目を越えるとき

本章では、固有値の実部がちょうど $0$ の「境目」を調べた。次章では、パラメータを動かして境目を**越える**ときを扱う。

<div class="flex flex-col gap-6 mt-8">
<div class="px-5 py-2 border-l-4 border-gray-500 bg-white bg-opacity-5">

**固有値が虚軸を横切った後、乱れはどうなるか**

センターの正規形にパラメータ $\mu$ を入れると、Stuart-Landau 方程式 $\dot{z} = (\mu + i\omega)z + c_1|z|^2 z$ になる。$\mu > 0$ で生まれる振動の大きさは $\mathrm{Re}(c_1)$ の符号で決まる。

</div>
<div class="px-5 py-2 border-l-4 border-gray-500 bg-white bg-opacity-5">

**「構造的に脆い」とはどういうことか**

接続軌道やセンターは、わずかな摂動で消えたり形が変わったりした。これを構造安定性として定式化し、どんな系がどんな仕方で脆いかを分類する。

</div>
</div>

<div class="mt-8">

→ **第3章** 分岐理論

</div>
