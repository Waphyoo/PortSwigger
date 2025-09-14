



result=[]
for i in range(50):
    result.append("wiener")
    result.append("carlos")
    result.append("carlos")

writefile = open("Authentication/username2.txt", "w")
for line in result:
    writefile.write(line + "\n")
writefile.close()