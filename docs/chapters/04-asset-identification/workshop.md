# Workshop 4 — สร้าง Asset Inventory ที่ตรวจคุณภาพได้

**เวลาแนะนำ:** 35 นาที · **ระดับ:** Beginner · **ข้อมูล:** โรงแรมสมมติใน CSV

## เป้าหมาย

ตรวจ Missing Owners, Data Classification, Lifecycle และแยกสิ่งที่ Architecture ระบุออกจากสิ่งที่ Runtime ยืนยัน

## ขั้นตอนที่ 1 — อ่าน CSV

```powershell
Import-Csv .\labs\04-assets\asset_inventory.csv |
    Format-Table -AutoSize
```

สังเกตแถว `OPS-01` ที่ไม่มี Owner ซึ่งควรถูกจัดเป็น `needs-review` ไม่ใช่ลบทิ้งเพราะมองว่าไม่สำคัญ

## ขั้นตอนที่ 2 — รัน Inventory Analyzer

```powershell
py labs/04-assets/inventory_report.py
```

ผลที่คาดหวังสำหรับ Dataset ตั้งต้น:

```text
Discovered/declared assets: 4
Missing owner: ['OPS-01']
Owner coverage among these records: 75.0%
This does NOT measure organization-wide discovery coverage.
```

## ขั้นตอนที่ 3 — ทดสอบ Duplicate Asset ID

สำรอง CSV ก่อน แล้วเพิ่มรายการใหม่ที่มี `asset_id=OPS-01` อีกหนึ่งแถว รัน Script ใหม่ ควรได้รับ `ValueError: duplicate asset_id` เพื่อป้องกัน Record ซ้ำ

คืน CSV ให้เหมือนเดิมหลังทดลอง

## ขั้นตอนที่ 4 — เพิ่ม Enrichment Fields

ทดลองเพิ่ม Columns `business_function`, `dependencies`, `last_seen_utc`, `verification_source` ลง CSV แล้วระบุว่า Field ใดต้องยืนยันจาก Runtime หรือ Business Owner เพิ่มเติม

## ขั้นตอนที่ 5 — ทำ Relationship Map

```text
Booking Web → Booking API → Reservations DB
                          → Payment Provider API
Recovery Team → Backup Storage
```

อธิบายว่าทำไม Backup Storage มี Criticality สูงแม้ไม่ให้ผู้ใช้ทั่วไปเข้าถึงโดยตรง

## Verification

```powershell
py -m unittest discover -s labs/04-assets -p 'test_*.py' -v
```

ผลควร `OK`; อย่าใช้ Owner Coverage สรุปว่าค้นพบทุก Asset แล้ว เพราะ Scope คือ 4 Records ในไฟล์เท่านั้น

## Cleanup

กู้คืน CSV ต้นฉบับที่สำรองไว้เมื่อจบการทดลอง

[Quiz →](/chapters/04-asset-identification/quiz)
