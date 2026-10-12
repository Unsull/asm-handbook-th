import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import KnowledgeQuiz from '../components/KnowledgeQuiz.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('KnowledgeQuiz', KnowledgeQuiz)
  }
} satisfies Theme
