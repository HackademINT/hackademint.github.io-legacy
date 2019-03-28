#!/usr/bin/python2

import pwn
import random
import hashlib
from Crypto.Cipher import AES

r = pwn.remote('quals.shadow-league.org', 5002)

print(r.recvuntil('key is ').decode())
secretkey = r.recvline()
print(secretkey.decode())
deb = secretkey[:15].decode()
fin = secretkey[-17:-2].decode()

for s in range(1, 10000):
    random.seed(s)
    key = 0xffffffff
    for i in range(10):
        key ^= random.randint(0x00000000, 0xffffffff)
    secret = hashlib.sha256(str(key))
    skey = secret.hexdigest().decode()
    if skey[:15] == deb and skey[-15:] == fin:
        break

print(r.recvuntil('Challenge : '))
challenge = r.recvline()[:-2].decode('hex')

encryption_suite = AES.new(secret.digest(), AES.MODE_CBC, 'LmQHJ6G6QnE5LxbV')
decrypted_challenge = encryption_suite.decrypt(challenge)

r.sendline(decrypted_challenge.encode())
print(r.recvuntil('}'))
