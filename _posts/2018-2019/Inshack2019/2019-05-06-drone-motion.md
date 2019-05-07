---
title: "drone-motion"
subtitle: "Challenge issu de l'Inshack2019"
author: "patate"
ctf: "InsHack"
annee: "2019"
team: "HackademINT"
---

# > Enoncé

We intercepted a drone flying above a restricted area and retrieved a [log](/writeup-scripts/2018-2019/Inshack2019/drone-motion/5e97cfb3f4c64201c201a1703440c397f91be74b.tar.gz) from its memory card.

Help us find out what this drone was doing above our heads!

Flag must match the regex: `INSA\{[a-z0-9]+\}`

# > Analyse du problème


## Fichiers fournis

On nous fournit une [archive](/writeup-scripts/2018-2019/Inshack2019/drone-motion/drone-motion.zip) dont nous pouvons extraire un [fichier](/writeup-scripts/2018-2019/Inshack2019/drone-motion/sensors.log) contenant les logs de mouvement d'un drone.



## But du challenge

On comprend que le but du challenge est de reconstituer la trajectoire du drone en question.



## Méthode de résolution

Afin de reconstituer notre trajectoire, nous utiliserons la librairie python matplotlib qui permet notamment de tracer des graphes en 3d.




# > Résolution


## Des vitesses et des accélérations

En ouvrant le fichier de logs, on s'aperçoit qu'on dispose de l'historique des accélérations et des vecteurs vitesse successifs du drone. Ce qui nous intéresse étant les positions successives du drone, la définition du vecteur position par rapport à l'accéléation et à la vitesse nous permet d'établir les expressions suivantes: 
x(t+1) = x(t)+ acc(t+1) + vx(t+1)
y(t+1) = y(t)+ acc(t+1) + vy(t+1)
z(t+1) = z(t)+ acc(t+1) + vz(t+1)



## Proposition de script

Le script suivant devrait permettre de récupérer le graphe que l'on veut obtenir.

```python
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import re


log = open('./sensors.log', 'r').read()

acc = list(map(lambda a: float(a), re.findall(r'accel: ([-]?\d)\[drone\]\(DEBUG\)> d', log)))
vx = list(map(lambda a: float(a), re.findall(r'x=([-]?\d\.\d+),', log)))
vy = list(map(lambda a: float(a), re.findall(r'y=([-]?\d\.\d+),', log)))
vz = list(map(lambda a: float(a), re.findall(r'z=([-]?\d\.\d+)\)', log)))

x = [0]
y = [0]
z = [0]

for i in range(len(acc)):
    x.append(x[-1] + 3*acc[i] + 3*vx[i])
    y.append(y[-1] + 3*acc[i] + 3*vy[i])
    z.append(z[-1] + 3*acc[i] + 3*vz[i])


fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, c='r', marker='.')

ax.set_xlabel('x')
ax.set_xlabel('y')
ax.set_xlabel('z')


plt.show()
```

On obtient l'affichage suivant:

![graphe](/assets/images/Inshack2019-drone-motion-graphe.png)

N'ayant pas trouvé le moyen de zoomer correctement avec matplotlib, j'ai sélectionné dans mon script petit à petit les portions du graphe, ce qui m'a permis de déchiffrer le flag dont voici le premier morceau:

![zoom](/assets/images/Inshack2019-drone-motion-zoom.png)



## Difficultés rencontrées pour lire le flag

Si on s'aperçoit rapidement que le flag ne contient que des valeurs hexadécimales (les lettres sont affichées en majuscules mais elles doivent être en minuscule dans le flag pour matcher la regex qu'on nous donne), il n'est pas facile de différencier les E des F. 

Ainsi, la première version du flag que j'ai obtenu: INSA{66333db55f9ca50f9f9c4c94dc45250532832dc4681d531f0fab6d1a255c8578} n'était pas correcte.

J'ai alors généré toutes les possibilités de flags en alternant les E et les F avec le script suivant:
```python
import itertools

flag = '66333db55{}9ca50{}9{}9c4c94dc45250532832dc4681d531{}0{}ab6d1a255c8578'

print('\n'.join([ 'INSA{'+flag.format(*permutation)+'}' for permutation in list(itertools.product('ef', repeat=5))]))
```



## Flag

En essayant tous les flags possibles sur la plateforme, on finissait par trouver le bon flag parmi cette [liste](/writeup-scripts/2018-2019/Inshack2019/drone-motion/flags.txt).
