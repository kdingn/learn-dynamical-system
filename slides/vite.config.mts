import { resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { defineConfig } from 'vite'

// Slidev の publicDir は既定で `dirname(entry)/public`（= slides/public）になる。
// リポジトリ直下の public/ を直接指すことで、Python の生成物
// (public/figures, public/animations) を二重のパスなしに参照する。
// 拡張子は .mts — package.json に "type": "module" がないため .ts だと
// CommonJS 扱いになり Vite が警告を出す。
const here = fileURLToPath(new URL('.', import.meta.url))

export default defineConfig({
  publicDir: resolve(here, '../public'),
})
