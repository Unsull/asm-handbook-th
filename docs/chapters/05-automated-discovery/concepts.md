# แนวคิดเชิงลึก — Automating Asset Discovery

## 1. เหตุใด Manual Inventory จึงล้าสมัยง่าย?

ในร้านค้าออนไลน์ Cloud Autoscaling อาจสร้าง Server Instance ชั่วคราวและลบทิ้งในเวลาไม่กี่นาที การตรวจ Assets รายสัปดาห์จึงมีโอกาสไม่เห็นทรัพยากรดังกล่าว ระบบสมัยใหม่ยังมี Containers, Serverless, SaaS และ CI Runners ที่เปลี่ยนตาม Deployment Events

**Automated Discovery** คือการใช้ Collectors/APIs/Agents และกระบวนการตรวจทานข้อมูล เพื่อลดช่องว่างระหว่าง *สิ่งที่ทำงานจริง* กับ *สิ่งที่ Inventory รู้จัก* ไม่ได้หมายความว่าค้นพบ 100% โดยอัตโนมัติ

## 2. Breadth of Enterprises และ Cloud Complications

### Growth and Change

องค์กรขยายจาก Web+DB เป็น Web+API+Microservices+Message Queues+Cloud Storage ระบบที่พึ่ง Manual Spreadsheet ต้องมี Data Stewardship, Owner และ Change Process ก่อนเพิ่ม Automation

### Global Organizations

หลาย Region/Network Zones อาจมีข้อจำกัดเรื่อง Data Residency และ Routing ควรใช้ Regional Collectors ดึง Metadata ขั้นต่ำ แล้วรวมผลอย่างควบคุมสิทธิ์ แทนการส่งข้อมูล Sensitives ทั้งหมดไป Central Platform

### Cloud Complications

Cloud มี Ephemeral IDs, Multiple Accounts/Projects, APIs ที่ต้องให้สิทธิ์, Resources ที่ไม่เปิด Network Ports และ Tags ที่อาจไม่ครบ ควรใช้ Cloud Lifecycle Events **ควบคู่** กับ Scheduled Reconciliation เพราะ Snapshot อย่างเดียวอาจพลาด Resources ที่เกิดและหายระหว่างรอบ

## 3. Network Scanning: มองเห็นอะไรจริง?

Network Scanner ตรวจได้ว่าปลายทางตอบสนองและ Ports/Services ใดรับการเชื่อมต่อจากจุดที่สแกน ตัวอย่าง `nmap -sT -p 80,443 127.0.0.1` ใช้กับเครื่องตนเองเพื่อเรียนรู้ Port States

| State | ความหมายโดยย่อ | ไม่ควรสรุป |
|---|---|---|
| open | มีบริการตอบ TCP Connection | ไม่มีช่องโหว่หรือปลอดภัยแล้ว |
| closed | ไม่มี Listener ที่ Port นั้นจากจุดตรวจ | ไม่มี Service ทั้งระบบ |
| filtered | การกรอง/ไม่ตอบสนองทำให้แยกไม่ได้ | Host หยุดทำงาน |

การตรวจจาก Loopback ไม่พิสูจน์ Internet Reachability และชื่อ Service ที่ Scanner เสนออาจมาจาก Port Lookup ไม่ใช่ Product Fingerprint ที่ยืนยัน

## 4. Cloud Analysis: Management Plane สำคัญกว่า Port Scan อย่างเดียว

ใช้ Cloud Resource APIs เพื่อค้นหา VM, Object Storage, Identity, Load Balancers, Serverless Functions และ Resources ที่ไม่มี Public IP เก็บ Native Resource ID, Project, Region, Owner, Tags, Exposure และ Discovery Time แล้วทำ Correlation กับ DNS/Runtime Events

ตัวอย่าง SaaS บริษัทอาจมี Cloud Storage Bucket ที่ Public Access ถูกเปิดโดย Policy แต่ไม่มี IP Address ให้สแกน ดังนั้น Network-only Discovery จึงไม่ครอบคลุมความเสี่ยงนี้

## 5. API Identification

ค้นหา Endpoints ผ่าน OpenAPI, API Gateway, Code Routes และ Traffic Logs **OpenAPI ไม่รับประกันว่า Routes ทั้งหมดอยู่ใน Schema** เช่น FastAPI มี `include_in_schema=False` ได้

Inventory ที่เหมาะสมบันทึก Method, Path Template, Authentication Requirement, Data Sensitivity, Owner, Traffic Observations และการยืนยันว่ามี Permission Checks ต่อ Object หรือไม่

ตัวอย่าง `GET /orders/{order_id}` สำคัญกว่าเพียงนับ Endpoint เพราะเส้นทางเดียวสามารถเข้าถึง Order Records จำนวนมากได้หาก Authorization Policy ผิดพลาด

## 6. Data Discovery

ค้นหา Database Schemas, Storage Buckets, Backups, Sensitive Datasets และ Data Flows ควรเน้น Metadata/Schema ก่อน Content Sampling และตรวจสิทธิ์เสมอ โดยเฉพาะข้อมูลลูกค้า/การเงิน

ตัวอย่างทีมพบ `orders_archive` ใน Backup Storage ที่ไม่มี Owner และยังให้ Service Account รุ่นเก่าอ่านได้ นี่ไม่ใช่เพียง Asset Unknown แต่เป็น Identity/Retention/Access Review Scenario ต้องตรวจ Policy จริงก่อนตัดสินใจ

## 7. Challenges: False Positives, False Negatives และ Deduplication

- **False Negative:** Firewall ทำให้ Active Scanner ไม่เห็น Host ทั้งที่ Cloud API ยืนยันว่ามี Resource
- **False Positive:** Scanner จัด Port 5432 เป็น PostgreSQL ทั้งที่บริการอื่นฟัง Port เดียวกัน
- **Identity Drift:** Container ID เปลี่ยนแต่ Logical Service เดิม
- **Coverage Gap:** Cloud Account ใหม่ไม่อยู่ใน Collector Scope
- **Data Freshness:** ไม่มี Timestamp หรือ Last Seen จึงแยก Unavailable กับ Retired ไม่ได้

เทคนิค Correlation ที่ดีคือเก็บ Logical Asset ID กับ Runtime Instance ID แยกกัน และบันทึกเหตุผล/หลักฐานที่เชื่อมสอง Records เข้าด้วยกัน

## 8. Features ที่ให้ผลตอบแทนคุ้มค่า

| Feature | ใช้ทำอะไร | วิธีประเมิน |
|---|---|---|
| Search/Filters | หา Assets ตาม Owner, Tag, Exposure | ค้นหาจากหลาย Sources ได้จริงหรือไม่ |
| Data Presentation | Tables, Relationships, Timelines | Analyst ตาม Attack Path ได้หรือไม่ |
| Analytics | New/Missing Assets, Coverage, Freshness | มี Definitions และ Baseline หรือไม่ |
| Advanced Automation | Event-driven Diff, Tickets, Risk Enrichment | มี Approval/False Positive Review หรือไม่ |

ตัวเลข **New Assets** ไม่ใช่จำนวนบริการใหม่เสมอไป อาจเกิดจากการเพิ่ม Collector ทำให้ค้นพบ Assets เดิมที่เคยมองไม่เห็น

## 9. Design Pattern: Discovery Pipeline

```text
Sources → Collect → Normalize → Correlate → Enrich
                       ↓
                 Verify / Confidence
                       ↓
                 Inventory + Diff → Review → Action
```

แนะนำเริ่มจาก CSV/JSON ที่ตรวจสอบได้ทุก Record ก่อนสร้างระบบ Scanning ขนาดใหญ่ ตัวอย่าง Automation ที่ปลอดภัยที่สุดคืออ่าน Docker Metadata และเปรียบเทียบ Snapshots โดยไม่ต้องสแกนเครือข่ายภายนอก

**อ่านต่อ:** [Nmap Reference](https://nmap.org/book/man.html), [OWASP Attack Surface Analysis](https://cheatsheetseries.owasp.org/cheatsheets/Attack_Surface_Analysis_Cheat_Sheet.html)
