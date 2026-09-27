"""Entry point for rendering all animations.

Usage:
    rye run animations

``animations/chNN.py`` を置いて ``render_all()`` を定義すると自動的に拾われる。
まだ動画を使っていない章では、何も書き出さずに終了する。
"""

import importlib
import pkgutil
import shutil

from learn_dynamical_system import animations


def main() -> None:
    modules = sorted(
        name for _, name, _ in pkgutil.iter_modules(animations.__path__)
        if name.startswith("ch")
    )
    if not modules:
        print("書き出す Scene がありません（animations/chNN.py が未作成）。")
        return

    # manim は重い依存なので、動画を使う章ができるまで未インストールでもよい。
    # `rye run figures` の連鎖をここで止めないよう、無ければスキップする。
    try:
        from learn_dynamical_system import animation
    except ModuleNotFoundError:
        print("manim が未インストールのため、動画の書き出しをスキップします"
              "（必要になったら `rye add manim`）。")
        return

    animation.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Output directory ready: {animation.OUTPUT_DIR}")

    for name in modules:
        module = importlib.import_module(f"{animations.__name__}.{name}")
        module.render_all()
        print(f"  {name} animations rendered.")

    # manim の中間ファイル（partial_movie_files / .manim）は成果物ではないので消す
    for junk in ("partial_movie_files", ".manim"):
        shutil.rmtree(animation.OUTPUT_DIR / junk, ignore_errors=True)


if __name__ == "__main__":
    main()
