# แนวคิดเชิงลึก — Types of Attack Surfaces

## 1. ขอบเขตของ Attack Surface กว้างกว่าที่คิด

องค์กรสมัยใหม่มีสินทรัพย์ผสมกันระหว่าง On-premises, Cloud, SaaS, Identity Providers, Endpoints และ Third-party Integrations จึงควรแบ่ง Surface ตามลักษณะการเข้าถึง **ไม่ใช่** แบ่งตามแผนกเจ้าของเท่านั้น บริการหนึ่งอาจอยู่ได้หลายกลุ่ม เช่น Cloud-hosted API ที่ใช้ SaaS Identity Provider และอยู่ภายใต้ CI/CD Supply Chain

## 2. Traditional IT: Physical, Legacy และ Virtualization

**Traditional IT** ประกอบด้วย Physical Servers, Switches, Firewalls, File Shares, Domain Controllers, Desktops และ Legacy Services ที่อาจไม่ได้รับการ Patch หรือไม่มีผู้ดูแลชัดเจน ระบบ Legacy ไม่จำเป็นต้องมีช่องโหว่เสมอ แต่มีความท้าทายในการเปลี่ยน Version และตรวจสอบ

Virtual Machines เพิ่ม Layer ของ Hypervisor, Management Plane, Snapshots และ Virtual Networks ถ้า Administrator Console ถูกตั้งค่าไม่เหมาะสม ก็อาจกระทบ VM จำนวนมากได้จากจุดเดียว

ตัวอย่างโรงแรมสมมติ: เครื่องเซิร์ฟเวอร์ระบบจองยังใช้ Windows รุ่นเก่าที่จำเป็นต่ออุปกรณ์ Check-in การแก้ไม่ใช่สั่ง Upgrade ทันที แต่ต้องมี Business Impact, Compatibility Test และ Segmentation/Compensating Controls ตามข้อเท็จจริง

## 3. Modern IT: Containers, Microservices และ IoT

**Containers** เพิ่ม Images, Registries, Daemon Sockets, Runtime Permissions และ Short-lived Workloads คำสั่ง `docker ps` ช่วยเห็น Instances ที่กำลังทำงาน แต่ไม่แสดง Dependencies หรือ SaaS Roles ทั้งหมด

**Microservices** ลดขนาดแต่ละบริการแต่เพิ่ม API-to-API Calls, Tokens, Service Discovery และ Failure Paths ส่วน **IoT** เพิ่ม Firmware, Physical Access, Default Credentials, Remote Management และ Device Enrollment

| ประเภท | สิ่งที่ต้องค้นหา | Control Candidate |
|---|---|---|
| VM | Hypervisor Management, Snapshots | MFA, Segmentation, Supported Versions |
| Container | Images, Ports, Socket Mounts | Least Privilege, Image Scan |
| Microservice | APIs, Service Identities | mTLS/Authentication, Scope-limited Tokens |
| IoT | Devices, Firmware, Key Lifecycle | Inventory, Secure Updates, Revocation |

## 4. Websites และ Certificates

เว็บไซต์อาจเปิดหลาย Entry Points แม้ใช้ Port 443 เพียง Port เดียว เช่น Login, Reset Password, File Upload, Shopping Cart, GraphQL และ Admin Routes ดังนั้น **จำนวน Port ไม่ใช่จำนวน Attack Paths**

TLS Certificates เป็นส่วนหนึ่งของ Security Posture ต้องดู Issuer, Expiry, Key Management และ Domain Ownership แต่ Certificate ที่ยังไม่หมดอายุไม่ได้พิสูจน์ว่า App Authorization ถูกต้อง

ตัวอย่าง: เว็บร้านค้ามี HTTPS ถูกต้อง แต่ `GET /orders/{id}` ไม่มี Object-level Authorization ผู้ใช้จึงอาจเข้าถึงข้อมูลที่ไม่มีสิทธิ์ได้ ประเด็นนี้เป็น Application Security ไม่ใช่ Transport Security

## 5. Cloud: Responsibility และ Dynamic Resources

Cloud เพิ่ม IAM, Storage Policies, Public Endpoints, Serverless, Cloud Logs และ Account/Project Boundaries Shared Responsibility Model หมายความว่าผู้ให้บริการและผู้ใช้รับผิดชอบคนละส่วน โดยรายละเอียดแตกต่างตาม IaaS/PaaS/SaaS

ตัวอย่าง: บริษัทใช้ Object Storage เก็บไฟล์ใบเสร็จ และเปิด Bucket ให้ Public โดยไม่จำเป็น สิ่งที่ต้องตรวจไม่ใช่เพียง Firewall ของ VM แต่รวม Storage Resource Policy, Object ACL และ Public Access Settings

**Cloud Discovery** ควรใช้ APIs มากกว่า Scan อย่างเดียว เพราะ Private Resources บางรายการไม่มี Listening Port ที่เครื่องสแกนเข้าถึงได้ ติดตาม Resource ID, Region, Account, Owner, Tags และ Last Seen

## 6. SaaS: ข้อมูลและสิทธิ์ที่มองข้ามง่าย

SaaS อาจเป็น CRM, Email, File Sharing, HR หรือ Helpdesk Attack Surface หลักคือ Users, OAuth Grants, Shared Links, API Tokens, Third-party Apps และ Role Management

ตัวอย่างเจ้าหน้าที่แชร์ Spreadsheet ลูกค้าผ่าน Public Link จนทุกคนที่มี URL สามารถเปิดได้ แม้ Web Server ขององค์กรไม่เคยเปิด Public Database Port ปัญหานี้เกิดจาก Data Access Policy บน SaaS

ควรทำ SaaS Inventory ร่วมกับ Identity Provider, Access Review และข้อมูลจาก Procurement/Business Owner; การรู้ว่าซื้อ Subscription อะไรยังไม่เท่ากับรู้ทุก App ที่พนักงานใช้จริง

## 7. Identity: Human, Machine และ Privilege Graph

Identity Surface รวม Account, MFA Settings, Session Tokens, Service Principals, API Keys และ Privileged Roles เครื่องมือเครือข่ายไม่เห็นว่าบัญชีหนึ่งเข้าถึงข้อมูลได้กี่ประเภท

มองเป็น Graph: `Developer → CI Token → Production Deploy` หรือ `API Service → DB Credential → Orders Database` การลด Trust Paths ที่ไม่จำเป็นอาจสำคัญกว่าการปิด Port เพิ่มอีกหนึ่งรายการ

แนวทางหลักคือ Least Privilege, Short-lived Credentials, MFA ที่เหมาะสม, Joiner/Mover/Leaver Process, Rotation และ Auditable Access Decisions

## 8. Supply Chain: Dependencies และการส่งต่อความเชื่อถือ

Supply Chain Surface รวม Source Dependencies, Build Pipeline, Code Signing, Package Registries, Artifact Storage และ Outsourced Services การใช้ Software ที่ทันสมัยไม่ได้ตัดความเสี่ยงจาก Transitive Dependencies และ Compromised Build Credentials

| ชั้น | สิ่งที่ควรตรวจ | ตัวอย่างหลักฐาน |
|---|---|---|
| Source | Dependency Version และ Provenance | Lockfile / SBOM |
| Build | Runner Privileges และ Secret Injection | CI Workflow / Permissions |
| Artifact | Image Digest, Signature, Scan | Registry Records |
| Deploy | Approval, Environment Separation | Release/Change Logs |

การค้นพบ CVE ใน Library ไม่ได้ยืนยัน Exploitability จนกว่าจะตรวจ Version, Configuration และ Execution Path จริง

## 9. BYOD, Mobile และ AI

**BYOD/Mobile:** อุปกรณ์ส่วนตัวอาจมีข้อมูล Cache, Tokens และ Lost-device Risks ควรมี Endpoint Management, Revocation และนโยบาย Data Separation ที่สมดุลกับความเป็นส่วนตัว

**AI Systems:** Attack Surface ใหม่รวม Prompts, Retrieval Documents, Model APIs, Agent Tools, Data Pipelines และ Model Supply Chain โดยเฉพาะ Agent ที่มีสิทธิ์แก้ Systems อื่น การเก็บ Conversation Logs ยังเสี่ยงต่อข้อมูลส่วนบุคคลและคำสั่งจากแหล่งไม่น่าเชื่อถือ

## 10. สรุปวิธีทำ Inventory ข้าม Surface

เริ่มจาก `asset_id`, `type`, `owner`, `environment`, `exposure`, `identities`, `dependencies`, `data_classification`, `evidence_source`, `last_verified` แล้วเชื่อม Record ข้าม Surface อย่านับ Cloud Container และ API เป็น Asset เดียวกันโดยอัตโนมัติ แต่ให้จัดความสัมพันธ์ระหว่าง Physical/Logical/Runtime Instances

**อ่านต่อ:** [OWASP API Security](https://owasp.org/API-Security/), [NIST CSF](https://www.nist.gov/cyberframework)
