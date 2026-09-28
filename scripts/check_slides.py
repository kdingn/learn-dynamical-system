"""Slidev スライドの「全容確認」用チェッカー.

`slidev export --format png` で書き出した各スライドの PNG を解析し、

* 内容がスライド枠からはみ出していないか（パディング帯にインクが侵入していないか）
* 不自然な余白が残っていないか（内容領域に対する占有率が低すぎないか）
* 図を等倍で貼っているか（md の `width:` と PNG の画素幅が対応しているか）

を機械的に判定する。目視確認の前段として使い、ここを通ってから実際に画像を見る。

Usage:
    rye run check-slides slides/01-basics.md
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image

# Slidev の論理キャンバス: @slidev/parser の canvasWidth=980, aspectRatio=16/9
CANVAS_W = 980.0
CANVAS_H = CANVAS_W * 9 / 16  # 551.25

# .slidev-layout は `px-14 py-10` (= 3.5rem / 2.5rem)
PAD_X = 56.0
PAD_Y = 40.0

# 内容がこれ以上パディングに食い込んだら TIGHT とみなす（CSS px）
INTRUSION_TOL = 2.0
# キャンバス端からこの距離以内にインクがあれば CLIP（実際に切れている）
EDGE_TOL = 2.0
# 四隅の `abs-bl` / `abs-br` 注記が入る領域。TIGHT 判定のみ免除する（CSS px）
CORNER_W_PX = 400.0
CORNER_H_PX = 72.0
# 内容領域の高さに対する占有率がこれを下回ったら余白過多として報告
MIN_FILL_RATIO = 0.45
# 背景との差がこれ以上ある画素を「インク」とみなす
INK_THRESHOLD = 24


@dataclass
class SlideReport:
    index: int
    path: Path
    ink_box_css: tuple[float, float, float, float] | None
    clipped: list[str]
    tight: list[str]
    fill_ratio: float

    @property
    def ok(self) -> bool:
        return not self.clipped and not self.tight and self.fill_ratio >= MIN_FILL_RATIO


def _ink_mask(img: Image.Image) -> np.ndarray:
    """背景色から十分に離れた画素のマスクを返す."""
    rgb = np.asarray(img.convert("RGB"), dtype=np.int16)
    # 四隅の中央値を背景色とみなす（明背景・暗背景どちらでも動く）
    corners = np.stack(
        [rgb[0, 0], rgb[0, -1], rgb[-1, 0], rgb[-1, -1]]
    )
    bg = np.median(corners, axis=0)
    diff = np.abs(rgb - bg).max(axis=2)
    return diff > INK_THRESHOLD


def _bbox(mask: np.ndarray) -> tuple[int, int, int, int] | None:
    if not mask.any():
        return None
    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]
    return int(cols[0]), int(rows[0]), int(cols[-1]), int(rows[-1])


def split_slides(entry: Path) -> list[str]:
    """Markdown を Slidev のスライド単位に分割する（先頭の headmatter は除く）."""
    lines = entry.read_text(encoding="utf-8").splitlines()
    chunks: list[list[str]] = [[]]
    for line in lines:
        if line.rstrip() == "---":
            chunks.append([])
        else:
            chunks[-1].append(line)
    # 先頭が `---` で始まるファイルでは chunks[0] が空、chunks[1] が headmatter
    if lines and lines[0].rstrip() == "---":
        chunks = chunks[2:]
    return ["\n".join(c) for c in chunks]


def analyse(path: Path, index: int, source: str = "") -> SlideReport:
    img = Image.open(path)
    scale = img.width / CANVAS_W  # export は 2x なので通常 2.0

    mask = _ink_mask(img)
    box = _bbox(mask)
    if box is None:
        return SlideReport(index, path, None, [], [], 0.0)

    x0, y0, x1, y1 = (v / scale for v in box)

    # `abs-bl` / `abs-br` などで四隅に置く注記はパディング帯に出るのが正しい。
    # そのスライドの Markdown が実際に `abs-` を使っているときだけ四隅を
    # TIGHT 判定から外す。CLIP 判定には常に全体を使う。
    body = mask
    if "abs-" in source:
        body = mask.copy()
        cx, cy = int(CORNER_W_PX * scale), int(CORNER_H_PX * scale)
        body[:cy, :cx] = body[:cy, -cx:] = False
        body[-cy:, :cx] = body[-cy:, -cx:] = False
    body_box = _bbox(body)
    if body_box is not None:
        bx0, by0, bx1, by1 = (v / scale for v in body_box)
    else:
        bx0, by0, bx1, by1 = x0, y0, x1, y1

    # キャンバス端に到達している = 実際に切れている
    clipped: list[str] = []
    if x1 > CANVAS_W - EDGE_TOL:
        clipped.append("右端で切れている")
    if y1 > CANVAS_H - EDGE_TOL:
        clipped.append("下端で切れている")
    if x0 < EDGE_TOL:
        clipped.append("左端で切れている")
    if y0 < EDGE_TOL:
        clipped.append("上端で切れている")

    # 切れてはいないがパディング帯に食い込んでいる（四隅の注記は除外済み）
    tight: list[str] = []
    if bx0 < PAD_X - INTRUSION_TOL:
        tight.append(f"左 {PAD_X - bx0:.0f}px")
    if bx1 > CANVAS_W - PAD_X + INTRUSION_TOL:
        tight.append(f"右 {bx1 - (CANVAS_W - PAD_X):.0f}px")
    if by0 < PAD_Y - INTRUSION_TOL:
        tight.append(f"上 {PAD_Y - by0:.0f}px")
    if by1 > CANVAS_H - PAD_Y + INTRUSION_TOL:
        tight.append(f"下 {by1 - (CANVAS_H - PAD_Y):.0f}px")

    content_h = CANVAS_H - 2 * PAD_Y
    fill_ratio = (by1 - by0) / content_h

    return SlideReport(index, path, (x0, y0, x1, y1), clipped, tight, fill_ratio)


def export_slides(entry: Path, out_dir: Path) -> list[Path]:
    cmd = [
        "npx", "slidev", "export", str(entry),
        "--format", "png", "--output", str(out_dir), "--timeout", "60000",
    ]
    # export は既定で light。スライドが dark 固定ならそちらで書き出さないと
    # 実際の見え方と食い違う（図は透過 PNG なのでテーマに追従できない）。
    headmatter = entry.read_text(encoding="utf-8").split("---", 2)
    if len(headmatter) > 1 and "colorSchema: dark" in headmatter[1]:
        cmd.append("--dark")
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        shell=(sys.platform == "win32"),
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stdout + proc.stderr)
        raise SystemExit(f"slidev export に失敗しました (exit {proc.returncode})")
    return sorted(out_dir.glob("*.png"), key=lambda p: int(p.stem))


#: `<img src="/figures/xxx.png" ... width: NNNpx ...>` を拾う
IMG_RE = re.compile(
    r'<img[^>]*src="/figures/([\w-]+\.png)"[^>]*?width:\s*(\d+)px', re.S)


def check_image_scale(entry: Path) -> list[str]:
    """図を等倍で貼っているかを確認する.

    図は `savefig.dpi = 192`（= 96 CSS px の2倍）で書き出しているので、
    PNG の画素幅の半分が「スライド上で占めるべき CSS px」になる。md 側の
    `width:` がこれとずれていると拡大縮小がかかり、図中の文字が本文と
    違う大きさになる（SLOT_* の値と md を手で揃えるのは間違えやすい）。
    """
    public = entry.resolve().parents[1] / "public" / "figures"
    problems: list[str] = []
    for name, width in IMG_RE.findall(entry.read_text(encoding="utf-8")):
        png = public / name
        if not png.exists():
            problems.append(f"{name}: PNG がない（rye run figures を先に実行）")
            continue
        with Image.open(png) as im:
            expected = im.width / 2
        if abs(expected - int(width)) > 0.5:
            problems.append(
                f"{name}: md は {width}px だが PNG は {expected:.0f}px 相当"
                f" — 図が {int(width) / expected:.3f} 倍に拡大縮小される"
            )
    return problems


def main() -> int:
    # Windows の既定は cp932 で、本スクリプトの出力（— や日本語）が落ちる
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entry", type=Path, help="スライドの .md")
    parser.add_argument(
        "--keep", type=Path, default=None,
        help="書き出した PNG を残すディレクトリ（目視確認用）",
    )
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        out_dir = args.keep if args.keep else Path(tmp) / "png"
        out_dir.mkdir(parents=True, exist_ok=True)
        pages = export_slides(args.entry, out_dir)
        sources = split_slides(args.entry)
        if len(sources) != len(pages):
            sys.stderr.write(
                f"注意: Markdown の分割数 {len(sources)} が書き出し枚数 "
                f"{len(pages)} と一致しません。四隅の注記の判定のみ影響します。\n"
            )
            sources = [""] * len(pages)
        reports = [
            analyse(p, i + 1, sources[i]) for i, p in enumerate(pages)
        ]

        print(f"{args.entry} — {len(reports)} スライド "
              f"(キャンバス {CANVAS_W:.0f}x{CANVAS_H:.0f}, 内容領域 "
              f"{CANVAS_W - 2 * PAD_X:.0f}x{CANVAS_H - 2 * PAD_Y:.0f})\n")
        bad = 0
        for r in reports:
            if r.clipped:
                status, detail = "CLIP", ", ".join(r.clipped)
                bad += 1
            elif r.tight:
                status, detail = "TIGHT", "パディングに侵入: " + ", ".join(r.tight)
                bad += 1
            elif r.index == 1:
                # タイトルスライドは余白が多いのが正しいので占有率を問わない
                status, detail = "OK  ", f"占有 {r.fill_ratio:5.0%} (表紙)"
            elif r.fill_ratio < MIN_FILL_RATIO:
                status, detail = "GAP ", f"占有 {r.fill_ratio:5.0%} — 余白が多い"
                bad += 1
            else:
                status, detail = "OK  ", f"占有 {r.fill_ratio:5.0%}"
            print(f"  [{status:5}] p{r.index:>2}  {detail}")

        scale_problems = check_image_scale(args.entry)
        if scale_problems:
            print()
            print("  図の等倍表示（SLOT と md の width）に不一致:")
            for msg in scale_problems:
                print(f"    - {msg}")
            bad += len(scale_problems)

        print()
        if bad:
            print(f"{bad} 件の要確認スライドがあります。")
        else:
            print("すべてのスライドが枠内に収まっています。")
        if args.keep:
            print(f"PNG: {out_dir}")
        return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
