# กรณีศึกษา — Threat Model ของระบบ Checkout

## Case A: ลูกค้าค้น Order ID ของผู้อื่น

สมมติ Checkout Application มี `GET /orders/{id}` และผู้ใช้ A ส่ง ID ของ Order ที่เป็นของผู้ใช้ B ด้วย Account ที่มีสิทธิ์ Login

### DFD ที่ต้องวาด

```text
Customer Browser -- HTTPS --> Public Gateway
                                  |
                              Orders API
                                  |
                         Authorization Decision
                                  |
                              Orders DB
```

**Trust Boundary 1:** Browser → Backend ต้องไม่เชื่อ `user_id` จาก Request Body เป็น Identity ที่รับรองแล้ว

**Trust Boundary 2:** API → Database หาก DB Role อ่านทุก Record ได้ ต้องให้ Application ตรวจ Object Ownership อย่างถูกต้อง และมี Tests ครอบคลุม

### STRIDE ที่เกี่ยวข้อง

- **Information Disclosure:** เข้าถึงข้อมูล Order ที่ไม่ได้รับอนุญาต
- **Spoofing:** ใช้ Session ที่ไม่ใช่ของตน
- **Repudiation:** ไม่มี Audit Trail ที่โยงการเข้าถึงกับ Authenticated Session

อย่าเรียกทั้งสามว่า Vulnerabilities ที่เกิดขึ้นจริงจนกว่าจะมี Code/Runtime Evidence แต่ใช้เป็น Threat Hypotheses สำหรับ Design Review

## Case B: Service-to-Service Token ไปถึง Refund API

Order Worker มี Token ที่ควรทำงานอ่าน Status แต่ IAM Policy ให้เรียก Refund API ได้ด้วย

```text
Order Worker → Service Token → Refund API → Payment Provider
```

กรณีนี้ไม่มี Public Port เพิ่ม แต่ Trust Graph/Permission Surface เปลี่ยน ทำให้ต้องตรวจ Least Privilege และ Business Approval

### ตัวอย่าง Threat Register

| ID | Threat | Control | Validation |
|---|---|---|---|
| TM-01 | Unauthorized Order Read | Object-level Authorization | Test User A vs Order B |
| TM-02 | Worker Calls Refund | Scope-limited Machine Token | Forbidden Operation Returns 403 |
| TM-03 | Checkout DoS | Rate Controls/Scaling | Authorized Load Test in Lab |

## แบบฝึก

ให้วาด Threat Dragon Diagram และระบุ Data Flows, Trust Boundaries อย่างน้อยสองจุด จากนั้นสร้าง Security Test Cases อย่างละหนึ่งรายการสำหรับ Spoofing, Tampering และ Information Disclosure
