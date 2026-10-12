# Workshop 8 — Fix, Regression Test และ Verified Closure

**เวลาแนะนำ:** 45 นาที · **ระดับ:** Beginner–Intermediate · **ข้อมูล:** Synthetic Orders

## เป้าหมาย

พิสูจน์ว่า Application-layer Object Authorization ช่วยปฏิเสธ Cross-user Access และสร้าง Test ที่ตรวจพบ Regression ได้จริง

## ขั้นตอนที่ 1 — อ่านฟังก์ชันทดสอบ

เปิด `labs/08-remediation/authorization.py` จะเห็น Orders จำลองของ `alice` และ `bob` และฟังก์ชัน `read_order(user_id, order_id)`

นี่เป็น Unit-level Policy Demonstration **ไม่ใช่ Authentication System ที่พร้อมใช้จริง** เพราะไม่มี Session/Token Verification Layer

## ขั้นตอนที่ 2 — รัน Regression Tests

```powershell
py -m unittest discover -s labs/08-remediation -p 'test_*.py' -v
```

Expected Result: 3 Tests ผ่าน ได้แก่ Cross-user Denied, Owner Allowed และ Missing Order Handling

## ขั้นตอนที่ 3 — เข้าใจ Bug ที่เรากำลังป้องกัน

แนวคิดโค้ดที่ไม่ปลอดภัยหากไม่มี Control ชั้นอื่น:

```python
def read_order(user_id, order_id):
    return ORDERS[order_id]  # lacks object-level ownership policy
```

**อย่าแก้ Production Code ตามตัวอย่างโดยไม่ตรวจ Context**; โค้ดนี้มีไว้เปรียบเทียบ Root Cause เท่านั้น

## ขั้นตอนที่ 4 — Mutation Test ใน Lab เท่านั้น

สำรองไฟล์ `authorization.py` แล้ว Comment เงื่อนไขตรวจ Owner ใน Lab จากนั้นรัน Tests ซ้ำ Test `test_cross_user_denied` ควรล้มเหลว คืนโค้ดทันทีหลังทดลองแล้วรันทดสอบอีกครั้งจนผ่าน

## ขั้นตอนที่ 5 — สร้าง Remediation Evidence

ตัวอย่าง Record:

| Field | Value |
|---|---|
| Finding | Synthetic BOLA Policy Gap |
| Before | Negative Test fails after intentional mutation |
| Change | Object Owner Check |
| After | Negative and Positive Tests pass |
| Environment | Local isolated lab |
| Production Status | Not assessed |

## ขั้นตอนที่ 6 — เพิ่ม Dependency Scanning (Optional)

บนโปรเจกต์ Node/Python ของตนเองเท่านั้น:

```powershell
npm audit
```

```powershell
py -m pip --version
```

สำหรับ Python Audit สามารถติดตั้ง `pip-audit` ใน Virtual Environment และใช้ `pip-audit -r requirements.txt` โดยตรวจ Compatibility/Lockfile ก่อนเลือก Fix; อย่าสั่ง Force Upgrade โดยไม่ทดสอบ

## Acceptance Criteria

- มี Test ที่ FAIL เมื่อเอา Authorization Check ออก
- Test ผ่านเมื่อคืน Control
- แยก Fixed in Code / Deployed / Validated / Closed
- ไม่อ้างว่า Lab นี้พิสูจน์ Production Security

## Cleanup

คืนไฟล์ `authorization.py` ฉบับปลอดภัย; ไม่มี Services ถูกเปิดใช้งาน

[Quiz →](/chapters/08-remediation/quiz)
