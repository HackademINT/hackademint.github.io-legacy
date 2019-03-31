---
title: "Cheesy"
ctf: "TamuCTF"
annee: "2019"
published: true
author: "Bdenneu"
---
# Description
Nous avons accés à un binaire.
Lorsque l'on exécute celui ci, on obtient le texte suivant:

![Cheesy1](/assets/images/TamuCTF2019/tamuctf2019_cheesy1.png)

Il s'agit de phrases en base64, dont une qui nous indique que nous avons raté le flag.
# Solution
En lançant un string sur le fichier, on obtient une chaine qui n'est pas affiché de base.
Il s'agit de la base64 du flag.

![Cheesy2](/assets/images/TamuCTF2019/tamuctf2019_cheesy2.png)

# Le flag
On obtient: gigem{3a5y_R3v3r51N6!}
