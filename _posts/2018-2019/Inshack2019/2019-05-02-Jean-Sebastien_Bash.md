---
title: "CRYPTO.Jean-Sebastien_Bash"
ctf: "InsHack"
annee: "2019"
published: true
author: "Bdenneu"
---
# Description
Nous nous retrouvons sur une machine qui nous precise que pour lancer une commande, il faut utiliser /cmd "arg" où arg est la commande chiffrée en AES CBC.

![JSB1](/assets/images/Inshack2019/inshack2019_jsb1.png)

# Rappel
L'AES CBC est une méthode de chiffrement par bloc de 16 caractères avec rétroaction du bloc précédent sur le suivant. Comme l'entrée n'est pas forcément un bloc de 16, un padding est ajouté à la fin. Il consiste à completer le dernier bloc avec des caractères qui indiquent la longueur du padding. Par exemple, si le dernier bloc est de longueur 11 (avant chiffrement), il sera complété par 5 \x05. Ainsi, on peut savoir si le bloc est valide en le déchiffrant.

![JSB2](/assets/images/Inshack2019/inshack2019_jsb2.png)

# Solution
La première idée à avoir est que le dechiffrement se fait bloc par bloc.
![JSB3](/assets/images/Inshack2019/inshack2019_jsb3.png)
Premierement, si l'on a qu'un seul bloc en entrée, on ne pourra pas intéragir avec la sortie. Cependant, si l'on en met deux, on pourra se servir du premier bloc pour modifier le plaintext en sortie du deuxieme. On pourra alors par exemple mettre un ";" pour lancer une nouvelle commande. Il faudra juste chercher le dernier caractère du premier bloc chiffré pour que la commande se lance (mettre un \x01 à la fin du bloc dechiffré suffit).

![JSB4](/assets/images/Inshack2019/inshack2019_jsb4.png)

Deuxièmement, on va effectuer un xor entre le deuxième bloc dechiffré et le bloc dechiffré que l'on souhaite avoir (comme le premier bloc chiffré est composé de \x00, on n'a pas besoin de le xor).
```python
s1 = [i for i in b"Dr\x95\x8d\xad~S\xa1'\xe8-\xe1\x8c"]
s2 = [i for i in b";cat flag.txt"]
print("0000"+"".join(["0" * ((2 - len(hex(s1[i] ^ s2[i])[2:]))%2) + hex(s1[i] ^ s2[i])[2:] for i in range(13)])+"ed"+"0"*32)
```

![JSB5](/assets/images/Inshack2019/inshack2019_jsb5.png)

# Le flag
On obtient alors : INSA{or4cle_P4dd1ng} 
