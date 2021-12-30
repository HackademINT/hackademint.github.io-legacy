---
title: "NoSourceJr"
ctf: "EasyCTF"
annee: "2018"
author: "zTeeed"
published: true
---
<br />
<a href="/writeup-scripts/2017-2018/EasyCTF/NoSourceJr/file.js">download file.js</a>
<br />
<a href="/writeup-scripts/2017-2018/EasyCTF/NoSourceJr/solve.py">download solve.py</a>
<br />
<br />
From dev tools we get :
<br />
```js
window.encryptionKey = 'nosource';

function process(a, b) {
  'use strict';
  var len = Math.max(a.length, b.length);
  var out = [];
  for (var i = 0, ca, cb; i < len; i++) {
    ca = a.charCodeAt(i % a.length);
    cb = b.charCodeAt(i % b.length);
    out.push(ca ^ cb);
  }
  return String.fromCharCode.apply(null, out);
}

(function (global) {
  'use strict';
  var formEl = document.getElementById('flag-form');
  var inputEl = document.getElementById('flag');
  var flag = 'Fg4GCRoHCQ4TFh0IBxENAE4qEgwHMBsfDiwJRQImHV8GQAwBDEYvV11BCA==';
  formEl.addEventListener('submit', function (e) {
    e.preventDefault();
    if (btoa(process(inputEl.value, global.encryptionKey)) === flag) {
      alert('Your flag is correct!');
    } else {
      alert('Incorrect, try again.');
    }
  });
})(window);
```

chaine is the flag decoded from base64 to ascii number equivalence you can chack on asciitohex website it is xor cipher
<br />
<br />
```python
#! /usr/bin/python
chaine="22 14 6 9 26 7 9 14 19 22 29 8 7 17 13 0 78 42 18 12 7 48 27 31 14 44 9 69 2 38 29 95 6 64 12 1 12 70 47 87 93 65 8"
L=chaine.split(" ")
for i in range(len(L)):
    L[i]=int(L[i])
print (L)

def process(b,L):
    maxi=max(len(L),len(b))
    liste=[]
    for i in range(maxi):
        ca = L[i % len(L)]
        cb = ord(b[i % len(b)])
        liste.append(ca ^ cb)
    return liste

b="soupy"
X=process(b,L)
#flag ^ key = cipher
#cipher ^ key = flag
# cipher ^ flag = key
s=""
for u in X:
    s+=str(chr(u))
print s
```
