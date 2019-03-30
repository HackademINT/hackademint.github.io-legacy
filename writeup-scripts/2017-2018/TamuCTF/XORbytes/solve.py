#! /usr/bin/env python3
f = open("./hexxy", "rb")
startkey = b"|"
data = f.read()
startkey += bytes([ord('E') ^ data[1]]) #data[1]=0x07
startkey += bytes([ord('L') ^ data[2]]) #data[2]=0x7d
startkey += bytes([ord('F') ^ data[3]]) #data[3]=0x21

keypart = b""
keypart+= bytes([0 ^ int("51",16)])
keypart+= bytes([0 ^ int("42",16)])
keypart+= bytes([0 ^ int("31",16)])
keypart+= bytes([0 ^ int("67",16)])
keypart+= bytes([0 ^ int("33",16)])
keypart+= bytes([0 ^ int("6c",16)])
keypart+= bytes([0 ^ int("34",16)])
keypart+= bytes([0 ^ int("42",16)])
keypart+= bytes([0 ^ int("35",16)])
keypart+= bytes([0 ^ int("75",16)])
keypart+= bytes([0 ^ int("7a",16)])
keypart+= bytes([0 ^ int("50",16)])
keypart+= bytes([0 ^ int("6a",16)])
keypart+= bytes([0 ^ int("6a",16)])
keypart+= bytes([0 ^ int("44",16)])
keypart+= bytes([0 ^ int("34",16)])

print (startkey) #b'QB1g3l4B5uzPjjD4'
print (keypart)  #b'|B1g'
key=keypart
cleartext = b""

for i in range(len(data)):
    cleartext += bytes([key[i % len(key)] ^ data[i]])

out = open("cleartext", "wb")
out.write(cleartext)
out.close()

f.close()
