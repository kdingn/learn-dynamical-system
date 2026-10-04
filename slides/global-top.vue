<script setup lang="ts">
// 全スライドの右上に「Ch.N › Part k: 問い」を表示する（現在地表示）。
//
// - 章名と問いの一覧は headmatter の `chapter` / `roadmap` に書く
//   （headmatter のカスタムキーは $slidev.configs にそのまま入る）
// - Part の扉の frontmatter に `part: k` を書くと、そのスライドから次の
//   `part:` までが Part k になる。`part: 0` で表示を消す（まとめなど）
// - `part:` を持つスライドより前（表紙・動機・見取り図）には何も出さない
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'

const { $slidev } = useSlideContext()

const label = computed(() => {
  const configs = $slidev.configs as Record<string, any>
  const roadmap: string[] | undefined = configs.roadmap
  if (!configs.chapter || !roadmap)
    return ''
  const no = $slidev.nav.currentSlideNo
  let part = 0
  for (const route of $slidev.nav.slides) {
    if (route.no > no)
      break
    const p = route.meta?.slide?.frontmatter?.part
    if (typeof p === 'number')
      part = p
  }
  if (part < 1 || part > roadmap.length)
    return ''
  return `${configs.chapter} › Part ${part}: ${roadmap[part - 1]}`
})
</script>

<template>
  <div v-if="label" class="where-label">{{ label }}</div>
</template>

<style scoped>
/* 上パディング帯（40px）の中に収める。check_slides.py はこの帯の右側を
   TIGHT 判定から外している（TOP_LABEL_H_PX）。 */
.where-label {
  position: absolute;
  top: 12px;
  right: 56px;
  font-size: 12px;
  line-height: 16px;
  opacity: 0.55;
  pointer-events: none;
}
</style>
