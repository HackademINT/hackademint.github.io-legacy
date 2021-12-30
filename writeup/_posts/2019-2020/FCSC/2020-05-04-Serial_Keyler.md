---
title: "Serial Keyler"
subtitle: "Challenge de Reverse du FCSC 2020"
published: true
author: "Bdenneu"
ctf: "FCSC"
annee: "2020"
---

# L'énoncé

On vous demande d'écrire un générateur d'entrées valides pour ce binaire, puis de le valider sur les entrées fournies par le service distant afin d'obtenir le flag.

[SerialKeyler](/writeup-scripts/2019-2020/FCSC/SerialKeyler)

Service : nc challenges2.france-cybersecurity-challenge.fr 3001

# On reverse!

Ce challenge est un keygenme en 64bits. Voici la fonction main :

![](/assets/images/FCSC2020/SerialKeyler/1.png)

Le programme récupere un username (scanf), puis un Serial (scanf). Enfin, il lance une fonction (surement de vérification (0x55cde3d7483a) puis, selon le resultat, affiche "[>] Valid serial!" (si eax=1) et "[!] Incorrect serial." sinon. Les arguments de la fonction de vérification seront username (rbp-0x90 mis dans rdi) et serial (rbp-0x50 mis dans rsi).
Voyons cette fonction de vérification:

![](/assets/images/FCSC2020/SerialKeyler/2.png)

Cette fois ci, pour être plus didactique, je vais expliquer ce qui se passe en statique.

![](/assets/images/FCSC2020/SerialKeyler/3.png)

Le username est stocké dans rbp-0x78, et le serial est stocké dans rbp-0x80. Les instructions qui suivent sont les vérifications de canary.

![](/assets/images/FCSC2020/SerialKeyler/4.png)

Ensuite, un strlen est effectué (récupère la longueur de l'entrée utilisateur), la valeur est stockée dans rbp-0x58.

![](/assets/images/FCSC2020/SerialKeyler/5.png)

Le memset(rbp-0x58, 0, 0x40) alloue une zone mémoire.

![](/assets/images/FCSC2020/SerialKeyler/6.png)

On rentre ensuite dans une boucle. Le compteur est rbp-0x60. Sa valeur est comparée à rbp-0x58 (longueur de l'entrée utilisateur). Tant que sa valeur est inférieure (jb = jump below), on continue la boucle.

Dans la première partie, on récupere le username rbp - 0x78 (mov rdx ...) , que l'on additionne au compteur rbp-0x60 (mov rax ..., add rax, rdx), et on en récupére le premier byte (movzx eax...). Cette valeur est mise dans rbp-0x61.

On peut résumer l'opération par mov byte rbp-0x61, username[rbp-0x60].

Dans la seconde partie, on récupère la longueur du username rbp-0x58 (mov rax ...), auquelle on soustrait le compteur rbp-0x60 et 1, et on le met dans rax.

On peut résumer l'opération par mov rax, len(username)-compteur-1.

On remet ensuite rbp-0x61 dans rdx, on le xor avec 0x1f, et on le place dans rbp+rax-0x50. On itére le compteur, et on continue.

Au final, voila une traduction de la boucle en python:

```python

calculated = [b'' for i in range(0x40)]
for i in range(len(username)):
	calculated[len(username)-i-1] = username[i]^0x1f

```

Enfin, on compare juste cette chaine avec le serial.
Essayons donc de créer un sérial valide:

![](/assets/images/FCSC2020/SerialKeyler/7.png)

![](/assets/images/FCSC2020/SerialKeyler/8.png)

Parfait! Maintenant, il faut juste scripter pour récupérer les usernames du serveur, et renvoyer un serial correct:

```python

from pwn import *
import re
r = remote('challenges2.france-cybersecurity-challenge.fr', 3001)
while 1:
    data = b''
    while data == b'':
	data = r.recvrepeat(0.1)
    print(data)
    x = re.findall(b"username: (.*?)\n>>>", data)[0]
    x = b''.join([bytes([i^0x1f]) for i in x[::-1]])
    r.sendline(x)

```
# Flag

![](/assets/images/FCSC2020/SerialKeyler/9.png)


