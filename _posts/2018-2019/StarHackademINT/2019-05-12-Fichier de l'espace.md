---
title: "STEGANO.Fichier de l'espace"
ctf: "StarHackademINT"
annee: "2018"
published : true
author: "Archonte"
---

Dans ce challenge, on découvre l'intérêt de lire les challenges...
En effet, là où certains perdront des heures à explorer des techniques de stéganographie, un observateur avisé utilisant la technique secrète ancestrale de "Lire l'énoncé" se rendra compte d'un indice important fourni par l'auteur.

Cette indication est "Un fichier peut en cacher un autre".

![Une indication ...](/assets/images/SpaceFile1.png)

La première chose qui doit vous mettre la puce à l'oreille est le mot "fichier" et non "image" ...
La stéganographie se concentrant souvent sur le fait de cacher une image dans une autre image, le mot "fichier" semble inapproprié. Sauf, bien sûr, dans un cas, celui des archives où un "fichier", l'archive, en "cache" d'autres qu'il contient.

'''Bash
unzip alien.jpeg
'''

Cette commande nous donne entre autres un dossier Thumbnail qui contient une image.

![Le flag :)](/assets/images/SpaceFile2.png)

Cette image contient le flag :)
Mais comme zTeeed a trop compressé l'image, elle n'est plus lisible :'(
Allez le voir pour le flag xD
