# แนวคิดเชิงลึก — Minimizing Attack Surfaces

## 1. How to Minimize Attack Surfaces

เป้าหมายของการลด Attack Surface ไม่ใช่ “ปิดทุก Service จนระบบใช้งานไม่ได้” แต่คือการรักษา **Minimum Necessary Exposure and Privilege** ตาม Business Requirements

ตัวอย่างโรงแรมใช้ Public Booking Web, Internal Booking API, Private Database และ Admin Portal หาก Admin Portal ไม่ต้องเปิดให้แขกจากอินเทอร์เน็ตเข้าถึงโดยตรง ก็ควรออกแบบ Access Controls ที่แยกจาก Public Web แทนการเผยแพร่ทุก Service บน Host Interfaces เดียวกัน

**Reduction vs Hardening vs Remediation**: การถอด Unused Host Port คือ Reduction, การเพิ่ม MFA ให้หน้าที่ต้องใช้คือ Hardening, การแก้ Authorization Bug คือ Remediation ทั้งสามทำร่วมกันได้แต่ไม่ควรใช้คำแทนกันโดยไม่มีบริบท

## 2. Strategic Methods: ลดจากการออกแบบ

### Secure-by-Design

กำหนด Trust Boundaries ก่อนเขียนระบบ: Browser → HTTPS Gateway → Application → Private Data Zone พร้อม Default-deny Network Paths, Server-side Authorization และ Sensitive Operation Approval อย่าฝัง Admin Privilege ลง User-facing Services หากไม่จำเป็น

### Least Privilege

ลดสิทธิ์ของ Human/Machine Identities: ร้านค้าออนไลน์มี Token สำหรับอ่าน Catalog ไม่ควรใช้ Token เดียวกับ Payment Refund Management และ CI Runner ไม่ควรมี Production Secrets ทั้งหมดตลอดเวลา

### Network Segmentation

ออกแบบ Connectivity Matrix ว่าใครต้องคุยกับใคร เช่น `web→api:443`, `api→db:5432`, `ops→admin:443` และให้ Security/Operations ยืนยัน Actual Reachability ข้อเท็จจริงสำคัญคือ **การอยู่ใน Network เดียวกันไม่ได้หมายความว่ามี Controls ครบ** และ “ไม่มี Public IP” ไม่ได้แก้ Excessive Trust ระหว่าง Internal Services

### Lifecycle and Governance

กำหนด Retirement Process สำหรับ Old Admin Apps, Staging Environments, API Tokens และ Unused Cloud Resources ทุกการลบต้องตรวจ Dependencies, Backup, Audit Retention และ Business Owner Approval

## 3. Tactical Techniques: ปรับทีละ Surface

### Host/Network Surface

ตรวจ <code v-pre>docker ps --format "table {{.Names}}\t{{.Ports}}"</code> และ `Get-NetTCPConnection -State Listen` แล้วระบุ Host Ports ที่ไม่จำเป็น การ Publish Port `0.0.0.0` อาจเปิดหลาย Host Interfaces ขณะที่ `127.0.0.1` มีข้อจำกัดตาม Docker/OS Version จึงต้องยืนยัน Effective Reachability จาก Vantage ที่ถูกต้อง

### Container Runtime

ลด Linux Capabilities, ใช้ Non-root Process, Read-only Root Filesystem เท่าที่ Compatible, จำกัด Volumes/Socket Mounts, Scan Base Images และกำหนด Resource Limits อย่านำ Hardening Template ของ Stateless App ไปใช้กับ Stateful Database โดยไม่ทดสอบ File/Volume Permissions

### API Surface

ลบ Unused Routes เมื่อผ่าน Dependency Review, จำกัด Admin Endpoints, ใช้ Rate Limits/Authorization ตาม Operation, ลด Sensitive Error Messages และทบทวน API Documentation Exposure การปิด `/docs` ของ FastAPI **ไม่ได้เพิ่ม Authentication ให้ Routes โดยอัตโนมัติ**

### Data Surface

เก็บเฉพาะข้อมูลที่จำเป็นและตามนโยบาย Retention, ลด Public Shared Links, ควบคุม Backups และ Temporary Exports การลบข้อมูลโดยไม่ตรวจ Legal Retention อาจก่อปัญหามากกว่าประโยชน์

### Identity and Secret Surface

แยก Roles, Revoke Credentials รุ่นเก่า, ลด OAuth Scopes, กำหนด Owner/Expiration และอย่า Commit Secrets ลด Secret Copies ที่ไม่มีความจำเป็นและตรวจการใช้สิทธิ์ย้อนหลัง

### Supply Chain Surface

ลบ Dependencies ที่ไม่มี Runtime Usage, Pin/Review Versions, ใช้ SBOM/Lockfile/Artifact Scanning และ Build Pipeline ที่จำกัดสิทธิ์ อย่าลบ Packages เพราะ Scanner ระบุว่า “Unused” โดยไม่มีการทดสอบระบบที่ครอบคลุม

## 4. Security Validation ต้องตรวจ 2 ด้าน

| Change | Security Evidence | Functional Evidence |
|---|---|---|
| ถอด DB Host Port | Host/NAT Path ถูกปิด | API ยังเชื่อม DB ได้ |
| จำกัด Admin Route | Unauthorized Client เข้าไม่ได้ | Admin เข้าได้เมื่อมีสิทธิ์ |
| Rotate Token | Old Token ถูก Revoked | Job ใช้ New Token สำเร็จ |
| Read-only Container | Write Paths ที่ไม่จำเป็นถูกจำกัด | App เริ่มและทำงานครบ |

การรายงานว่า Ports ลดจาก 10 เป็น 4 คือ **Host-published Surface ลดลง 60% ภายใต้ Scope ที่วัด** ไม่ใช่ Cyber Risk ลดลง 60% เพราะ Risk ไม่แปรผันตรงกับจำนวน Ports

## 5. แนวทางป้องกันการกลับมาเปิด Surface

เพิ่ม Tests ที่ตรวจ Approved Network Bindings/Policies ใน CI/CD, Review Configuration Drift และกำหนด Owner สำหรับ Exceptions ถ้าเพียงแก้ Compose แล้วไม่ตรวจ Runtime อาจยังมี Container เก่าที่ใช้ค่าก่อนเปลี่ยน

**อ่านต่อ:** [Docker Port Publishing](https://docs.docker.com/engine/network/port-publishing/), [OWASP Attack Surface Analysis](https://cheatsheetseries.owasp.org/cheatsheets/Attack_Surface_Analysis_Cheat_Sheet.html)
