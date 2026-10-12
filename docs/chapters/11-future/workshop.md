# Workshop 11 — Future ASM: ML, Crypto Inventory และ Edge Integrity

**เวลาแนะนำ:** 75 นาที · **ระดับ:** Intermediate · **ข้อมูล:** Synthetic E-commerce และ Kiosk Device

## ส่วน A — Machine Learning Anomaly Detection

### 1. เตรียม Environment

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install numpy scikit-learn
```

ควรรันจาก Project Root และใช้ Virtual Environment แยกจาก Python Projects อื่น หากใช้ Linux/macOS ให้ใช้ `.venv/bin/python`

### 2. รัน Lab

```powershell
.\.venv\Scripts\python.exe labs/11-future/anomaly.py
```

Script ใช้ IsolationForest เรียน Synthetic Normal Baseline (Denied Requests และ Error Rate) แล้ว Flag Case ที่ควร Review ผลขึ้นกับ Algorithm/Versions ไม่ใช่การยืนยัน Cyberattack

### 3. วิเคราะห์ False Positive/Negative

ลองเปลี่ยนตัวอย่าง `denied-spike` หรือ `rpc-spike` แล้วดูว่า Model แจ้งเตือนหรือไม่ คิดว่าหากพึ่ง ML อย่างเดียว จะพลาด Port ใหม่ที่ไม่อยู่ใน Features ได้อย่างไร?

---

## ส่วน B — Cryptographic Inventory สำหรับ PQC Readiness

### 1. อ่าน Inventory

เปิด `labs/11-future/crypto_inventory.csv` จะเห็นรายการ TLS, Document Signature และ Content Hash ซึ่งมี Verification Status ต่างกัน

### 2. เพิ่ม Columns

ใส่ `library_version`, `algorithm`, `key_owner`, `key_storage_reference`, `rotation_policy`, `retention`, `last_verified` **ห้ามเก็บ Private Keys จริงใน CSV**

### 3. สร้าง Migration Notes

| Primitive | ความเสี่ยงที่ต้องติดตาม | สิ่งที่ต้องทดสอบ |
|---|---|---|
| RSA/ECDSA Signing | Quantum-capable Cryptanalysis ในอนาคต | Protocol & Validator Compatibility |
| TLS Key Exchange | Long-term Confidentiality | Supported Provider/Cipher Suites |
| SHA-256 | Quantum Search Considerations | Long-term Hash Assurance/Versioning |

Workshop นี้เป็น Inventory/Planning ไม่ใช่การติดตั้งหรือทดสอบ Post-Quantum Algorithms โดยตรง

---

## ส่วน C — Edge Manifest Authentication และ Replay

### 1. รัน Standard-library Lab

```powershell
py labs/11-future/edge_integrity.py
```

Expected Output:

```text
INTEGRITY_MISMATCH
ACCEPTED_FOR_FURTHER_VALIDATION
REPLAY
```

### 2. อ่านสิ่งที่ Code ทำจริง

- HMAC ตรวจว่า Manifest ถูกสร้างด้วย Lab Shared Secret เดียวกัน
- SHA-256 ตรวจว่าข้อมูลตรงกับ Digest ใน Manifest
- In-memory Set ตรวจว่า `capture_id` ซ้ำในการรันครั้งเดียวหรือไม่

**ข้อจำกัด:** ไม่ใช่ Device Attestation, ไม่ได้พิสูจน์เวลา Capture, ไม่มี Durable Replay Database และไม่ควรนำ Shared Secret ที่ Hardcode ไปใช้จริง

### 3. ทดสอบ Lab

```powershell
py -m unittest discover -s labs/11-future -p 'test_*.py' -v
```

### 4. ออกแบบ Control ก่อน Production

เพิ่ม Secure Device Enrollment, Hardware-protected Credentials, Authenticated Transport, Durable Nonce/ID Registry, Trusted Time Handling, Key Revocation และ Offline Queue Recovery

---

## ส่วน D — Final Assessment

เขียน Future Security Roadmap 3 ระยะ โดยกำหนด `owner`, `risk`, `evidence_needed`, `success_metric` สำหรับ AI Assistant, Crypto Agility และ Edge Devices และระบุเงื่อนไขที่ห้าม Automation ทำ Privileged Changes โดยไม่มี Human Approval

## Cleanup

หากสร้าง Virtual Environment เฉพาะ Lab สามารถลบ `.venv` หลังปิด Terminal และเก็บเพียงไฟล์ Source/Synthetic Data

[ทำแบบทดสอบปิดท้าย →](/chapters/11-future/quiz)
