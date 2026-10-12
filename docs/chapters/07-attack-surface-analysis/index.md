# บทที่ 07 — Measuring Attack Surface

> วิเคราะห์ Data Flow, Trust Boundary และ Threats

บทนี้เป็นหนึ่งในชุดคู่มือเรียนรู้ ASM ภาษาไทยที่เขียนใหม่โดยอิสระ โดยใช้ลำดับหัวข้อที่ตรวจสอบกับ [สารบัญของ O’Reilly](https://www.oreilly.com/library/view/attack-surface-management/9781098165079/ch07.html) และขยายความด้วยแนวปฏิบัติจากเอกสารมาตรฐานและกรณีศึกษาสมมติ

## หัวข้อหลักจากสารบัญต้นฉบับ

- Attack Surface Analysis
- Internal and External Attack Surfaces
- Tools for Assessing Attack Surfaces
- Threat Modeling
- Integrating Threat Modeling with Attack Surface Mapping

## เลือกส่วนที่ต้องการอ่าน

<div class="chapter-links">

<a href="/asm-handbook-th/chapters/07-attack-surface-analysis/concepts.html">แนวคิดเชิงลึก<small>ทำความเข้าใจและเชื่อมข้อจำกัด</small></a>
<a href="/asm-handbook-th/chapters/07-attack-surface-analysis/examples.html">กรณีศึกษา<small>ฝึกคิดกับระบบทั่วไป</small></a>
<a href="/asm-handbook-th/chapters/07-attack-surface-analysis/workshop.html">Workshop<small>ขั้นตอนทดลองและตรวจผล</small></a>
<a href="/asm-handbook-th/chapters/07-attack-surface-analysis/quiz.html">แบบทดสอบ<small>5 ข้อ พร้อมเฉลยอธิบาย</small></a>

</div>

## วิธีเรียนบทนี้

1. เริ่มจาก **แนวคิดเชิงลึก** โดยพยายามอธิบายศัพท์ใหม่ด้วยตัวเอง
2. ใช้ **กรณีศึกษา** เพื่อแยกข้อค้นพบจริงออกจากสมมติฐาน
3. ทำ **Workshop** กับระบบจำลองหรือระบบที่ได้รับอนุญาตเท่านั้น
4. ทำ **แบบทดสอบ** ท้ายบทแล้วทบทวนข้อที่ไม่เข้าใจ

> **ขอบเขต:** ตัวอย่างทั้งหมดเป็นสถานการณ์สมมติ ไม่ใช่รายงานช่องโหว่ของธุรกิจหรือบริการจริง
