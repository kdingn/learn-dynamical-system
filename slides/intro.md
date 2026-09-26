---
theme: default
title: 力学系入門
drawings:
  persist: false
transition: slide-left
---

# 力学系入門

Learn Dynamical Systems

---

## 力学系とは

状態 $\mathbf{x} \in \mathbb{R}^n$ の時間発展を記述する系：

$$
\frac{d\mathbf{x}}{dt} = \mathbf{f}(\mathbf{x})
$$

- **固定点**: $\mathbf{f}(\mathbf{x}^*) = 0$
- **安定性**: 固定点近傍の線形化 $J = D\mathbf{f}(\mathbf{x}^*)$ の固有値で判定

---

## 例: ローレンツ方程式

$$
\begin{cases}
\dot{x} = \sigma(y - x) \\
\dot{y} = x(\rho - z) - y \\
\dot{z} = xy - \beta z
\end{cases}
$$

典型的なパラメータ: $\sigma = 10,\; \rho = 28,\; \beta = 8/3$

<img src="/figures/lorenz.png" class="mx-auto h-60" />

---

## 目次（予定）

1. 固定点と安定性
2. 分岐理論
3. ホップ分岐
4. カオスとリアプノフ指数
5. 流体力学への応用
