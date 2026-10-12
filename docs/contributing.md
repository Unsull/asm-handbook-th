# วิธีร่วมปรับปรุงคู่มือ

ยินดีต้อนรับ Pull Requests ที่ทำให้เนื้อหาเข้าใจง่าย ถูกต้อง และทดลองทำตามได้อย่างปลอดภัย

## รูปแบบเนื้อหาที่ต้องการ

1. อธิบายคำศัพท์แรกพบทั้งภาษาไทยและ Technical English
2. เรียงลำดับ **แนวคิด → กลไก → เหตุผล → ตัวอย่าง → วิธีตรวจสอบ → ข้อจำกัด**
3. ทุกกรณีสมมติต้องระบุให้ชัดว่าไม่ใช่ข้อค้นพบจริง
4. Workshop ต้องระบุ Prerequisites, Scope, Steps, Expected Results, Troubleshooting และ Cleanup
5. อ้างอิง Primary Sources (NIST, OWASP, Vendor Docs) พร้อม URL
6. ไม่คัดลอกข้อความจากหนังสือลิขสิทธิ์หรือเว็บไซต์อื่นเป็นจำนวนมาก
7. ห้าม Commit Real Credentials, Personal Data หรือ Confidential Work Data

รัน `python scripts/validate_content.py` และ `npm run docs:build` ก่อนส่ง Pull Request
