# กรณีศึกษา — Future Attack Surface ของธุรกิจทั่วไป

## Case A: AI Shopping Assistant ที่เรียก Refund Tool ได้

ร้านค้าเพิ่ม AI Assistant เพื่อค้น FAQ และอัปเดตสถานะการจัดส่ง ทีมเสนอให้ Assistant เรียก Refund API โดยตรงเพื่อให้สะดวกขึ้น

### Surface ใหม่

- Model API/Prompts ที่รับข้อมูลจากลูกค้า
- Retrieval Documents ที่อาจมีข้อความไม่น่าเชื่อถือ
- Tool Credentials ที่เชื่อม Payment Operations
- Logs ที่อาจเก็บข้อมูลส่วนบุคคล

**Design Choice:** เริ่มด้วย Read-only Customer Support, จำกัดข้อมูลที่ Assistant อ่าน และให้ Privileged Refund Action ผ่าน Server-side Authorization + Human Approval แยกจากการสรุปข้อความ

## Case B: Smart Kiosk แบบ Offline

ร้านค้ามี Kiosk รับ Orders ระหว่าง Internet Down แล้ว Sync กลับ Cloud ภายหลัง อุปกรณ์อาจถูกขโมยหรือ Local Queue ถูกแก้ไข

ควรใช้ Device Enrollment, Protected Key Storage, Authenticated Upload, Monotonic/Unique Order IDs, Idempotency และ Integrity Validation ที่ Server อย่าถือว่า Hash ตรงกับ Manifest แล้วพิสูจน์ Device Identity หรือเวลาได้

### States ที่ควรแยก

```text
Captured on device → Pending Sync → Server Received
                                 → Integrity Verified
                                 → Business Accepted
```

การ Sync สำเร็จไม่ได้หมายความว่า Payment/Order Fulfillment สำเร็จตามขั้นตอนธุรกิจ

## Case C: วางแผน Post-Quantum Migration

บริษัทเก็บเอกสารที่ต้องตรวจย้อนหลัง 15 ปี จึงทำ Cryptographic Inventory ว่าระบบใช้ TLS/Certificate/Signing Key อะไรบ้าง ใครเป็น Owner และ Logs สามารถ Verify Historical Signatures ได้อย่างไร

สำหรับ RSA/ECC ต้องพิจารณา Post-Quantum Migration ตามมาตรฐานและ Vendor Support ขณะที่ SHA-256 มี Quantum Security Considerations คนละรูปแบบ ไม่ควรสั่งเปลี่ยน Algorithms ทั้งหมดโดยไม่วิเคราะห์ Protocol Compatibility

## แบบฝึก

เลือก Scenario หนึ่ง แล้วเขียน `New Asset / New Trust Boundary / Potential Threat / Existing Control / Verification Method / Owner` ให้ครบ หากมี AI แนะนำให้เปลี่ยน Production Credentials ต้องระบุ Approval Boundary ก่อนทุกครั้ง
