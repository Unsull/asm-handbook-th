# กรณีศึกษา — ASM ใช้แก้ปัญหาอะไร?

## Case A: ร้านค้าออนไลน์เพิ่มหน้า Admin โดยไม่มี Asset Owner

บริษัทสมมติเปิดหน้า `admin.shop.example` ให้ทีมงานติดตามคำสั่งซื้อ แต่ไม่ได้เพิ่มชื่อ Domain/Service ใน Inventory ทีมดูแล Network คิดว่ามีเพียง `www.shop.example` และ `api.shop.example` ภายใน Scope

### วิเคราะห์เป็นลำดับ

1. **Observation ที่ต้องเก็บ:** DNS/Deployment Configuration แสดงรายการ Admin Service จริงหรือไม่
2. **Asset:** Admin Web, Session Store, Application Role, Orders API
3. **Entry Point:** Web Login และ API สำหรับเปลี่ยนข้อมูลคำสั่งซื้อ
4. **Potential Threat:** Credential Abuse, Privilege Escalation, Information Disclosure
5. **Business Impact:** ข้อมูลลูกค้ารั่วไหลหรือถูกเปลี่ยนสถานะการจัดส่งผิด
6. **Controls to Verify:** MFA, IP Restrictions ตามบริบท, Authorization, Logging, Session Invalidation

ถ้ารายงานเพียงว่า “พบ Subdomain เพิ่มหนึ่งรายการ” จะยังไม่ตอบว่าปัญหาคืออะไร ต้องเชื่อม Domain กับ Business Function และ Owner ก่อน

### ตัวอย่าง Finding ที่ดี

> พบ Admin Service ใน Deployment Configuration แต่ยังไม่มีรายการ Owner/Authorization Baseline ใน Asset Inventory; แนะนำให้ทีม Operations ตรวจยืนยัน Usage, Environment และสิทธิ์ก่อนทำ External Exposure Assessment

รายงานนี้ไม่ได้สรุปว่า Admin Service ไม่ปลอดภัยโดยไม่มีหลักฐาน

## Case B: ระบบจองโรงแรมใช้ API Token สิทธิ์สูงในงานอ่านข้อมูล

บริการส่ง Confirmation Email มี Token ที่อ่าน/แก้ Reservation Records ได้ทั้งหมด ทั้งที่ฟังก์ชันที่ใช้จริงอ่านได้เพียงข้อมูลการจองบางส่วน

- **Attack Surface:** Machine Identity + API Permissions
- **Threat Scenario:** หาก Token รั่วจาก Application Log ผู้โจมตีอาจแก้ Reservation Data ได้
- **Reduce Surface:** ออก Token/Role ใหม่ที่ Read-only และจำกัด Scope
- **Verify:** Confirmation Emails ยังทำงาน ขณะที่ Token เดิมถูกเพิกถอน และ Modify Request ถูกปฏิเสธ

### เปรียบเทียบสองกรณี

กรณี A เป็น **Visibility Gap** ส่วนกรณี B เป็น **Privilege Surface** ทั้งสองอาจเกิดแม้ไม่มี Known Software CVE

## คำถามฝึกคิด

- หาก Admin Service อยู่หลัง VPN จะไม่มี Attack Surface เลยหรือไม่? (ไม่: ยังมี Identity, VPN และ Internal Access Paths)
- ถ้าปิด Service A แต่เพิ่ม Token ที่มีสิทธิ์มากกว่าเดิม จะสรุปว่าระบบเสี่ยงน้อยลงได้หรือไม่? (ยังไม่ได้ ต้องประเมิน Trust/Impact)

[ไป Workshop →](/chapters/01-foundations/workshop)
