
# **Path Traversal คืออะไร?**

**Path Traversal** หรือที่เรียกอีกชื่อว่า **Directory Traversal** เป็นช่องโหว่ที่ทำให้แฮกเกอร์สามารถเข้าไปอ่านไฟล์ต่างๆ บนเซิร์ฟเวอร์ได้แบบไม่มีข้อจำกัด 

## **แฮกเกอร์สามารถเข้าถึงอะไรได้บ้าง?**

- **โค้ดของแอพพลิเคชัน** และข้อมูลสำคัญต่างๆ
- **Username/Password** ของระบบแบ็กเอนด์
- **ไฟล์สำคัญของระบบปฏิบัติการ** เช่น ไฟล์คอนฟิก

ในบางกรณี แฮกเกอร์อาจจะสามารถ**เขียนไฟล์**ลงในเซิร์ฟเวอร์ได้ด้วย ซึ่งจะทำให้สามารถแก้ไขข้อมูลหรือพฤติกรรมของแอพ และในที่สุดก็**ควบคุมเซิร์ฟเวอร์ได้ทั้งหมด**

## **ตัวอย่างการโจมตี Path Traversal**

ลองนึกภาพว่าเรามี**เว็บช้อปปิ้ง**ที่แสดงรูปภาพสินค้า โดยใช้ HTML แบบนี้:

```html
<img src="/loadImage?filename=218.png">
```

### **เซิร์ฟเวอร์ทำงานยังไง?**

1. URL `/loadImage` รับพารามิเตอร์ `filename` 
2. ไฟล์รูปภาพถูกเก็บไว้ที่ `/var/www/images/`
3. เซิร์ฟเวอร์จะเอา filename ที่ส่งมาต่อท้าย base directory
4. ผลลัพธ์ที่ได้คือ: `/var/www/images/218.png`

### **จุดอ่อนของระบบ**

เว็บนี้**ไม่มีการป้องกัน path traversal** เลย! 

แฮกเกอร์จึงสามารถส่ง URL แบบนี้:
```
https://insecure-website.com/loadImage?filename=../../../etc/passwd
```

### **เกิดอะไรขึ้น?**

เซิร์ฟเวอร์จะพยายามอ่านไฟล์จาก:
```
/var/www/images/../../../etc/passwd
```

**`../` หมายถึงอะไร?**
- `../` = **ย้อนกลับไปโฟลเดอร์แม่ 1 ระดับ**
- `../../../` = **ย้อนกลับ 3 ระดับ** จนถึง root directory

ดังนั้นเส้นทางจริงที่ถูกอ่านคือ:
```
/etc/passwd
```

### **ไฟล์ `/etc/passwd` คืออะไร?**

ในระบบ Unix/Linux นี่คือ**ไฟล์มาตรฐาน**ที่เก็บรายชื่อผู้ใช้ทั้งหมดในเซิร์ฟเวอร์ แฮกเกอร์สามารถใช้เทคนิคเดียวกันนี้เข้าถึง**ไฟล์อื่นๆ** ได้ด้วย

## **กรณีของ Windows**

ใน Windows ใช้ทั้ง `../` และ `..\` ได้ ตัวอย่างการโจมตี:
```
https://insecure-website.com/loadImage?filename=..\..\..\windows\win.ini
```

---

**สรุป:** Path Traversal เป็นช่องโหว่ที่อันตรายมาก เพราะทำให้แฮกเกอร์สามารถเข้าถึงไฟล์ใดๆ ในเซิร์ฟเวอร์ได้ การป้องกันที่ดีคือต้อง**validate และ sanitize** input จากผู้ใช้ก่อนนำไปใช้เสมอ!


# **อุปสรรคในการโจมตี Path Traversal และวิธีหลีกเลี่ยง**

แอพพลิเคชันส่วนใหญ่ในปัจจุบันมีการป้องกัน path traversal แล้ว แต่**แฮกเกอร์ก็มีเทคนิคหลีกเลี่ยงได้เหมือนกัน!**

## **เทคนิคการหลีกเลี่ยงการป้องกัน**

### **1. ใช้ Absolute Path (เส้นทางเต็ม)**

ถ้าระบบตัด `../` ออก เราอาจจะใช้เส้นทางเต็มแทน:
```
filename=/etc/passwd
```

**ทำไมได้?** เพราะเราไม่ได้ใช้ `../` เลย เลยไม่โดนระบบกรอง!

### **2. Nested Traversal Sequences (ซ้อนกัน)**

ใช้เทคนิค**ซ้อนกัน** เช่น:
```
....//
....\/
```

**มันทำงานยังไง?**
- เมื่อระบบตัด `../` ตรงกลางออก
- `....//` จะกลายเป็น `../` 
- `....\/` จะกลายเป็น `..\`

### **3. URL Encoding และ Double Encoding**

เว็บเซิร์ฟเวอร์บางตัวจะตัด directory traversal ออก แต่เราสามารถ**เข้ารหัส**เพื่อหลบหลีกได้:

**URL Encoding ปกติ:**
```
../  →  %2e%2e%2f
```

**Double URL Encoding:**
```
../  →  %252e%252e%252f
```

**Non-standard Encoding:**
```
..%c0%af
..%ef%bc%8f
```

💡 **Pro Tip:** ใครใช้ Burp Suite Professional สามารถใช้ payload list **"Fuzzing - path traversal"** ที่มี encoded sequences ให้ใช้เลย!

### **4. ต้องมี Base Folder**

บางแอพกำหนดว่าไฟล์ต้อง**เริ่มต้นด้วยโฟลเดอร์ที่กำหนด** เช่น `/var/www/images`

**วิธีหลีกเลี่ยง:** ใส่ base folder ไปแล้วค่อย traversal
```
filename=/var/www/images/../../../etc/passwd
```

### **5. ต้องลงท้ายด้วย Extension**

บางแอพบังคับให้ไฟล์ต้อง**ลงท้ายด้วยนามสกุลที่กำหนด** เช่น `.png`

**วิธีหลีกเลี่ยง:** ใช้ **Null Byte** (`%00`) เพื่อตัดไฟล์ path
```
filename=../../../etc/passwd%00.png
```

**เกิดอะไรขึ้น?**
- ระบบจะเห็นว่ามีนามสกุล `.png` ✅
- แต่เมื่อประมวลผลจริง **null byte จะตัดทุกอย่างหลังมัน**
- ผลลัพธ์จริง: `../../../etc/passwd`


ตัวอย่างที่ยกมานั้นเป็นเฉพาะพฤติกรรมของ PHP (โดยเฉพาะเวอร์ชันก่อน 5.3.4) ที่จะตีความ null byte (`%00`) เป็นตัวสิ้นสุดสตริง ทำให้ส่วน `.jpg` ที่อยู่หลัง null byte ถูกตัดออกไป

ในภาษาโปรแกรมมิ่งอื่นๆ null byte injection อาจทำงานต่างกันไป:

**ตัวอย่างเช่น:**
- **Java/C#**: โดยปกติจะไม่ตีความ null byte เป็นตัวสิ้นสุดสตริงเหมือน PHP
- **C/C++**: จะหยุดประมวลผลเมื่อเจอ null byte เพราะใช้เป็น string terminator
- **Python**: สตริงสามารถมี null byte ได้โดยไม่หยุดการประมวลผล
- **Node.js**: ขึ้นอยู่กับ API ที่ใช้งาน บางตัวอาจหยุดที่ null byte

ดังนั้นการโจมตีแบบ null byte injection จึงต้องปรับเปลี่ยนตามภาษาและระบบที่เป็นเป้าหมาย ไม่สามารถใช้วิธีเดียวกันได้กับทุกระบบ

## **สรุปสำคัญ**

การป้องกัน path traversal **ไม่ใช่เรื่องง่าย** เพราะแฮกเกอร์มีเทคนิคหลากหลายในการหลีกเลี่ยง:

1. **Absolute paths** - ไม่ใช้ `../` เลย
2. **Nested sequences** - ซ้อนกันเพื่อหลบการกรอง  
3. **Encoding** - เข้ารหัสให้ระบบมองไม่เห็น
4. **Base folder bypass** - ใส่โฟลเดอร์ที่ต้องการไปด้วย
5. **Null byte injection** - ตัด extension ออก

**ข้อแนะนำ:** ระบบป้องกันที่ดีต้อง**ตรวจสอบหลายชั้น** และ**validate ผลลัพธ์สุดท้าย**ด้วย ไม่ใช่แค่กรอง input ตั้งต้นเท่านั้น!


# **วิธีป้องกันการโจมตี Path Traversal**

การป้องกัน path traversal ที่**ดีที่สุด**คือ **หลีกเลี่ยงการส่ง user input ไปยัง filesystem API** เลย! หลายฟังก์ชันสามารถเขียนใหม่ให้ปลอดภัยกว่าได้

## **กรณีที่หลีกเลี่ยงไม่ได้**

ถ้าจำเป็นต้องใช้ user input กับ filesystem API ให้ใช้**การป้องกันสองชั้น**:

### **ชั้นที่ 1: Validate User Input**

**วิธีที่ดีที่สุด** - ใช้ **Whitelist**:
```
✅ อนุญาตเฉพาะค่าที่กำหนดไว้ล่วงหน้า
เช่น: ["image1.jpg", "image2.png", "document.pdf"]
```

**วิธีสำรอง** - ตรวจสอบเนื้อหา:
```
✅ อนุญาตเฉพาะตัวอักษรและตัวเลข (alphanumeric)
❌ ไม่อนุญาต: ../ \  / : * ? " < > |
```

### **ชั้นที่ 2: Canonicalize Path**

หลังจาก validate แล้ว ให้:

1. **รวม input กับ base directory**
2. ใช้ **platform filesystem API** เพื่อ **canonicalize path** (ทำให้เป็นเส้นทางมาตรฐาน)
3. **ตรวจสอบ**ว่า canonicalized path เริ่มต้นด้วย base directory ที่คาดหวัง

## **ตัวอย่างโค้ด Java**

```java
File file = new File(BASE_DIRECTORY, userInput);
if (file.getCanonicalPath().startsWith(BASE_DIRECTORY)) {
    // ปลอดภัย สามารถประมวลผลไฟล์ได้
} else {
    // อันตราย! ไม่อนุญาต
}
```

## **ทำไม Canonicalize Path สำคัญ?**

**Canonicalization** คือการแปลงเส้นทางให้เป็น**รูปแบบมาตรฐาน**:

```
เส้นทางที่มี traversal:
/var/www/images/../../../etc/passwd

หลัง canonicalize:
/etc/passwd
```

**การตรวจสอบ:**
```java
// BASE_DIRECTORY = "/var/www/images"
// canonicalPath = "/etc/passwd" 

"/etc/passwd".startsWith("/var/www/images") 
// → false ❌ (ไม่อนุญาต)
```

## **ตัวอย่างการใช้งานจริง**

### **❌ วิธีที่ไม่ปลอดภัย:**
```java
String filename = request.getParameter("file");
File file = new File("/var/www/images/" + filename);
// อันตราย! ไม่มีการตรวจสอบ
```

### **✅ วิธีที่ปลอดภัย:**
```java
String filename = request.getParameter("file");

// ชั้นที่ 1: Validate input
if (!filename.matches("[a-zA-Z0-9._-]+")) {
    throw new SecurityException("Invalid filename");
}

// ชั้นที่ 2: Canonicalize และตรวจสอบ
File file = new File(BASE_DIRECTORY, filename);
String canonicalPath = file.getCanonicalPath();

if (!canonicalPath.startsWith(BASE_DIRECTORY)) {
    throw new SecurityException("Path traversal detected");
}

// ตอนนี้ปลอดภัยแล้ว
processFile(file);
```

## **เคล็ดลับเพิ่มเติม**

### **1. ใช้ Path Libraries**
```java
// Java 7+ ใช้ java.nio.file.Path
Path basePath = Paths.get(BASE_DIRECTORY).normalize();
Path userPath = basePath.resolve(userInput).normalize();

if (!userPath.startsWith(basePath)) {
    // Path traversal detected!
}
```

### **2. Additional Validations**
- ตรวจสอบ**ความยาวไฟล์เนม**
- ตรวจสอบ**นามสกุลไฟล์**
- ตรวจสอบ**ขนาดไฟล์**

### **3. Logging และ Monitoring**
```java
if (!canonicalPath.startsWith(BASE_DIRECTORY)) {
    logger.warn("Path traversal attempt: " + userInput + 
                " from IP: " + request.getRemoteAddr());
    // บล็อก IP หรือเพิ่มการ monitoring
}
```

## **สรุปหลักการสำคัญ**

1. **หลีกเลี่ยง user input ใน filesystem** ถ้าทำได้
2. **Validate input** ด้วย whitelist หรือ pattern matching
3. **Canonicalize path** และตรวจสอบว่าอยู่ใน base directory
4. **Log การพยายามโจมตี** เพื่อ monitoring
5. **Test อย่างละเอียด** ด้วย penetration testing

การป้องกันที่ดีต้อง**ทำหลายชั้น** เพราะแฮกเกอร์มีเทคนิคหลากหลายในการหลีกเลี่ยงการป้องกัน!