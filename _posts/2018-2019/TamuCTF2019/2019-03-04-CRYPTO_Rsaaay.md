---
title: "CRYPTO.Rsaaay"
ctf: "TamuCTF"
annee: "2019"
published: true
author: "Bdenneu"
---
# Description
Le titre du challenge insinue fortement qu'il s'agit d'un challenge de RSA. On a accès à un couple de nombre et à une suite de nombre dite secrete.
![Rsaaay](/assets/images/TamuCTF2019/tamuctf2019_rsaaay.png)

# Solution
 On peut supposer vu la taille des premiers nombres qu'il s'agit de n (2531257) et e (43). Comme n est petit, on peut le factoriser en p (509) et q (4973). On inverse le rsa pour chaque nombre. Il s'agit d'une suite des codes ascii du flag.
 
103 105103 101109 12383 97118 97103 10195 83105 12095 70108 121105 110103 9584 105103 101114 115125

On la reconverti et on obtient le flag.

```python
import gmpy
n,e = (2531257, 43)
p,q = 509,4973
phi = (p-1)*(q-1)
d = gmpy.invert(e,phi)
data = "906851 991083 1780304 2380434 438490 356019 921472 822283 817856 556932 2102538 2501908 2211404 991083 1562919 38268".split(" ")
res = ""
for i in data:
	res += str(pow(int(i),d,n))

data = ""
while len(res) > 0:
	if res[0] == "1":
		data += chr(int(res[:3]))
		res = res[3:]
	else:
		data += chr(int(res[:2]))
		res = res[2:]
print(data)
```
# Le flag
On obtient alors: gigem{Savage_Six_Flying_Tigers}


