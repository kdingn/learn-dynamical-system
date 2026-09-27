# learn-dynamical-system 設計方針

## ツール選定

- **画像**: matplotlib + scienceplots（論文品質、CM フォント）
- **動画**: manim（カラーパレットのみ matplotlib と共有 → `palette.py`）
- **資料**: Slidev（スライド形式、図・動画を多用しやすい）

## アーキテクチャ

- Python 側は `public/figures/` および `public/animations/` に生成物を出力する
- Slidev 側は `slides/public/` を静的アセットとして参照する（`slides/public` → `../public` のシンボリックリンク）
- `slides/` + `public/` + `package.json` を切り出せば Slidev 単独プロジェクトとして独立できる

## コマンド

- `rye run figures` — 全図を一括生成して `public/figures/` に出力
- `npm run dev` — 目次スライド（intro.md）を起動
- `npm run dev:01` — Ch.1 のスライドを起動（章が増えたら `dev:02`, `dev:03`, ... を追加）

## スタイル規約

- `style.apply()` を各 figure スクリプト先頭で呼ぶ
- 色は `palette.py` の定数を使う（ハードコード禁止）

## スタイル規約（スライド）

- スライドの frontmatter に `transition` を設定しない（アニメーションなし）
- `<v-click>` などの段階表示も使わない
- 図のラベル・凡例は英語（matplotlib のフォントが日本語非対応のため）

## 検証手順

- figure スクリプトを追加・変更したら `rye run figures` を実行し、エラーなく完了することを確認する
- スライドに画像を追加したら Slidev を `--no-open` 付きで起動し、画像が HTTP 200 で配信されること・import エラーが出ないことを確認する
  - 例: `npx slidev --no-open slides/01-basics.md` → `curl -s -o /dev/null -w "%{http_code}" http://localhost:3030/figures/<name>.png`

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
