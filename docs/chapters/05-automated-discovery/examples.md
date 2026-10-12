# กรณีศึกษา — Automated Discovery ใน Cloud และ Docker

## Case A: Containers อายุสั้นหายจาก Daily Snapshot

ระบบร้านค้าออนไลน์มี Background Worker Autoscale ตอนสั่งซื้อสูง บาง Worker อยู่เพียง 4 นาที แต่ระบบ Inventory ดึง `docker ps` วันละครั้ง จึงพลาด Instances บางส่วน

### วิเคราะห์และออกแบบ

- **Problem:** Snapshot Coverage ต่ำเมื่อ Asset Lifetime สั้นกว่ารอบตรวจ
- **Evidence:** Container Events, Orchestrator API, CI Deploy Events
- **Design:** เก็บ Lifecycle Events และ Scheduled Reconciliation ไปด้วยกัน
- **Identity:** เชื่อม Runtime Instance กับ Logical Service/Deployment ID
- **Risk:** หากมี Unapproved Image/Port ก็อาจเกิด Exposure ที่ไม่ถูก Review

การเปลี่ยนจากตรวจวันละครั้งเป็นทุกชั่วโมงช่วยได้บางส่วน แต่ไม่รับประกันว่าจะพบ Container ที่อยู่เพียง 4 นาที

## Case B: Cloud Storage ไม่มี Open Port ให้สแกน

บริษัทใช้ Cloud Object Storage สำหรับใบเสร็จ Public Access Policy อาจถูกเปลี่ยนโดยไม่ผ่าน Review การใช้ Nmap อย่างเดียวไม่สามารถประเมิน Storage Policy ได้อย่างครบถ้วน

จึงต้องใช้ Cloud Resource APIs, Audit Events และ Policy Assessment ผ่านสิทธิ์ Read-only ที่เหมาะสม แล้วเชื่อมกับ Asset Owner

## Case C: API Inventory ได้จาก OpenAPI แต่ไม่ครบ

ทีมอ่าน `/openapi.json` ของ FastAPI และได้ 14 Operations แต่ Source Code มี Route สำหรับ Health/Admin ที่ถูกซ่อนจาก Schema ด้วย `include_in_schema=False`

ข้อมูล OpenAPI ควรถูกติด `source=openapi` และ `coverage=declared schema`; หากต้องการตรวจเพิ่มให้เปรียบเทียบ Source Routes, API Gateway/Traffic Logs ตาม Scope ที่ได้รับอนุญาต

## แผน Data Quality

| Field | ตัวอย่าง | ทำไมต้องเก็บ |
|---|---|---|
| `last_seen` | UTC timestamp | ตรวจความใหม่ |
| `source` | Docker API | ตรวจว่ามาจากไหน |
| `verification` | Observed | ไม่กล่าวอ้างว่าผ่าน Manual Review |
| `logical_id` | `checkout-api` | ติดตาม Service ข้าม Recreate |
| `instance_id` | Container ID | วิเคราะห์เหตุการณ์เฉพาะ Instance |

## แบบฝึก

ตั้งสมมติฐานว่า Cloud Account ใหม่เข้ามาแต่ยังไม่ได้เชื่อม Collector: ตัวชี้วัด `100% of discovered assets have owners` พิสูจน์ได้ไหมว่าค้นพบ Assets ทั้งหมดแล้ว? (ไม่ได้ เพราะ Denominator จำกัดเฉพาะที่ค้นพบ)
