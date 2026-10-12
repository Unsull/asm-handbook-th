import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'th-TH',
  title: 'ASM Handbook TH',
  titleTemplate: ':title | ASM Handbook TH',
  description: 'คู่มือเรียนรู้ Attack Surface Management ภาษาไทย 11 บท พร้อมทฤษฎี กรณีศึกษา Lab และ Quiz',
  base: '/asm-handbook-th/',
  head: [
    ['meta', { name: 'theme-color', content: '#0e766e' }],
    ['meta', { name: 'referrer', content: 'strict-origin-when-cross-origin' }]
  ],
  markdown: { lineNumbers: true, math: true },
  themeConfig: {
    siteTitle: 'ASM Handbook TH',
    outline: { level: [2,3], label: 'หัวข้อในหน้านี้' },
    docFooter: { prev: 'บทก่อนหน้า', next: 'หน้าถัดไป' },
    returnToTopLabel: 'กลับขึ้นด้านบน',
    sidebarMenuLabel: 'สารบัญ',
    darkModeSwitchLabel: 'ธีม',
    search: { provider: 'local' },
    nav: [
      { text: 'หน้าแรก', link: '/' },
      { text: 'สารบัญ', link: '/learning-path' },
      { text: 'กรณีศึกษา', link: '/case-study/' },
      { text: 'อภิธานศัพท์', link: '/glossary/' },
      { text: 'อ้างอิง', link: '/references/' }
    ],
    sidebar: [
      {
        text: '01 · Foundations',
        collapsed: true,
        items: [
          { text: 'บทนำ', link: '/chapters/01-foundations/' },
          { text: 'แนวคิดเชิงลึก', link: '/chapters/01-foundations/concepts' },
          { text: 'กรณีศึกษา', link: '/chapters/01-foundations/examples' },
          { text: 'Workshop', link: '/chapters/01-foundations/workshop' },
          { text: 'แบบทดสอบ', link: '/chapters/01-foundations/quiz' },
        ]
      },
      {
        text: '02 · Types & Surfaces',
        collapsed: true,
        items: [
          { text: 'บทนำ', link: '/chapters/02-types-of-surfaces/' },
          { text: 'แนวคิดเชิงลึก', link: '/chapters/02-types-of-surfaces/concepts' },
          { text: 'กรณีศึกษา', link: '/chapters/02-types-of-surfaces/examples' },
          { text: 'Workshop', link: '/chapters/02-types-of-surfaces/workshop' },
          { text: 'แบบทดสอบ', link: '/chapters/02-types-of-surfaces/quiz' },
        ]
      },
      {
        text: '03 · Risk Assessment',
        collapsed: true,
        items: [
          { text: 'บทนำ', link: '/chapters/03-risk/' },
          { text: 'แนวคิดเชิงลึก', link: '/chapters/03-risk/concepts' },
          { text: 'กรณีศึกษา', link: '/chapters/03-risk/examples' },
          { text: 'Workshop', link: '/chapters/03-risk/workshop' },
          { text: 'แบบทดสอบ', link: '/chapters/03-risk/quiz' },
        ]
      },
      {
        text: '04 · Asset Inventory',
        collapsed: true,
        items: [
          { text: 'บทนำ', link: '/chapters/04-asset-identification/' },
          { text: 'แนวคิดเชิงลึก', link: '/chapters/04-asset-identification/concepts' },
          { text: 'กรณีศึกษา', link: '/chapters/04-asset-identification/examples' },
          { text: 'Workshop', link: '/chapters/04-asset-identification/workshop' },
          { text: 'แบบทดสอบ', link: '/chapters/04-asset-identification/quiz' },
        ]
      },
      {
        text: '05 · Automated Discovery',
        collapsed: true,
        items: [
          { text: 'บทนำ', link: '/chapters/05-automated-discovery/' },
          { text: 'แนวคิดเชิงลึก', link: '/chapters/05-automated-discovery/concepts' },
          { text: 'กรณีศึกษา', link: '/chapters/05-automated-discovery/examples' },
          { text: 'Workshop', link: '/chapters/05-automated-discovery/workshop' },
          { text: 'แบบทดสอบ', link: '/chapters/05-automated-discovery/quiz' },
        ]
      },
      {
        text: '06 · Crown Jewels',
        collapsed: true,
        items: [
          { text: 'บทนำ', link: '/chapters/06-prioritization/' },
          { text: 'แนวคิดเชิงลึก', link: '/chapters/06-prioritization/concepts' },
          { text: 'กรณีศึกษา', link: '/chapters/06-prioritization/examples' },
          { text: 'Workshop', link: '/chapters/06-prioritization/workshop' },
          { text: 'แบบทดสอบ', link: '/chapters/06-prioritization/quiz' },
        ]
      },
      {
        text: '07 · ASA & Threat Modeling',
        collapsed: true,
        items: [
          { text: 'บทนำ', link: '/chapters/07-attack-surface-analysis/' },
          { text: 'แนวคิดเชิงลึก', link: '/chapters/07-attack-surface-analysis/concepts' },
          { text: 'กรณีศึกษา', link: '/chapters/07-attack-surface-analysis/examples' },
          { text: 'Workshop', link: '/chapters/07-attack-surface-analysis/workshop' },
          { text: 'แบบทดสอบ', link: '/chapters/07-attack-surface-analysis/quiz' },
        ]
      },
      {
        text: '08 · Remediation',
        collapsed: true,
        items: [
          { text: 'บทนำ', link: '/chapters/08-remediation/' },
          { text: 'แนวคิดเชิงลึก', link: '/chapters/08-remediation/concepts' },
          { text: 'กรณีศึกษา', link: '/chapters/08-remediation/examples' },
          { text: 'Workshop', link: '/chapters/08-remediation/workshop' },
          { text: 'แบบทดสอบ', link: '/chapters/08-remediation/quiz' },
        ]
      },
      {
        text: '09 · Minimization',
        collapsed: true,
        items: [
          { text: 'บทนำ', link: '/chapters/09-minimization/' },
          { text: 'แนวคิดเชิงลึก', link: '/chapters/09-minimization/concepts' },
          { text: 'กรณีศึกษา', link: '/chapters/09-minimization/examples' },
          { text: 'Workshop', link: '/chapters/09-minimization/workshop' },
          { text: 'แบบทดสอบ', link: '/chapters/09-minimization/quiz' },
        ]
      },
      {
        text: '10 · Continuous Monitoring',
        collapsed: true,
        items: [
          { text: 'บทนำ', link: '/chapters/10-monitoring/' },
          { text: 'แนวคิดเชิงลึก', link: '/chapters/10-monitoring/concepts' },
          { text: 'กรณีศึกษา', link: '/chapters/10-monitoring/examples' },
          { text: 'Workshop', link: '/chapters/10-monitoring/workshop' },
          { text: 'แบบทดสอบ', link: '/chapters/10-monitoring/quiz' },
        ]
      },
      {
        text: '11 · Future of ASM',
        collapsed: true,
        items: [
          { text: 'บทนำ', link: '/chapters/11-future/' },
          { text: 'แนวคิดเชิงลึก', link: '/chapters/11-future/concepts' },
          { text: 'กรณีศึกษา', link: '/chapters/11-future/examples' },
          { text: 'Workshop', link: '/chapters/11-future/workshop' },
          { text: 'แบบทดสอบ', link: '/chapters/11-future/quiz' },
        ]
      },
    ],
    socialLinks: [{ icon: 'github', link: 'https://github.com/Unsull/asm-handbook-th' }],
    footer: { message: 'Independent Thai-language study guide · ไม่ใช่คำแปลอย่างเป็นทางการของหนังสือ', copyright: 'เรียนรู้และแบ่งปันอย่างรับผิดชอบ' }
  }
})
