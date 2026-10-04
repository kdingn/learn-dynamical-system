<script setup lang="ts">
// 章の見取り図: headmatter の `roadmap`（問いの列）を縦に並べる。
//
//   <Roadmap />             すべての問いを同じ強さで（章の見取り図）
//   <Roadmap :current="2" /> Part 2 だけ強調し、他を薄くする（Part の扉）
//   <Roadmap answers />     各問いに headmatter の `roadmapAnswers` を添える（まとめ）
//
// 図ではなくコンポーネントにしているのは、問いが日本語だから
// （matplotlib のフォントは日本語非対応）。答えの `$…$` は KaTeX で組む。
import { computed } from 'vue'
import katex from 'katex'
import { useSlideContext } from '@slidev/client'

const props = defineProps<{
  current?: number
  answers?: boolean
}>()

const { $slidev } = useSlideContext()
const configs = $slidev.configs as Record<string, any>
const questions = computed<string[]>(() => configs.roadmap ?? [])
const answerTexts = computed<string[]>(() => configs.roadmapAnswers ?? [])

function renderMath(text: string): string {
  return text
    .split(/(\$[^$]+\$)/)
    .map((seg) => {
      if (seg.startsWith('$') && seg.endsWith('$') && seg.length > 1)
        return katex.renderToString(seg.slice(1, -1), { throwOnError: false })
      return seg.replace(/&/g, '&amp;').replace(/</g, '&lt;')
    })
    .join('')
}

function state(i: number): string {
  if (!props.current)
    return ''
  return i + 1 === props.current ? 'current' : 'dim'
}
</script>

<template>
  <div class="roadmap" :class="{ 'with-answers': answers }">
    <template v-for="(q, i) in questions" :key="i">
      <div class="row" :class="state(i)">
        <span class="tag">Part {{ i + 1 }}</span>
        <span class="question">{{ q }}</span>
        <span v-if="answers" class="answer" v-html="renderMath(answerTexts[i] ?? '')" />
      </div>
    </template>
  </div>
</template>

<style scoped>
.roadmap {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.row {
  display: grid;
  grid-template-columns: 64px 1fr;
  align-items: center;
  column-gap: 14px;
  padding: 6px 14px;
  border-left: 4px solid rgba(255, 255, 255, 0.25);
  background: rgba(255, 255, 255, 0.04);
}
.with-answers .row {
  grid-template-columns: 64px 300px 1fr;
}
.tag {
  font-size: 0.8em;
  opacity: 0.7;
}
.question {
  font-weight: 600;
}
.answer {
  font-size: 0.92em;
  line-height: 1.45;
}
.row.current {
  border-left-color: #2dd4bf; /* teal-400: 定理の枠と同じ色 */
  background: rgba(45, 212, 191, 0.1);
}
.row.dim {
  opacity: 0.35;
}
</style>
