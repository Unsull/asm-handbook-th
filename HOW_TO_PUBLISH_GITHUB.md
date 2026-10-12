# วิธีนำ ASM Handbook TH ขึ้น GitHub และเผยแพร่เว็บ

คู่มือนี้เขียนสำหรับ **Windows 11 / PowerShell** และบัญชี GitHub `Unsull` ตามตัวอย่าง หากคุณใช้บัญชีอื่นให้เปลี่ยนชื่อผู้ใช้และ URL ที่เกี่ยวข้อง

## 1) สร้าง Repository บน GitHub

1. เปิด <https://github.com/new> ด้วยบัญชีที่ต้องการ
2. Repository name: **`asm-handbook-th`**
3. Visibility: **Public** (เพราะต้องการแชร์คู่มือให้คนทั่วไปอ่าน)
4. **ไม่ต้อง**เลือก Add a README, .gitignore หรือ License (เพราะมีไฟล์เหล่านี้อยู่ในโปรเจกต์แล้ว)
5. กด **Create repository**

> โค้ดประกอบการเรียนรู้เป็นของโปรเจกต์นี้เอง แต่คู่มือไม่ได้เป็นคำแปลอย่างเป็นทางการของหนังสือ O'Reilly และไม่ควรนำข้อความหรือรูปจากหนังสือไปเผยแพร่โดยไม่ได้รับสิทธิ์

## 2) Push โปรเจกต์จากเครื่องไปยัง GitHub

หลังจากแตกไฟล์ ZIP ของโปรเจกต์ ให้เปิด PowerShell ในโฟลเดอร์ `asm-handbook-th` ซึ่งมี `package.json` และ `README.md` อยู่

ทางเลือก A — ใช้สคริปต์ที่จัดเตรียมไว้:

```powershell
.\publish.ps1
```

สคริปต์ตรวจสอบ Git, สร้าง Local Repository (หากยังไม่มี), Commit และ Push เข้า `https://github.com/Unsull/asm-handbook-th.git` และจะไม่ลบ/เขียนทับ Remote ที่ไม่ตรงกัน

ทางเลือก B — รันเองทีละคำสั่ง:

```powershell
git init -b main
git add .
git commit -m "Initial release: Thai ASM handbook"
git remote add origin https://github.com/Unsull/asm-handbook-th.git
git push -u origin main
```

หาก Git ขอให้ระบุตัวตน ให้ตั้งค่า `user.name` / `user.email` และยืนยันตัวตนกับ GitHub ด้วยวิธีที่ Git บนเครื่องรองรับ เช่น Git Credential Manager

> **สำคัญ:** โปรเจกต์นี้เป็น Repository Source ที่จัดเตรียมไว้ใน ZIP ยังไม่ได้ถูกสร้างหรือ Push ไปยัง GitHub โดยอัตโนมัติ

## 3) เปิดใช้ GitHub Pages

1. เปิด Repository ที่เพิ่ง Push
2. เข้า **Settings → Pages**
3. ใน **Build and deployment → Source** เลือก **GitHub Actions**
4. เปิดแท็บ **Actions** และเลือก Workflow **Deploy ASM Handbook to GitHub Pages**
5. หาก Push แรกเกิดขึ้นก่อนตั้งค่า Pages สามารถกด **Run workflow** (บน Branch `main`) หลังเลือก GitHub Actions เป็น Source
6. เมื่อ Workflow สำเร็จ เว็บไซต์จะเปิดได้ที่ <https://unsull.github.io/asm-handbook-th/>

หากใช้ชื่อ Repository ต่างจาก `asm-handbook-th` ต้องแก้ `base` ใน `docs/.vitepress/config.ts` ให้ตรงกับชื่อ Repository ก่อน Build

## 4) รันและทดสอบในเครื่อง

ต้องมี Node.js **22 หรือใหม่กว่า** และ npm

```powershell
npm install
npm run docs:dev
```

ตรวจ Source/Tests/Build:

```powershell
python scripts/validate_content.py
python scripts/run_lab_tests.py
npm run docs:build
```

ถ้าต้องการอ่านโดยไม่ต้องติดตั้ง Node.js ให้เปิด ZIP ชุด **offline preview** ซึ่งแยกให้ดาวน์โหลดต่างหาก แล้วเปิด `index.html` ใน Browser

## 5) ตรวจงานก่อนเผยแพร่

- กดเข้าให้ครบทุกบทและทุกหน้า (สารบัญ/กรณีศึกษา/Workshop/Quiz)
- ทดลองค้นหาด้วยทั้งภาษาไทยและภาษาอังกฤษ
- ตรวจความถูกต้องของ Diagram และ Math Rendering หลัง Build
- ทดสอบ Interactive Quiz บนเว็บจริง
- ตรวจ GitHub Actions Status และ GitHub Pages URL
- ตรวจว่ามี Secret/Token/ข้อมูลส่วนบุคคลหรือไม่
- หากแก้ Workshop ให้รัน Test และทำในเครื่อง/Network ที่ได้รับอนุญาต

## 6) แก้ไขและเผยแพร่รุ่นต่อไป

แก้ Markdown ใน `docs/chapters/*/` แล้ว:

```powershell
python scripts/validate_content.py
python scripts/run_lab_tests.py
npm run docs:build
git add .
git commit -m "docs: improve Thai ASM lessons"
git push
```

Workflow จะ Build และ Deploy เวอร์ชันใหม่หลัง Push ไปยัง `main` (ตามสิทธิ์และ Settings ของ Repository)

## ปัญหาที่พบบ่อย

- **Workflow บอกว่า Pages ยังไม่ถูกเปิดใช้:** ไป Settings → Pages และเลือก Source เป็น GitHub Actions
- **เว็บโหลด Assets ไม่ขึ้น:** ตรวจ `base: '/asm-handbook-th/'` และชื่อ Repository ว่าตรงกัน
- **npm install ไม่สำเร็จ:** ตรวจการเชื่อมต่อ npm Registry, Proxy และ Node.js Version
- **Git push ถูกปฏิเสธ:** ตรวจ GitHub Authentication และสิทธิ์ Push; หลีกเลี่ยง Force Push
- **VitePress build ไม่ผ่าน:** เปิดรายละเอียด Error ใน GitHub Actions แล้วแก้ที่ Source ก่อน Deploy อีกครั้ง
