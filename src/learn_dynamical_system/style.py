"""Matplotlib rcParams shared configuration.

Call ``apply()`` at the top of every figure script to ensure a consistent look.
Figures use transparent backgrounds with light-coloured text/axes so they
blend naturally into dark-themed Slidev slides.
"""

import matplotlib.pyplot as plt
import scienceplots  # noqa: F401  (registers styles on import)

from learn_dynamical_system.palette import FG


def apply() -> None:
    """Activate the project-wide matplotlib style."""
    plt.style.use(["science", "no-latex"])
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["CMU Serif", "Computer Modern Roman", "DejaVu Serif"],
            "mathtext.fontset": "cm",
            "font.size": 12,
            "axes.labelsize": 14,
            "axes.titlesize": 14,
            "xtick.labelsize": 11,
            "ytick.labelsize": 11,
            "legend.fontsize": 11,
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            # --- dark-slide support: transparent bg + light foreground ---
            "figure.facecolor": "none",
            "axes.facecolor": "none",
            "savefig.facecolor": "none",
            "savefig.transparent": True,
            "text.color": FG,
            "axes.labelcolor": FG,
            "axes.edgecolor": FG,
            "xtick.color": FG,
            "ytick.color": FG,
            "legend.facecolor": "none",
            "legend.edgecolor": "none",
            "legend.labelcolor": FG,
        }
    )
