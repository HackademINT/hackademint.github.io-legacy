#! /usr/bin/env python3
import struct


def lcg(m, a, c, x):
    return (a*x + c) % m


f = open("flag.png.enc", "rb")
ciphertext = f.read()
f.close()

# D'après les headers de PNG...
cleartext = b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A\x00\x00\x00\x0D\x49\x48\x44\x52"

print("m: {}".format(pow(2, 32)))
for i in range(len(cleartext)//4):
    block = struct.unpack(">I", ciphertext[i*4:(i+1)*4])[0]
    key = block ^ struct.unpack(">I", cleartext[i*4:(i+1)*4])[0]

    print("key {}: {}".format(i, key))

# On a maintenant les 4 premières clés, on peut résoudre ez le système
# d'équations:
# https://www.wolframalpha.com/input/?i=(2445943554*x%2By)%252%5E32+%3D+2225636917,+(2225636917*x%2By)%252%5E32+%3D+1320590709,+(1320590709*x%2By)%252%5E32+%3D4196912501

# et hop on decipher

a = 3204287424
c = 1460809397
m = pow(2, 32)

block = struct.unpack(">I", ciphertext[:4])[0]
x = block ^ struct.unpack(">I", cleartext[:4])[0]

cleartext = b""

for i in range(len(ciphertext)//4):
    cipherchunk = struct.unpack(">I", ciphertext[i*4:(i+1)*4])[0]
    cleartext += struct.pack(">I", x ^ cipherchunk)
    x = lcg(m, a, c, x)

f = open("flag.png", "wb")
f.write(cleartext)
f.close()
