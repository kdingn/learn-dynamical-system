"""Shared colour palette for matplotlib and manim.

スライドは暗いテーマ（`colorSchema: dark`）に固定しているため、色は
**暗背景でのコントラスト**を基準に選んでいる。
背景は `#121212`、本文の文字色は `#ddd`（`@slidev/client/uno.config.ts`）。

図は透過 PNG なので背景に追従できない。テーマを切り替えるなら、
各スライドの `colorSchema` とこのファイルを必ずセットで変更すること。
"""

# Foreground colour for text, axes, ticks. スライド本文の文字色に合わせる。
FG = "#dddddd"
# スライドの背景色。図の背景は透過のままにし、これは図中のラベルの下敷き
# （線の上に文字を置くときの bbox）にだけ使う。manim の背景もこの色。
BG = "#121212"

# Base colours — keep the tuple order stable so index-based access stays
# consistent across figures and animations.
# 括弧内は背景 (#121212) に対するコントラスト比。
COLORS: tuple[str, ...] = (
    "#5BA3E8",  # blue   (7.0:1)
    "#FF6B4A",  # red    (6.6:1)
    "#3DDC84",  # green  (10.5:1)
    "#FFB347",  # orange (10.5:1)
    "#BE9BD6",  # purple (7.9:1)
    "#A8A8A8",  # grey   (7.9:1)
    "#CCCCCC",  # light grey (11.7:1) — 補助線・強調用
)

BLUE, RED, GREEN, ORANGE, PURPLE, GREY, LIGHT_GREY = COLORS
