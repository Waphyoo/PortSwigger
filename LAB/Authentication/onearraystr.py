import json

readfile = open("Authentication/password.txt", "r")
content = readfile.read()
content = content.splitlines()

result=[]

for i in range(len(content)):
    
    result.append(f"{content[i]}")

print(json.dumps(result))