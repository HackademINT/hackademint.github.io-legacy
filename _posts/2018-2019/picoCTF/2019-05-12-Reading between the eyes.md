---
title: "STEGANO.Reading between the eyes"
ctf: "picoCTF"
annee: "2018"
published : true
author: "Archonte"
---

On a ici une jolie image de Husky vraiment trop mignon.

![Il est vraiment trop mignon !](/assets/images/husky.png)

En effectuant une analyse bit à bit, on se rend comte que les bits de poids 0 de chaque couleur sont anormalement vides ...
Sauf tout en haut à gauche !


Comme on a déterminé qu'il y a quelquechose d'important sur ces bits, on les extrait pour regarder à quoi ça ressemble si on ne considère qu'eux.

![Tadaaa !](/assets/images/reading.png)

Tadaaaaaaa !!

Le flag est donc picoCTF{r34d1ngb37w33n 7h3_by73s}.
