# แนวคิดเชิงลึก — Measuring Attack Surface & Threat Modeling

## 1. Attack Surface Analysis (ASA) คืออะไร?

ASA วิเคราะห์ Entry/Exit Points, Data Flows, Trust Boundaries, Access Paths และ Security Controls เพื่อระบุว่าควรปกป้องอะไร และค้นหา Evidence Gaps ตรงไหน **ไม่ใช่แค่จำนวน Open Ports** และไม่ใช่หลักฐานว่าพบ Vulnerability ทุกจุดที่วิเคราะห์

### How Does ASA Work?

1. กำหนด Scope, Assets, Environment และ Authorization
2. ค้นหา Interfaces/Users/Services ที่รับหรือส่งข้อมูล
3. ทำ Data Flow/Dependency Map และ Trust Boundaries
4. ตั้ง Threat Hypotheses พร้อม Asset/Business Impact
5. ตรวจ Existing Controls, Reachability, Vulnerability/Exposure Evidence
6. จัดลำดับและสร้าง Verification Tasks
7. ตรวจซ้ำเมื่อระบบเปลี่ยน

### ASA Enhances Security Posture อย่างไร?

การเห็นช่องทางมากขึ้นช่วยให้ตั้ง Tests/Controls ได้ตรงจุด แต่จำนวน Findings ที่เพิ่มจาก Discovery รอบแรก **อาจหมายถึง Visibility ดีขึ้น** ไม่ใช่ระบบเสี่ยงกว่าเมื่อวานโดยอัตโนมัติ

## 2. Internal และ External Attack Surfaces

External Surface คือเส้นทางที่เข้าถึงได้จาก Trust Zone ภายนอก เช่น Public Website, Internet-facing API หรือ Remote Management Portal ส่วน Internal Surface คือส่วนที่เข้าถึงได้ภายใน Trust Zones เช่น Database Ports, Service Accounts และ Shared Secrets

**Overlap** เกิดเมื่อ Public API ใช้ Internal Credential อ่าน Orders DB ผู้โจมตีอาจไม่ต้องเข้าถึง DB โดยตรง หาก Web Endpoint สามารถออกคำสั่งเกินสิทธิ์ได้

| สิ่งที่ตรวจ | External | Internal |
|---|---|---|
| Reachability | DNS/HTTPS/Gateway | Network Policies/Service Routes |
| Authorization | Public API / Customer Identity | Service Identity / DB Roles |
| Evidence | External Test from approved vantage | Runtime Config and Restricted Tests |
| Common Blind Spot | Shadow Subdomains | Excessive East-West Trust |

## 3. Tools for Assessing Surfaces

- **Nmap:** ตรวจ Host/Port Reachability จากมุมมองที่กำหนด แต่ไม่วัด Business Risk
- **Docker / Cloud APIs:** ตรวจ Runtime, Network Bindings และ Resource Metadata แต่ไม่ยืนยัน Exploitability
- **OpenAPI / Gateway:** ค้น Documented Endpoints แต่อาจพลาด Hidden Routes
- **OWASP ZAP / Threat Dragon:** ช่วยประเมิน Web/App และวาด DFD/Threats ตามขอบเขตที่ได้รับอนุญาต
- **Logs/Tracing:** เห็น Observed Flows แต่ไม่รับประกันว่าครอบคลุม Traffic ทุกช่วง

## 4. Threat Modeling คืออะไร?

Threat Modeling คือการถามอย่างเป็นระบบว่า “อะไรผิดพลาดได้บ้าง, ใครจะได้รับผลกระทบ, เราควรป้องกันอย่างไร, และจะรู้ได้อย่างไรว่าป้องกันสำเร็จ” สามารถทำตั้งแต่ Design Stage ก่อนเกิดช่องโหว่จริง

### Data Flow Diagram และ Trust Boundary

```text
[Customer Browser] --HTTPS--> [Web/API Trust Zone]
                                     |
                           Authorization Check
                                     |
                         [Private Orders Database]
                                     |
                         [External Payment API]
```

เมื่อข้อมูลข้าม Boundary เช่น Browser → Backend หรือ Backend → Payment Provider ต้องตรวจ Authentication/Authorization, Validation, Encryption/Transport และ Error Handling ตามลำดับชั้น

## 5. STRIDE: 6 หมวดภัยคุกคาม

| STRIDE | Meaning | Example Shop |
|---|---|---|
| S — Spoofing | ปลอมตัวตน | Stolen Customer Session |
| T — Tampering | แก้ข้อมูลผิดสิทธิ์ | เปลี่ยนจำนวนสินค้าหรือราคาโดยไม่มี Validation |
| R — Repudiation | ปฏิเสธการกระทำ | คืนเงินโดยไม่มี Audit Evidence |
| I — Information Disclosure | เปิดเผยข้อมูล | อ่าน Order ของคนอื่น |
| D — Denial of Service | ทำให้บริการใช้การไม่ได้ | Checkout API Unavailable |
| E — Elevation of Privilege | ได้สิทธิ์เกิน | Customer เข้า Admin Function |

หมวด STRIDE เป็นกรอบตั้งสมมติฐาน ไม่ใช่การยืนยันว่าระบบมีช่องโหว่ครบทั้งหกหมวด

## 6. Methodologies อื่นที่ควรรู้จัก

**PASTA** เชื่อม Threats กับ Business Risk, **LINDDUN** เน้น Privacy, **Attack Trees** แตกเส้นทางไปยัง Attacker Goals, **STRIDE** เหมาะเริ่มกับ Data Flows และ Application APIs เลือกวิธีตาม Scope, Stakeholders และชนิดข้อมูล ไม่จำเป็นต้องใช้ทุกแนวทางพร้อมกัน

## 7. Integrating Threat Modeling with Attack Surface Mapping

ASM พบรายการ Assets/Interfaces ใหม่ได้ ขณะที่ Threat Modeling ช่วยบอก Security Questions ที่ต้องตรวจเพิ่ม เช่น เพิ่ม Customer Upload API แล้วต้องตรวจ File Validation, Storage Authorization และ Scan Limits

ในทางกลับกัน เมื่อ Threat Model อธิบายว่า Admin API ควรอยู่หลัง VPN แต่ Discovery เห็น Public Reverse Proxy ต้องสร้าง Finding เพื่อยืนยัน Control Gap ไม่ควรสรุปว่าระบบถูกโจมตีสำเร็จแล้ว

## 8. Metrics ของ Attack Surface มีข้อจำกัด

- `Internet-facing Assets`: ขึ้นกับ Scope และ Vantage Point
- `Privileged Service Accounts`: ต้องดู Policy และ Usage ไม่ใช่ตัวเลขอย่างเดียว
- `Unreviewed Entry Points`: วัด Assessment Backlog ไม่ใช่จำนวนช่องโหว่
- `Mean Time to Discover`: ใช้เวลาที่สร้าง Asset และเวลาที่ตรวจพบซึ่งต้องเชื่อถือได้
- `Open Attack Paths`: ต้องยืนยัน Preconditions ก่อนนับเป็น Reachable

**อย่ารายงาน** “Ports ลดลง 50% แปลว่า Risk ลดลง 50%” เพราะ Risk ไม่ขึ้นกับจำนวน Ports แบบเส้นตรง

**อ่านต่อ:** [OWASP Attack Surface Analysis](https://cheatsheetseries.owasp.org/cheatsheets/Attack_Surface_Analysis_Cheat_Sheet.html), [OWASP Threat Dragon](https://owasp.org/www-project-threat-dragon/)
