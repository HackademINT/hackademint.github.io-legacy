---
title: "Obfuscaxor"
ctf: "tamuctf2019"
annee: "2019"
published: true
Author: "Bdenneu"
---
# Description
Nous avons accés à un binaire.
Lorsque l'on exécute celui ci, on nous demande une clé produit. Le but est de la trouver. Pour obtenir le flag, il faut envoyer le bon mot de passe sur rev.tamuctf.com sur le port 7224

Accés au binaire: [binaire](source/obfuscaxor)

# Solution

Décomposons le binaire:

![Obfuscaxor1](/assets/images/tamuctf2019_obfuscaxor1.png)

Le programme demande une clé produit, lance la fonction verify_key_char, et si la sortie est 1, affiche le flag

![Obfuscaxor2](/assets/images/tamuctf2019_obfuscaxor2.png)

La fonction vérifie que la longueur de la clé produit est comprise entre 9 et 64, l'encode, puis la compare avec une valeur en mémoire. Le titre nous incite à penser à un xor. Il faut donc récupérer une clé, la même clé chiffré, ainsi que la chaine attendue (celle en mémoire).
En xorant les trois, on obtiendra le flag.

![Obfuscaxor3](/assets/images/tamuctf2019_obfuscaxor4.png)

![Obfuscaxor4](/assets/images/tamuctf2019_obfuscaxor3.png)

```python
def stacktodata(x):
	res = []
	for i in x.split(' '):
		res += [int(i[8:10],16),int(i[6:8],16),int(i[4:6],16),int(i[2:4],16)]
	return res
entry = [ord(i) for i in "0000000000000000"]
output= stacktodata("0xdf8e9dee 0xdf8e9dee 0xdf8e9dee 0xdf8e9dee")
wanted= stacktodata("0x9cff9eae 0x81d3c7ab 0x8afbeee7 0xae8def9d")
key = "".join([chr(entry[i] ^ output[i] ^ wanted[i]) for i in range(len(entry))])
print(key)
```

On obtient alors la clé:

![Obfuscaxor5](/assets/images/tamuctf2019_obfuscaxor5.png)

# Le flag

On obtient : gigem{x0r_64d5by}
