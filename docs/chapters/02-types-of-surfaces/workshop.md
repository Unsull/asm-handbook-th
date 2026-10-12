# Workshop 2 — Classification Across Multiple Attack Surfaces

**เวลาแนะนำ:** 30 นาที · **ระดับ:** Beginner · **ขอบเขต:** CSV จำลอง ไม่เชื่อม Cloud/SaaS จริง

## เป้าหมาย

ฝึกระบุว่า Asset หนึ่งอาจเกี่ยวข้องกับ Network, Application, Identity, Cloud, SaaS และ Supply-chain Surface พร้อมกัน และสร้าง Control Checklist ต่อ Surface

## ขั้นตอนที่ 1 — โหลด Dataset

```powershell
$rows = Import-Csv .\labs\02-surfaces\surface_inventory.csv
$rows | Format-Table -AutoSize
```

ค่า `1` หมายถึง Asset มีความเกี่ยวข้องกับหมวดดังกล่าวในสถานการณ์จำลอง **ไม่ใช่การพบ Vulnerability**

## ขั้นตอนที่ 2 — สรุปจำนวน Assets ตาม Surface

```powershell
$categories = 'network','application','identity','cloud','saas','supply_chain'
foreach ($c in $categories) {
    $count = @($rows | Where-Object { $_.$c -eq '1' }).Count
    "{0,-14} {1}" -f $c, $count
}
```

คำสั่งนี้เป็นเพียงการจัดหมวดข้อมูล CSV ไม่ได้ตรวจหรือสแกน Network ใด ๆ

## ขั้นตอนที่ 3 — เชื่อม Surface กับ Control

สร้าง `surface_controls.csv` เพิ่มเอง โดยมี `asset`, `surface`, `owner`, `control`, `validation_evidence`

ตัวอย่าง:

```csv
asset,surface,owner,control,validation_evidence
Reservations SaaS,identity,IT,Disable departed staff accounts,SSO access review
Smart Camera,network,Facilities,Segment devices,Approved connectivity test
Build Runner,supply_chain,DevOps,Least privilege token,Workflow permissions review
```

## ขั้นตอนที่ 4 — วิเคราะห์ Surface ซ้อนทับ

ตอบว่า Build Runner ซึ่งอยู่ทั้ง Cloud/Identity/Supply-chain อาจทำให้ผู้โจมตีข้าม Trust Boundary ได้อย่างไร แม้ไม่มี Public Website ของตัวเอง

## Expected Result

มี Classification Matrix และรายการตรวจ Controls ต่อ Surface อย่างน้อย 4 รายการ โดยทุกข้อเสนอมี Evidence Needed ไม่กล่าวอ้างว่ายืนยันแล้ว

## Troubleshooting

หาก `Import-Csv` อ่านภาษาไทยแสดงผิด ให้ตรวจการบันทึก UTF-8 หรือเปิดผ่าน VS Code แล้ว Save with UTF-8

## Cleanup

ไม่มี Runtime Change ให้ลบเฉพาะ CSV ที่คุณสร้างทดลองเอง

[Quiz →](/chapters/02-types-of-surfaces/quiz)
