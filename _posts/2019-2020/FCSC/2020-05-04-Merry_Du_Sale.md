---
title: "Merry"
subtitle: "Challenge de Crypto du FCSC 2020"
published: true
author: "Headorteil"
ctf: "FCSC"
annee: "2020"
---

# L'énoncé

Un serveur a été conçu pour utiliser un algorithme d'échange de clés avec ses clients. Cet algorithme génère et garde le même bi-clé pour plusieurs requêtes. Il notifie aussi ses clients quand l'échange a échoué et que la clé partagée n'est pas la même. Votre but est de retrouver la clé secrète du bi-clé généré par le serveur.

[merry.py](/writeup-scripts/2019-2020/FCSC/merry.py)

Service : nc challenges1.france-cybersecurity-challenge.fr 2001

# TL;DR

On nous donne donc accès à un netcat ainsi qu'à un code python. Quand on se connecte au netcat avec `nc challenges1.france-cybersecurity-challenge.fr 2001`.

```
Here are the server public parameters:
A = eJxs3Xf4v3P9//+3rSg...
B = eJxd2WnYj2UaBnDhTWg...
Possible actions:
  [1] Key exchange
  [2] Get flag
  [3] Exit
>>> 
```

On nous donne un A et un B qui sont 2 matrices encodées en base 64. On peut faire autant de "Key exchange" qu'on veut pour leak de l'information sur \__S_a et \__E_a afin de les retrouver et de les renvoyer pour flag.

Je précise tout de suite que la résolution de ce challenge est très TRES contre-optimisée (oui j'invente des concepts mais vous allez voir, ma méthode mérite au moins ça), donc si vous vous attendez à une solution élégante ou même rapide, passez votre chemin.

Et puis d'abord ça fonctionne alors hein, voila, non mais.

# Analyse

On a A et B, on pourra donc retrouver E_a facilement quand on aura retrouvé S_a puisque : `self.B     = np.mod(self.A * self.__S_a + self.__E_a, self.q)`
On a donc une infinité d'essais sur le key exchange pour connaître S_a.

La ligne qui va nous intéresser est : `key_a = self.__decode(np.mod(C - np.dot(U, self.__S_a), self.q))`.
Ici, on contrôle C et U et on comparera key_a avec une valeur qu'on contrôle et on obtiendra une valeur booléenne : notre input (key_b) est égal ou non à key_a.

À partir de là, comment récupérer de l'information?

On va poser U la patrice nulle de dimension m_bar * n avec seulement un 1 en position (0, 0).

$$
\begin{equation*}
U = 
\begin{pmatrix}
1 & 0 & \cdots & 0 \\
0 & 0 & \cdots & 0 \\
0 & 0 & \cdots & 0 \\
0 & 0 & \cdots & 0 \\
\end{pmatrix}
\end{equation*}
$$

Ensuite posons :
$$
\begin{equation*}
C = 
\begin{pmatrix}
257 & 257 & 257 & 257 \\
0   & 0   & 0   & 0 \\
0   & 0   & 0   & 0 \\
0   & 0   & 0   & 0 \\
\end{pmatrix}
\end{equation*}
$$

On voit que si
$$
\begin{equation*}
S_a = 
\begin{pmatrix}
1      & 0      & -1     & 1 \\
x      & y      & z      & t \\
\vdots & \vdots & \vdots & \vdots & \\
\end{pmatrix}
\end{equation*}
$$

Alors :
$$
\begin{equation*}
C - np.dot(U, S_a) = 
\begin{pmatrix}
256 & 257 & 258 & 256 \\
0   & 0   & 0   & 0 \\
0   & 0   & 0   & 0 \\
0   & 0   & 0   & 0 \\
\end{pmatrix}
\end{equation*}
$$

On passe ensuite dans la fonction decode qui applique simplement à tous les éléments de son input deux fonctions: recenter et null_and_round.
Ici (et c'est là la stupidité de ma solution), on ne va pas utiliser recenter puisque on a choisi d'utiliser 257 comme valeur de base, peu importe si l'input est 256, 257 ou 258, recenter ne changera pas notre matrice, par contre null_and_round oui.

Je n'ai quand même pas choisi 257 au hasard, c'est une valeur limite de null_and_round : `round((257 / (self.q / 4))) != round((256 / (self.q / 4)))`, le 1er donne 1 et le 2ème 0.
En essayant toutes les combinaisons de 1 et de 0 sur le 1ère ligne de key_b, on va pouvoir déterminer quels endroits de S_a contiennent des 1.

Malheureusement `round((257 / (self.q / 4))) == round((258 / (self.q / 4)))`, on ne peut donc pas différencier les 0 des -1.
Ici : deux réactions possibles :
  - 1 vous avez un cerveau et vous vous dites que c'est quand même bizarre de pas exploiter recenter, vous cherchez donc une valeur plus pertinente que 257 afin de pouvoir distinguer vos 3 cas : -1, 0 ou 1 d'un coup
  - 2 vous n'avez pas beaucoup dormi ces derniers temps et puis à quoi bon faire simple et rapide quand on peut faire lent et compliqué? Vous refaites donc la même méthode que vous avez faite pour distinguer les 1 mais avec 256 au lieu de 257 pour distinguer les 0 du reste, c'est pas compliqué, il suffit de sortir itertools et de générer toutes les combinaisons possibles de 256 et 257 sur la 1ère ligne de C puis de compter combien de fois on obtient des 0 ou des 1, avec des petits calculs que je ne vais pas détailler on peut retrouver la valeur de chaque élément.

On a donc retrouvé théoriquement la 1ère ligne de S_a, on peut refaire la même chose en décalant le 1 de U d'un cran vers la droite, on va alors trouver la 2ème ligne... Jusqu'à avoir complètement S_a !

Un fois S_a trouvé, c'est très simple de retrouver E_a en faisant : `E_a = np.mod(B - np.dot(A, S_a), q)` en faisant bien attention à remplacer les valeurs égales à q-1 par -1 (à cause du module).

Plus qu'à encoder S_a et E_a, à les envoyer et hop, on a le flag.

# Le code

```python
#! /usr/bin/python3

import numpy as np
from zlib import decompress, compress
from base64 import b64encode as b64e, b64decode as b64d
import pwn
import itertools


if __name__ == "__main__":
    q = 2 ** 11
    n = 280
    n_bar = 4
    m_bar = 4
    valplus = 2**8 + 1
    valmoins = 2**8
    S_a = np.zeros((n, n_bar), dtype=np.int64)
    r = pwn.remote("challenges1.france-cybersecurity-challenge.fr", 2001,
                   level="error")
    # Bien pratique pour faire des tests en local :
    # r = pwn.process(['python3',  './merry.py'], level="error")
    ctenu = r.recvuntil(b'>>> ').decode()
    _, a, b = ctenu.split(" = ")
    a = a.split('\n')[0]
    b = b.split('\n')[0]
    A = np.reshape(np.frombuffer(decompress(b64d(a)), dtype=np.int64),
                   (n, n))
    B = np.reshape(np.frombuffer(decompress(b64d(b)), dtype=np.int64),
                   (n, n_bar))
    log = pwn.log.progress("Ligne")
    for i in range(n):
        U = np.zeros((m_bar, n), dtype=np.int64)
        U[0][i] = 1
        u = b64e(compress(U.tobytes()))

        moinsun = [0, 0, 0, 0]
        zero = [0, 0, 0, 0]
        un = [0, 0, 0, 0]
        exitfor = False
        # Le fameux itertools de la débilité
        for j in itertools.product([valplus, valmoins], repeat=4):
            if exitfor:
                exitfor = False
                break
            C = np.zeros((m_bar, n_bar), dtype=np.int64)
            for k in range(len(j)):
                C[0][k] = j[k]
            c = b64e(compress(C.tobytes()))

            for k in itertools.product([0, 1], repeat=4):
                key_b = np.zeros((m_bar, n_bar), dtype=np.int64)
                for l in range(len(k)):
                    key_b[0][l] = k[l]
                kb = b64e(compress(key_b.tobytes()))

                r.sendline("1")
                r.recvuntil(" = ")
                r.sendline(u)
                r.recvuntil(" = ")
                r.sendline(c)
                r.recvuntil(" = ")
                r.sendline(kb)
                a = r.recvuntil(">>> ").decode()
                if "Success" in a:
                    # ici on compte les valeurs pour retrouver les -1, les 0 et les 1
                    for indice in range(len(C[0])):
                        if C[0][indice] == valmoins and key_b[0][indice] == 1:
                            moinsun[indice] += 1
                        if C[0][indice] == valmoins and key_b[0][indice] == 0:
                            zero[indice] += 1
                        if C[0][indice] == valmoins and key_b[0][indice] == 0:
                            un[indice] += 1
                        if C[0][indice] == valplus and key_b[0][indice] == 1:
                            moinsun[indice] += 1
                        if C[0][indice] == valplus and key_b[0][indice] == 1:
                            zero[indice] += 1
                        if C[0][indice] == valplus and key_b[0][indice] == 0:
                            un[indice] += 1
                    ct = 0
                    # et ici la formule que je n'ai pas expliqué mais en gros si un
                    # compteur dépasse 8, c'est que c'est la bonne valeur
                    # source : tkt crois moi ça marche
                    for indice in range(len(C[0])):
                        if moinsun[indice] > 8:
                            S_a[i][indice] = -1
                            ct += 1
                        elif zero[indice] > 8:
                            S_a[i][indice] = 0
                            ct += 1
                        elif un[indice] > 8:
                            S_a[i][indice] = 1
                            ct += 1

                    if ct == 4:
                        exitfor = True
                        break

        log.status(str(i + 1) + "/" + str(n))

    E_a = np.mod(B - np.dot(A, S_a), q)
    for i in range(len(E_a)):
        for j in range(len(E_a[0])):
            if E_a[i][j] == 2047:
                E_a[i][j] = -1
    sa = b64e(compress(S_a.tobytes()))
    se = b64e(compress(E_a.tobytes()))
    r.sendline("2")
    r.recvuntil(" = ")
    r.sendline(sa)
    r.recvuntil(" = ")
    r.sendline(se)
    log.success(r.recvline().decode())
```

# Flag

Après SEULEMENT quelques heures (c'est quand même marrant que le but du challenge qui suivait celui-ci soit limité en requêtes, ça m'a obligé à activer mon cerveau et à changer ma méthode :/), on a un superbe flag: FCSC{4aed95f4374652d9ed3af1080e7a7d0c1cc798aa70592780f2e81a11fb78bd4e}
