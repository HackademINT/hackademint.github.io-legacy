---
title: "MISC.HELLO_WORLD"
ctf: "TamuCTF"
annee: "2019"
published: true
author: "Bdenneu"
---
# Description
On a accès à ![Hello_world.cpp](/_posts/2018-2019/TamuCTF2019/source/hello_world.cpp)

# Solution
Lorsque l'on ouvre le fichier, on remarque en début du fichier une alternance d'espace et de retour à la ligne.

![hello_world](/assets/images/TamuCTF2019/tamuctf2019_helloworld.png)

Il s'agit de binaire. On remplace les espaces par des 0 et les retours à la ligne par des 1.

```python
import binascii
with open('hello_world.cpp','rb') as f:
	data = f.read()
res = []
for i in data.split(b'\n'):
	if len(i) == 1:
		break
	current = ""
	for j in i:
		if j == 32:
			current += "0"
		else:
			current += "1"
	res += [chr(int(current,2))]
print("".join(res))
```

On obtient: gigem{0h_my_wh4t_sp4c1ng_y0u_h4v3}!ecapsetihw fo tol a si erus taht ,eeg yllog teews lleW

# Le flag

On obtient: gigem{0h_my_wh4t_sp4c1ng_y0u_h4v3}
