#! /usr/bin/env python3
cipherhex="fbf9eefce1f2f5eaffc5e3f5efc5efe9fffec5fbc5e9f9e8f3eaeee7"
alpha="0123456789abcdef"
cipher=""
for i in range(1,len(cipherhex),2):
        cipher+=chr(16*alpha.index(cipherhex[i-1])+alpha.index(cipherhex[i]))
print (cipher)
k=0
while ord(cipher[0])^k!=ord('a'):
    k+=1
key=chr(k)
plain=""
for i in range(len(cipher)):
    plain+=chr(ord(cipher[i])^ord(key))
print (plain)
