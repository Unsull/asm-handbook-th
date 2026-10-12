# Workshop 9 — ลด Docker Host Exposure โดยคง Internal Connectivity

**เวลาแนะนำ:** 40–60 นาที · **ระดับ:** Intermediate · **เครื่องมือ:** Docker Desktop/Engine, PowerShell

## Prerequisites และ Scope

ทดสอบบน Docker Engine ของตนเองเท่านั้น ตรวจ `docker context show` ก่อนทุกครั้ง อย่าใช้ Production Context หรือใช้ชื่อ Compose Project ซ้ำกับของจริง

## ขั้นตอนที่ 1 — สร้าง Before State

เปิด PowerShell ที่ Project Root:

```powershell
cd labs/09-minimization
docker context show
docker compose -f compose.before.yaml config --services
```

ตรวจว่า Host Ports `18088`, `18089` ยังว่าง แล้วเริ่ม Test Containers:

```powershell
docker compose -f compose.before.yaml up -d
```

ทั้ง `web` และ `internal-api` ใช้ Nginx Image แบบเดียวกัน แต่มีบทบาทต่างกันใน Lab

## ขั้นตอนที่ 2 — ตรวจ Baseline

```powershell
Test-NetConnection 127.0.0.1 -Port 18088
Test-NetConnection 127.0.0.1 -Port 18089
```

เมื่อ Containers ทำงาน ทั้งสองควรเชื่อม Host Port ที่ Publish ได้

ทดสอบ Internal Service Discovery:

```powershell
docker compose -f compose.before.yaml exec web wget -qO- http://internal-api/
```

ควรเห็น HTML ของ Nginx ตอบกลับจาก `internal-api` โดยผ่าน Docker Network

## ขั้นตอนที่ 3 — เปลี่ยนเป็น After State

ใน `compose.after.yaml` ไม่มี `ports` ของ `internal-api` แล้ว:

```powershell
docker compose -f compose.after.yaml up -d
```

Compose อาจ Recreate Container เพื่อใช้ Config ใหม่ โปรดรอให้ Services พร้อม

## ขั้นตอนที่ 4 — ตรวจ Security และ Function

```powershell
Test-NetConnection 127.0.0.1 -Port 18089
Test-NetConnection 127.0.0.1 -Port 18088
docker compose -f compose.after.yaml exec web wget -qO- http://internal-api/
```

Expected:

- Host Port `18089` ไม่รับการเชื่อมต่อ (ถ้าไม่มี Process อื่นใช้แทน)
- Host Port `18088` ยังรับการเชื่อมต่อ
- Container `web` ยังเรียก `internal-api` ได้

การทดสอบจาก Host/Loopback ไม่พิสูจน์ Internet Exposure ทั้งหมด ต้องตรวจ Router/Firewall/NAT ตาม Environment หากจะอ้างการเข้าถึงภายนอกจริง

## ขั้นตอนที่ 5 — ลดสิทธิ์เพิ่มอย่างระมัดระวัง

ทดลองอ่าน Docker Security Options `user`, `cap_drop`, `read_only` และ `security_opt` จากเอกสาร Docker ก่อน ไม่ควรคัดลอก Hardening Template ไปใช้กับ Stateful Database โดยไม่มี Volume Permission Tests

## Cleanup (สำคัญ)

```powershell
docker compose -f compose.after.yaml down
```

เนื่องจากทั้งสอง Compose Files ใช้ `name: asm9-isolated-lab` เดียวกัน คำสั่งนี้จะปิดเฉพาะ Containers/Networks ของโปรเจกต์ Lab ตาม Docker Compose Project Namespace

## Acceptance Criteria

มีผล Before/After สามทาง (Host → Web, Host → Internal API, Web → Internal API) และคำอธิบายว่าจำนวน Published Ports ลดไม่ได้แปลว่า Risk ลดเป็นสัดส่วนเท่ากัน

[Quiz →](/chapters/09-minimization/quiz)
