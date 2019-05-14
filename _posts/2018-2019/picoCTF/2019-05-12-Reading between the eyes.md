---
title: "STEGANO.Reading between the eyes"
ctf: "picoCTF"
annee: "2018"
published : true
author: "Archonte"
---

On a ici une jolie image de Husky vraiment trop mignon.

![Il est vraiment trop mignon !](/assets/images/husky.png)

En effectuant une analyse bit à bit grâce à stegsolve, on se rend comte que les bits de poids 0 de chaque couleur sont anormalement vides ...
Sauf tout en haut à gauche !
ci-dessous la différence entre les bits bleus 0 et 1:

![Il est vraiment trop mignon !](/assets/images/bit0husky.png)
![Il est vraiment trop mignon !](/assets/images/bit1husky.png)

Comme on a déterminé qu'il y a quelquechose d'important sur ces bits, on les extrait pour regarder à quoi ça ressemble si on ne considère qu'eux.

![Tadaaa !](/assets/images/extracthusky.png)

Tadaaaaaaa !!

Le flag est donc picoCTF{r34d1ngb37w33n 7h3_by73s}.
