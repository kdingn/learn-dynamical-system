"""Shared colour palette for matplotlib and manim."""

# Foreground colour for text, axes, ticks on dark slide backgrounds.
FG = "#d4d4d4"

# Base colours — keep the tuple order stable so index-based access stays
# consistent across figures and animations.
COLORS: tuple[str, ...] = (
    "#4A90D9",  # blue  (brighter for dark bg)
    "#FF5733",  # red   (slightly softened for dark bg)
    "#00D95A",  # green (brighter for dark bg)
    "#FFB347",  # orange (brighter for dark bg)
    "#A87BC2",  # purple (brighter for dark bg)
    "#999999",  # grey
    "#cccccc",  # light grey
)

BLUE, RED, GREEN, ORANGE, PURPLE, GREY, LIGHT_GREY = COLORS
