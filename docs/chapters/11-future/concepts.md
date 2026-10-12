# แนวคิดเชิงลึก — The Future of ASM

## 1. Emerging Trends

เทคโนโลยีใหม่ไม่ได้เพิ่มแค่จำนวน Assets แต่เปลี่ยนความเร็วในการสร้างระบบและรูปแบบ Trust Relationships: AI Agents มีสิทธิ์เรียก Tools, Edge Devices ทำงาน Offline, Cryptographic Protocols ต้องรองรับการย้ายมาตรฐาน และ Cloud Workloads ถูกสร้าง/ลบเป็นวินาที

## 2. AI และ Machine Learning ใน ASM

### AI-assisted Discovery และ Correlation

Model ช่วยเสนอว่า Container, Process, Service Entry และ Repo Record อาจเป็น Logical Asset เดียวกัน แต่อาศัยการตรวจ Stable ID/Deployment Evidence ก่อน Merge Records เพราะการรวมผิดทำให้ Owner และ Risk Scope คลาดเคลื่อน

### Anomaly Detection

เทียบ **Rule-based Detection** เช่น “Denied Requests > 20” กับ **Unsupervised ML** เช่น IsolationForest ที่เรียน Distribution ของ Metrics ทั้งสองควรใช้ร่วมกันเพราะ ML อาจไม่จับเหตุการณ์สำคัญที่อยู่นอก Feature Set และอาจแจ้ง False Positive เมื่อเกิด Maintenance ที่ถูกต้อง

| วิธี | จุดแข็ง | จุดอ่อน |
|---|---|---|
| Deterministic Rule | อธิบายง่าย เหมาะ Policy Violations | บางรูปแบบไม่ผ่าน Threshold |
| Statistical/ML | หา Pattern หลายมิติ | ต้องดู Drift, Data Quality, Labels |
| LLM Assistant | สรุปเหตุการณ์/Runbook | Hallucination, Prompt Injection, Data Exposure |

### AI ก็เป็น Attack Surface ใหม่

รวม Model APIs, Retrieval Sources, Prompt Inputs, Tool Credentials, Agent Actions และ Logs ออกแบบ Read-only เริ่มต้น, Least Privilege, Tool-side Authorization, Sanitization และ Human Approval สำหรับการเปลี่ยน Critical Systems

## 3. Quantum Computing และ Cryptographic Agility

Quantum Computing มีผลต่อ Cryptographic Algorithms ไม่เท่ากัน **Shor's Algorithm** เป็นภัยสำคัญต่อ RSA/ECC เมื่อมี Fault-tolerant Quantum Computer ที่ใหญ่เพียงพอ ส่วน **Grover's Algorithm** เกี่ยวข้องกับ Quantum Search ซึ่งมีผลต่อระดับความปลอดภัยของ Symmetric/Hash Functions แต่ไม่ใช่การทำลาย SHA-256 และ ECDSA ในลักษณะเดียวกัน

NIST เผยแพร่ FIPS 203 **ML-KEM**, FIPS 204 **ML-DSA** และ FIPS 205 **SLH-DSA** สำหรับการเตรียม Post-Quantum Cryptography การเลือก Algorithms ต้องสัมพันธ์กับ Protocol/Implementation และ Migration Requirements ไม่ใช่แทน String ใน Config แล้วเสร็จ

**Crypto Agility** คือความสามารถเปลี่ยน Cryptographic Suite พร้อมรักษา Interoperability, Key Lifecycle และ Historical Verification มีขั้นตอน:

1. Inventory Algorithms, Certificates, Keys, Libraries และ Owners
2. Map Data Retention/Long-term Confidentiality และ Signature Verification Needs
3. ทดสอบ Supported Protocols กับ Crypto Providers
4. วางแผน Hybrid/Migration ตามคำแนะนำมาตรฐานที่เกี่ยวข้อง
5. บันทึก Evidence/Versioning และ Rollback Plan

## 4. Edge Computing Challenges

อุปกรณ์ปลายทาง เช่น Smart Shop Camera, Kiosk, Mobile Scanner อาจมี Physical Exposure, Firmware, Local Keys, Offline Queue และ Synchronization Risks การตรวจ Hash ของไฟล์ที่อัปโหลดให้ผลด้าน Byte Integrity แต่ **ไม่พิสูจน์ Device Identity หรือความน่าเชื่อถือของเวลา** หาก Manifest และ Hash ถูกแก้พร้อมกัน

ออกแบบ `device_id`, `capture_id`, authenticated manifest, protected storage, replay detection, revocation และสถานะ `captured/pending/uploaded/verified` แยกกัน สำหรับอุปกรณ์ Offline ต้องมี Durable Queue และนโยบาย Trusted Timestamps

## 5. Evolving Cybersecurity Challenges

- **Ephemeral Assets:** Scanner รอบวันอาจพลาด Cloud Instances ที่อายุไม่กี่นาที
- **Identity as Surface:** API Tokens/CI Runners มีสิทธิ์กว้างแม้ไม่มี Public Port
- **Software Supply Chain:** Dependencies, Build Pipeline, Registry และ Artifact Trust
- **Data Sovereignty:** Privacy/Retention แตกต่างตาม Region/Service
- **AI-generated Noise:** Findings มากแต่ไม่ผ่าน Validation อาจทำให้ทีมหมดแรงตรวจ
- **Long-lived Evidence:** Historical Trust อาจต้องตรวจ Cryptographic Provenance ข้ามหลายเทคโนโลยี

## 6. Staying Ahead in ASM Practices

แนวทางที่คงคุณค่าในระยะยาวคือ Continuous Asset Intelligence, Policy as Code, Validated Controls, Risk-based Automation และ Measurable Outcomes ไม่ใช่ซื้อเครื่องมือใหม่ทุกครั้งที่มีคำศัพท์ใหม่

ตัวอย่าง Metric ที่เหมาะ: Mean Time to Discover, Unknown Owner Rate, Exposure Duration, Verified Closure Rate, Crown Jewel Control Coverage และ Algorithm Inventory Coverage ทั้งหมดต้องมี Definition, Scope และ Data Source ชัดเจน

## 7. Continuous Learning and Skill Development

จัดแผนฝึก Networking, Linux/Windows, Cloud APIs, Threat Modeling, Risk Communication, Incident Response, AI/ML Evaluation และ Cryptography เริ่มจาก Lab Synthetic ก่อนใช้ระบบจริง ฝึกเขียน Finding แยก Observation/Evidence/Risk Hypothesis/Remediation ชัดเจน

## 8. Stay Hungry, Never Give Up

หัวใจของ ASM คือ *ยอมรับว่าความรู้และระบบเปลี่ยนได้เสมอ* ไม่ใช้เครื่องมือใดเป็นหลักฐานแทนการตรวจบริบทจริง ตั้งคำถามกับ Assumptions วัดผล Controls และนำ Lessons Learned กลับมาแก้ Engineering Process

**อ่านต่อ:** [NIST PQC](https://csrc.nist.gov/projects/post-quantum-cryptography), [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework), [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/)
