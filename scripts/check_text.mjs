// スライドの「文字の組まれ方」を、ブラウザで描画した DOM から測る。
//
// check_slides.py の PNG 解析では分からない次の4つを検出する:
//   1. 見出し (h2) が1行に収まっていない／他より背が高い（数式で字が大きくなる等）
//   2. 段落・箇条書き・表のセルの最終行が数文字だけ（「い。」だけの行など）
//   3. 表の短いセルが折り返している／セルが3行以上になっている
//   4. 狭い段組み（2カラムのテキスト側など）で行数が多すぎる
// あわせてスライドごとの文字数（数式は1個 = MATH_CHARS 文字で換算）を出す。
//
// Slidev の dev サーバを自分で起動し、各スライド（/1, /2, ...）を playwright で開いて測る
// （/print は dev サーバでは無効）。結果は JSON で標準出力に出す（check_slides.py が整形する）。
//
// Usage: node scripts/check_text.mjs slides/01-basics.md <スライド数> [port]

import { spawn, execSync } from 'node:child_process'
import { chromium } from 'playwright-chromium'

const entry = process.argv[2]
const total = Number(process.argv[3])
const port = Number(process.argv[4] ?? 3099)

// Windows では npx が .cmd なので shell 経由で起動する（引数は固定値とパスだけ）
const server = spawn(`npx slidev --no-open --port ${port} "${entry}"`, {
  shell: true,
  stdio: 'ignore',
})

function stopServer() {
  try {
    if (process.platform === 'win32')
      execSync(`taskkill /pid ${server.pid} /T /F`, { stdio: 'ignore' })
    else
      server.kill()
  }
  catch {}
}

async function waitForServer() {
  for (let i = 0; i < 240; i++) {
    try {
      const res = await fetch(`http://localhost:${port}/`)
      if (res.ok)
        return
    }
    catch {}
    await new Promise(r => setTimeout(r, 500))
  }
  throw new Error('slidev の起動待ちでタイムアウトしました')
}

// ブラウザ内で実行する計測。引数のしきい値はすべて「本文の字の大きさ (em)」基準
function measure({ MATH_CHARS, page }) {
  const MATH = '.katex'
  const results = []

  // 要素内のインライン内容を行ごとにまとめ、[{top, bottom, left, right}] を返す。
  // KaTeX は内部に高さの違う箱を多数持つので、数式は外側の箱1つとして扱う
  function lineBoxes(el) {
    const rects = []
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT)
    let node = walker.nextNode()
    while (node) {
      if (node.nodeType === Node.ELEMENT_NODE && node.matches(MATH)) {
        const html = node.querySelector('.katex-html') ?? node
        for (const r of html.getClientRects())
          rects.push(r)
        // 数式の中身は飛ばす
        let next = node
        while (next && !next.nextSibling && next !== el) next = next.parentNode
        if (!next || next === el)
          break
        walker.currentNode = next
        node = walker.nextSibling() ?? walker.nextNode()
        continue
      }
      if (node.nodeType === Node.TEXT_NODE && node.textContent.trim()) {
        const range = document.createRange()
        range.selectNodeContents(node)
        for (const r of range.getClientRects()) {
          if (r.width > 0)
            rects.push(r)
        }
      }
      node = walker.nextNode()
    }
    rects.sort((a, b) => (a.top + a.bottom) / 2 - (b.top + b.bottom) / 2)
    const fs = Number.parseFloat(getComputedStyle(el).fontSize)
    const lines = []
    for (const r of rects) {
      const c = (r.top + r.bottom) / 2
      const last = lines.at(-1)
      if (last && Math.abs(c - last.center) < 0.6 * fs) {
        last.left = Math.min(last.left, r.left)
        last.right = Math.max(last.right, r.right)
      }
      else {
        lines.push({ center: c, left: r.left, right: r.right })
      }
    }
    return { lines, fs }
  }

  function visibleText(el) {
    const clone = el.cloneNode(true)
    clone.querySelectorAll(MATH).forEach(m => m.replaceWith('∎'))
    return clone.textContent.replace(/\s+/g, ' ').trim()
  }

  // 表示中のスライドだけを測る（他のスライドも DOM に残っている）
  const containers = [document.querySelector(`.slidev-page-${page}`)]
  containers.forEach((slide) => {
    const scale = slide.getBoundingClientRect().width / 980
    const layout = slide.querySelector('.slidev-layout') ?? slide
    const contentW = (layout.getBoundingClientRect().width / scale) - 112
    const issues = []

    // 1. 見出し
    for (const h of layout.querySelectorAll('h1, h2')) {
      const { lines } = lineBoxes(h)
      const height = h.getBoundingClientRect().height / scale
      const lh = Number.parseFloat(getComputedStyle(h).lineHeight)
      if (lines.length > 1)
        issues.push({ kind: 'heading', msg: `見出しが ${lines.length} 行に折り返している` })
      else if (h.tagName === 'H2' && height > lh * 1.15)
        issues.push({ kind: 'heading', msg: `見出しの高さ ${height.toFixed(0)}px が通常 (${lh.toFixed(0)}px) より大きい（数式で字が大きい?）` })
    }

    // 2〜4. 段落・箇条書き・セル
    for (const el of layout.querySelectorAll('p, li, td, th')) {
      // `<br>` で意図して改行している要素（表の見出し列など）は対象外
      if (el.querySelector('.katex-display, p, ul, ol, table, img, br'))
        continue
      const text = visibleText(el)
      if (!text)
        continue
      const { lines, fs } = lineBoxes(el)
      const n = lines.length
      const tail = text.slice(-12)
      if (n >= 2) {
        const lastW = (lines.at(-1).right - lines.at(-1).left) / scale
        if (lastW < 2.5 * fs)
          issues.push({ kind: 'orphan', msg: `最終行が ${(lastW / fs).toFixed(1)} 文字分だけ: 「…${tail}」` })
      }
      const isCell = el.matches('td, th')
      if (isCell && n >= 2 && (el.matches('th') || text.length <= 20))
        issues.push({ kind: 'cell', msg: `短いセルが ${n} 行に折り返している: 「${text.slice(0, 24)}」` })
      else if (isCell && n >= 3)
        issues.push({ kind: 'cell', msg: `セルが ${n} 行: 「${text.slice(0, 24)}…」（列の配分か文の長さを見直す）` })
      const w = el.getBoundingClientRect().width / scale
      if (!isCell && w < 0.6 * contentW && n >= 4)
        issues.push({ kind: 'narrow', msg: `幅 ${w.toFixed(0)}px の段組みで ${n} 行: 「${text.slice(0, 16)}…」` })
    }

    // 文字数（数式は1個を MATH_CHARS 文字と数える）
    const clone = layout.cloneNode(true)
    const nMath = clone.querySelectorAll(MATH).length
    clone.querySelectorAll(MATH).forEach(m => m.remove())
    const chars = clone.textContent.replace(/\s+/g, '').length + MATH_CHARS * nMath

    results.push({ page, chars, issues })
  })
  return results
}

let browser
try {
  await waitForServer()
  browser = await chromium.launch()
  const page = await browser.newPage({ viewport: { width: 980, height: 552 } })
  const results = []
  for (let no = 1; no <= total; no++) {
    await page.goto(`http://localhost:${port}/${no}`, { waitUntil: 'networkidle', timeout: 120000 })
    await page.waitForSelector(`.slidev-page-${no}`, { state: 'visible' })
    await page.waitForTimeout(300)
    results.push(...await page.evaluate(measure, { MATH_CHARS: 4, page: no }))
  }
  process.stdout.write(JSON.stringify(results))
}
finally {
  await browser?.close()
  stopServer()
}
