---
theme: default
# 図は透過 PNG でテーマに追従できないため、既定の auto ではなく dark に固定する
colorSchema: dark
title: 力学系入門
drawings:
  persist: false
---

# 力学系入門

Learn Dynamical Systems

<div class="abs-br mr-6 mb-6 text-sm opacity-50">
全体を貫く軸: 固有値の物語
</div>

---

## 目次

全10章。各章で固有値の概念がどう拡張されるかが物語の背骨。

| Ch. | タイトル                   | 固有値の役割                    |
| --- | -------------------------- | ------------------------------- |
| 1   | 力学系の基礎と線形安定性   | $\lambda$ of $J$ → 固定点分類   |
| 2   | 不変多様体と非線形解析     | $\mathrm{Re}(\lambda)=0$ の世界 |
| 3   | 分岐理論                   | $\lambda$ が虚軸を横切る        |
| 4   | リミットサイクルと位相縮約 | Floquet 乗数                    |
| 5   | カオスへの道               | Floquet 乗数の分岐              |
| 6   | カオスとアトラクタ         | リアプノフ指数                  |
| 7   | 流体力学の力学系的視点     | 作用素のスペクトル              |
| 8   | 低次元化手法               | POD / DMD の固有値              |
| 9   | データ駆動型力学系         | Koopman 固有関数                |
| 10  | 安定性解析と制御           | 全章の統合                      |

---

## 各章の起動方法

```bash
npm run dev:01   # Ch.1 力学系の基礎と線形安定性
npm run dev:02   # Ch.2 不変多様体と非線形解析
npm run dev:03   # Ch.3 分岐理論
```

章が追加されたら `dev:04`, `dev:05`, ... で起動できます。
