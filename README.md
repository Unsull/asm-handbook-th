# ASM Handbook TH — คู่มือ Attack Surface Management ภาษาไทย

คู่มือเรียนรู้ **Attack Surface Management (ASM)** แบบอิสระ 11 บท เขียนคำอธิบายใหม่เป็นภาษาไทย พร้อมศัพท์เทคนิคภาษาอังกฤษ กรณีศึกษาร้านค้าออนไลน์ ระบบ SaaS และ Cloud, Workshop ที่ใช้ข้อมูลจำลอง, แบบทดสอบรายบท และอภิธานศัพท์

> **สถานะ**: เนื้อหาฉบับเริ่มต้นสำหรับการศึกษาและทบทวน; ต้องตรวจสอบเงื่อนไขและเวอร์ชันจริงก่อนใช้คำสั่งกับระบบปฏิบัติงาน
>
> **การอ้างอิง**: โครงลำดับหัวข้อได้รับแรงบันดาลใจจากสารบัญของ *Attack Surface Management: Strategies and Techniques for Safeguarding Your Digital Assets* โดย Ron Eddings และ MJ Kaufmann (O'Reilly, 2025) แต่ข้อความ ตัวอย่าง กรณีศึกษา แบบฝึกหัด และโค้ดใน Repository นี้เป็นงานเขียนเพื่อการศึกษา **ไม่ใช่คำแปลอย่างเป็นทางการหรือฉบับทดแทนหนังสือต้นฉบับ** และไม่เกี่ยวข้องกับ O'Reilly Media หรือผู้เขียน โปรดสนับสนุนและอ่านหนังสือต้นฉบับเมื่อศึกษาลึกขึ้น

## เริ่มอ่าน

เมื่อเปิด GitHub Pages แล้ว เว็บไซต์จะอยู่ที่ `https://unsull.github.io/asm-handbook-th/`

- [เริ่มต้นใช้งาน](docs/getting-started.md)
- [สารบัญ 11 บท](docs/learning-path.md)
- [กรณีศึกษาร้านค้าออนไลน์](docs/case-study/index.md)
- [อภิธานศัพท์](docs/glossary/index.md)
- [แหล่งอ้างอิง](docs/references/index.md)

## รันบนเครื่อง (Node.js 22+)

```bash
npm install
npm run docs:dev
```

เปิด URL ที่ Terminal แสดง (โดยปกติ `http://127.0.0.1:5173/asm-handbook-th/`)

```bash
python scripts/validate_content.py
python scripts/run_lab_tests.py
npm run docs:build
npm run docs:preview
```

## โครงสร้าง

- `docs/chapters/01-...` ถึง `11-...`: บทนำ, ทฤษฎี, ตัวอย่าง, Workshop และ Quiz แยกบท
- `docs/.vitepress`: Navigation, Theme และ Interactive Quiz Component
- `labs/`: Synthetic labs ที่ไม่แตะระบบจริง
- `.github/workflows`: Validate, Build และ Deploy
- `scripts/validate_content.py`: ตรวจความครบถ้วนและ Markdown Links เบื้องต้น

ดูขั้นตอนละเอียดใน [HOW_TO_PUBLISH_GITHUB.md](HOW_TO_PUBLISH_GITHUB.md) หรือใช้ `publish.ps1` บน PowerShell หลังสร้าง Repository ว่างแล้ว

## เผยแพร่ผ่าน GitHub Pages

1. สร้าง Repository **Public** ชื่อ `asm-handbook-th` ในบัญชี GitHub ที่ต้องการ (หากใช้ชื่ออื่นให้แก้ค่า `base` ใน `docs/.vitepress/config.ts`).
2. Push โปรเจกต์ขึ้น Branch `main`.
3. เข้า `Settings → Pages → Build and deployment → Source` แล้วเลือก **GitHub Actions**.
4. ดู `Actions → Deploy ASM Handbook to GitHub Pages` และตรวจผล Build/Deploy.
5. เว็บไซต์จะเปิดได้ที่ `https://<username>.github.io/asm-handbook-th/` เมื่อ Deploy สำเร็จ

## แนวทางความปลอดภัยและการมีส่วนร่วม

- Lab ทำได้เฉพาะเครื่องหรือ Network ที่มีสิทธิ์ตรวจสอบ; หลีกเลี่ยง Production และข้อมูลผู้ใช้จริง
- `127.0.0.1` และ IP `192.0.2.0/24` ที่ปรากฏเป็นตัวอย่าง ไม่ใช่ Targets จริง
- ผลสแกนและตัวเลขในบทเรียนเป็น **ผลจำลอง** จนกว่าจะระบุว่ามีการทดสอบจริง
- ห้าม Commit Tokens, Private Keys หรือ Audit Logs ที่มีข้อมูลอ่อนไหว
- สำหรับคำสั่งที่เปลี่ยนระบบ ต้องสร้าง Backup/Change Plan และ Test Rollback ตามความเหมาะสม

## แหล่งข้อมูลหลัก

- [O'Reilly — Attack Surface Management (2025)](https://www.oreilly.com/library/view/attack-surface-management/9781098165079/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [VitePress Documentation](https://vitepress.dev/)

**การให้เครดิตและลิขสิทธิ์:** คำอธิบายทั้งหมดเป็นงานเรียบเรียงอิสระ ไม่อนุญาตให้เพิ่มเนื้อหาที่คัดลอกจากหนังสือหรือภาพมีลิขสิทธิ์โดยไม่มีสิทธิ์ใช้งาน กรุณาเสนอ Pull Request โดยระบุแหล่งอ้างอิงและหลักฐานการทดสอบ Workshop ให้ครบถ้วน
