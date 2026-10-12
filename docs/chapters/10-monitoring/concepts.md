# แนวคิดเชิงลึก — Continuous Monitoring and Management

## 1. Digital Ecosystems เปลี่ยนตลอดเวลา

ระบบร้านค้าออนไลน์อาจปรับจำนวน API Instances อัตโนมัติ เพิ่ม Feature Checkout, เปลี่ยน Cloud Policy หรือย้าย Payment Integration ทุกการเปลี่ยนควรสะท้อนใน Inventory, Threat Model และ Monitoring ไม่ใช่พึ่ง Dashboard ที่ออกแบบจากสถาปัตยกรรมเก่า

**Technological Shifts** เพิ่ม Workloads, Protocols และ Automation; **Organizational Changes** เพิ่ม/เปลี่ยน Users, Roles, Vendors และ Assets Ownership แม้ไม่มี Port ใหม่ Identity Surface ก็อาจเปลี่ยนเมื่อพนักงานย้ายทีมแต่ Token เดิมยังใช้งานได้

## 2. แยก Monitoring 4 ประเภท

| ประเภท | ตัวอย่าง Signal | ข้อจำกัด |
|---|---|---|
| Availability | `up` หรือ HTTP Health | Target ตอบ ไม่รับประกัน Business Workflow |
| Performance | Latency, Errors, Queue Depth | ปัญหาอาจไม่ใช่ Security Incident |
| Security | Auth Failures, Privilege Changes | ต้อง Triage Context และรักษา Logs |
| Attack Surface | New Public Endpoint, Role Drift | ต้องมี Approved Baseline เพื่อเทียบ |

## 3. Setting Alert Thresholds

Alert Rule ที่ดีมี **Metric/Condition + Pending Window + Severity + Owner + Action + Runbook** ตัวอย่าง “Checkout 5xx มากกว่า 5% ต่อเนื่อง 5 นาที” ควรตรวจ Baseline/SLO ก่อนเลือกตัวเลข

**Prometheus** ประเมิน PromQL และใช้ `for` สำหรับ Pending Period ก่อน Firing แต่ `up == 0` หมายถึง Metrics Scrape Failed ไม่ได้บอกว่าธุรกิจหยุดให้บริการ และ Target ที่หายจาก Discovery อาจไม่มี Series ให้ Alert ประเมิน ต้องวาง No-data/Absent-series Policy

### False Positives, False Negatives และ Alert Fatigue

False Positive ทำให้ทีมเสียเวลาและอาจมองข้าม Incident จริง ส่วน False Negative คือภัยที่ไม่แจ้งเตือน การปรับ Threshold เพื่อลด Noise จนไม่มี Alerts เลยเป็นอันตราย ควรใช้ Maintenance Windows, Contextual Labels, Grouping และ Review of Historical Incidents

### Contextual Awareness

เพิ่ม `service`, `environment`, `asset_owner`, `first_seen`, `dashboard`, `runbook` เพื่อให้ Triage ตัดสินใจได้ ลดข้อความกำกวมเช่น `ALERT 500` ควรใช้ “Checkout 5xx higher than baseline; Payment Provider status pending verification”

## 4. Integrating with Incident Response

```text
Detect → Validate → Declare → Contain → Preserve Evidence
   → Recover → Verify → Lessons Learned → Tune Detection
```

Incident Response ต้องมี Escalation, On-call Ownership และ Approval สำหรับ Privileged Actions ไม่ควรให้ Monitoring Tool Restart/Rotate Critical Services โดยอัตโนมัติหากยังไม่มีเงื่อนไขและ Recovery Plan

### Simulating Breach Scenarios

เริ่มจาก Tabletop และ Isolated Lab เช่น Payment API Unavailable, Unauthorized Refund Request, Unapproved Admin Login และ Public Bucket Created ทดสอบว่า Alert ถึง Owner หรือไม่, Evidence/Logs ครบหรือไม่, Business Impact ถูกระบุถูกต้องหรือไม่

### Rapid Response

เลือก Containment ตาม Threat: Revoke Session สำหรับ Account Compromise, จำกัด Network/Token สำหรับ Suspicious API Access, Preserve Audit Logs และสร้าง Recovery Criteria ห้ามยืนยันการบุกรุกจาก Metric เดียวโดยไม่ตรวจ Evidence

## 5. Periodic Reviews and Audits

แม้ Metrics ปกติ Software ก็อาจมี CVE ใหม่ จึงต้องมี Scheduled Dependency/Container Scans, Control Validation, Access Reviews และการทบทวน Crown Jewels ตาม Change Events

| ความถี่ตัวอย่าง | สิ่งที่ทบทวน |
|---|---|
| ทุก PR/Build | Dependency/Config Scan |
| Daily | Critical Alerts, Asset Drift |
| Weekly | Unresolved Findings, False Positive Review |
| Monthly | Owner/Role Audit, Runbook Review |
| Quarterly | Threat Models, Crown Jewels, Recovery Drill |

กำหนดความถี่ตาม Risk Appetite, Criticality และภาระงานจริง ไม่ใช่ใช้ Schedule นี้เป็นมาตรฐานบังคับ

## 6. Feedback Loops และ Continuous Improvement

หลัง Incident ให้ตรวจว่ารู้ปัญหาเมื่อใด, Alert ชัดเจนหรือไม่, มีมิติที่ไม่ได้ตรวจอะไร, Fix/Recovery สร้าง Regression หรือไม่ แล้วปรับ Detection/Controls พร้อม Change Records

ตัวอย่าง: Prometheus Scrape API ได้ `up=1` แต่ Checkout ส่งคำสั่งซื้อไม่สำเร็จ จึงต้องเพิ่ม Functional Synthetic Check และ Business-level Metrics ไม่ใช่พึ่ง Metrics Endpoint Availability อย่างเดียว

## 7. Automation และ AI ใน Monitoring

Automation ช่วย Routing/Tickets/Correlation; AI อาจช่วย Summarize Sanitized Logs และเสนอ Triage Steps แต่ต้องกัน Data Leakage, Excessive Agent Permissions และ Hallucinations การอนุมัติ Change ต่อ Production ควรอยู่กับผู้มีอำนาจ พร้อม Logging/Approval

## 8. Metrics เพื่อวัดกระบวนการเอง

**MTTD**, **MTTA**, **MTTR** ใช้ติดตามเวลาในกระบวนการแต่ต้องนิยาม Clock Start/End ให้ชัด ส่วน Alert Precision = `TP/(TP+FP)` และ Recall = `TP/(TP+FN)` จะคำนวณได้ดีเมื่อมีชุดเหตุการณ์ที่ติด Labels ถูกต้อง ไม่ใช่เพียงเดาค่า TN/FN จากสิ่งที่ Scanner พบ

**อ่านต่อ:** [Prometheus Alerting Rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/), [NIST Incident Response](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
