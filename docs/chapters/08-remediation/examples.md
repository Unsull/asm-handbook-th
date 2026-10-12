# กรณีศึกษา — จาก Finding สู่ Verified Closure

## Case A: Python API มี Authorization Bug

ทีมพบว่า Endpoint `GET /reservations/{id}` ตรวจว่า Login แล้ว แต่ไม่ตรวจว่า Reservation นั้นเป็นของผู้ใช้หรือไม่ บน Test Environment ที่มีข้อมูลจำลองสามารถสร้าง Evidence ว่าบัญชี A อ่านของ B ได้จริง

### รายงานก่อนแก้

- **Finding:** Confirmed Broken Object Level Authorization in isolated test
- **Impact:** Potential cross-user reservation disclosure
- **Root Cause:** Missing server-side object ownership check
- **Fix:** Add policy check + negative/positive tests
- **Verification:** Test A cannot read B (403), B can read B (200)

Code Change ที่ผ่าน Unit Test แต่ยังไม่ได้ Deploy เป็น Production ไม่ควรถูกปิดเป็น Production Finding

## Case B: PostgreSQL Host Port ถูก Publish โดยไม่จำเป็น

Compose มี `ports: ["5432:5432"]` และ Backend อยู่บน Docker Network เดียวกับ Database ทีมทดลองใน Isolated Environment แล้วพบว่าถอด Published Port ได้โดย API ยังเชื่อมต่อ Database ได้

### Before/After Evidence

| Check | Before | After |
|---|---|---|
| Docker Host Port Mapping | Present | Not present |
| Host Port Connectivity | Reachable | Not reachable via same host port |
| Backend to DB | Success | Success |
| Approved Admin Path | Not reviewed | Documented/verified |

การเปลี่ยนนี้เป็น Exposure Reduction ไม่ใช่หลักฐานว่าปัญหาทุกประเภทใน PostgreSQL หมดไป

## Case C: Scanner แจ้ง CVE แต่ Version ไม่ได้รับผลกระทบ

ทีมตรวจ Vendor Advisory แล้วพบว่า Scanner จับ Product ผิดเพราะ Version Fingerprinting จาก Port Default จึงจัดเป็น False Positive พร้อมหลักฐาน Version/Build/Configuration ที่ยืนยันได้

**การปิด Finding เพราะ False Positive** ต้องมี Evidence ต่างจาก **การแก้ช่องโหว่สำเร็จ** และควรบันทึก Reason/Reviewer/Date เพื่อป้องกันการปิดลอย ๆ

## แบบฝึก

เขียน Remediation Ticket ที่มี `Impact`, `Repro Steps (safe)`, `Fix Strategy`, `Rollback Plan`, `Verification Tests`, `Change Reference`, `Residual Risk`, `Owner` และ `Closure Evidence` แล้วให้เพื่อนตรวจว่าข้อสรุปผูกกับหลักฐานจริงหรือไม่
