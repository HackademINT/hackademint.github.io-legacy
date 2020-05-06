---
title: "Patchinko"
subtitle: "Challenge de Pwn du FCSC 2020"
published: true
author: "Bdenneu"
ctf: "FCSC"
annee: "2020"
---

# L'énoncé

Venez tester la nouvelle version de machine de jeu Patchinko ! Les chances de victoire étant proches de zéro, nous aidons les joueurs. Prouvez qu'il est possible de compromettre le système pour lire le
fichier flag .

[patchinko.bin](/writeup-scripts/2019-2020/FCSC/patchinko.bin)


Note : le service permet de patcher le binaire donné avant de l'exécuter.

Service : nc challenges1.france-cybersecurity-challenge.fr 4009

# On reverse!

Dans ce challenge, on a le droit de modifier un byte du binaire avant son exécution. Voici la fonction main :

![](/assets/images/FCSC2020/Patchinko/1.png)

Le programme récupere l’entrée utilisateur (fgets), lance strlen dessus pour nous demander si l’on s’est déjà connecté, puis lance un jeu de divination.
L’idée la plus simple que j’ai trouvé ici a été de modifier le call sym.imp.strlen pour le transformer en call sym.imp.system vu que le call est relatif à l’endroit où il est appelé.
Dans la plt, system est juste après strlen (écart de 0x10) :

![](/assets/images/FCSC2020/Patchinko/2.png)

Le call de sym.imp.strlen dans main est à l’offset 0x888.

![](/assets/images/FCSC2020/Patchinko/3.png)

Notre payload sera donc 889 (emplacement du call ) et 43 (0x33+0x10) pour qu’il execute system au lieu de strlen.

![](/assets/images/FCSC2020/Patchinko/4.png)

# Flag

```
FCSC{b4cbc07a77bb0984b994c9e34b2897ab49f08524402c38621a38bc4475102998}
```
