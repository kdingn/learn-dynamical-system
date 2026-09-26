# learn-dynamical-system 設計方針

## ツール選定

- **画像**: matplotlib + scienceplots（論文品質、CM フォント）
- **動画**: manim（カラーパレットのみ matplotlib と共有 → `palette.py`）
- **資料**: Slidev（スライド形式、図・動画を多用しやすい）

## アーキテクチャ

- Python 側は `public/figures/` および `public/animations/` に生成物を出力する
- Slidev 側は `public/` を静的アセットとして参照する
- `slides/` + `public/` + `package.json` を切り出せば Slidev 単独プロジェクトとして独立できる

## コマンド

- `rye run figures` — 全図を一括生成して `public/figures/` に出力
- `npm run dev -- slides/<name>.md` — Slidev 開発サーバーを起動

## スタイル規約

- `style.apply()` を各 figure スクリプト先頭で呼ぶ
- 色は `palette.py` の定数を使う（ハードコード禁止）

## 検証手順

- figure スクリプトを追加・変更したら `rye run figures` を実行し、エラーなく完了することを確認する
- スライドに画像を追加したら `npm run dev -- slides/<name>.md` でビルドエラーが出ないことを確認する
