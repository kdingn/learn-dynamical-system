"""Entry point for generating all figures.

Usage:
    rye run figures
"""

from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parents[3] / "public" / "figures"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Output directory ready: {OUTPUT_DIR}")

    from learn_dynamical_system.figures import ch01, ch02

    ch01.generate_all(OUTPUT_DIR)
    ch02.generate_all(OUTPUT_DIR)


if __name__ == "__main__":
    main()
