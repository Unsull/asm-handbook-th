# แนวคิดเชิงลึก — Foundations of Attack Surface Management

## 1. Attack Surface คืออะไร และสำคัญอย่างไร?

**Attack Surface** หมายถึงชุดของจุดติดต่อ ความสามารถ สิทธิ์ และเส้นทางที่ผู้ไม่ประสงค์ดี *อาจ* ใช้เพื่อเข้าถึงข้อมูลหรือทำให้บริการเกิดผลที่ไม่ต้องการ ขอบเขตนี้กว้างกว่า “พอร์ตที่เปิดอยู่” เพราะรวม API, Account, Secret, Cloud Policy, Web Form, Physical Access และ Dependency Trust Relationships ด้วย

ลองมองระบบร้านค้าออนไลน์: หน้าเว็บรับคำค้นสินค้า, API รับคำสั่งซื้อ, Database เก็บข้อมูลลูกค้า, ระบบจัดการหลังร้านมีสิทธิ์คืนเงิน และ Pipeline สามารถ Deploy Code ใหม่ได้ ทั้งหมดมี Attack Surface ต่างชนิดกัน

การพบจุดติดต่อ **ไม่เท่ากับ** การค้นพบ Vulnerability; บริการที่จำเป็นย่อมมี Entry Points อย่างไรก็ตาม ทุก Entry Point ต้องมี Owner, Security Requirement, Verification Method และหลักฐานว่ามาตรการยังทำงาน

| คำศัพท์ | คำถามที่ตอบ | Example Shop |
|---|---|---|
| Asset | อะไรมีคุณค่าที่ต้องดูแล | Orders DB |
| Entry Point | ข้อมูล/คำสั่งเข้าตรงไหน | `POST /login` |
| Attack Surface | จุด/สิทธิ์/ความสัมพันธ์ใดอาจถูกใช้เป็นช่องทาง | Public API, admin roles, CI tokens |
| Attack Vector | วิธีการที่ผู้โจมตีใช้ผ่านช่องทางนั้น | Credential stuffing ผ่าน Login |
| Vulnerability | จุดอ่อนที่ใช้ประโยชน์ได้ | API ไม่ตรวจ Object Ownership |
| Threat | เหตุการณ์ที่อาจทำให้เกิดความเสียหาย | ดูออเดอร์ของผู้อื่น |
| Risk | ความไม่แน่นอนของผลกระทบต่อเป้าหมาย | การรั่วไหลข้อมูลลูกค้าและค่าจัดการเหตุการณ์ |

### Attack Surface ต่างจาก Attack Vector

หน้าล็อกอินเป็น **Attack Surface** เพราะเป็นช่องทางโต้ตอบกับระบบ ส่วนการใช้รหัสผ่านที่หลุดจากบริการอื่นมาลองล็อกอินเป็น **Attack Vector** ที่ผู้โจมตีเลือกใช้ ช่องทางเดียวอาจมีหลาย Vectors เช่น Brute Force, Phishing-derived Credentials หรือ Session Abuse การลดจำนวนหน้าเว็บไม่ได้แก้ Vectors เหล่านี้ทั้งหมด ถ้ายังมี Authentication Weakness เหมือนเดิม

## 2. ทำไมการตรวจครั้งเดียวไม่พอ?

องค์กรเปลี่ยนระบบตลอดเวลา: Deploy Microservice ใหม่, เพิ่ม DNS Subdomain, เปิด Cloud Storage, เพิ่ม OAuth Integration, เปลี่ยน Firewall Rules หรือสร้าง CI/CD Token คนละชุดกับของเดิม การเปลี่ยนแต่ละอย่างอาจขยาย Attack Surface โดยไม่ปรากฏใน Architecture Diagram รุ่นเก่า

ลองให้ทีมพัฒนาเพิ่ม Admin Dashboard ที่ `admin.shop.example` (โดเมนสมมติ) แต่ไม่ลงทะเบียนใน Inventory ทีมตรวจ Security ที่ดูเฉพาะ Domain หลักจะมองข้าม Interface ใหม่ การทำ ASM จึงต้องมี **Discovery + Change Tracking** มากกว่าการทำ Audit เป็นครั้งคราว

## 3. วงจรการทำ ASM ที่นำไปปฏิบัติได้

```text
Identify → Classify → Prioritize → Remediate/Reduce
   ↑                         ↓
   └──── Adapt ← Monitor ←───┘
```

### Identification

ค้นหาสินทรัพย์จากหลายแหล่ง เช่น DNS, Cloud APIs, Docker/Kubernetes Runtime, CMDB และ Code Repository แล้วบันทึก `source`, `first_seen`, `last_seen` ไม่ควรถือว่าทะเบียนเดิมครอบคลุมของจริงทั้งหมด

### Classification

เพิ่ม Context: Owner, Environment, Business Function, Data Classification, Exposure, Lifecycle, Dependencies ตัวอย่าง Database สองตัวอาจใช้ Engine เดียวกันแต่ตัวหนึ่งเก็บข้อมูลลูกค้า Production ส่วนอีกตัวเก็บ Synthetic Test Data จึงควรมีมาตรการต่างกัน

### Prioritization

แยก **Asset Criticality** (สำคัญต่อธุรกิจ) จาก **Current Risk** (สถานการณ์และ Controls ในเวลานั้น) เลือกจัดการปัญหาที่ทำให้เกิดผลกระทบสูงหรือมีหลักฐานการโจมตี โดยไม่ยึดติดกับคะแนน Severity เพียงค่าเดียว

### Remediation / Reduction

แก้ Root Cause เช่น Object-level Authorization หรือถอด Host Port ที่ไม่จำเป็น ตรวจ Regression ก่อนและหลัง Deploy และบันทึกว่ามาตรการใดเป็น Fix จริงหรือเป็น Temporary Mitigation

### Adapting

เมื่อ Organization/Technology เปลี่ยน ต้องกลับมาทบทวน Threat Model, Key/Owner Inventory และ Policies ไม่ใช่คัดลอก Rules เก่าทั้งหมดไปใช้กับ Architecture ใหม่

### Monitoring

เก็บสัญญาณจาก Runtime, Configuration, Logs และ Business Workflows ตั้ง Alert ที่มี Owner และ Runbook แต่ต้องแยก “สังเกตเห็นผิดปกติ” จาก “ยืนยันว่าเกิดการโจมตี”

## 4. มองจากมุมผู้โจมตีอย่างมีขอบเขต

ผู้ดูแลระบบมักมองเป็นทีม: Web, Database, Payment, Operations แต่ผู้โจมตีอาจมองเป็น “เส้นทางข้าม Trust Boundaries” เช่น Public API → Overprivileged Service Account → Internal Database

การเปลี่ยนมุมมองนี้ทำให้ทีมถามคำถามที่ดีขึ้น: ถ้า Endpoint หนึ่งถูกควบคุม จะเข้าถึงอะไรต่อได้? Secrets อยู่ตรงไหน? มี User Roles ที่กว้างเกินไปหรือไม่? Logging จะเชื่อมการกระทำย้อนกลับได้หรือไม่?

::: warning ขอบเขตการปฏิบัติ
มุมมองแบบผู้โจมตีช่วยตั้งสมมติฐานการป้องกัน ไม่ใช่สิทธิ์ให้สแกนระบบของผู้อื่น การทดสอบต้องมี Scope และ Authorization ชัดเจน
:::

## 5. Use Cases และอุปสรรคในการนำ ASM มาใช้

| ความท้าทาย | ผลกระทบ | วิธีเริ่มแก้ |
|---|---|---|
| Visibility Gap | มี Asset ที่ทีมไม่รู้จัก | Compare Runtime + Cloud + IaC |
| Shadow IT | มีบริการที่ไม่มี Owner | Register Owner + Review Business Use |
| Duplicate Assets | ข้อมูลจากหลาย Scanner ซ้ำ | Stable ID + Correlation Rules |
| No Business Context | ให้ Priority ผิด | Map Critical Business Processes |
| Poor Communication | ทีมแก้ช้าเพราะไม่เข้าใจผลกระทบ | Risk Scenario + Action + Owner |
| Policy Drift | Configuration กลับมาเปิดอีก | Policy as Code + Continuous Verification |

สำหรับองค์กรเล็กไม่จำเป็นต้องเริ่มจาก Enterprise Platform แพง ๆ เริ่มด้วย Inventory ที่มี Owner, Source และ Last Verified ครบ แล้วเพิ่ม Automation เมื่อจำนวน Assets หรืออัตราเปลี่ยนสูงขึ้น

## 6. ความเข้าใจผิดที่พบบ่อย

**“ยิ่งมี Assets น้อยยิ่งปลอดภัยเสมอ”** — ไม่จริง หากนำทุกบริการมารวมบน Host เดียวแล้วเพิ่มสิทธิ์ข้ามระบบ ความเสี่ยงอาจสูงกว่าเดิม

**“มี Firewall แล้ว Attack Surface หายไป”** — Firewall ลดบางเส้นทาง แต่ API Permissions, Secrets, Supply Chain และ Malicious Insiders ยังคงต้องจัดการ

**“ไม่มี Public IP แปลว่าไม่เสี่ยง”** — Internal Service อาจถูกใช้ผ่าน Compromised Identity หรือ Service-to-Service Trust

**“Scanner ให้ Risk Score 9.8 หมายความว่าโอกาสถูกโจมตี 98%”** — ผิด CVSS Severity ไม่ใช่ Probability และต้องใช้บริบทธุรกิจเพิ่มเติม

## 7. ลองคิดด้วยตัวเอง

ร้านค้าออนไลน์มี Public Website, Internal Order API, Private Database และ CI/CD Runner ที่สามารถ Deploy Production ได้ ให้ระบุอย่างน้อย 4 Assets, 3 Entry Points, 2 Trust Boundaries และ 1 Control ต่อจุด จากนั้นเปรียบเทียบกับ [กรณีศึกษาในบทนี้](/chapters/01-foundations/examples)

**อ่านต่อ:** [OWASP Attack Surface Analysis](https://cheatsheetseries.owasp.org/cheatsheets/Attack_Surface_Analysis_Cheat_Sheet.html), [NIST CSF](https://www.nist.gov/cyberframework)
