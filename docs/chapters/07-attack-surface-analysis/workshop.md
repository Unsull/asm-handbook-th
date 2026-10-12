# Workshop 7 — ทำ Threat Model ให้ Checkout API

**เวลาแนะนำ:** 60–90 นาที · **ระดับ:** Intermediate · **เครื่องมือ:** [OWASP Threat Dragon](https://owasp.org/www-project-threat-dragon/) หรือกระดาษ/diagrams.net

## เป้าหมาย

สร้าง Data Flow Diagram (DFD), Trust Boundaries, STRIDE Threat Register และ Security Test Cases ที่ตรวจสอบได้โดยไม่แตะระบบจริง

## ขั้นตอนที่ 1 — กำหนด Scope

ระบบ Example Shop จำลองมี Customer Browser, HTTPS Gateway, Checkout API, Orders DB, Payment Provider และ Back-office Admin

```text
Customer Browser
   | HTTPS (Boundary: External → Application)
   v
[HTTPS Gateway] → [Checkout API] → [Orders DB]
                          |
                          v
                 [Payment Provider]
Admin → [Back-office] → [Checkout API]
```

## ขั้นตอนที่ 2 — เปิด Threat Dragon

สร้าง Model ชื่อ `Example Shop Checkout` แล้วเพิ่ม Actor, Processes, Data Store, Data Flows และ Trust Boundaries อย่างน้อย 3 จุด

หากไม่มี Threat Dragon สามารถใช้ Markdown/กระดาษได้ การเรียนรู้ Threat Modeling ไม่ขึ้นกับ Product ใด Product หนึ่ง

## ขั้นตอนที่ 3 — ทำ STRIDE Walkthrough

| Category | Question |
|---|---|
| Spoofing | มีใครสวมรอย Session หรือ Service Identity ได้หรือไม่ |
| Tampering | ใครเปลี่ยน Order Price/Quantity ได้ และ Server ตรวจซ้ำหรือไม่ |
| Repudiation | Audit Trail ระบุผู้ Refund ได้เพียงใด |
| Information Disclosure | ลูกค้า A อ่าน Order B ได้หรือไม่ |
| Denial of Service | ถ้า Payment Provider ไม่ตอบ ระบบอยู่ในสถานะอะไร |
| Elevation of Privilege | User/Worker เรียก Admin/Refund Operations ได้หรือไม่ |

ใช้ไฟล์ `labs/07-threat-model/threat_register.csv` เป็น Template แล้วเพิ่มคอลัมน์ `evidence_needed`, `likelihood`, `impact`, `owner`, `test_case`

## ขั้นตอนที่ 4 — ทำ Negative Test Design

สำหรับ TM-01 เขียนผลที่คาดหวังว่า:

```text
Given Order B belongs to bob
When alice (authenticated) requests Order B
Then API must deny access and must not return B's private data
```

ถ้ายังไม่ได้รันทดสอบ ให้ Status เป็น `not_executed` ไม่ใช่ `passed`

## ขั้นตอนที่ 5 — Risk Prioritization

จับคู่ Threat Register กับ Business Impact ของ Customer Privacy/Payments แล้วถามว่ามี Preconditions ใดทำให้ Attack Path ไม่สำเร็จ อย่าใช้ STRIDE Category เพื่อกำหนด Severity อัตโนมัติ

## Acceptance Criteria

- Diagram มี Trust Boundaries ไม่น้อยกว่า 3 จุด
- Threats มี Asset, Scenario และ Control
- Negative Tests มี Expected Result
- แยก Hypothesis/Confirmed Evidence ชัดเจน

## Cleanup

ไม่มี Test Traffic จริง ส่งออก Model Diagram และ CSV เก็บในโฟลเดอร์ Lab ของคุณได้

[Quiz →](/chapters/07-attack-surface-analysis/quiz)
