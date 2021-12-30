---
title: "PWN.aarchibald"
ctf: "ECSC préqualifications"
annee: "2019"
published: true
author: "Bdenneu"
---

# Enoncé
```
Exploitez le binaire fourni pour en extraire flag.
nc challenges.ecsc-teamfrance.fr 4005


```

# Exploitation

On récupère le pseudo code d'IDA:

![aarchibald1](/assets/images/Préquals_ECSC/aarchibald1.png)

Le programme récupère l'entrée utilisateur, xor chaque caractère avec 0x36 et la compare avec une chaine en mémoire. Ensuite, le programme vérifie si une variable en mémoire a changé ou pas. Il est alors très probable qu'il s'agisse de buffer overflow.
Première étape, on récupère le mot de passe:

![aarchibald2](/assets/images/Préquals_ECSC/aarchibald2.png)

On obtient le mot de passe **SuPerpAsSworD**.
Par réflexe, j'ai entré des caractères dans le nc en plus pour creuser la piste du buffer overflow.
On obtient un shell:

![aarchibald3](/assets/images/Préquals_ECSC/aarchibald3.png)

# Le flag

ECSC{32fb7ccc57121703b0a9a401e269e774c561b2bc}

