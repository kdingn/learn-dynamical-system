## Learn Dynamical System

力学系を理解するための教材プロジェクト。

### セットアップ

```bash
# Python 依存（rye）
rye sync

# Slidev 依存（Node.js）
npm ci
```

### 使い方

```bash
# 全図を一括生成 → public/figures/ に出力
rye run figures

# Slidev 開発サーバーを起動（スライドファイルを指定）
npm run dev -- slides/intro.md
```

### ディレクトリ構成

| パス | 説明 |
|------|------|
| `src/learn_dynamical_system/models/` | 力学系モデル定義 |
| `src/learn_dynamical_system/figures/` | 画像生成スクリプト |
| `slides/` | Slidev スライド (.md) |
| `slides/vite.config.mts` | Slidev の `publicDir` を直下の `public/` に向ける設定 |
| `public/figures/` | 生成された画像（gitignore） |
| `public/animations/` | 生成された動画（gitignore） |
