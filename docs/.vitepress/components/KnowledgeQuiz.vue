<script setup lang="ts">
import { computed, ref } from 'vue'
import questionBank from '../quizzes.json'

type Question = { prompt: string; options: string[]; answer: number; why: string }
const props = defineProps<{ chapter: number }>()
const questions = computed(() => (questionBank as Record<string, Question[]>)[String(props.chapter)] ?? [])
const answers = ref<Record<number, number>>({})
const submitted = ref(false)
const answered = computed(() => Object.keys(answers.value).length)
const score = computed(() => questions.value.reduce((count, q, index) => count + (answers.value[index] === q.answer ? 1 : 0), 0))
function select(questionIndex: number, optionIndex: number) {
  answers.value[questionIndex] = optionIndex
  submitted.value = false
}
function reset() {
  answers.value = {}
  submitted.value = false
}
</script>

<template>
  <section class="quiz" aria-label="Knowledge check">
    <div class="quiz-header">
      <div>
        <span class="eyebrow">KNOWLEDGE CHECK</span>
        <h2>ทบทวนความเข้าใจ</h2>
        <p>เลือกคำตอบที่เหมาะสมที่สุดเพียงหนึ่งข้อในแต่ละคำถาม</p>
      </div>
      <span class="progress">{{ answered }}/{{ questions.length }}</span>
    </div>
    <div v-for="(q, i) in questions" :key="i" class="question-card">
      <fieldset>
        <legend><span class="question-number">{{ String(i + 1).padStart(2, '0') }}</span> {{ q.prompt }}</legend>
        <label v-for="(option, j) in q.options" :key="j" class="option" :class="{ picked: answers[i] === j, correct: submitted && q.answer === j, incorrect: submitted && answers[i] === j && j !== q.answer }">
          <input type="radio" :name="`asm-quiz-${chapter}-${i}`" :checked="answers[i] === j" @change="select(i, j)" />
          <span class="option-letter">{{ String.fromCharCode(65 + j) }}</span>
          <span>{{ option }}</span>
        </label>
      </fieldset>
      <div v-if="submitted" class="feedback" :class="answers[i] === q.answer ? 'success' : 'needs-review'" role="status">
        <strong>{{ answers[i] === q.answer ? '✓ ถูกต้อง' : `คำตอบที่เหมาะสม: ${String.fromCharCode(65 + q.answer)}` }}</strong>
        <p>{{ q.why }}</p>
      </div>
    </div>
    <div class="quiz-actions">
      <button class="check" type="button" :disabled="answered !== questions.length" @click="submitted = true">ตรวจคำตอบ</button>
      <button class="reset" type="button" @click="reset">เริ่มใหม่</button>
    </div>
    <div v-if="submitted" class="result" role="status" aria-live="polite">
      <strong>{{ score }}/{{ questions.length }}</strong>
      <p>{{ score === questions.length ? 'เข้าใจหลักการสำคัญครบแล้ว' : 'ทบทวนคำอธิบายของข้อที่ยังผิด แล้วลองทำอีกครั้ง' }}</p>
    </div>
  </section>
</template>

<style scoped>
.quiz { border: 1px solid var(--vp-c-divider); border-radius: 20px; padding: clamp(16px, 3vw, 28px); margin: 28px 0; background: var(--vp-c-bg-soft); }
.quiz-header { display:flex; gap:18px; justify-content:space-between; align-items:start; }
.quiz-header h2 { margin: 6px 0 4px; padding:0; border:0; font-size:23px; }
.quiz-header p { margin:0; color:var(--vp-c-text-2); font-size:14px; }
.eyebrow { font-size:11px; letter-spacing:.13em; color:var(--vp-c-brand-1); font-weight:800; }
.progress { flex:none; font-size:13px; font-weight:700; color:var(--vp-c-brand-1); background:var(--vp-c-brand-soft); border-radius:20px; padding:5px 10px; }
.question-card { margin-top:25px; padding-top:23px; border-top:1px solid var(--vp-c-divider); }
fieldset { margin:0; padding:0; border:0; min-width:0; }
legend { padding:0 0 14px; font-weight:700; font-size:15px; line-height:1.8; }
.question-number { color:var(--vp-c-brand-1); font-size:12px; margin-right:6px; }
.option { display:flex; gap:12px; align-items:flex-start; line-height:1.8; margin:8px 0; padding:12px; border:1px solid var(--vp-c-divider); border-radius:12px; cursor:pointer; background:var(--vp-c-bg); transition:border-color .15s; font-size:14px; }
.option:hover,.option.picked { border-color:var(--vp-c-brand-1); }
.option input { flex:none; margin-top:6px; accent-color:var(--vp-c-brand-1); }
.option-letter { font-weight:800; color:var(--vp-c-text-2); flex:none; }
.option.correct { border-color:#22a074; background:rgba(34,160,116,.07); }
.option.incorrect { border-color:#d66e64; }
.feedback { border-left:3px solid var(--vp-c-brand-1); padding:10px 14px; margin-top:12px; background:var(--vp-c-bg); border-radius:5px; font-size:13px; }
.feedback.needs-review { border-left-color:#db8171; }
.feedback p { margin:5px 0 0; }
.quiz-actions { display:flex; gap:10px; margin-top:24px; }
.quiz-actions button { padding:10px 18px; border-radius:10px; font-weight:700; font-size:14px; cursor:pointer; }
.check { background:var(--vp-c-brand-1); color:white; }
.check:disabled { cursor:not-allowed; opacity:.35; }
.reset { border:1px solid var(--vp-c-divider); background:var(--vp-c-bg); }
.result { text-align:center; background:var(--vp-c-bg); border-radius:14px; padding:18px; margin-top:18px; }
.result strong { color:var(--vp-c-brand-1); font-size:34px; }
.result p { font-size:13px; color:var(--vp-c-text-2); margin:0; }
</style>
