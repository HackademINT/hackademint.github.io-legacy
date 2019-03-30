#! /usr/bin/python
import base64

plaindata="El Psy Congroo"
cipherdata="IFhiPhZNYi0KWiUcCls="
cipherflag="I3gDKVh1Lh4EVyMDBFo="

cipherdata=base64.b64decode("IFhiPhZNYi0KWiUcCls=")
cipherflag=base64.b64decode("I3gDKVh1Lh4EVyMDBFo=")

key=""
maxi=max(len(plaindata),len(cipherdata))
for i in range(maxi):
    key+=chr(ord(plaindata[i%len(plaindata)])^ord(cipherdata[i%len(cipherdata)]))
print key

flag=""
maxi=max(len(key),len(cipherflag))
for i in range(maxi):
    flag+=chr(ord(cipherflag[i%len(cipherflag)])^ord(key[i%len(key)]))
print flag
