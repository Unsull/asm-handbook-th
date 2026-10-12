# กรณีศึกษา — ประเมิน Risk ของร้านค้าออนไลน์

## Case A: ลูกค้าอาจอ่านออเดอร์ของผู้อื่น

ระบบสมมติมี `GET /orders/{id}` โดยทีม Security สงสัยว่าอาจมี Object-level Authorization ที่ไม่ครบ **ตอนนี้ยังเป็น Hypothesis** ไม่ใช่ Confirmed Vulnerability

### นิยาม Scenario

- **Threat Actor:** บัญชีลูกค้าที่ Login ได้
- **Asset:** Customer Orders Data
- **Condition:** API ส่งข้อมูล Order โดยไม่ตรวจว่าผู้ใช้เป็นเจ้าของหรือได้รับสิทธิ์
- **Consequence:** Confidentiality Breach และอาจต้องแจ้ง Incident ตามกฎหมายที่ใช้
- **Unknowns:** Source Code, Test Results, Logging และการเข้าถึง API จริง

### Qualitative Risk Register

| Field | Candidate Value | Confidence |
|---|---|---|
| Impact | High | Business Owner ต้องยืนยัน |
| Likelihood | Unknown | ต้องตรวจเงื่อนไข Authorization |
| Existing Control | Login | ยืนยัน Login ไม่เท่ากับ Object Ownership |
| Treatment | Validate → Fix if confirmed | Owner: API Team |

จงสังเกตว่าเราไม่ควรกำหนด Likelihood = 5 เพียงเพราะ Endpoint เปิดสู่ Internet; หาก API ตรวจ Ownership ถูกต้องความเสี่ยง Scenario นี้ก็อาจต่ำมาก

## Case B: ประมาณ Cost ของ Booking Service Outage

บริษัทจองโรงแรมมี Historical Records สมมติว่าเหตุบริการจองหยุดชนิดหนึ่งทำให้สูญเสียค่าใช้จ่ายเฉลี่ย 180,000 บาทต่อครั้ง และคาดว่าความถี่ 0.4 ครั้ง/ปี

\[
ALE = 180{,}000 \times 0.4 = 72{,}000\text{ บาท/ปี}
\]

ถ้าเสนอ Redundancy/Monitoring ที่ทำให้ความถี่คาดการณ์เหลือ 0.1 ครั้ง/ปี โดยต้นทุนมาตรการ 30,000 บาท/ปี จะได้ Expected Avoided Loss = 54,000 บาท/ปี และ Net Expected Benefit = 24,000 บาท/ปี ภายใต้สมมติฐานนี้

**ข้อจำกัด:** จำนวนตัวอย่างเหตุการณ์น้อยทำให้ Rate ไม่เสถียร ช่วงความสูญเสียอาจเบ้สูง บางเหตุมีผลกฎหมาย/ความเชื่อมั่นที่ตีเป็นเงินไม่ได้

## Case C: สื่อสารต่อผู้บริหาร

ข้อความเชิงเทคนิค: “Public endpoint อาจมี BOLA”

ข้อความที่ตัดสินใจได้: “กำลังตรวจว่าลูกค้าสามารถเห็นคำสั่งซื้อที่ตนไม่มีสิทธิ์ได้หรือไม่ หากยืนยันจะต้องจำกัดการเข้าถึงและแก้ภายในรอบฉุกเฉิน เจ้าของงานคือ API Team พร้อม Security Negative Test ก่อนปิด Finding”

## ลองฝึก

ให้สร้าง Risk Register อีกหนึ่ง Scenario เช่น Refund Approval Abuse ระบุ Evidence Needed, Controls, Owner และเกณฑ์ปิดงาน ไม่ต้องเดาความเสี่ยงเป็นตัวเลขหากไม่มีข้อมูลเพียงพอ
