---
title: "Gronsfeld"
ctf: "IceCTF2018"
annee: "2018"
author: "Bdenneu"
published: true
type: crypto
---
# Description
Dans ce challenge de cryptographie, nous disposons d'une image avec la fusion de garfield et d'une personnage de serie, avec en haut à droite qui s'apparente à une date et en bas, le flag chiffré.

![Gronsfeld](/assets/images/IceCTF2018/icectf2018_garfeld.png)

# Solution
Il s'avère que le nom de l'épreuve est un calembour avec la méthode de chiffrement de Gronsfeld. La clé est le nombre en haut à droite. J'ai utilisé ce script pour decoder le flag:
```python
from string import ascii_lowercase,ascii_uppercase
code = "IjgJUO{P_LOUV_AIRUS_GYQUTOLTD_SKRFB_TWNKCFT}"
cle = "07271978"
res = ""
index = 0
for i in range(len(code)):
        if code[i] in ascii_lowercase:
                res += ascii_lowercase[(ascii_lowercase.index(code[i]) - int(cle[index%len(cle)]))%len(ascii_lowercase)]
                index += 1
        elif code[i] in ascii_uppercase:
                res += ascii_uppercase[(ascii_uppercase.index(code[i]) - int(cle[index%len(cle)]))%len(ascii_uppercase)]
                index += 1
        else:
                res += code[i]

print(res)
```
# Le flag:
On obtient : IceCTF{I_DONT_THINK_GRONSFELD_LIKES_MONDAYS}
