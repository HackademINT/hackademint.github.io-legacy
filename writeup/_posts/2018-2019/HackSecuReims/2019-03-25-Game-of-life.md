---
title: "Game-of-life"
ctf: "HackSecuReims"
annee: "2019"
author: "Headorteil"
published: true
type: web
---

# Introduction

Dans de challenge, on dispose d'un site qui nous demande de lui renvoyer l'étape
n + \<étapes\> de l'état actuel d'une matrice composée de cases blanches et de
cases noires. On peut lire qu'il s'agit du jeu de la vie, on peut donc deviner
qu'on doit itérerer selon les règles de "Conway's game of life". On nous demande
de répéter l'opération, j'ai donc mis mon code de résolution dans une boucle while.


# Solution

```python
import time
import math
import requests
import numpy

def voisins(i,j, taille):
    """retourne la liste des voisins de matrice[i][j]"""
    T = []
    if i != 0:
        T.append([i-1, j])
        if j != 0:
            T.append([i-1, j-1])
        if j != taille-1:
            T.append([i-1, j+1])
    if i != taille-1:
        T.append([i+1, j])
        if j != 0:
            T.append([i+1, j-1])
        if j != taille-1:
            T.append([i+1, j+1])
    if j != 0:
        T.append([i, j-1])
    if j != taille-1:
        T.append([i, j+1])
    return T

def viv(T):
    """retourne le nombre de voisins vivants parmi T qui est la liste des voisins"""
    nb=0
    for c in T:
        nb += M[c[0]][c[1]]
    return nbr

r = requests.get("http://10.22.6.197/speed/3_rEivfOKq-Dueb-xgzG-sKXdDJeahGWaPHnu/server.php", headers={"Cookie":"PHPSESSID=pjc4h1440bdp7384e9cjdkkup7"})

while 1:
    print(r.content)

    data = r.json()
    R=data["cases"]

    taille = math.sqrt(len(R))

    M = [[0]*taille]*taille
    M=numpy.array(M)

    #On transforme les données en matrice parce que en ligne c'est pas très pratique
    for i in range(len(R)):
        M[i//taille][i%taille] = R[i]

    N=[[0]*taille]*taille
    N=numpy.array(N)

    for Z in range(data["etapes"]):
    #on fait une boucle pour arriver au rang demandé

        for i in range(taille):
            for j in range(taille):
                a = viv(voisins(i, j, taille))
                if M[i][j] == 0 and a == 3:
                    N[i][j] = 1
                elif M[i][j] == 1 and a < 2:
                    N[i][j] = 0
                elif M[i][j] == 1 and (a == 2 or a == 3):
                    N[i][j] = 1
                elif M[i][j] == 1 and a > 3:
                    N[i][j] = 0
        M = numpy.copy(N)

    R=[0]*(taille**2)

    #On retransforme notre matrice en liste pour renvoyer au bon format
    for i in range(taille):
        for j in range(taille):
            R[i*taille+j]=N[i][j]

    # On met un sleep, sinon on nous reproche de flood
    time.sleep(2)

    data = {}
    for i in range(taille**2):
        data["cases[" + str(i) + "]"] = R[i]

    r = requests.post('http://10.22.6.197/speed/3_rEivfOKq-Dueb-xgzG-sKXdDJeahGWaPHnu/server.php',headers={"Cookie":"PHPSESSID=pjc4h1440bdp7384e9cjdkkup7"},data=data)
```

# Le flag

On obtient alors le code suivant : 3G5w26l1-xtBL-TBS7-jZs1Kpsf2pmjFgfR

On peut alors rentrer le code dans le champ dédié sur le site et on obtient
alors le flag suivant : URCACTF{o6tV6KFi-WdPZ-c9g1-aBOCiv9gsDDeAvjd}
