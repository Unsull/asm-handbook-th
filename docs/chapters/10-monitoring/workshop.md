# Workshop 10 — Prometheus, Grafana Alerts และ Incident Runbook

**เวลาแนะนำ:** 60–90 นาที · **ระดับ:** Intermediate · **เครื่องมือ:** Docker Desktop/Engine และ Browser

## Scope และความปลอดภัย

Lab นี้สร้าง Synthetic Shop Metrics ด้วย Python Standard Library ไม่แตะ Payment Credentials หรือ Production Services แม้จะใช้ Prometheus/Grafana Images รุ่นที่ Pin ไว้เพื่อการสอน แต่ควรตรวจเวอร์ชันล่าสุดก่อนใช้งานจริง

## ขั้นตอนที่ 1 — เตรียม Lab

จาก Project Root:

```powershell
cd labs/10-monitoring
docker context show
$env:LAB_GRAFANA_PASSWORD = Read-Host 'Set lab-only Grafana password'
docker compose config --services
```

ตรวจว่า Ports 19090 และ 13000 บน Host ไม่ถูกใช้งาน และ Docker Context ไม่ชี้ไป Production

## ขั้นตอนที่ 2 — Start Metrics Stack

```powershell
docker compose up -d
docker compose ps
```

เปิด `http://127.0.0.1:19090` สำหรับ Prometheus และ `http://127.0.0.1:13000` สำหรับ Grafana

Prometheus เก็บ Metrics ทุก 15 วินาทีจาก `mock-exporter:9108/metrics` ซึ่งไม่ Publish Host Port

## ขั้นตอนที่ 3 — ตรวจ PromQL

ลอง Query:

```promql
shop_lab_api_healthy
```

```promql
shop_lab_payment_error_ratio
```

```promql
up{job="mock_shop"}
```

Initial Values จาก `status.json` คือ Healthy = 1 และ Error Ratio = 0.01

## ขั้นตอนที่ 4 — ตรวจ Alert Rules

```powershell
docker compose exec prometheus promtool check config /etc/prometheus/prometheus.yml
docker compose exec prometheus promtool check rules /etc/prometheus/alerts.yml
```

Rules ตรวจ API Healthy, Payment Error Ratio และ Scrape Target Down ใช้ `for` ก่อน Firing

## ขั้นตอนที่ 5 — จำลอง Failure

แก้ `status.json`:

```json
{"api_healthy": 0, "payment_error_ratio": 0.12}
```

ตรวจ Alerts ใน Prometheus หลังช่วง Evaluation/Pending Window คาดว่า `ShopAPIUnhealthy` และ `ShopPaymentErrorsHigh` เข้าสู่ Firing ตามเงื่อนไขที่กำหนด

## ขั้นตอนที่ 6 — Grafana Dashboard และ Webhook

1. ใน Grafana เพิ่ม Prometheus Data Source URL **ภายใน Docker Network** เป็น `http://prometheus:9090`
2. เพิ่ม Stat Panels สำหรับ Healthy/Error Ratio/`up`
3. สร้าง Contact Point ชนิด Webhook URL `http://mock-exporter:9108/alert`
4. กด Test Contact Point และตรวจ Logs:

```powershell
docker compose logs --tail 20 mock-exporter
```

จะเห็น `Synthetic test webhook received` เมื่อรับ Test Webhook ซึ่ง Lab **ไม่ Log Payload** เพื่อไม่สร้างนิสัยเก็บ Sensitive Alerts แบบไม่จำเป็น

5. สร้าง Grafana-managed Alert จาก Prometheus Query `shop_lab_api_healthy` ด้วยเงื่อนไข Last < 1, Pending 30s และเลือก Contact Point ของ Lab

**สำคัญ:** Prometheus-native Alerts ใน Lab ประเมินและแสดง Firing ได้ แต่ไม่ได้ส่ง Notifications จนกว่าจะเชื่อม External Alertmanager/Notification Pipeline ส่วน Grafana-managed Alert ใช้ Grafana Alerting ซึ่งแยกจาก Prometheus Rules ระวังส่ง Alerts ซ้ำหากกำหนดทั้งสองระบบ

## ขั้นตอนที่ 7 — Restore และ Resolve

คืน `status.json`:

```json
{"api_healthy": 1, "payment_error_ratio": 0.01}
```

ตรวจว่าการแจ้งเตือนกลับสู่ Normal/Resolved และผู้รับ Notification ทราบผลปิดเหตุการณ์ตาม Settings

## ขั้นตอนที่ 8 — Incident Tabletop

สมมติ `shop_lab_api_healthy=1` แต่คำสั่งซื้อยังล้มเหลว: Runbook ควรตรวจ Functional Transaction Outcomes, Payment Provider, Queue Worker และ Error Logs เพิ่ม ไม่ควรสรุปว่าระบบใช้งานปกติเพราะ Metrics Target ยัง UP

## Troubleshooting

- Grafana ติดต่อ `127.0.0.1:19090` ไม่ได้ภายใน Container: เปลี่ยนเป็น `http://prometheus:9090`
- Alert ไม่ Firing: ตรวจ Query/Prometheus Targets, Scrape Interval, Rule `for` และช่วงเวลาที่แก้ `status.json`
- Webhook ไม่ได้รับ: ตรวจ `mock-exporter` Logs และ Contact Point Test

## Cleanup

```powershell
docker compose down
```

ไม่มี Named Volumes จึงไม่รับประกันว่า Dashboards/Settings ภายใน Containers จะคงอยู่หลังลบ หากต้องการใช้ต่อให้ Export/Provision Configuration ก่อน Cleanup

[Quiz →](/chapters/10-monitoring/quiz)
