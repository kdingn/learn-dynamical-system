"""用語の初出スライドを一覧する（前方参照の検出用）。

スライドは前から順に読まれるので、**定義より前に使われている用語**があると
そこで読者が止まる。Ch.1 では「双曲型」が定義（p19）より前の p16 で使われていた。
機械的に定義の有無までは判定できないので、初出位置を出して目視で確認する。

Usage:
    rye run check-terms slides/01-basics.md
    rye run check-terms slides/02-manifolds.md --terms サドル 中心多様体
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

#: 章をまたいで使う基本用語。章固有の用語は --terms で足す。
DEFAULT_TERMS = [
    "相空間", "フロー", "軌道", "固定点", "ベクトル場",
    "ヤコビアン", "固有値", "固有ベクトル",
    "安定", "漸近安定", "不安定", "双曲型",
    "ノード", "サドル", "スパイラル", "センター",
    "セパラトリクス", "多様体", "不変多様体", "中心多様体",
    "リミットサイクル", "分岐", "ハミルトニアン",
]


def split_slides(entry: Path) -> list[str]:
    """Markdown を Slidev のスライド単位に分割する（先頭の headmatter は除く）."""
    lines = entry.read_text(encoding="utf-8").splitlines()
    chunks: list[list[str]] = [[]]
    for line in lines:
        if line.rstrip() == "---":
            chunks.append([])
        else:
            chunks[-1].append(line)
    if lines and lines[0].rstrip() == "---":
        chunks = chunks[2:]
    return ["\n".join(c) for c in chunks]


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entry", type=Path, help="スライドの .md")
    parser.add_argument("--terms", nargs="*", default=[],
                        help="この章固有の用語を追加する")
    args = parser.parse_args()

    slides = split_slides(args.entry)
    terms = DEFAULT_TERMS + list(args.terms)

    print(f"{args.entry} — {len(slides)} スライド\n")
    print("  用語ごとの初出スライド（定義がその位置にあるかは目視で確認する）:\n")

    found = False
    for term in terms:
        pages = [i for i, s in enumerate(slides, 1) if term in s]
        if not pages:
            continue
        found = True
        rest = f"  （以降 p{', p'.join(map(str, pages[1:6]))}"
        rest += ", …）" if len(pages) > 6 else "）" if len(pages) > 1 else ""
        print(f"    {term:<12} 初出 p{pages[0]:<3}{rest if len(pages) > 1 else ''}")

    if not found:
        print("    （該当する用語がありません）")
    print("\n  初出スライドでその用語が説明されていなければ、順序の入れ替えか"
          "その場での定義を検討する。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
