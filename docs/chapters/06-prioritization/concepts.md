# แนวคิดเชิงลึก — Prioritization & Crown Jewel Analysis

## 1. ทำไมต้องจัดลำดับ?

ไม่มีทีมไหนแก้ทุก Finding พร้อมกันได้ การจัดลำดับช่วยตัดสินว่าทรัพยากรจำกัดควรปกป้อง Asset ไหนก่อน อย่างไรก็ตาม **Asset Criticality** เป็นคุณค่าต่อธุรกิจ ส่วน **Vulnerability Severity** เป็นความรุนแรงด้านเทคนิค และ **Risk Priority** เป็นความเร่งด่วนภายใต้ Threat/Exposure/Controls ปัจจุบัน คำทั้งสามไม่ควรใช้แทนกัน

ตัวอย่างระบบร้านค้าออนไลน์: Checkout Service อาจ Critical ต่อ Revenue แม้ไม่มี Public CVE; ส่วน Marketing Preview Tool อาจมี CVSS สูงแต่แยกจาก Production จริง ต้องพิจารณาเงื่อนไขการโจมตีก่อนจัดลำดับ

## 2. Comparison กับกระบวนการเชิงกลยุทธ์อื่น

| กระบวนการ | คำถาม |
|---|---|
| Asset Management | มีอะไร ใครรับผิดชอบ |
| Business Impact Analysis | หากบริการหยุด/ข้อมูลเสียหาย ธุรกิจเสียอะไร |
| Vulnerability Management | Software/Config มี Known Weakness หรือไม่ |
| Risk Management | เหตุการณ์ใดมีผลกระทบและโอกาสภายใต้ Controls อย่างไร |
| ASM Prioritization | จะตรวจและจัดการ Attack Paths ใดก่อน |

การรวมผลไม่ใช่การเอา Ratings ต่างสเกลมาบวกกันเฉย ๆ ต้องมีเกณฑ์และผู้มีอำนาจยืนยัน

## 3. Prioritization Criteria

### Value to Organization

ค่าของ Asset อาจเป็น Revenue, Brand Trust, Legal Obligations หรือความสามารถให้บริการต่อเนื่อง Orders Database อาจมี Hardware Cost ต่ำแต่ Business Value สูง

### Operational Impact

ดูเหตุการณ์ Confidentiality Breach, Data Tampering, Downtime, Fraud และ Recovery Complexity แยกกัน บริการที่หยุดชั่วโมงเดียวอาจมีผลต่างกันตามเวลาธุรกิจ เช่น Checkout ล่มระหว่าง Flash Sale กับเวลากลางคืน

### Data Sensitivity

Data Classification เน้นข้อกำหนดการเก็บ/เปิดเผยข้อมูล แต่ Criticality เน้นภารกิจ Dashboard อาจไม่มีข้อมูลลับมาก แต่สำคัญต่อ Incident Response ในเหตุการณ์ใหญ่

### Dependencies / Substitutability

หาก API Gateway เดียวเชื่อมหลายบริการ หรือ DNS/Identity Provider ตัวเดียวเป็น Single Point of Failure ค่า Dependency Criticality อาจสูงแม้ Asset นั้นไม่เก็บ Business Data เอง

## 4. Obtaining Business Context

คุยกับ Business Owner, Data Owner, Developers, SRE และ Compliance เพื่อยืนยัน Scope, Impact Thresholds, Workarounds, Seasonal Criticality และ Recovery Objectives

คำถามตัวอย่าง: หาก Checkout หยุด 2 ชั่วโมง มี Back-office ทางเลือกหรือไม่? หาก Orders ถูกแก้ย้อนหลัง จะต้องทบทวน Refunds เท่าไร? ใครมีสิทธิ์ Accept Risk ที่เหลือ?

ห้ามให้ทีม Security กำหนด Crown Jewels เพียงจากความรู้สึกโดยไม่มี Business Approval

## 5. Mapping Business Functions และ Impact Assessment

```text
Take order → Web → Checkout API → Orders DB
                    ↘ Payment Gateway
Dispatch   → Worker → Inventory DB → Logistics API
Recovery   → Backup Service → Storage Credentials
```

สร้าง Graph เพื่อเห็น Dependencies และ Blast Radius หาก Payment Provider มี Outage, Checkout อาจรับคำสั่งซื้อได้แต่การชำระเงินยัง Pending ตาม Design ไม่ใช่สรุปว่าทุกบริการ Down

RTO/RPO เป็น Business-approved Objectives ไม่ใช่ตัวเลขที่ Security ตั้งเอง และสำหรับ Integrity-centric Systems ควรเพิ่มความสามารถในการพิสูจน์ข้อมูลที่กู้คืนได้ด้วย

## 6. Determining Actual Prioritization

หนึ่งแนวทางการสอนคือ Weighted Scoring เช่น `0.25*Business + 0.25*Operational + 0.20*Data + 0.20*Dependency + 0.10*Exposure` โดยทุกมิติให้ 1–5 **สูตรนี้ไม่ใช่มาตรฐานสากล** และอาจบดบัง Threat Scenario เร่งด่วน

จึงควรแยก:

- **Business Criticality Tier:** โดยมากค่อนข้างเสถียรตาม Business Function
- **Risk Treatment Priority:** เปลี่ยนตาม Exploit Evidence, Reachability, Threats และ Existing Controls

## 7. Determining Crown Jewels

Crown Jewels คือ Assets หรือ Capabilities ที่สูญเสียหรือถูกควบคุมแล้วสร้างผลกระทบยอมรับไม่ได้ ไม่จำเป็นต้องเป็นข้อมูลลับหรือ Server ราคาแพงที่สุด

สำหรับร้านค้าออนไลน์ Candidate อาจเป็น Payment Credential Management, Orders Ledger, Customer Account Identity และ Ability to Fulfill Orders แต่ต้องให้ Business/Risk Owners อนุมัติ ไม่ควรกำหนดทุก Asset เป็น Crown Jewel เพราะจะทำให้ Priority ใช้ไม่ได้

## 8. High-value Assets และ Ranking Everything Else

กำหนด Tier เช่น Tier 0 Crown Jewel, Tier 1 High-value, Tier 2 Supporting, Tier 3 Low Impact แล้วกำหนด Minimum Baseline ทุก Tier บริการ Tier 3 ยังอาจเป็น Attack Path ไป Tier 0 ได้ถ้ามี Token/Trust Relationship จึงต้องตรวจ Privilege Graph เสมอ

## 9. Periodic Review

ทบทวนเมื่อย้ายระบบขึ้น Cloud, เพิ่ม Payments Channel, เปลี่ยน Identity Provider, เกิด Incident หรือเปลี่ยน Data Policy บันทึกเหตุผลและ Approval ของทุก Tier Change เพื่อให้จัดลำดับแบบ Audit ได้

**อ่านต่อ:** [NIST SP 800-30](https://csrc.nist.gov/pubs/sp/800/30/r1/final), [NIST CSF](https://www.nist.gov/cyberframework)
