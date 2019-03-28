#! /usr/bin/python3

cipher="-);1+<.3/!$+>!8;8>!!8;*)%0'+ ,;!'5"
flag_start="easyctf{"
keytest=""
for i in range(len(flag_start)):
    keytest+=chr(ord(flag_start[i])^ord(cipher[i]))
key=keytest[0] # lenght = 1
print ("KEY = "+key)
flag=""
for i in range(len(cipher)):
    flag+=chr(ord(cipher[i])^ord(key))
print ("FLAG = "+flag)
