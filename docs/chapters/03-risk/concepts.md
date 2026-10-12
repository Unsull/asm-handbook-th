# แนวคิดเชิงลึก — How Attack Surface Relates to Risk

## 1. Attack Surface ≠ Risk

การเปิดรับการเชื่อมต่อ (Exposure) เป็นเพียงหนึ่งปัจจัยของความเสี่ยง Risk Assessment ต้องระบุ **สถานการณ์** ที่เป็นรูปธรรม: “ผู้ใดอาจทำอะไรต่อสินทรัพย์ใด ผ่านเงื่อนไขอะไร และส่งผลต่อเป้าหมายธุรกิจอย่างไร”

ตัวอย่างร้านค้าออนไลน์: `GET /orders/{id}` เป็น Entry Point ส่วน Risk Scenario คือผู้ใช้ที่ Login แล้วอาจเข้าถึงออเดอร์ของคนอื่น เพราะระบบไม่ได้ตรวจ Object Ownership ผลกระทบคือข้อมูลส่วนบุคคลรั่วไหล **ห้าม** เรียกว่า Vulnerability ที่ยืนยันแล้วก่อนมี Test Evidence

## 2. วัด Risk อย่างไร?

แบบจำลองสอนที่ใช้บ่อยคือ `Likelihood × Impact` โดยให้แต่ละมิติ 1–5 แต่ต้องระวังว่า 1–5 เป็น Rating ที่ผู้ประเมินออกแบบ ไม่ใช่ Probability ต่อปี และการคูณคะแนน Ordinal ไม่ใช่สูตรทางฟิสิกส์ที่ให้ค่าจริง

| Likelihood | ความหมายเชิงนโยบายตัวอย่าง |
|---|---|
| 1 | แทบไม่พบเงื่อนไข เหตุการณ์ต้องอาศัยหลายปัจจัย |
| 2 | เกิดได้ยากภายใต้ Controls ปัจจุบัน |
| 3 | มีเส้นทางที่เป็นไปได้ ต้องติดตาม |
| 4 | มี Exposure/Threat Conditions สนับสนุน |
| 5 | มีหลักฐานโจมตีหรือเงื่อนไขเร่งด่วน ต้อง Triage |

เกณฑ์ Impact ควรพิจารณา Operational Downtime, Financial Loss, Confidentiality, Legal/Compliance และ Trust/Brand ไม่ใช่ใช้ความรู้สึกโดยไม่มีนิยาม แต่ละองค์กรควรอนุมัติ Risk Appetite และเกณฑ์ Escalation ของตัวเอง

## 3. Qualitative Risk Assessment

การประเมินเชิงคุณภาพใช้คำอธิบายและระดับ Low/Medium/High มีประโยชน์เมื่อข้อมูลตัวเลขยังไม่ครบ ประหยัดเวลา และสื่อสารกับเจ้าของธุรกิจได้ง่ายกว่าในระยะแรก

**ข้อจำกัด:** ผู้ประเมินสองคนอาจให้ระดับต่างกัน หากไม่มี Criteria, Review Process และ Evidence Log การเปรียบเทียบข้ามทีมจะไม่เสถียร

ตัวอย่าง Scenario: “ผู้มีสิทธิ์หลังร้านถูก Phishing แล้วเปลี่ยนบัญชีรับเงินคืนสินค้า” อาจจัด High Impact เพราะเกี่ยวข้องกับการเงิน แต่ Likelihood ต้องตรวจ MFA, Workflow Approval และ Login Telemetry จริง

## 4. Quantitative Risk Assessment

เมื่อมีข้อมูลที่เชื่อถือได้ สามารถประมาณต้นทุนโดยใช้แนวคิด:

\[
SLE = AV \times EF,\qquad ALE = SLE \times ARO
\]

- **AV** Asset Value หรือมูลค่าที่ใช้ในโมเดล
- **EF** Exposure Factor สัดส่วนความเสียหายต่อเหตุการณ์
- **SLE** Single Loss Expectancy
- **ARO** Annualized Rate of Occurrence (ความถี่โดยประมาณต่อปี)
- **ALE** Expected Annualized Loss

ตัวอย่าง: ร้านค้าออนไลน์คาดว่าต้นทุนจาก Order Service Outage แบบหนึ่งคือ 200,000 บาทต่อเหตุการณ์ และคาดว่าต้องเผชิญ 0.3 เหตุการณ์ต่อปี ดังนั้น `ALE ≈ 60,000 บาท/ปี` **ภายใต้สมมติฐานนี้**

ARO ไม่จำเป็นต้องเป็น Probability เสมอไป: ถ้าคาดว่าเกิด 2 ครั้ง/ปี ก็ใช้ 2 ได้ ความแม่นยำของ ALE ขึ้นกับฐานข้อมูลและความไม่แน่นอนของ AV/EF/ARO หากมีช่วงค่ากว้าง ควรทำ Scenario/Sensitivity Analysis แทนการรายงานเป็นตัวเลขแม่นยำหลอก ๆ

## 5. เลือก Qualitative, Quantitative หรือ Hybrid?

| เงื่อนไข | แนวทางที่เหมาะสม |
|---|---|
| มีข้อมูลผลกระทบน้อย เพิ่งเริ่ม Inventory | Qualitative + Evidence Gaps |
| มี Incident/Loss Records และต้นทุนที่ใช้ได้ | Quantitative พร้อมช่วงความไม่แน่นอน |
| ต้องจัดลำดับเร็ว แต่บางเรื่องมีค่าทางการเงิน | Hybrid |

สำหรับร้านค้าออนไลน์ ให้ทีม Operations ประเมิน Operational Impact เชิงคุณภาพก่อน แล้วใช้ข้อมูล Transaction Loss และ Recovery Cost เมื่อมีพร้อม พึงระวังการนับ Cost ซ้ำระหว่าง Revenue Loss กับ Compensation

## 6. Inherent Risk และ Residual Risk

**Inherent Risk** คือการพิจารณาความเสี่ยงโดยยังไม่รวม Controls ที่ใช้จริงในกรอบการประเมินนั้น ส่วน **Residual Risk** คือความเสี่ยงที่เหลือหลัง Controls ถูกนำมาประเมิน ไม่ใช่ `Inherent − CVSS` หรือผลต่างของคะแนนใด ๆ โดยอัตโนมัติ

ตัวอย่าง: API ของร้านค้าอยู่หลัง Authentication แต่ถ้าไม่มี Object-level Authorization, Authentication เพียงอย่างเดียวอาจไม่ได้ลด Risk Scenario ของ BOLA มากนัก หลังเพิ่ม Authorization Checks และ Negative Tests แล้วจึงประเมิน Residual Risk ใหม่ด้วยหลักฐาน

## 7. Frameworks และบริบทการทำงาน

**NIST SP 800-30** ให้แนวทาง Risk Assessment, **NIST CSF 2.0** ช่วยเชื่อม Governance/Identification/Protection/Detection/Response/Recovery, **ISO 31000 / ISO 27005** สนับสนุนการบริหารความเสี่ยง, **COSO ERM** มองมิติองค์กร, **OCTAVE** เน้นกระบวนการวิเคราะห์โดยองค์กร และ **ITIL** มองการบริหารบริการที่เกี่ยวข้อง

ไม่มีเหตุผลให้เริ่มจากการนำทุก Framework มาใช้พร้อมกัน เลือกให้สอดคล้องกับ Business Owner, Scope, Regulations และวุฒิภาวะกระบวนการ

## 8. Communicating Risk to Business Teams

ผู้บริหารต้องการรู้ **ผลกระทบต่อธุรกิจ, ทางเลือก, ต้นทุน, ผู้รับผิดชอบ และวันตัดสินใจ** มากกว่ารายชื่อ Ports หรือ Payloads อย่างเดียว

เปลี่ยนรายงานจาก “CVSS 9.8 ที่ API” เป็น “มีช่องโหว่ที่ยืนยันแล้วใน API Checkout ซึ่งอาจเปิดเผยข้อมูลลูกค้า; แนะนำจำกัดการเข้าถึงทันทีและแก้โดยทีม API ภายใน SLA ที่อนุมัติ พร้อม Security Regression Tests”

## 9. Risk Register ที่ตรวจสอบย้อนกลับได้

| Field | เหตุผล |
|---|---|
| Risk ID + Scenario | ลดความกำกวม |
| Asset/Business Function | ผูกกับสิ่งที่ธุรกิจให้คุณค่า |
| Evidence & Confidence | แยก Observation กับ Assumption |
| Likelihood/Impact | จัดลำดับตามเกณฑ์ |
| Existing Controls | ป้องกันการประเมินเกินจริง |
| Risk/Action Owner | มีคนรับผิดชอบ |
| Decision/Review Date | ป้องกันการค้างแบบไม่มีใครตัดสิน |

**อ่านต่อ:** [NIST SP 800-30](https://csrc.nist.gov/pubs/sp/800/30/r1/final), [FIRST CVSS](https://www.first.org/cvss/)
