# แนวคิดเชิงลึก — Remediation

## 1. Remediation ไม่เท่ากับแค่กด Update

Remediation คือการจัดการ Root Cause ของ Finding หรือยกระดับ Controls จนความเสี่ยงถูกจัดการตามเกณฑ์ที่กำหนด อาจต้องแก้ Code, Infrastructure Configuration, Roles, Secrets หรือเปลี่ยน Architecture

**Finding** คือข้อค้นพบจากหลักฐาน เช่น “Database Port ถูก Publish บน Host” ซึ่งยังไม่เท่ากับ “ฐานข้อมูลถูกเจาะ” ต้องตรวจ Effective Reachability และ Business Use ก่อนประเมิน Risk

## 2. Assessing the Remediation Need

ให้ตรวจ 3 ส่วน: (1) Finding Applicability, (2) Severity/Impact และ (3) Cost-Benefit/Constraints

### Vulnerability Severity: CVE, CWE, CVSS, EPSS และ KEV

| ตัวอ้างอิง | สิ่งที่ให้ข้อมูล | สิ่งที่ไม่บอก |
|---|---|---|
| CVE | ตัวระบุช่องโหว่ | Probability ต่อ Server เรา |
| CWE | ประเภท Weakness | Asset-specific Business Impact |
| CVSS | Technical Severity | Complete Organizational Risk |
| EPSS | โอกาส CVE ถูก Exploit ในวงกว้างภายใน 30 วัน | โอกาส Host เฉพาะถูกเจาะสำเร็จ |
| CISA KEV | CVE ที่มีหลักฐาน Used-in-the-wild | ยืนยันว่าระบบเราถูก Compromise แล้ว |

เมื่อ Scanner แจ้ง CVE ต้องยืนยัน Affected Version และเงื่อนไข Vulnerable Configuration ก่อน Avoid False Positives ที่ทำให้ทีมเสียเวลา

### Potential Impact

ดู Confidentiality, Integrity, Availability, Financial, Operational, Privacy, Legal และ Trust หาก Checkout API มี BOLA อาจกระทบ Customer Privacy โดยตรง แต่ต้องยืนยันด้วย Test ที่ได้รับอนุญาต

### Cost-Benefit

ใช้ Cost-Benefit เทียบแนวทาง เช่น Patch ตอนนี้อาจใช้ 2 ชั่วโมงแต่มี Breaking Change ต้องทดสอบ Payment Flow; Network Restriction อาจทำเร็วกว่าเพื่อ Temporary Mitigation แต่ยังไม่แก้ Code Root Cause

ค่า `Expected Annual Loss Before − After − Annualized Fix Cost` เป็นโมเดลเศรษฐศาสตร์อย่างง่ายที่ขึ้นกับ Assumptions ไม่ควรใช้ปฏิเสธมาตรการที่กฎหมายกำหนด

## 3. Prioritization of Findings

พิจารณา **Ease of Exploitation, Discoverability, Attacker Interest, Business Impact และ Remediation Complexity** ร่วมกับ Threat Evidence

ตัวอย่าง: CVSS 8.0 ใน Public Checkout API ที่มีหลักฐานการใช้โจมตีจริงอาจเร่งด่วนกว่าช่องโหว่ CVSS 9.8 บนระบบทดสอบที่แยกและไม่ได้ถูกใช้งาน แต่ต้องตรวจทั้งหมดภายใต้ Risk Criteria ที่อนุมัติ

**Remediation Complexity สูงไม่ใช่เหตุผลปล่อย Critical Risk ไว้โดยไม่ทำอะไร** อาจใช้ Containment/Compensating Control ตาม Change Management แล้วดำเนินการ Fix ระยะยาว

## 4. Remediation Strategies

| Strategy | วิธีการ | เงื่อนไข |
|---|---|---|
| Patch/Upgrade | อัปเดต Library/OS | Compatibility & Version Scope |
| Code Fix | เพิ่ม Authorization/Validation | Unit + Negative + Regression Tests |
| Configuration Hardening | จำกัด Port, Methods, Roles | Actual Runtime Verification |
| Architecture Change | แยก Trust Zone | Dependency Review |
| Decommission | ถอด Service ที่ไม่ใช้ | Data Retention/Owner Approval |
| Temporary Mitigation | จำกัด Reachability ชั่วคราว | Expiration/Review Date |
| Risk Acceptance | ให้ผู้มีอำนาจรับ Residual Risk | Recorded Decision and Review |

## 5. Validation of Remediation Efforts

ขั้นตอนสำคัญคือ `Fix in Branch → Test → Deploy → Validate Runtime → Monitor → Close` การมี Git Commit ไม่ยืนยันว่า Production ใช้ Version ใหม่แล้ว เช่นเดียวกับ Scanner ผ่านไม่ได้แปลว่า Authentication Logic ไม่พัง

การตรวจควรมีทั้ง **Security Validation** เช่น Unauthorized Request ถูกปฏิเสธ และ **Functional Validation** เช่น Authorized Customer ยังดู Order ของตนได้

### Feedback Loop และ Stakeholders

Security ระบุ Finding/Criteria, Developer แก้ Code, SRE Deploy/Monitor, QA ตรวจ Regression, Business Owner อนุมัติผลกระทบและข้อยกเว้น ต้องมี Owner ที่ตรวจสอบได้ ไม่ใช่ Ticket ไปกองรวมโดยไม่มีผู้รับ

### Collateral Damage

การปิด Port อาจทำให้ Internal Integration หยุด การเปลี่ยน Token อาจทำให้ Queue Worker เรียก API ไม่ได้ การอัปเดต Dependency อาจเกิด Breaking Change จึงต้องวาง Rollback Criteria และ Monitoring หลัง Deploy

### Documentation

บันทึก `Finding ID, Before Evidence, Asset, Root Cause, Fix, Commit, Deployment ID, Tests, Verification Time, Reviewer, Residual Risk, Status` ใช้สถานะ `fixed in code` แยกจาก `deployed` และ `validated` เสมอ

## 6. เมื่อไรถือว่าปิด Finding ได้?

เมื่อ (1) ปัญหาและ Scope ถูกเข้าใจ (2) มีการแก้/จัดการ Risk ตามนโยบาย (3) Change อยู่ใน Environment ที่อยู่ใน Scope (4) มี Test Evidence และ (5) Owner/Reviewer อนุมัติ หากไม่มีหลักฐานให้ใช้ `pending verification` แทน `closed`

**อ่านต่อ:** [FIRST CVSS](https://www.first.org/cvss/), [FIRST EPSS](https://www.first.org/epss/), [OWASP API Security](https://owasp.org/API-Security/)
