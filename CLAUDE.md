# learn-dynamical-system 設計方針

## ツール選定

- **画像**: matplotlib + scienceplots（論文品質、CM フォント）
- **動画**: manim（カラーパレットのみ matplotlib と共有 → `palette.py`）
- **資料**: Slidev（スライド形式、図・動画を多用しやすい）

## アーキテクチャ

- Python 側は `public/figures/` および `public/animations/` に生成物を出力する
  - 生成スクリプトは出力先を `mkdir(parents=True, exist_ok=True)` で自分で作る
    （`public/` 配下は丸ごと gitignore。`.gitkeep` は置かない）
- Slidev の `publicDir` は `slides/vite.config.mts` でリポジトリ直下の `public/` に向けている
  - Slidev の既定は `dirname(entry)/public`（= `slides/public`）だが、リンクや複製で
    同じ画像が2つのパスに見えるのを避けるため設定で上書きしている
  - 拡張子は `.mts`。`package.json` に `"type": "module"` がないため `.ts` だと
    CommonJS 扱いになり Vite が警告を出す
- `slides/` + `public/` + `package.json` を切り出せば Slidev 単独プロジェクトとして独立できる

## コマンド

- `rye run figures` — 全図を一括生成して `public/figures/` に出力
- `npm run dev` — 目次スライド（intro.md）を起動
- `npm run dev:01` — Ch.1 のスライドを起動（章が増えたら `dev:02`, `dev:03`, ... を追加）
- `npm run check:01` — Ch.1 を PNG に書き出してレイアウトを機械チェック
  （実体は `rye run check-slides slides/01-basics.md`。`--keep <dir>` で PNG を残せる）

## スタイル規約

- `style.apply()` を各 figure スクリプト先頭で呼ぶ
- 色は `palette.py` の定数を使う（ハードコード禁止）
  - `facecolor="white"` のような個別指定もしない。背景色・枠色は
    `style.apply()` の rcParams（透過）に任せる
  - matplotlib 組み込みのカラーマップ（`coolwarm` など）も使わない。中間色が
    背景に埋もれるため、`style.sequential_cmap(...)` で palette から作る

### テーマは dark に固定する

- 各スライドの headmatter に `colorSchema: dark` を書く。
  Slidev の既定は `auto` で、**閲覧環境の設定次第で背景が白にも黒にもなる**。
  図は透過 PNG でテーマに追従できないため、固定しないと文字が背景に埋もれる
- `palette.py` は背景 `#121212` / 本文 `#ddd`（`@slidev/client/uno.config.ts`）を
  前提にコントラストを取っている。テーマを変えるなら `colorSchema` と
  `palette.py` を必ずセットで変更する
- `check_slides.py` は headmatter を読んで `--dark` を付けて書き出すので、
  チェック結果は実際の見え方と一致する

## 図のサイズとフォント（スライドに載せる図の作り方）

図の文字がスライド本文と違う大きさに見える原因は、ほぼ**図の縮小表示**にある。
これを防ぐため、図は**スライド上の表示サイズちょうどで作り、等倍で貼る**。

- figsize は `style.slot(width_px, height_px)` で CSS px から逆算する
- スライド側は同じ px で表示する — `<img ... style="width: {width_px}px" />`
- スロットの値は figure スクリプトの `SLOT_*` 定数に置き、**md 側の `width` と一致させる**
  （ずれた瞬間に拡大縮小がかかり、フォントが本文と合わなくなる）
- フォントは `style.apply()` が設定する `BASE_FONT_PT`(13.2) / `SMALL_FONT_PT` に任せ、
  個別の `fontsize=` 指定は原則書かない
- `savefig.bbox="tight"` は使わない。出力画素数が figsize からずれて等倍の前提が壊れる。
  余白は `constrained_layout`（`style.apply()` で有効化済み）で詰める
- **見出し・キャプションとの間隔は、スライド側の margin ではなく図の外周 pad で取る**
  （`style.FIGURE_PAD_PX = 20`）。理由は下記
- 複数パネルの図では、どのタイトル・軸がどのパネルのものか分かるよう、
  パネル間を離す（`constrained_layout.wspace/hspace = 0.09`。既定の 0.02 は詰まりすぎ）
- ラベル同士・ラベルと軸線の重なりは書き出した PNG でしか分からない。
  フォントを大きくすると新たに衝突するので、目視確認で必ず見る

根拠となる実寸（`@slidev/parser`, `@slidev/client/styles/layouts-base.css` より）:

| 項目 | 値 |
|------|-----|
| キャンバス | 980 × 551.25 CSS px（`canvasWidth: 980`, 16:9） |
| `.slidev-layout` のパディング | `px-14 py-10` = 左右 56px / 上下 40px |
| 内容領域 | 868 × 471.25 px |
| 本文 | `text-[1.1rem]` = 17.6px |
| `h2` 見出し | `text-3xl` = 30px（行高 36px） |

つまり `h2` + 図だけのスライドなら図に使える高さは約 **420px**、
キャプションを1〜2行入れるなら **330〜380px** が上限。

### 間隔は「図の外周 pad」で取る（スライド側の margin ではなく）

matplotlib の既定の外周 pad は `0.04167in` = **4 CSS px** しかなく、そのままでは
見出しやキャプションに図が接触して見える。これを `style.FIGURE_PAD_PX`(20px) に
広げてある。スライド側に margin を足す方式より、次の点で扱いやすい:

- `constrained_layout` は**外周 pad を確保してからパネルを配置する**ので、
  pad を入れてもパネルの配置ロジックにしわ寄せが行かない
- PNG の画素数は SLOT のまま変わらない。つまり **SLOT_* の値がそのまま
  「スライド上で占める総量」**になり、上の高さ計算に margin を足し引きしなくて済む
- 図ごとに margin を書く必要がないので、書き忘れによる接触が構造的に起きない

実測（Ch.1 の図スライド）: 見出し下端から図の上端まで **27〜30px**。
pad を入れる前は約 7.5px だった。

### アスペクト固定は内部余白の原因になる

`set_aspect("equal")` を掛けた軸は正方形に固定されるため、横長のスロットに
置くと**図の内側に**大きな余白ができる（`eigenvalue_plane` では左右に
120px / 82px あった）。等方性が意味を持たない模式図では掛けない。

逆に、等方性が必要な図（相図など）を格子に並べると、パネルの大きさは
**行の高さだけで決まり、幅を広げても大きくならない**。大きくしたいときは
タイトルの行数・目盛・軸ラベルといった縦方向のオーバーヘッドを削るか、
段数を減らす（スライドを分ける）。

## スタイル規約（スライド）

- スライドの frontmatter に `transition` を設定しない（アニメーションなし）
- `<v-click>` などの段階表示も使わない
- 図のラベル・凡例は英語（matplotlib のフォントが日本語非対応のため）
- **図を載せるスライドは「見出し + 図 + 説明1〜3行」に留める**。
  本文が多くて収まらないなら、図を別スライドに分けるか2カラムにする。
  図を小さくして詰め込むのは禁止（文字が本文と合わなくなり読めなくなる）
- 2カラムは `<div class="grid grid-cols-[1fr_{width_px}px] gap-8 items-center">` で、
  図の列幅をスロットの px に合わせる

## 記号の規約（数式）

章をまたいで記号を揃える。ここがぶれると、同じ量が章ごとに別物に見える。

| 量 | 記号 | 備考 |
|----|------|------|
| 状態ベクトル | $\boldsymbol{q}$ | 流体・ROM の文献に合わせる。成分は $q_1, q_2, \dots$ |
| 固定点 | $\boldsymbol{q}^*$ | |
| ベクトル場 / 写像 | $\boldsymbol{f}$, $\boldsymbol{F}$ | |
| 摂動（固定点からのずれ） | $\boldsymbol{\xi}$ | 状態そのものではないので $q$ にしない |
| 零ベクトル | $\boldsymbol{0}$ | スカラーの $0$ と区別する |
| ヤコビアン | $J = D\boldsymbol{f}(\boldsymbol{q}^*)$ | |
| 固有値 / 固有ベクトル | $\lambda_k$, $\boldsymbol{v}_k$ | |

- **ベクトルの太字は `\boldsymbol` を使い、`\mathbf` は使わない**
  - `\mathbf` はボールド立体（セリフ）で角ばって見える。`\boldsymbol` はボールド
    イタリックで、ISO 80000-2 のベクトル表記もこちら
  - `\mathbf` はギリシャ文字に効かないので、混在させると $\boldsymbol{\xi}$ だけ
    字形が変わってしまう
- **図の軸ラベルは本文と同じ記号にする**。本文が $\boldsymbol{q}$ なのに図が
  $x_1, x_2$ だと別の量に見える。記号を変えるときは `slides/*.md` と
  `figures/*.py` の両方を必ず一緒に直す
- 物理的に意味のある変数（単振り子の $\theta, \omega$ など）は、抽象的な状態
  ベクトルとは役割が違うので無理に $q$ に統一しない

## 検証手順

- figure スクリプトを追加・変更したら `rye run figures` を実行し、エラーなく完了することを確認する
- スライドに画像を追加したら、先に `rye run figures` で PNG を生成してから Slidev を
  `--no-open` 付きで起動し、画像が配信されること・import エラーが出ないことを確認する
  - **ステータスコードだけ見てはいけない**: Slidev は SPA なので存在しないパスにも
    `index.html` を 200 で返す。`Content-Type` が `image/png` であることまで確認する
- **章を書き終えたら、必ず最後にスライドの全容を確認する**（図を後から足した場合は特に）
  1. `npm run check:01` を実行し、全スライドが `OK` になるまで直す
     - `CLIP` = 内容がキャンバス端で切れている（最優先で修正）
     - `TIGHT` = 切れてはいないがパディング帯に食い込んでいる
     - `GAP` = 内容領域の占有率が低く、余白が不自然に多い
  2. 機械チェックを通したうえで、`--keep` で残した PNG を**全枚数目視する**。
     figure のフォントが本文と同じ大きさに見えるか、余白が偏っていないかを見る
  3. 収まらないスライドは、図を縮めるのではなく**分割する**（上記スライド規約）
  - 例: `npx slidev --no-open slides/01-basics.md` →
    `curl -s -D - -o /dev/null http://localhost:3030/figures/<name>.png | grep -i content-type`

## 章を追加するとき

1. `src/learn_dynamical_system/figures/chNN.py` を作り、`figures/__main__.py` から呼ぶ
2. 図ごとに `SLOT_*` 定数を決めてから描く（先にスライド上の置き場所を決める）
3. `slides/NN-*.md` を作る。headmatter に `colorSchema: dark` を忘れない
4. `package.json` に **`dev:NN` と `check:NN` の両方**を追加する
   （`check:NN` は `rye run check-slides slides/NN-*.md --keep .slides-check`）
5. `rye run figures` → `npm run check:NN` → PNG を全枚数目視

## 環境・編集上のハマりどころ

実際に踏んだもの。同じ失敗を繰り返さないために残す。

- **LaTeX を含む md をシェル経由で書かない**。`cat > file <<'EOF'` のように
  ヒアドキュメントをクォートしても `\\` が `\` に潰れ、`\begin{cases}` や
  `pmatrix` の改行が壊れる（レンダリング結果が1行に潰れるだけなので気づきにくい）。
  Write / Edit ツールで直接書くこと。同じ理由で、検証のための `grep` パターンも
  シェル経由だと壊れるので、確認はファイルを直接読むほうが確実
- **`public/figures/` は図をリネーム・分割しても古い PNG が残る**。参照が消えた
  ファイルは配信され続けるので気づけない。名前を変えたときは
  `rm -rf public && rye run figures` で作り直して確認する
- **Windows では `npx` の出力が cp932 で decode 失敗する**。`subprocess` は
  `encoding="utf-8", errors="replace"` を指定する（`check_slides.py` 対応済み）。
  日本語を print するスクリプトは `sys.stdout.reconfigure(encoding="utf-8")` も必要
- **クローン直後は `playwright-chromium` のブラウザが落ちてこない**。npm が
  install script をブロックするため、`npm install-scripts approve playwright-chromium`
  を実行する。これをしないと `npm run check:NN` が export で失敗する
- 起動時に出る `Failed to patch FloatingVue ... reading 'Popper'` は Slidev 53 と
  floating-vue の既知の警告。twoslash のツールチップ以外に影響しないので無視してよい

## カリキュラム

全体を貫く軸は**固有値**。各章で固有値の概念がどう拡張されるかが物語の背骨。

対象: 流体力学×機械学習のアカデミア研究者。数学系の人とも共通言語で話せるレベル。
方針: 数学的な背景・導出・前提定理を押さえてリッチに作る。

| # | スライドファイル | タイトル | 内容 | 固有値の役割 |
|---|-----------------|---------|------|-------------|
| 1 | `slides/01-basics.md` | 力学系の基礎と線形安定性 | 相空間・フロー・写像、固定点、ヤコビアン、固有値の実部（減衰/成長）と虚部（振動）、ノード・スパイラル・サドル・センターの分類、Hartman-Grobman定理 | λ of J → 固定点分類 |
| 2 | `slides/02-manifolds.md` | 不変多様体と非線形解析 | 安定・不安定・中心多様体、中心多様体定理、安定多様体定理、正規形理論の導入、「線形で足りない場合」の扱い | 中心多様体上（Re(λ)=0）の非線形ダイナミクス |
| 3 | `slides/03-bifurcation.md` | 分岐理論 | 構造安定性、余次元1分岐（サドルノード・トランスクリティカル・ピッチフォーク・ホップ）、各正規形の導出、Stuart-Landau方程式（ホップ正規形＝流体起源）、分岐図 | λ が虚軸を横切る → 定性変化 |
| 4 | `slides/04-limit-cycle.md` | リミットサイクルと位相縮約 | 周期軌道、ポアンカレ写像、Floquet理論（モノドロミー行列）、Floquet乗数による安定性判定、位相縮約・アイソクロン、Poincaré-Bendixson定理 | Floquet乗数 = 周期軌道版の固有値 |
| 5 | `slides/05-routes-to-chaos.md` | カオスへの道 | 周期倍分岐（Feigenbaum）、準周期→カオス（Ruelle-Takens）、間欠性（Pomeau-Manneville）、分岐点での固有値構造がルートを決定 | Floquet乗数が−1を横切る → 周期倍分岐 etc. |
| 6 | `slides/06-chaos.md` | カオスとアトラクタ | ストレンジアトラクタ、リアプノフ指数の定義と計算、Lorenz系の詳細解析、エルゴード性・混合、フラクタル次元 | リアプノフ指数 = 軌道に沿った固有値の時間平均 |
| 7 | `slides/07-fluid-dynamics.md` | 流体力学の力学系的視点 | Navier-Stokesを無限次元力学系として定式化、関数空間・作用素、Orr-Sommerfeld方程式（線形安定性）、Kuramoto-Sivashinsky方程式、9方程式モデル | 行列の λ → 作用素のスペクトル |
| 8 | `slides/08-reduction.md` | 低次元化手法 | Galerkin射影、POD（固有直交分解）、DMD（動的モード分解）、これらの数学的関係の整理 | POD=共分散の固有値、DMD≈Koopmanの固有値 |
| 9 | `slides/09-data-driven.md` | データ駆動型力学系 | Koopman作用素理論（非線形→線形の持ち上げ）、EDMD、SINDy（スパース回帰による支配方程式同定）、Neural ODE / PINN、オペレータ学習（DeepONet, FNO） | Koopman固有関数 = 非線形系の「座標」 |
| 10 | `slides/10-control.md` | 安定性解析と制御 | データ駆動安定性解析、モデル予測制御、強化学習による制御 | 全章の固有値解析を制御に接続 |

### 構成の意図

- **1→2→3**: 古典的な固定点解析の三段構え（線形→非線形→分岐）
- **3→4→5→6**: 固定点→周期軌道→カオスへの発展。各段階で固有値の概念が拡張される
- **7→8→9**: 無限次元の世界に入り、それをどう扱うかの三段構え
- **10**: 全体の統合と応用
- K-S方程式は7章で導入し、9章のSINDy/Neural ODEで「同じ方程式をデータから復元する」例として再登場

### 進め方

- 1章から順に作成し、読みながら修正を繰り返す
- 既存の `slides/intro.md` は目次・導入として残し、各章スライドへのナビゲーションとする
