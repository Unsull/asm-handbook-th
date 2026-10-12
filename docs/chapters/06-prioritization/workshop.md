# Workshop 6 — Asset Prioritization และ Crown Jewel Proposal

**เวลาแนะนำ:** 45 นาที · **ระดับ:** Intermediate · **ข้อมูล:** E-commerce Synthetic Assets

## ขั้นตอนที่ 1 — อ่านเกณฑ์คะแนน

เปิด `labs/06-prioritization/priorities.csv` แล้วดูมิติ Business, Operational, Data, Dependency และ Exposure (ให้ 1–5)

น้ำหนักในตัวอย่างคือ `25%, 25%, 20%, 20%, 10%` ตามลำดับ เป็นโมเดลเพื่อการเรียน ไม่ใช่สูตรมาตรฐานที่ต้องใช้จริง

## ขั้นตอนที่ 2 — คำนวณคะแนน

```powershell
py labs/06-prioritization/priority.py
```

Script เรียงจากคะแนนสูงไปต่ำ พร้อมเตือนว่า Ranking ไม่ใช่การอนุมัติ Crown Jewel

## ขั้นตอนที่ 3 — วิเคราะห์ Business Dependencies

ใช้ตัวอย่าง:

```text
Checkout API → Orders Database → Backup / Recovery
             → Payment Integration
Marketing Preview → Public Landing Content
```

ตอบว่า Service ไหนมี Single Point of Failure, อะไรมี Alternative Path และ Impact หากล่มกลาง Flash Sale ต่างจากช่วงไม่มีผู้ใช้หรือไม่

## ขั้นตอนที่ 4 — แยก Asset Tier จาก Finding Priority

สมมติ Checkout API เป็น Tier 0 แต่ไม่มี Confirmed Vulnerability; Marketing Preview เป็น Tier 3 แต่เกิด Active Exploitation ที่เชื่อมไป Production ได้ คุณจะจัด Remediation อย่างไร?

แนวคำตอบคือ **Threat/Exposure Conditions ที่ยืนยันแล้วอาจทำให้ Finding บน Tier 3 เร่งด่วนมาก** ขณะที่ Business Tier ต้องไม่เปลี่ยนโดยอัตโนมัติจากเหตุการณ์เดียว

## ขั้นตอนที่ 5 — สร้าง Crown Jewel Proposal

ส่งตารางอย่างน้อย 3 Candidates พร้อม `Business Owner`, `Loss Scenario`, `Data Sensitivity`, `Dependencies`, `Existing Controls`, `Evidence Needed`, `Approval Status`

## Verification

```powershell
py -m unittest discover -s labs/06-prioritization -p 'test_*.py' -v
```

## Common Mistakes

- “คะแนน 4.7/5” ไม่ใช่โอกาสถูกโจมตี 94%
- Criticality สูง ≠ Confirmed Vulnerability
- ทุก Asset เป็น Crown Jewel จะทำให้การจัดลำดับไม่มีประโยชน์

## Cleanup

ไม่มีการแตะ Infrastructure จริง; คืน CSV เมื่อต้องการเริ่มใหม่

[Quiz →](/chapters/06-prioritization/quiz)
