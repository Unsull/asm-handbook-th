# แนวคิดเชิงลึก — Identification and Classification of Assets

## 1. ทำไมต้องรู้จัก Asset ก่อนลดความเสี่ยง?

การประเมินความปลอดภัยโดยไม่มี Asset Inventory เหมือนดูแลอาคารโดยไม่รู้ว่ามีกี่ห้องและประตูทางออกอยู่ตรงไหน **Asset** ไม่จำกัดแค่ Hardware แต่รวม Software, Data, Digital Identities, Cloud Resources, API Services, Certificates และ Business Processes

ตัวอย่างบริษัทจองโรงแรมมี Booking Web, Reservation API, Database, Payment Provider Account, Hotel Staff Portal, Export Jobs และ Backup Storage บาง Asset ไม่มี Public Port แต่สำคัญต่อธุรกิจและข้อมูลลูกค้าอย่างมาก

## 2. Identification: รู้ว่าอะไรมีอยู่จริง

ค้นหาสินทรัพย์จาก **หลาย Sources** เช่น Cloud APIs, Host Agents, DNS, Code Repositories, Docker Runtime, Logs และ CMDB การอ่าน Compose File บอกสิ่งที่ *ตั้งใจ Deploy* แต่ไม่ยืนยันว่าบริการทำงานจริง เช่นเดียวกับ Port Scan ที่พบ Service แต่ไม่ทราบ Data Owner

ควรเก็บ `source`, `observation_time`, `verification_status` เพื่อแยก:

| Status | ความหมาย |
|---|---|
| Declared | พบใน Configuration/Repository |
| Observed | พบใน Runtime หรือ Telemetry |
| Verified | ยืนยัน Identity/Owner/Function แล้ว |
| Unknown | ข้อมูลไม่ครบหรือมีข้อขัดแย้ง |
| Retired | ผ่านการยกเลิกใช้งานตาม Change Process |

## 3. Asset Inventory และการออกแบบ Identifiers

Inventory ที่ดีใช้ Stable ID ของ Logical Assets และแยก Resource Instances ที่เปลี่ยนตาม Deployment เช่น `service=booking-api` เป็น Logical Service ขณะที่ Container ID ใหม่เป็น Runtime Instance ที่เชื่อมกับ Service นั้น

ข้อมูลขั้นต่ำ:

| Field | เหตุผล | ตัวอย่าง |
|---|---|---|
| Asset ID | ผูกข้อมูลข้าม Tools | `API-BOOKING-01` |
| Name + Type | เข้าใจบทบาท | `Reservation API` |
| Owner | Routing Findings | `Booking Team` |
| Environment | แยก Prod/Test | `production` |
| Business Function | ประเมิน Impact | `Room Booking` |
| Exposure | วิเคราะห์ทางเข้า | `gateway-only` |
| Data Classification | ป้องกันข้อมูล | `confidential` |
| Dependencies | ระบุ Single Points | `reservations-db` |
| Last Verified | ตรวจความสดใหม่ | Timestamp UTC |

อย่าเก็บ Secrets จริงลง Inventory หากจำเป็นต้องอ้าง Credential ให้เก็บ Reference ไปยัง Secret Manager และ Access Policy

## 4. การเลือก Inventory Solution

สำหรับทีมเล็กเริ่มจาก CSV/Spreadsheet ได้ แต่ควรมี Schema และ Validation ไม่ให้แต่ละคนเขียน `Prod`, `production`, `PRD` ปะปนกัน

เมื่อระบบขยาย ให้พิจารณา Asset Platform หรือ CMDB ที่เชื่อม APIs/Automation ได้ และมี Version/Ownership History ระวังการซื้อ Platform ก่อนกำหนด Data Stewardship และ Source of Truth เพราะ Automation ไม่สามารถแก้ความผิดพลาดเชิงความหมายทั้งหมดด้วยตัวเอง

## 5. Discovery: Active, Passive, API, Agent

| Method | สิ่งที่เห็น | ข้อจำกัด |
|---|---|---|
| Active Scan | Reachable Hosts/Ports | Firewall, Coverage, Rate Limits |
| Passive Traffic | Observed Communications | ไม่เห็นบริการที่ไม่มี Traffic |
| Cloud/Docker API | Resources/Metadata | Permissions/Scope |
| Agent | Host Packages/Processes | Agent Coverage/Health |
| Repo/IaC Review | Desired State | ไม่ยืนยัน Runtime |

การสแกนต้องได้รับสิทธิ์และมี Scan Window เหมาะสม การพบ Service บน Port หนึ่งไม่ได้ยืนยัน Product หรือ Vulnerability โดยไม่ตรวจเพิ่ม

## 6. Classification for Asset Enrichment

Enrichment คือการเติมบริบทให้ Asset มีประโยชน์ต่อ Risk Decision เช่น `IP: 192.0.2.15` กลายเป็น `Reservations DB / Prod / Owner=Data Team / Confidential / Private / Backup every 4h`

### Asset Type Details และ Configuration Data

บันทึก Technology, Version, Runtime, Ports, Auth Mode และ Actual vs Desired Configuration ควรเก็บ Source Evidence เช่น `docker inspect` หรือ Cloud Resource ID โดย Mask ข้อมูลลับก่อนเก็บ

### Data Classification

เริ่มจากระดับตัวอย่าง **Public, Internal, Confidential, Restricted** แต่ใช้ชื่อตามนโยบายองค์กรจริง แยก Data Sensitivity ออกจาก Business Criticality: Monitoring Dashboard อาจเก็บข้อมูลลับน้อยแต่มีความสำคัญต่อ Recovery สูง

### Usage และ Location

เก็บว่าใครเรียกใช้งานเมื่อใด อยู่ Cloud Region/Network Zone ใด ความถี่การใช้งานช่วยระบุ Candidates สำหรับ Retirement แต่ไม่ควรลบบริการเพราะไม่มี Traffic ในช่วงสั้นเพียงอย่างเดียว

### Interdependencies

เชื่อม `Web → API → DB`, `API → Payment Provider`, `Admin → IAM` เพื่อระบุ Business Impact และ Single Points of Failure การมี Dependency Graph ช่วยแยกความสำคัญของ API Gateway ออกจาก Data Storage ได้

### Security Posture และ Lifecycle

บันทึก Known Vulnerabilities, Patch Status, Authentication, Logging, Backup และ Control Verification รวมทั้ง Lifecycle `planned/active/retiring/retired` **ไม่มีหลักฐาน** ว่ามี Control ไม่ได้เท่ากับ **พิสูจน์ว่าไม่มี** Control; ใช้ `not_verified` แทนการให้ค่า False โดยไม่มีหลักฐาน

## 7. Integrating Inventory with Business Strategy

Inventory ช่วยการจัดลำดับแก้ไข, Software License Audit, Compliance Evidence และ Cost Allocation แต่ต้องตรวจ Coverage ด้วย เช่น Owner Coverage = `Assets ที่มี Owner / Assets ที่ค้นพบ` ซึ่ง **ไม่ได้พิสูจน์ว่าค้นพบทุก Asset ในองค์กรแล้ว**

## 8. คุณภาพของ Inventory ที่ควรตรวจ

- **Completeness:** Fields สำคัญครบหรือไม่
- **Accuracy:** ข้อมูลตรงกับ Runtime หรือไม่
- **Freshness:** ตรวจล่าสุดเมื่อใด
- **Coverage:** แหล่งข้อมูลที่ควรค้นได้ถูกเชื่อมครบหรือไม่
- **Uniqueness:** Logical Asset กับ Instances ซ้ำกันหรือไม่
- **Accountability:** มี Owner และ Reviewer หรือไม่

**อ่านต่อ:** [NIST CSF Identify](https://www.nist.gov/cyberframework), [Docker Networking](https://docs.docker.com/compose/how-tos/networking/)
