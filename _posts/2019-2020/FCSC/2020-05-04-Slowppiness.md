---
title: "Slowppiness"
subtitle: "Challenge de Reverse du FCSC 2020"
published: true
author: "Bdenneu"
ctf: "FCSC"
annee: "2020"
---

# L'énoncé

Vous retrouvez ces fichiers dans vos archives qui doivent afficher un flag, mais il y a visiblement un problème. Pourrez-vous le résoudre ?

[slowppiness](/writeup-scripts/2019-2020/FCSC/slowppiness)

[data16.u32](/writeup-scripts/2019-2020/FCSC/data16.u32)

[data128.u32](/writeup-scripts/2019-2020/FCSC/data128.u32)

[data256.u32](/writeup-scripts/2019-2020/FCSC/data256.u32)

[data4096.u32](/writeup-scripts/2019-2020/FCSC/data4096.u32)

# On reverse!

Ce challenge est un problème d'optimisation de code. Voici le début de la fonction main :

![](/assets/images/FCSC2020/Slowppiness/1.png)

Le programme va lancer la fonction 0x55d208afc400 sur les 4 fichiers donénes (16, 128, 256 puis 4096). Après chacun des 3 premiers, il va vérifier le hash que la fonction renvoit (les 16 premiers bytes).

Il utilisera le dernier hash (4096) en temps que flag:

![](/assets/images/FCSC2020/Slowppiness/2.png)

Voyons donc ce que fais la fonction 0x55d208afc400 plus en détail. Les arguments données sont (nom de fichier,taille, zone_mémoire, bout_de_hash).

![](/assets/images/FCSC2020/Slowppiness/3.png)

La fonction ouvre le fichier, y lit 0x4000 bytes, le ferme puis vérifie que le debut de sha256sum est bien bout_de_hash.

La taille mise alors en argument est stockée dans r8, puis on rentre dans une boucle:

![](/assets/images/FCSC2020/Slowppiness/4.png)

On initialise deux zones mémoires: une à 0x12345678 (z1) et l'autre à 0 (z2)
Tant que r8 n'est pas égal à 0:
*on lance 0x55d208afbc80(contenu_du_fichier, 0,r8>>1)
*on lance 0x55d208afbc80(contenu_du_fichier, r8>>1+1, r9)
*on stocke dans z1 la valeur (z1*0x19660d+0x3c6ef35f)&0xffffffff (ce qui fait penser à une suite)
*on ajoute 1 à z2
*on compare [rbx+r9*4] et [rbx+r8*4], et on les trie.

![](/assets/images/FCSC2020/Slowppiness/5.png)

On récupère ensuite le nombre stocké dans z2, et on s'en sert pour générer une suite. On va ensuite xor contenu_du_fichier (qui a été modifiée par 0x55d208afbc80) avec cette suite. On en fait un sha256, et on renvoit le résultat.

C'est parti pour l'analyse de 0x55d208afbc80.

# Diving into the abyss

Peut être qu'au début de ce write up, vous vous êtes demandé pourquoi ne pas attendre simplement la fin du programme pour avoir le flag affiché ? En fait, la fonction 0x55d208afbc80 est une fonction récursive avec plein de boucles imbriquées (rendant son exécution rapide pour u16, mais interminable pour u4096).

![](/assets/images/FCSC2020/Slowppiness/6.png)

Au début du programme, il compare les arguments: si rsi (premier nombre en argument) >= rdx (deuxieme nombre en argument), fin du programme.

![](/assets/images/FCSC2020/Slowppiness/7.png)

Ce bout de code est répété plusieurs fois à quelques offsets près. Il va relancer la fonction mais avec d'autres arguments. Il sépare le programme en plusieurs intervalles de longueur differentes puis rappelle la fonction dessus. Pour séparer son intervalle, il calcule (début+fin)//2, puis ajoute 1 pour le début du suivant jusqu'à atteindre la fin de l'intervalle.

Cette séparation se fait 7 fois au maximum.

Par exemple, pour [0, 7], il ferait:
*[0, 3] (0+7)//2 = 3
*[4, 5]  (4+7)//2 = 5
*[6, 6]  (6+7)//2 = 6

![](/assets/images/FCSC2020/Slowppiness/8.png)

Le deuxième bout de code répété lui aussi à quelques offsets près et celui la. Comme en haut, il calcule le terme suivant pour la suite le place dans z1, ajoute 1 à z2 et inverse les élements dans r15+rcx*4 et r15*rbx*4.Le code est répété jusqu'a ce que rsp+0x68 (fin de l'intervalle) pour ce bout de code soit égal à rsp+0x68 (début de l'intervalle) en diminuant à chaque itération rsp+0x68. Tant que les valeurs ne sont pas égales, il relance le bout de code d'en haut.

Si l'on y réflechi bien, il ne fait que relancer la fonction, mais sur entre le debut des intervalles, et la fin données au départ-1.

Par exemple, pour [0, 7], il ferait:
*[6, 6]  (7-1 = 6)
*[4, 6]
*[0, 6]

Au final, ce n'est un algorithme de tri avec une complexité dégueulasse, qui garde en mémoire le nombre de calcul qu'il a fait.

Comme ce qui importe, c'est le nombre d'opération, on peut le précalculer, puis ensuite, appliquer les opérations sur le contenu du fichier. Au lieu de calculer chaque étape récursivement (ce qui rend le programme long), on va créer une liste des valeurs, et s'en servir au lieu de recalculer à chaque fois.

Ensuite, on va recalculer la suite, la trier (on peut faire un sort en stockant tout dans une liste), puis finalement, calculer le hash!

```python

import binascii
import hashlib

to_check = "data4096.u32"
with open(to_check, "rb") as f:
    data = f.read()

to_sort = [int(binascii.hexlify(data[4*i:4*(i+1)][::-1]),16) for i in range(len(data)//4)]

def count(x, L):
    global n
    if x < 2:
        return x
    start = 0
    mid = 0
    intervals = []
    while start < x:
        mid = (start + x)>>1
        intervals += [(start, mid)]
        start = mid+1
    res = 0
    for i in intervals:
        res += L[i[1]-i[0]]+ L[x-1 - i[0]]
    return res + len(intervals)

def xor(a, b):
    return b''.join([bytes([a[i]^b[i]]) for i in range(len(a))])

L = [0, 1]
for i in range(2, 2048):
    new_el = count(i, L)
    L += [new_el]

res = 0
for i in range(len(to_sort)-1, 0 ,-1):
    start = 0
    mid = i >> 1
    end = i
    res += L[mid-start]
    res += L[end-(mid++1)]
    res += 1
print("f(4096)=", res)
to_sort.sort()
start = res
data = b""
for i in range(len(to_sort)):
    start *= 0x19660d
    start = (start + 0x3c6ef35f)&0xffffffff
    data += binascii.unhexlify('%08x'%(to_sort[i]^start))[::-1]
print('FCSC{'+hashlib.sha256(data).hexdigest()+'}')

```

Ensuite, on va calculer la valeur
# Flag

![](/assets/images/FCSC2020/Slowppiness/9.png)


