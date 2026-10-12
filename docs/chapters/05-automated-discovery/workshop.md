# Workshop 5 — Docker Discovery, Snapshot Diff และ Local Nmap

**เวลาแนะนำ:** 45–60 นาที · **ระดับ:** Intermediate · **สิทธิ์:** เครื่อง Docker ของตนเองเท่านั้น

## Prerequisites

- Python 3.11+ และ Docker Engine/Desktop (สำหรับ Runtime Part)
- Docker Context ชี้มาที่เครื่องทดลอง ไม่ใช่ Production
- Nmap เป็นทางเลือกสำหรับ Loopback Scan เท่านั้น

## ขั้นตอนที่ 1 — ตรวจ Docker Context ก่อน

```powershell
docker context show
docker ps -a
```

ถ้า Context เป็น Remote Engine หรือ Production ให้ **หยุดก่อน** และเปลี่ยนไปใช้ Test Engine ที่ได้รับอนุญาต

## ขั้นตอนที่ 2 — บันทึก Snapshot

```powershell
py labs/05-discovery/docker_snapshot.py --out baseline.json
```

Script ใช้คำสั่งอ่าน `docker ps -a` เท่านั้น ไม่สร้าง/ลบ Containers และบันทึก Docker Context ลง Snapshot

## ขั้นตอนที่ 3 — สร้าง Snapshot อีกครั้ง

หลังจากคุณสร้าง/หยุด Test Container ด้วยตนเองตามวิธีที่ได้รับอนุญาต:

```powershell
py labs/05-discovery/docker_snapshot.py --baseline baseline.json --out new.json
```

Script จะแสดง `new_instances` และ `missing_instances` โดยใช้ Container ID เหตุที่ Container ID เปลี่ยนไม่ได้แปลว่ามี Logical Service ใหม่เสมอไป

## ขั้นตอนที่ 4 — Network Scan เฉพาะ Loopback

ถ้าติดตั้ง Nmap และมี Local Services เปิดจริง:

```powershell
nmap -sT -p 80,443,3000,8000 127.0.0.1
```

คำสั่งไม่สแกน IP อื่นและใช้ `-sT` TCP Connect Mode อย่าอนุมานว่า Local Open Port เปิดสู่อินเทอร์เน็ตได้

## ขั้นตอนที่ 5 — API Identification (กรณีมี Local FastAPI)

หากมี FastAPI Test Service และเปิด OpenAPI ที่ Default URL:

```powershell
$spec = Invoke-RestMethod http://127.0.0.1:8000/openapi.json
$spec.paths.PSObject.Properties.Name
```

สิ่งที่ได้เป็น Documented Paths เท่านั้น Routes ที่ไม่ได้ประกาศใน Schema อาจไม่แสดง

## ขั้นตอนที่ 6 — ทดสอบ Snapshot Parser

```powershell
py -m unittest discover -s labs/05-discovery -p 'test_*.py' -v
```

## Expected Results และข้อจำกัด

- มี JSON Snapshot ที่บอก Docker Context และ Timestamp
- พบรายการ Container Instance เพิ่ม/หายตามข้อมูลจำลองของคุณ
- รู้ข้อจำกัดของ Port Scan กับ API/OpenAPI Discovery
- มีข้อมูล `source`, `last_seen`, `instance_id` สำหรับเชื่อม Asset Inventory

## Troubleshooting

ถ้า `docker` ไม่รู้จักคำสั่ง ให้เปิด Docker Desktop และตรวจ PATH/Context; ถ้า Nmap ไม่อยู่ใน PATH ให้ใช้ขั้นตอน Python Snapshot แทน ไม่ต้องติดตั้งเพื่อให้ Lab ผ่านทุกส่วน

## Cleanup

ลบ `baseline.json` และ `new.json` ที่สร้างทดลอง; Lab Script ไม่สร้าง Container เอง

[Quiz →](/chapters/05-automated-discovery/quiz)
