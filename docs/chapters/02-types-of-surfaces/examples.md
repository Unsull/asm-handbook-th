# กรณีศึกษา — หลาย Attack Surfaces ในธุรกิจเดียว

## Case A: โรงเรียนใช้ Web + SaaS + Cloud Storage

โรงเรียนสมมติมีเว็บไซต์ลงทะเบียนเรียน ฐานข้อมูลนักเรียนบน Cloud และ SaaS สำหรับส่งเอกสารให้ผู้ปกครอง

| Asset/Flow | Surface Type | Potential Weakness | Evidence ที่ต้องตรวจ |
|---|---|---|---|
| Registration Portal | Web/API | Broken Object Authorization | Source/Negative Tests |
| Cloud Database | Cloud/Network | Access Policy กว้างเกิน | Cloud Resource Policy |
| File-sharing SaaS | SaaS/Data | Public Shared Links | Sharing Audit |
| Staff SSO | Identity | Orphaned User Account | Identity Lifecycle |
| Build Pipeline | Supply Chain | Overprivileged Deploy Token | Workflow Permissions |

### ผลการวิเคราะห์

การตรวจ Port ของ Web Server อย่างเดียวจะไม่เห็น Public Shared Links ของ SaaS หรือ OAuth Token ที่ให้สิทธิ์เกิน จึงควรนำ SaaS Inventory, Cloud Policy และ Identity Data มารวมกับ Network Discovery

## Case B: ร้านกาแฟมี Smart POS และ IoT Cameras

ธุรกิจสมมติติดตั้ง POS Tablet, Wi-Fi Access Point และ IP Cameras ที่สาขาย่อย

ประเด็นที่ควรตรวจไม่ได้มีเฉพาะ Router Firewall แต่รวม Firmware Support, Device Owner, Secure Updates, Local Admin Credentials, Device Segmentation และการเพิกถอนสิทธิ์เมื่ออุปกรณ์สูญหาย

### Design Review

ถ้า POS และ Guest Wi-Fi ใช้ Network เดียวกัน ให้ตรวจ Segmentation/Access Policy ไม่ควรสรุปว่าเป็นช่องโหว่จากชื่อ SSID เพียงอย่างเดียว ต้องดู Effective Connectivity

หากกล้องส่งวิดีโอไป Cloud ให้ตรวจผู้ให้บริการ SaaS, Data Retention, Identity Permissions และ Third-party Access ด้วย

## Case C: AI Chatbot สำหรับ Helpdesk

ร้านค้าเพิ่ม Chatbot เพื่อให้ตอบคำถามจาก Knowledge Base หาก Chatbot สามารถเรียก API คืนเงินได้ด้วย จะเกิด Surface ใหม่คือ **Agent Tool Permissions** และ **Retrieved Documents** ที่อาจมีข้อความไม่น่าเชื่อถือ

ควรแยก Read-only Knowledge Search ออกจาก Refund Tool, ใช้ Server-side Authorization และบันทึก Actions ที่ต้อง Approval ก่อนดำเนินการ

## แบบฝึกเปรียบเทียบ

เลือกบริการหนึ่งในองค์กรสมมติ แล้วเติม 4 ช่อง: `logical asset / identity surface / data surface / supply-chain surface` จะเห็นว่า Asset หนึ่งไม่ได้อยู่ใน Surface Type เดียวเสมอไป
