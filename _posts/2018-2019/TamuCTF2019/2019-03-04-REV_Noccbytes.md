---
title: "REV.Noccbytes"
ctf: "TamuCTF"
annee: "2019"
published: true
author: "Bdenneu"
---
# Description
Nous avons accés à un binaire.
Lorsque l'on exécute celui ci, on nous demande une clé produit. Le but est de la trouver. Pour obtenir le flag, il faut envoyer le bon mot de passe sur rev.tamuctf.com sur le port 8188.

Accès au binaire: [binaire](/writeup-scripts/2018-2019/TamuCTF2019/noccbytes)

# Solution

Décomposons le binaire:

![Obfuscaxor1](/assets/images/TamuCTF2019/tamuctf2019_noccbytes1.png)

Le programme demande un mot de passe, lance la fonction passCheck_char, et si la sortie est 1, affiche le flag.

![Obfuscaxor2](/assets/images/TamuCTF2019/tamuctf2019_noccbytes2.png)

Le programme compare l'entrée et une chaine en mémoire. Si la valeur est la même, la sortie est 1.
On va donc voir quelles sont les valeurs comparées.

![Obfuscaxor3](/assets/images/TamuCTF2019/tamuctf2019_noccbytes3.png)

L'entrée est comparé avec "WattoSays". C'est le mot de passe.

![Obfuscaxor4](/assets/images/TamuCTF2019/tamuctf2019_noccbytes4.png)

On se connecte et on récupere le flag.

# Le flag
On obtient : gigem{Y0urBreakpo1nt5Won7Work0nMeOnlyMon3y}
