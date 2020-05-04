---
title: "Baby Xoring Networks"
subtitle: "Challenge de Misc du FCSC 2020"
published: true
author: "Headorteil"
ctf: "FCSC"
annee: "2020"
---

# L'énoncé

Nous vous proposons l'étude des réseaux de XOR (Xoring Networks) et le problème XNP associé.

Vous devez d'abord valider cette version avec des problèmes de petites dimensions avant de pouvoir accéder aux autres problèmes de plus grandes dimensions.

Plus d'informations ici : [Xoring Networks](assets/html/Xnw.html)

nc challenges2.france-cybersecurity-challenge.fr 6007

# TL;DR

On a deux matrices A et B, on veut passer de la matrice A à la matrice B et les seules opérations autorisées sont m xors de lignes `(Lx <- LX ^ Ly)` et une infinité de permutations de lignes. (rien que de simplifier l'énoncé en ce problème j'ai mis 1 jour :'( )
On va donc appliquer un algo de pivot de Gauss (modifié bien entendu, de sorte à ce qu'il ne fasse que des xors) sur A et sur B jusqu'à avoir A et B triangulaires supérieures(At et Bt), un fois cela fait on passe de At à Bt en faisant les xors nécessaires sur At en la parcourant de gauche à droite et de haut en bas. On obtient donc un réseau nous permettant de passer de A à B en recoupant toutes nos opérations et en les réorganisant mais évidemment on dépasse le nombre d'opérations maximal, on va donc faire du post-processing sur notre liste de xors pour essayer de la simplifier (en terme de nombres d'opérations).
Et comme ça ne suffit toujours pas quand les dimensions deviennent plus grandes, on va aussi faire du pre-processing totalement random jusqu'à tomber sur une matrice d'entrée qui nous donne un nombre d'opérations valide.

# La découverte

Quand on se connecte au netcat avec `nc challenges2.france-cybersecurity-challenge.fr 6007`, on nous donne cet input par exemple:

```raw
+++++++++++++++++++++++++++++++++++++++++
+++++ Xoring Network Problem Server +++++
+++++++++++++++++++++++++++++++++++++++++
I will send you several hand-crafted XNP instances, and you will send me one solution for each.
Once I have decided you solved enough, I will give you the flag ;-)
Good luck!

--------- BEGIN XNP ---------
4
6
0x2 0xc
0x3 0x1
0xf 0x4
0xa 0x2
---------- END XNP ----------

Now enter your solution. First line must be the number of XORs reached.
(Do not forget the 'XNP SOLUTION' delimiters.)
```

A partir de la récupère m et n (6 et 4) et on va construire nos matrices A et B en mettant les valeurs des inputs en binaire.

A sera l'état initial et B l'état à atteindre, ici :
$$
\begin{equation*}
A = 
\begin{pmatrix}
0 & 0 & 1 & 1 \\
0 & 0 & 1 & 0 \\
1 & 1 & 1 & 1 \\
0 & 1 & 1 & 0 \\
\end{pmatrix}
, B = 
\begin{pmatrix}
1 & 0 & 0 & 0 \\
1 & 0 & 1 & 0 \\
0 & 0 & 0 & 1 \\
0 & 1 & 0 & 0 \\
\end{pmatrix}
\end{equation*}
$$

Maintenant qu'on a des données exploitables, on va pouvoir, bah... les exploiter du coup.

# L'algorithme

Mon algorithme de résolution se compose de trois parties bien distinctes : le pre-processing complètement aléatoire, le coeur et pour finir le post-processing qui vise à compresser le nombre d'opérations.

## Le cœur de l'algorithme

### L'implémentation naïve

La partie principale de la résolution de l'algorithme est un algorithme de Gauss un peu modifié : on va transformer A et B en parallèle pour les rendre triangulaires supérieures, puis il sera facile de passer de l'une à l'autre.

Pour cela, on commence par les trier de sorte à avoir le triangle en bas à gauche de notre matrice avec un maximum de zéros pour pouvoir choisir un pivot.

Sur B, le tri donnerait :
$$
\begin{equation*}
tri(B) = 
\begin{pmatrix}
1 & 0 & 0 & 0 \\
1 & 0 & 1 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 0 & 1 \\
\end{pmatrix}
\end{equation*}
$$

On voit que il y'a un 1 de trop sur la 1ère colonne pour avoir une matrice triangulaire supérieures.
On va donc xorer les 2 premières lignes et mettre le résultat dans la 2ème :

$$
\begin{equation*}
B1 = 
\begin{pmatrix}
1 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 0 & 1 \\
\end{pmatrix}
\end{equation*}
$$

Ensuite on re trie et on refait la même chose pour les colonnes suivantes jusqu'à avoir une matrice triangulaires supérieures. Ici on a de la chance, il n'y a pas plus d'opérations à faire.

On fait donc ça sur A et B.

On se retrouve donc avec :

$$
\begin{equation*}
At = 
\begin{pmatrix}
1 & 1 & 1 & 1 \\
0 & 1 & 1 & 0 \\
0 & 0 & 1 & 1 \\
0 & 0 & 0 & 1 \\
\end{pmatrix}
, Bt = 
\begin{pmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1 \\
\end{pmatrix}
\end{equation*}
$$

Ensuite, du fait de la triangularité de At et Bt, il est très simple de passer de l'une à l'autre : on parcourt At de gauche à droite (i) et de haut en bas (j) et chaque fois qu'on tombe sur une valeur différente de Bt, on remplace At[j] par At[j] ^ At[i] puisqu'on sait que At[i] a un 1 à la position j et que des 0 avant (triangularité de At).

Par exemple, ici la 1ere étape serait de modifier At[0][1] qui est différente de Bt[0][1], on applique donc ce que je viens de décrire pour arriver à :

$$
\begin{equation*}
At1 = 
\begin{pmatrix}
1 & 0 & 0 & 1 \\
0 & 1 & 1 & 0 \\
0 & 0 & 1 & 1 \\
0 & 0 & 0 & 1 \\
\end{pmatrix}
\end{equation*}
$$

Et on itère jusqu'à obtenir Bt.

On aura bien sur conservé les opérations effectuées et on a donc une liste de xors (liste_xors(A -> At) + liste_xors(At -> Bt) + inverse(liste_xors(B -> Bt))) nous permettant de passer de A à B à une permutation près qu'on peut bien entendu retrouver très facilement.

Plutôt facile me diriez vous?

Oui mais non, l'algo est très rapide et ce peu importe la dimension (y'a des limites mais bon, ici n reste en dessous de 100 donc c'est très rapide), le problème est que on a un nombre d'opérations limitées et c'est un problème de taille parce que cet algorithme ne s'optimise pas trivialement en terme d'opérations à effectuer.

### Les optimisations

J'ai donc pensé à des optimisations faisables : à l'étape de la triangularisation, on peut choisir quelles lignes sont les plus pertinentes à xorer puisqu'en général on a plusieurs choix possibles.
On choisit donc le xor qui nous rapproche le plus vite d'une matrice triangulaire i.e le xor qui nous donne un 1 le plus à droite possible.

Ensuite, on peut choisir de mettre la nouvelle ligne résultant des lignes i et j de A soit dans i, soit dans j.
Pour se décider, on regarde quelles lignes i ou j sont les plus proches des lignes k et l de B qu'on a choisi de xorer et on les préserve, en choisissant donc de remplacer l'autre ligne de A par le xor choisi (parreil pour B).

## Le post processing

On nous donne donc une liste d'opérations à tous les coups mais une liste qui n'est pas optimisée.
J'ai donc cherché des patterns simplifiables et en ai trouvé 2, vous pourrez voir dans le code la fonction optichemin qui traite 2 cas et qui permet de gagner des xors.

## Le pré processing

Malgré tout ça, on n'arrive pas à tous les coups à avoir des chemins de longueur inférieurs à m.
On va donc essayer au hasard des xors à effectuer avant de lancer notre algo en espérant que le résultat ne soit pas trop sous-optimal.

Pour cela, on teste tous les xors possibles puis, toutes les 2-combinaisons de xors possibles puis toutes les 3-combinaisons... jusqu'à m.
Dès qu'on trouve un chemin correct on s'arrête, on récupère la liste des permutations, on envoie le résultat et on recommence avec les nouveaux inputs.

# Le code

Le préviens tout de suite : c'est assez lourd mais j'ai essayé de faire en sorte que ça soit le plus clair et lisible possible.

```python
#! /usr/bin/python3

import pwn
import numpy as np
import itertools


def xorlines(l1, l2):
    """Un simple xor de lignes """
    return [i ^ j for i, j in zip(l1, l2)]


def permlines(A, l1, l2, permuts):
    """Une simple permutation de lignes"""
    temp1 = A[l1].copy()
    temp2 = A[l2].copy()
    A[l1] = temp2
    A[l2] = temp1
    permuts[l1], permuts[l2] = permuts[l2], permuts[l1]
    return A, permuts


def tri(A, permuts, c, n):
    """Ce tri trie les lignes à partir de i avec un ordre d'inportance des
    valeurs croissants de gauche a droite."""
    lval = []
    for i in range(c, n):
        lval.append(0)
        for j in range(c, n):
            lval[-1] += (2 ** (n - j)) * A[i][j]
    slval = lval[::]
    slval.sort()
    slval.reverse()
    B = A.copy()
    permutsB = permuts.copy()
    for i in range(c, n):
        index = c + lval.index(slval[i - c])
        B[i] = A[index]
        permutsB[i] = permuts[index]
    return B, permutsB


def xorconc(x1, x2, perm1, perm2):
    """Concatene les xors de A et B pour en faire une suite cohérente"""
    nx2 = []
    for i in x2:
        nx2.append((perm1[perm2.index(i[0])], perm1[perm2.index(i[1])]))
    while len(x1) > 0 and len(nx2) > 0:
        if x1[-1] == nx2[-1]:
            x1.pop()
            nx2.pop()
        else:
            break
    return x1 + nx2[::-1]


def bonnespermuts(A, B, xors):
    """Retrouver la liste des permutations"""
    for i in xors:
        A[i[0]] = xorlines(A[i[0]], A[i[1]])
    permuts = []
    for i in A:
        for j in range(len(B)):
            if (i == B[j]).all() and j not in permuts:
                permuts.append(j)
    return permuts


def optichemin(xors):
    """Post processing pour essayer de simplifier des opérations"""
    ctr = 0
    while ctr < len(xors):
        i, j = xors[ctr]
        # 1er patern à simplifier
        if (j, i) in xors[ctr+1:]:
            end = ctr + 1
            valid = True
            while xors[end] != (j, i):
                k, m = xors[end]
                if k == i or m == i or k == j:
                    valid = False
                    break
                end += 1
            if valid:
                xors.pop(ctr)
                for x in range(end, len(xors)):
                    k, m = xors[x]
                    if k == i:
                        k = j
                    elif k == j:
                        k = i
                    if m == i:
                        m = j
                    elif m == j:
                        m = i
                    xors[x] = (k, m)
                ctr = 0
                continue
        # 2eme patern à simplifier
        if (i, j) in xors[ctr+1:]:
            end = ctr + 1
            valid = True
            while xors[end] != (i, j):
                k, m = xors[end]
                if m == i or k == j:
                    valid = False
                    break
                end += 1
            if valid:
                xors.pop(ctr)
                xors.pop(end - 1)
                ctr = 0
                continue
        ctr += 1
    return xors


def solved(A, B, n):
    """Retourne la liste des xors à effectuer pour passer de A à B modulo une
    permutation des lignes"""
    permutsA = list(range(n))
    permutsB = list(range(n))
    xorA = []
    xorB = []
    for i in range(n - 1):

        # 1ere étape : trouver quels xors sont les plus pertinents pour obtenir
        # le plus rapidement possible des matrices triangulaires supérieures.

        A, permutsA = tri(A, permutsA, i, n)
        B, permutsB = tri(B, permutsB, i, n)

        while A[i + 1][i] == 1 or B[i + 1][i] == 1:
            if A[i + 1][i] == 1 and B[i + 1][i] == 1:
                j = i
                bestxorA = [0, 0, -1]
                while j < n and A[j][i] == 1:
                    k = i
                    while k < n and A[k][i] == 1:
                        if j != k:
                            testxorsLines = xorlines(A[j], A[k])
                            ctr = n
                            for indice in range(n):
                                if testxorsLines[indice] == 1:
                                    ctr = indice
                                    break
                            if ctr >= bestxorA[2]:
                                bestxorA = [j, k, ctr]
                        k += 1
                    j += 1

                xlineA = xorlines(A[bestxorA[0]], A[bestxorA[1]])

                j = i
                bestxorB = [0, 0, -1]
                while j < n and B[j][i] == 1:
                    k = i
                    while k < n and B[k][i] == 1:
                        if j != k:
                            testxorsLines = xorlines(B[j], B[k])
                            ctr = n
                            for indice in range(n):
                                if testxorsLines[indice] == 1:
                                    ctr = indice
                                    break
                            if ctr >= bestxorB[2]:
                                bestxorB = [j, k, ctr]
                        k += 1
                    j += 1

                xlineB = xorlines(B[bestxorB[0]], B[bestxorB[1]])

                # 2eme étape : déterminer si où on met notre nouvelle ligne
                # dans matrice[bestxorB[0]] ou dans matrice[bestxorB[1]]
                # pour ça on regarde quelles lignes de A et B parmi les
                # lignes susceptibles d'être modifiées sont les plus proches
                # et on préserve ces lignes

                ctr = 0
                testxorsLines = xorlines(A[bestxorA[0]], B[bestxorB[0]])
                for indice in range(n):
                    ctr += (2 ** (n - indice)) * (testxorsLines[indice] ^ 1)

                ctr1 = 0
                testxorsLines1 = xorlines(A[bestxorA[0]], B[bestxorB[1]])
                for indice in range(n):
                    ctr1 += (2 ** (n - indice)) * (testxorsLines1[indice] ^ 1)

                ctr2 = 0
                testxorsLines2 = xorlines(A[bestxorA[1]], B[bestxorB[0]])
                for indice in range(n):
                    ctr2 += (2 ** (n - indice)) * (testxorsLines2[indice] ^ 1)

                ctr3 = 0
                testxorsLines3 = xorlines(A[bestxorA[1]], B[bestxorB[1]])
                for indice in range(n):
                    ctr3 += (2 ** (n - indice)) * (testxorsLines3[indice] ^ 1)

                maxi = max(ctr, ctr1, ctr2, ctr3)

                if maxi == ctr:
                    A[bestxorA[1]] = xlineA
                    B[bestxorB[1]] = xlineB
                    xorA.append((permutsA[bestxorA[1]], permutsA[bestxorA[0]]))
                    xorB.append((permutsB[bestxorB[1]], permutsB[bestxorB[0]]))
                elif maxi == ctr1:
                    A[bestxorA[1]] = xlineA
                    B[bestxorB[0]] = xlineB
                    xorA.append((permutsA[bestxorA[1]], permutsA[bestxorA[0]]))
                    xorB.append((permutsB[bestxorB[0]], permutsB[bestxorB[1]]))
                elif maxi == ctr2:
                    A[bestxorA[0]] = xlineA
                    B[bestxorB[1]] = xlineB
                    xorA.append((permutsA[bestxorA[0]], permutsA[bestxorA[1]]))
                    xorB.append((permutsB[bestxorB[1]], permutsB[bestxorB[0]]))
                else:
                    A[bestxorA[0]] = xlineA
                    B[bestxorB[0]] = xlineB
                    xorA.append((permutsA[bestxorA[0]], permutsA[bestxorA[1]]))
                    xorB.append((permutsB[bestxorB[0]], permutsB[bestxorB[1]]))

            # On traite à part le cas ou il reste seulement des opérations sur
            # B

            elif B[i + 1][i] == 1:
                j = i
                bestxorB = [0, 0, -1]
                while j < n and B[j][i] == 1:
                    k = i
                    while k < n and B[k][i] == 1:
                        if j != k:
                            testxorsLines = xorlines(B[j], B[k])
                            ctr = n
                            for indice in range(n):
                                if testxorsLines[indice] == 1:
                                    ctr = indice
                                    break
                            if ctr > bestxorB[2]:
                                bestxorB = [j, k, ctr]
                        k += 1
                    j += 1

                xlineB = xorlines(B[bestxorB[0]], B[bestxorB[1]])

                ctr = 0
                testxorsLines = xorlines(A[i], B[bestxorB[0]])
                for indice in range(n):
                    ctr += (2 ** (n - indice)) * (testxorsLines[indice] ^ 1)

                ctr1 = 0
                testxorsLines1 = xorlines(A[i], B[bestxorB[1]])
                for indice in range(n):
                    ctr1 += (2 ** (n - indice)) * (testxorsLines1[indice] ^ 1)

                maxi = max(ctr, ctr1)

                if maxi == ctr:
                    B[bestxorB[1]] = xlineB
                    xorB.append((permutsB[bestxorB[1]], permutsB[bestxorB[0]]))
                else:
                    B[bestxorB[0]] = xlineB
                    xorB.append((permutsB[bestxorB[0]], permutsB[bestxorB[1]]))

            # On traite à part le cas ou il reste seulement des opérations sur
            # A

            else:
                j = i
                bestxorA = [0, 0, -1]
                while j < n and A[j][i] == 1:
                    k = i
                    while k < n and A[k][i] == 1:
                        if j != k:
                            testxorsLines = xorlines(A[j], A[k])
                            ctr = n
                            for indice in range(n):
                                if testxorsLines[indice] == 1:
                                    ctr = indice
                                    break
                            if ctr > bestxorA[2]:
                                bestxorA = [j, k, ctr]
                        k += 1
                    j += 1

                xlineA = xorlines(A[bestxorA[0]], A[bestxorA[1]])

                ctr = 0
                testxorsLines = xorlines(B[i], A[bestxorA[0]])
                for indice in range(n):
                    ctr += (2 ** (n - indice)) * (testxorsLines[indice] ^ 1)

                ctr1 = 0
                testxorsLines1 = xorlines(B[i], A[bestxorA[1]])
                for indice in range(n):
                    ctr1 += (2 ** (n - indice)) * (testxorsLines1[indice] ^ 1)

                maxi = max(ctr, ctr1)

                if maxi == ctr:
                    A[bestxorA[1]] = xlineA
                    xorA.append((permutsA[bestxorA[1]], permutsA[bestxorA[0]]))
                else:
                    A[bestxorA[0]] = xlineA
                    xorA.append((permutsA[bestxorA[0]], permutsA[bestxorA[1]]))

            A, permutsA = tri(A, permutsA, i, n)
            B, permutsB = tri(B, permutsB, i, n)

    # A ce stade, A et B sont triangulaires supérieures, il est donc simple de
    # passer de l'une à l'autre :

    for i in range(1, n):
        for j in range(i):
            if A[j][i] != B[j][i]:
                A[j] = xorlines(A[i], A[j])
                xorA.append((permutsA[j], permutsA[i]))
    return xorconc(xorA, xorB, permutsA, permutsB)


if __name__ == "__main__":
    r = pwn.remote("challenges2.france-cybersecurity-challenge.fr", 6007,
                   level="error")
    log = pwn.log.progress("Probleme")
    line = 1
    while True:
        a = r.recvrepeat(1).decode()
        if 'FCSC' in a:
            r.close()
            log.success(a)
            break
        a = a.split("---------")[2].split('\n')[1:-1]
        n = int(a[0])
        m = int(a[1])
        log.status('n°' + str(line) + " en dim : " + str(n))
        matgch = np.zeros((n, len(a) - 2), dtype=int)
        matdte = np.zeros((n, len(a) - 2), dtype=int)
        for i in range(2, len(a)):
            mbin = [bin(int(j[2:], 16))[2:].
                    rjust(n, "0") for j in a[i].split(" ")]
            gch = [int(j) for j in mbin[0]]
            dte = [int(j) for j in mbin[1]]
            matgch[i - 2] = gch
            matdte[i - 2] = dte
        A = matgch.transpose()
        B = matdte.transpose()
        a = solved(A.copy(), B, n)
        a = optichemin(a)
        # A partir d'ici c'est la partir pre processing en full brute force
        compt = 0
        tmppossperm = list(itertools.product(list(range(n)), repeat=2))
        possperm = []
        for i in tmppossperm:
            if i[0] != i[1]:
                possperm.append(i)
        while len(a) > m:
            tmppossfin = list(itertools.product(possperm, repeat=compt))
            possfin = []
            for i in tmppossfin:
                repeat = False
                for j in range(len(i) - 1):
                    if i[j] == i[j + 1]:
                        repeat = True
                        break
                if not repeat:
                    possfin.append(i)
            for perm in possfin:
                copa = A.copy()
                perm = list(perm)
                for i in perm:
                    copa[i[0]] = xorlines(copa[i[0]], copa[i[1]])
                a = perm + solved(copa, B, n)
                a = optichemin(a)
                if len(a) <= m:
                    break
            compt += 1
        taille = len(a)
        perms = bonnespermuts(A, B, a)
        solve = "----- BEGIN XNP SOLUTION -----\n"
        solve += str(taille) + '\n'
        for i in a:
            x, y = str(i[0]), str(i[1])
            solve += x + " " + y + '\n'
        for i in perms[::-1]:
            solve += str(i) + '\n'
        solve += "------ END XNP SOLUTION ------\n"
        r.send(solve.encode())
        line += 1
```

Voila voila.

# Le flag

Ici on est sur la version Baby alors les dimensions s'arrêtent à 5, on trouve donc assez rapidement le résultat : FCSC{75b6b3c00ff050847712a584f8abbc6c7fc693f6d968025ce19a904c187eef0b}.

Malheureusement ça n'est pas assez performant dès qu'on monte un peu en dimensions, je n'ai donc pas réussi à flag la version "originale" du challenge qui monte jusqu'en dimension 16.
