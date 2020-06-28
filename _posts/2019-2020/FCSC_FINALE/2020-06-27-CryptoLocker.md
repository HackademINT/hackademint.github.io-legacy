---
title: "CryptoLocker v2"
subtitle: "Challenge de Forensic de la finale du FCSC 2020"
published: true
author: "Bdenneu"
ctf: "FCSC_FINALE"
annee: "2020"
---

# L'énoncé

Suite à une attaque que nous avons subie fin avril, notre prestataire informatique nous a fourni un nouveau programme de mise à jour en nous assurant, cette fois, qu'aucun virus n'était présent.

Cependant, en voulant l'appliquer sur un serveur ultra-sensible, nos admins se sont aperçus qu'il s'agissait d'un CryptoLocker, a priori une mise à jour du dernier.

Notre fichier important est une nouvelle fois chiffré, et nous comptons sur vous pour le récupérer.

SHA256(memory2.dmp.gz) = 4e6ebf8142c3c1a033e4664354b1bd9df0537e5a91827cf12209321c0cf3c609.

# Investigons!


On est face à un dump mémoire. Volatility nous indique qu'il s'agit d'une machine Windows.

```sh
volatility -f memory2.dmp imageinfo
```

![](/assets/images/FCSCFINALE2020/CryptoLocker/1.png)

```sh
volatility -f memory2.dmp --profile=Win7SP1x86_23418 filescan | grep -i Desktop
```

Pendant les préquals, le flag était sur le bureau. On y voit 2 fichiers intéressants: update_v0.8.exe et flag.txt.enc.

![](/assets/images/FCSCFINALE2020/CryptoLocker/2.png)

```sh
volatility -f memory2.dmp --profile=Win7SP1x86_23418 pstree
```

Le programme update_v0.8.exe a bien été lancé.

![](/assets/images/FCSCFINALE2020/CryptoLocker/3.png)

On récupère les deux fichiers.

```sh
mkdir dumped
volatility -f memory2.dmp --profile=Win7SP1x86_23418 dumpfiles -D dumped/ -Q 0x000000003e6ea808
volatility -f memory2.dmp --profile=Win7SP1x86_23418 dumpfiles -D dumped/ -Q 0x000000003eaec938
```

On a alors le flag chiffré:

\x0c\x17\x1b\x16,ke2,6y>~kn#gepp{d&qc~zb~z//|yq9~4{5uw#y}*v||a/5yfoea2*e.n~a8#0dw;I

Attention, volatility ajoute des null bytes à la fin des fichiers. Maintenant, il faut analyser le malware.
Radare2 nous indique que l'adresse de main est à 0x00401d3b.

![](/assets/images/FCSCFINALE2020/CryptoLocker/4.png)

![](/assets/images/FCSCFINALE2020/CryptoLocker/5.png)

Le programme génère 50 nombres aléatoires, inverse leur et l'utilise comme clé (xor). Heureusement pour nous, le programme lance un srand(time(NULL)) ce qui va nous permettre de récupérer la seed.
Le timestamp doit se trouver autour du moment où le programme a été lancé. D'après le pstree, il doit se trouver autour de 1586805493.


```c
//timestamp.c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
int main(int argc, char** argv)
{
	time_t x =  (time_t) strtol(argv[1], NULL, 10);
	srand(x);
	for(int i=0;i<50;i++){

		printf("%d\n",rand()%25+65);
	}
}
```

```python
import os
with open('flag.txt.enc', 'rb') as f:
    data = f.read()
base = 1586805493-100
for i in range(200):
	key = [int(i) for i in os.popen('./timestamp %d'%(base+i)).read().split('\n')[:-1]][::-1]
	flag = ''.join([chr(data[i]^key[i]) for i in range(len(key))])
	if "FCSC" in flag:
		print("Found")
		print(flag)
		break
```

Malheureusement pour moi, le programme n'a pas trouvé le flag. 3 heures avant la fin des épreuves, \J nous a donné un indice sur comment le résoudre. Le random n'est pas géré pareil sur Windows et sur Linux.

![](/assets/images/FCSCFINALE2020/CryptoLocker/6.png)

J'ai redémarré sous windows, et j'ai généré des clés que j'ai mis dans un fichier key.txt, et je suis retourné sur Linux.

```python
with open('keys.txt','rb') as f:
    data = f.read()

keys = data.split(b'\r\n')[:-1] //attention, fichier généré sous windows donc, le retour à la ligne sont différents.

with open('flag.txt.enc', 'rb') as f:
    data = f.read()

for key in keys:
    k = [i for i in key]
    k = k[::-1]
    flag = ''.join([chr(data[i] ^ k[i%len(k)]) for i in range(len(data))])
    if "FCSC" in flag:
        print("FOUND")
        break
print(flag)
```

![](/assets/images/FCSCFINALE2020/CryptoLocker/7.png)

# Flag

FCSC{93bcf2f427e455685b0580058ba028a0a6f96b42c7336ea13877be5e648aec42}


