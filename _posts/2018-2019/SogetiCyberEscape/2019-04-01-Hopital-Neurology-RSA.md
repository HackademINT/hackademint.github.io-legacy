---
title: "RSA"
subtitle: "Challenge tiré du Cyberescape de la Sogeti"
author: "zTeeed"
team: "HackademINT"
ctf: "SogetiCyberEscape"
annee: "2019"

---

# L'énoncé

Trouver x sachant que:

```bash
x ^ 65537 mod 120701443617098609 = 67721340430489711
```

# Solution

On utilise [RsaCtfTool](https://github.com/HackademINT/RsaCtfTool)

```
git clone https://github.com/HackademINT/RsaCtfTool
python3 RsaCtfTool/RsaCtfTool.py --createpub -n 120701443617098609 -e 65537 > key.pub
python3 RsaCtfTool/RsaCtfTool.py --publickey ./key.pub --private > key.priv
python3 RsaCtfTool/RsaCtfTool.py --key ./key.priv --dumpkey
```

Résultat:

key.pub

```bash
-----BEGIN PUBLIC KEY-----
MCMwDQYJKoZIhvcNAQEBBQADEgAwDwIIAazRUs6si3ECAwEAAQ==
-----END PUBLIC KEY-----
```

key.priv

```bash
-----BEGIN RSA PRIVATE KEY-----
MDkCAQACCAGs0VLOrItxAgMBAAECB3oqvEnw3ZECBAHffnUCBQDk8bGNAgQBQPDJ
AgQRikbdAgMfLiw=
-----END RSA PRIVATE KEY-----
```

dumpkey

```bash
[*] n: 120701443617098609
[*] e: 65537
[*] d: 34386935341440401
[*] p: 31424117
[*] q: 3841044877
```

On calcule m sachant que `m^e[n] = c` et que `c^d[n] = m`

```bash
[root@spider SogetiCyberEscape]# python3
Python 3.7.1 (default, Oct 22 2018, 10:41:28)
[GCC 8.2.1 20180831] on linux
Type "help", "copyright", "credits" or "license" for more information.

>>> c = 67721340430489711
>>> d = 34386935341440401
>>> n = 120701443617098609
>>> m = pow(c,d,n)
>>> m
163956092266063
```
