---
title: "WEB.Jack\_The\_Ripper"
ctf: "ECSC préqualifications"
annee: "2019"
published: true
author: "Bdenneu"
---

# Enoncé
```
Connectez-vous à l'adresse http://challenges.ecsc-teamfrance.fr:8002

```

# Situation

Nous avons accès à trois fichier.

![Jack The Ripper](/assets/images/Préquals_ECSC/jack_the_ripper1.png)

# Etude en local

En étudiant les fichiers, on remarque que les cookies sont gérés avec la fonction sérialize. 
De plus, il y a une variable debug associée à Core qui permet d'afficher le hash md5 du mot de passe d'un utilisateur. Ainsi, envoyer sur le site un cookie valide en local avec la variable debug mise à True affichera le mot de passe admin.

![En local](/assets/images/Préquals_ECSC/jack_the_ripper2.png)

En envoyant le cookie qui indique que l'on est connecté avec le debug qui vaut True:

![Sur le site](/assets/images/Préquals_ECSC/jack_the_ripper3.png)

# Le flag

ECSC{3ab6be9c0d274e7eeac6f20f4bee7d8b26303e44}

