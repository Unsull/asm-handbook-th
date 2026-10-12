# Workshop 3 — Risk Matrix และ Quantitative Scenario

**เวลาแนะนำ:** 40 นาที · **ระดับ:** Beginner–Intermediate · **ข้อมูล:** Synthetic E-commerce Scenarios

## เป้าหมาย

ทดลอง Qualitative Score 1–5, ระดับ Risk และ Annualized Loss โดยแยก Estimates ออกจากหลักฐานจริง

## ขั้นตอนที่ 1 — รัน Python Standard Library Lab

จาก Project Root:

```powershell
py labs/03-risk/risk_assessment.py
```

หรือบน Linux/macOS:

```bash
python3 labs/03-risk/risk_assessment.py
```

Script จะจัดอันดับ 3 Risk Hypotheses และคำนวณ Synthetic ALE

## ขั้นตอนที่ 2 — อ่าน Code และปรับตัวเลข

เปิด `labs/03-risk/risk_assessment.py` และดู `Risk(scenario, likelihood, impact)` ลองปรับ Scenario `checkout outage` จาก `(3,4)` เป็น `(2,5)` แล้วรันใหม่

- คะแนนเดิม `3×4=12` (High ในโมเดลนี้)
- คะแนนใหม่ `2×5=10` (Medium)

คะแนนลดไม่จำเป็นต้องหมายถึงความเสี่ยงจริงลดแล้ว เพราะเราเพียงเปลี่ยน Input สมมติ ต้องมี Evidence รองรับ

## ขั้นตอนที่ 3 — คำนวณ Quantitative Risk

เรียกฟังก์ชันใน Script หรือคิดเอง:

```text
Single loss = 180,000 THB
Annual rate = 0.4 events/year
ALE = 180,000 × 0.4 = 72,000 THB/year
```

ลองเปลี่ยน Annual Rate เป็น 0.2 และ 0.8 แล้วเปรียบเทียบ Sensitivity; ห้ามนำผลนี้ไปอ้างว่าเป็นค่าความเสียหายของบริษัทจริง

## ขั้นตอนที่ 4 — ออกแบบ Risk Register

| Field | ตัวอย่าง |
|---|---|
| Risk Scenario | Unauthorized cross-customer order access |
| Evidence Status | hypothesis |
| Business Impact | Pending owner confirmation |
| Controls | Object-level authorization (verification pending) |
| Treatment Owner | API Team |
| Review Date | กำหนดตามรอบงาน |

## ขั้นตอนที่ 5 — ทดสอบ Lab Function

```powershell
py -m unittest discover -s labs/03-risk -p 'test_*.py' -v
```

คาดว่าจะได้ `OK` จาก Tests ที่ทดสอบ Rating Bounds และ ALE Formula

## Common Pitfalls

- คิดว่า `5/5` คือโอกาสเกิด 100%
- นำ CVSS มาคูณกับ Rating ที่คนกำหนดแล้วเรียกเป็น Monetary Loss
- กำหนด Residual Risk ต่ำลงโดยไม่ตรวจว่า Control ใช้งานได้จริง

## Cleanup

ไม่มี Services หรือ Files ความลับถูกใช้งาน

[Quiz →](/chapters/03-risk/quiz)
