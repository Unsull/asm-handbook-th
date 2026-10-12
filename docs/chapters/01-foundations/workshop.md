# Workshop 1 — วาด Attack Surface Map โดยไม่ต้องสแกนระบบจริง

**เวลาแนะนำ:** 25–40 นาที · **ระดับ:** Beginner · **ระบบ:** Example Shop (ข้อมูลจำลอง)

## ผลลัพธ์ที่ต้องส่ง

- Asset Inventory ขั้นต่ำ 4 รายการ
- รายการ Entry Points, Exit Points และ Trust Boundaries
- Threat Hypothesis 2 รายการที่ไม่กล่าวอ้างว่าพบ Vulnerability แล้ว
- Controls to Verify ที่มี Owner อย่างน้อย 2 รายการ

## Prerequisites

ใช้ VS Code หรือ Spreadsheet เปิดไฟล์ `labs/01-foundations/surface_inventory.csv` ได้ โดยไม่ต้องติดตั้ง Docker หรือสแกนเครือข่ายภายนอก

## ขั้นตอนที่ 1 — อ่าน Inventory ที่เตรียมไว้

จาก Project Root:

```powershell
Import-Csv .\labs\01-foundations\surface_inventory.csv |
    Format-Table -AutoSize
```

จะเห็น Customer Web, Order API, Orders DB และ CI Deploy Token พร้อม Entry Points และ Verification Status ที่ยังไม่ได้ยืนยัน Runtime

## ขั้นตอนที่ 2 — สร้าง Data Flow

วาดเส้นทางตามนี้ใน Markdown/กระดาษ/diagrams.net:

```text
Customer → HTTPS Web → Order API → Orders DB
                               ↑
                    CI/CD Deployment Identity
```

จากนั้นเพิ่มเส้นแบ่ง Trust Boundary ระหว่าง Browser กับ Web, Application กับ Database และ CI/CD กับ Production

## ขั้นตอนที่ 3 — ระบุ Surface และ Vector แยกจากกัน

ตัวอย่างบันทึก:

| Asset | Surface | Potential Vector | ต้องตรวจ |
|---|---|---|---|
| Order API | `GET /orders/{id}` | IDOR/BOLA ถ้าขาด Object Auth | Negative Authorization Tests |
| CI Token | Deployment Identity | Token Theft / Excessive Scope | Token Scopes, Secret Storage |

นี่เป็น Threat Hypotheses ไม่ใช่ผลพบช่องโหว่จริง

## ขั้นตอนที่ 4 — เพิ่ม Owner และ Test

กำหนด Owner และตรวจว่ามี Proof Method เช่น Source Review, Staging Test, Runtime Permissions หลีกเลี่ยงการเขียน `secure=true` ถ้าไม่มี Evidence

## Verification / Acceptance Criteria

- ทุก Asset มี `asset_id`, `owner` หรือ `needs-review`
- Surface/Vector ไม่ปะปนกัน
- Trust Boundaries อย่างน้อยสองจุดถูกระบุ
- ทุก Threat Scenario มีวิธีตรวจโดยไม่ใช้ Production Data

## Common Mistakes

- ใช้จำนวน Host Ports เท่ากับจำนวน Attack Paths
- เรียก Service ที่ Internet-facing ว่ามี CVE โดยไม่มีหลักฐาน
- ไม่รวม Machine Identities ใน Inventory

## Cleanup

ไม่มี Service ถูกสร้างหรือแก้ไข ลบไฟล์ที่ทดลองเพิ่มได้ตามต้องการ

[กรณีศึกษา →](/chapters/01-foundations/examples) · [Quiz →](/chapters/01-foundations/quiz)
