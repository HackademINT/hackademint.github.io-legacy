---
title: "STEGANO.Escadron"
ctf: "Mars@Hack"
annee: "2019"
published : true
author: "Archonte"
---

On est ici face à une épreuve unique de stéganographie, assez simple techniquement mais poussant u npeu la réflexion.

![L'image fournie.](/assets/images/Mars@Hack/map.jpeg)

En se servant d'exiftool on se rend compte qu'il y a quelque chose de caché.

```Bash
exiftool map.jpeg
```
On le déterre avec exif, puis on refait un exiftool à la recherche d'informations.
```Bash
exif -e map.jpeg

mv map.jpeg 1vion.jpeg
exiftool Avion.jpeg
```

![L'image récupérée ainsi, un petit avion.](/assets/images/Mars@Hack/1vion.jpeg)

On a alors deux informations capitales :

   1) Il y a à nouveau une image à chercher
   2) Les métadonnées contiennent une position GPS
   
On note bien ces coordonnées et on reprend le même manège : exif puis exiftool puis on recommence jusqu'à ce qu'exiftool nous prévienne que l'on est arrivé à la dernière poupée russe.

Voici les coordonnées obtenues :

01vion.jpeg	48 deg 51' 39.80" N	2 deg 8' 52.30" E
02vion.jpeg	48 deg 48' 48.70" N	2 deg 11' 13.70" E
03vion.jpeg	48 deg 41' 58.00" N	2 deg 18' 1.10" E
04vion.jpeg	46 deg 9' 39.00" N	2 deg 7' 29.40" E
05vion.jpeg	48 deg 41' 6.90" N	2 deg 11' 37.70" E
06vion.jpeg	43 deg 7' 28.40" N	12 deg 53' 17.00" E
07vion.jpeg	48 deg 49' 54.80" N	2 deg 21' 45.00" E
08vion.jpeg	45 deg 46' 17.40" N	4 deg 52' 31.70" E
09vion.jpeg	48 deg 55' 28.00" N	2 deg 21' 36.60" E
10vion.jpeg	41 deg 22' 38.20" N	2 deg 6' 48.10" E
11vion.jpeg	40 deg 26' 44.90" N	3 deg 41' 19.90" W
12vion.jpeg	49 deg 1' 14.40" N	2 deg 30' 49.80" E

Maintenant, ouvrez votre logiciel de cartes en ligne préféré ! Google earth Pro est gratuit et fait très bien l'affaire mais même la version mobile de Maps fonctionnerait. Il va falloir reconnaître aux coordonnées fournies des lettres formées par des bâtiments, peintes au sol ou formées par la végétation !

![Voici ce que l'on voit aux coordonnées fournies par 1vion.jpeg. On y reconnaît un "S".](/assets/images/Mars@Hack/1lettre.jpeg)

En agissant ainsi pour les 12 images on obtinet le code suivant : "STEGANOPOWER"

Le flag est donc MARS{STEGANOPOWER} !
