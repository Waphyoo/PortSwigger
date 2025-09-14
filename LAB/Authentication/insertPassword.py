

readfile = open("Authentication/password.txt", "r")
content = readfile.read()
content = content.splitlines()
count = len(content)
print("Number of lines in the file:", count)
print(content)  # Display the first 5 characters of the file content
result=[]
for i in range(count):
    if i%2 == 0:
        result.append("peter")
    result.append(content[i])
print("Resulting list:", len(result))  # Display the first 5 characters of the result list  
print(result)  # Display the first 5 characters of the result list      
writefile = open("Authentication/password2.txt", "w")
for line in result:
    writefile.write(line + "\n")
writefile.close()
readfile.close()