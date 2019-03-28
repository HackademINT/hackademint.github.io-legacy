#! /usr/bin/env python3
import binascii
string="3d25373c2b39044f1d390a4a1c4b484e4f11204e4a20114f48204a4c3c0a0d16480620084c131c4f124c200b4f20352c20084f0d131b02"
plain=""
for i in range(1,len(string),2):
    duo=string[i-1:i+1]
    x=ord(binascii.unhexlify(duo))
    x=255-x
    if x<=128:
        x-=128
    elif x>=128:
        x-=128
    plain+=chr(x)
print (plain)

