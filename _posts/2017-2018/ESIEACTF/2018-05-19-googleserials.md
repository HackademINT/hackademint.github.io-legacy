---
title: "googleserials"
ctf: "ESIEACTF"
annee: "2018"
author: "zTeeed"
published: true
---

<br />
<a href="/writeup-scripts/2017-2018/ESIEACTF/googleserials/source_code.py">download source_code.py</a>
<br />
<a href="/writeup-scripts/2017-2018/ESIEACTF/googleserials/googleserials.py">download googleserials.py</a>
<br />
<br />
Un site web demandait de trouver deux 'google serials' vérifiant les conditions du code source (en python)
<br />
source_code.py
```python
#! /usr/bin/env python3
def are_same(serial):
	if (serial[0] != serial[1] and
		serial[1] != serial[2] and
		serial[0] != serial[2]):
		return False
	return True

def check_serial(serial):
	try:
		serials = serial.split('-')
	except:
		return False

	if len(serials) != 3:
		return False
	try:
		X = [ord(a) for a in list(serials[0])]
		Y = [ord(a) for a in list(serials[1])]
		Z = int(serials[2])
	except ValueError:
		return False
	except:
		return False

	if not len(X) == 3 or not len(Y) == 3:
		return False
	for a in X+Y:
		if a < 65 or a > 90:
			return False
	if are_same(X) or are_same(Y):
		return False
	if X[1] + 10 > X[2]:
		return False
	if Y[1] - 10 < Y[2]:
		return False
	sum1 = X[0] + X[1] + X[2]
	sum2 = Y[0] + Y[1] + Y[2]
	if sum1 == sum2:
		return False
	if sum1+sum2 != Z:
		return False
	if Z % 3 != 0:
		return False
	return True

</code></pre>
On cherche alors la liste des 'google serials' vérifiant toutes les conditions
<br />
<br />
googleserials.py
<pre><code class="hljs python">
#! /usr/bin/env python3
def find_serial():
    LX=[]
    for i in range(65,90):
        for j in range(65,90):
            for k in range(65,90):
                X=[i,j,k]
                if X[1] + 10 <= X[2]:
                    LX.append(X)
    LY=[]
    for i in range(65,90):
        for j in range(65,90):
            for k in range(65,90):
                Y=[i,j,k]
                if not Y[1] - 10 < Y[2]:
                    LY.append(Y)
    rang=0
    for X in LX:
        for Y in LY:
            rang+=1
            sum1 = X[0] + X[1] + X[2]
            sum2 = Y[0] + Y[1] + Y[2]
            Z=sum1+sum2
            if not sum1 == sum2 and not sum1+sum2 != Z and not Z % 3 != 0 and not are_same(X) and not are_same(Y):
                serial=""
                for i in X:
                    serial+=chr(i)
                serial+="-"
                for i in Y:
                    serial+=chr(i)
                serial+="-"
                serial+=str(Z)
                print(serial)
                print(check_serial(serial))

find_serial()
```
