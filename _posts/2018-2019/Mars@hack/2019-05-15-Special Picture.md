---
title: "Special Picture"
ctf: "Mars@Hack"
annee: "2019"
published : true
author: "Archonte"
---

Le but est de trouver le point commun de ces trois pictures :

![Première](/asssets/images/black.jpg)
![Deuxième](/asssets/images/brown.jpg)
![Troisième](/asssets/images/white.jpg)

Ce challenge peut être résolu en quelques secondes en se servant du plus puissant [outil](https://www.google.com/) à votre disposition.

En effet, en faisant une recherche d'image inversée, on trouve ce genre d'[article](https://natmchugh.blogspot.com/2014/11/three-way-md5-collision.html) sur l'obsolescence du md5.

Pour les novices ou c'est qui auraient oublilé, un petit [rappel](https://fr.wikipedia.org/wiki/Fonction_de_hachage) sur ce qu'est un Hash.

Les 3 images ont le même hash MD5, le flag est MARS{MD5}.
