# กรณีศึกษา — Crown Jewels ในธุรกิจทั่วไป

## Case A: E-commerce มี Checkout API กับ Marketing Dashboard

ทีม Security พบสอง Assets: Checkout API ไม่มี CVE ที่ตรวจยืนยันได้ แต่ถ้าหยุดใช้งานจะรับคำสั่งซื้อไม่ได้ ส่วน Marketing Dashboard มี Library Version เก่าและ Scanner ให้ Severity High

**ข้อสรุปที่ถูกต้อง:** Checkout API อาจมี Business Criticality สูง แต่ไม่ได้แปลว่ามี High Current Risk ขณะที่ Dashboard ต้องตรวจ Exploitability, Reachability และข้อมูลที่เข้าถึงได้ก่อนจัดลำดับ Findings

### Business Function Mapping

```text
Receive Order
  → Checkout API
      → Orders DB
      → Payment Integration
      → Inventory Worker
```

หาก Orders DB หยุด ทั้ง Checkout และ Fulfillment อาจได้รับผลกระทบ ต้องตรวจ Redundancy และ Workarounds ก่อนสรุป Total Outage

## Case B: Crown Jewels ของธุรกิจจองโรงแรม

Candidate Assets อาจเป็น Reservation Records, Payment Credential/Refund Approval Process และ Front Desk Check-in Capability

| Candidate | ผลกระทบหากเสียหาย | สิ่งที่ต้องยืนยัน |
|---|---|---|
| Reservation Records | ข้อมูลการจองผิด/สูญหาย | Owner, Backup/Restore |
| Refund Privileges | Fraud / Financial Loss | Approval, Separation of Duties |
| Check-in Capability | ให้บริการลูกค้าไม่ได้ | Offline Procedure, RTO |

การจัดเป็น Crown Jewel ต้องมี Business/Risk Owner ลงนาม ไม่ใช่ให้ Security Tool ประกาศอัตโนมัติ

## Case C: Dependency-driven Priority

DNS Provider อาจไม่เก็บข้อมูลลูกค้า แต่ถ้าล่มทำให้เว็บไซต์ทั้งหมดเข้าถึงไม่ได้ จึงมี Operational Criticality สูง ในทางกลับกันระบบทดสอบที่ใช้ Domain ทดสอบและแยก Credentials จริงอาจมี Criticality ต่ำกว่า

## แบบฝึก

จัด Tier 0–3 ให้ Assets ห้ารายการ ระบุ Business Justification และถามตัวเองว่ามี Tier 3 Asset ใดถือ Credential ที่ไปถึง Tier 0 หรือไม่ หากมี ต้องทบทวน Trust/Access Relationship เพิ่ม
