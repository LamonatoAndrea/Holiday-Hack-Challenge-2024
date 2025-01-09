outStr = ""
with open("ELF-HAWK-dump.csv", "r") as file:
    for line in file.read().split("\n")[1:-1]:
        for field in line.split(","):
            if field == "TRUE":
               outStr += "1"
            elif field == "FALSE":
                outStr += "0"

for i in range(0, len(outStr), 8):
    char = outStr[i:i+8]
    n = int(char, 2)
    print (n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(), end="")
