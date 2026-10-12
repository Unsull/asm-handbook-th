# กรณีศึกษา — Alerts, Context และ Incident Response

## Case A: Monitoring OK แต่ Checkout ล้มเหลว

Prometheus Scrape Service ได้ `up{job="checkout"}=1` แต่ผู้ใช้ชำระเงินไม่สำเร็จเพราะ Payment Provider Timeout

**บทเรียน:** Scrape Availability ไม่เท่ากับ Business Function Availability จึงควรเพิ่ม Functional Metrics เช่น `checkout_attempts_total`, `checkout_failures_total{reason="provider_timeout"}` หรือ Synthetic Transaction Check ที่ไม่ใช้ข้อมูลจริง

### ตัวอย่าง Alert Triage

| Observation | สิ่งที่ยังไม่สรุป |
|---|---|
| Metrics Target UP | ไม่ได้พิสูจน์ว่าทุกการชำระเงินสำเร็จ |
| API 5xx เพิ่ม | ยังไม่ยืนยันว่าเป็นการโจมตี |
| Payment Provider Latency สูง | ต้องตรวจ Provider Status/Local Network |
| Worker Queue โตขึ้น | ต้องตรวจ Retry และ Consumer Health |

## Case B: Public Storage Policy Drift

ทีมเคยปิด Public Read ของ Receipt Bucket แล้ว แต่ Infrastructure Change ใหม่เปิด Policy กลับมา Automated Cloud Policy Check พบ Drift และสร้าง Alert

### Detection-to-Response

1. ตรวจว่า Change เป็น Authorized หรือไม่
2. Validate Current Policy/Effective Public Access
3. Preserve Cloud Audit Records
4. Contain/Remediate ตาม Change Approval
5. Verify Policy และ Shared Links หลังแก้
6. ปรับ CI Policy Check ไม่ให้ Regression กลับมา

การมี Alert จาก Policy Drift ไม่ได้ยืนยันว่ามีการ Download ข้อมูลไปแล้ว ต้องตรวจ Access Logs โดยมีบริบท

## Case C: Alert Fatigue

ทีมตั้ง Threshold `Checkout 5xx > 0.1%` ทำให้แจ้งเตือนระหว่าง Spike ตามแผนบ่อยมาก แต่เมื่อมีเหตุจริงคนเริ่ม Ignore Alerts

แนวทางคือดู Historical Baseline, SLO, Pending Period, Severity, Grouping และ On-call Ownership แล้วออกแบบ Alert ที่มี **Action** ไม่ใช่เพิ่ม Threshold จนไม่มีการแจ้งเลย

## แบบฝึก

เขียน Runbook 7 ขั้นสำหรับ Checkout Incident: Detection, Validation, Scope, Business Impact, Containment, Recovery, Verification หลังจากนั้นตั้ง Tabletop Drill ว่าเมื่อ Monitoring Endpoint ยัง UP แต่ Checkout ล้มเหลว ทีมจะทราบได้อย่างไร
