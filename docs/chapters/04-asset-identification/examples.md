# กรณีศึกษา — Asset Inventory ของโรงแรมจำลอง

## Case A: ฝ่าย IT บันทึก Asset ไม่ครบ

โรงแรมสมมติมี Front Desk Software, Online Booking Web, Payment Integration, Reservations DB, Backup Storage และ SaaS Channel Manager แต่ Spreadsheet เดิมบันทึกเพียง Server 3 เครื่อง

ปัญหาไม่ได้มีแค่จำนวนรายการผิด: Payment Integration และ SaaS Channel Manager เป็น Logical Assets ที่มี Token/Owner/Business Dependencies ต่างจาก Servers จึงควรบันทึกแยกกัน

### Inventory ที่เพิ่มบริบทแล้ว

| Asset ID | Asset | Type | Classification | Business Criticality | Owner |
|---|---|---|---|---|---|
| APP-01 | Booking Web | Web | Internal/Public Content | High | Web Team |
| API-01 | Reservations API | API | Confidential | Critical | Booking Team |
| DB-01 | Reservations DB | Database | Confidential | Critical | Data Team |
| EXT-01 | Payment Provider | SaaS/API | Payment Tokens | High | Finance/IT |
| OPS-01 | Backups | Data Storage | Confidential | Critical | Infrastructure |

คำว่า Critical ที่ใส่ในตัวอย่างเป็น Candidate Rating ที่ต้องให้ Business Owner ตรวจ ไม่ใช่ผลประเมินโรงแรมจริง

## Case B: Logical Service กับ Runtime Instance

ทีม Deploy Reservations API ด้วย Docker และ Replica สองตัว `booking-api-7af...` และ `booking-api-9bd...` ทั้งสองเป็น Container Instances ต่างกัน แต่เชื่อมกับ Logical Service เดียว `API-01`

ถ้า Inventory สร้าง Logical Asset ใหม่ทุกครั้งที่ Recreate Container จะทำให้ Owner Count เพิ่มโดยไม่จำเป็น และค้น Incident History ตามบริการจริงลำบาก

โครงที่ควรได้:

```text
API-01 (Logical Reservations API)
 ├── instance-001 (Docker Container, last_seen ...)
 └── instance-002 (Docker Container, last_seen ...)
```

## Case C: Data Classification ≠ Priority

ไฟล์แนะนำโรงแรมเป็น Public แต่ Booking Gateway เป็น Critical เพราะ Availability สำคัญ ขณะที่ไฟล์รายงานภายในที่มีชื่อพนักงานอาจเป็น Confidential แต่ Business Criticality ปานกลาง

ควรเก็บทั้ง `classification` และ `criticality` โดยไม่ผสมความหมาย

## แบบฝึก

เพิ่ม Asset อีกห้ารายการจากระบบโรงเรียนหรือร้านค้าออนไลน์ ระบุ `observed/declared/verified` และเหตุผลว่าหลักฐานใดทำให้เปลี่ยนเป็น Verified ได้
