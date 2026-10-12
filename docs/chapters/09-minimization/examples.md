# กรณีศึกษา — ลด Surface โดยไม่ทำให้บริการล่ม

## Case A: แยก Internal API จาก Host Port

ร้านค้าออนไลน์จำลองมี Web Container และ Internal API Container ทั้งสองอยู่บน Docker Network เดียวกัน แต่มีกำหนด `ports` สำหรับ Internal API ซึ่งไม่จำเป็นต่อผู้ใช้ Host

**Before:** Host ติดต่อ `127.0.0.1:18089` ได้ และ Web ติดต่อ Internal API ผ่าน Service Name ได้

**After:** ถอด `ports` ของ Internal API, Recreate Container แล้วตรวจว่าจาก Host เข้าพอร์ตเดิมไม่ได้ แต่ Web ยังติดต่อ API ได้ตามเดิม

| Test | Expected After |
|---|---|
| Published Port List | ไม่มี Host Mapping ของ Internal API |
| Host TCP Port | ไม่รับการเชื่อมต่อที่ Port เดิม (หากไม่มี Process อื่น) |
| Web → Internal API | สำเร็จ |
| User-facing Web | สำเร็จ |

### ทำไมไม่เรียกว่า Risk ลด 50%?

หากมี 2 Host Ports และลดเหลือ 1 จำนวน Published Ports ลดลง 50% จริง แต่ Business Risk ยังขึ้นกับ Authorization, Secrets, Product Vulnerabilities และ Trust Relationships

## Case B: Decommission Admin Application รุ่นเก่า

บริษัทใช้ Admin UI ใหม่แล้ว แต่ Old Admin UI ยังอยู่ใน VM อีกหนึ่งตัวแม้ไม่มี Traffic ข้อควรทำก่อนลบ:

1. ตรวจ Scheduled Jobs/External Integrations ที่อาจเรียก UI เป็นครั้งคราว
2. ตรวจ Data Retention และ Logs ที่ต้องเก็บ
3. Review Owner/Approval และ Maintenance Window
4. Revoke Service Account/Secrets ที่ผูกกับ UI
5. Remove DNS/Proxy/Runtime ตาม Change Plan
6. Verify Absence และปรับ Asset Inventory

การพบ “ไม่มี Traffic 7 วัน” ไม่เพียงพอให้ลบ Production Service โดยอัตโนมัติ

## Case C: ลดสิทธิ์ผู้ใช้งานหลังร้าน

Marketing Analyst ต้องดู Conversion Reports แต่ Role เดิมรวม Refund Approval ด้วย การแยกเป็น Read-only Analytics Role ไม่ได้ลด Open Ports แต่ช่วยลด Privilege Attack Surface

**Verify:** Analytics ยังทำงาน และ Refund Action ผ่าน Role ใหม่นั้นต้องถูกปฏิเสธ

## แบบฝึก

ทำ Change Proposal ที่มี `Reduction Candidate`, `Business Dependency`, `Rollback`, `Before/After Check` แล้วอธิบายว่าทำไมควรลด Surface ชนิดนี้ก่อนอีกชนิดหนึ่ง
