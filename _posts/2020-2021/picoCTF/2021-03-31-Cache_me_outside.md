---
title: "Cache me outside"
subtitle: "malloc tcache exploit"
published: true
author: "Woni"
ctf: "picoCTF"
annee: "2021"
previewimage: "/assets/images/pico2021/5.png"
---

# Énoncé:
```
While being super relevant with my meme references, I wrote a program to see how much you understand heap allocations.
```
On nous donne la libc, le binaire (heapedit) et le makefile (ça ne sert à rien).

# Ça coince déjà
On ne nous donne pas l'interpréteur allant de paire avec la libc. Cependant, en utilisant la commande `sha256sum`, je me rends compte qu'il s'agit de la même libc que celle d'un autre challenge pour lequel j'ai un exploit et un shell. Je me connecte et je tente de voler l'interpréteur avec `nc` mais cela n'est pas autorisé.

Une fois sur le serveur, il suffit d'encoder le fichier en base64:
```sh
cat /lib64/ld-linux-x86-64.so.2 | base64 -w0
```
Il ne reste plus qu'à le décoder.

## Lancer le binaire

Il faut maintenant patcher le binaire avec la commande suivante:<br>
```sh
patchelf --set-interpreter /path/to/ld-linux.so.2 heapedit && patchelf --set-rpath /path/to/folder/with/libc.so.6/ heapedit
```

Il faut aussi se créer un flag.txt dans le même dossier que le binaire et c'est bon, on peut y aller !

# C'est parti

![](/assets/images/pico2021/1.png)<br>
Le binaire lit deux entrées utilisateur avec scanf, la première avec `%d` et la deuxième avec `%c`, toutes deux sans effet de bords et on contrôle un octet dans la mémoire. <br>
![](/assets/images/pico2021/2.png) <br>

Il y a un grand nombre de malloc, mettons un point d'arrêt juste avant le dernier à 0x400a45.

# Regardons plus en détail
![](/assets/images/pico2021/3.png)<br>
Le flag est bien sur le heap !<br>
![](/assets/images/pico2021/4.png) <br>
Cepandant le malloc final s'effectue sur une zone contenant un message qui n'est pas le flag, puis affiche ce qui s'y trouve.

Nous allons modifier un pointeur utilisé par malloc pour le forcer à allouer sur un chunk où se trouve le flag grâce au tcache.
<br>
Le tcache permet de gérer les allocations de mémoire récemment libérée pour réallouer ces zones rapidement sur le heap, il fonctionne avec des listes chaînées de pointeurs sur le heap.

Regardons les chunks et le tcache:<br>
![](/assets/images/pico2021/5.png) <br>

Nous avons plusieurs candidats où rediriger le malloc.

Voyons où est stocké le pointeur vers la mauvaise zone de mémoire afin de la corrompre avant qu'elle ne soit utilisée: <br>

![](/assets/images/pico2021/6.png) <br>
C'est donc ce pointeur qui se situe à 0x602088 qui va régir l'emplacement du prochain malloc.

Mettons un point d'arrêt juste après le dernier scanf pour voir ce qu'il advient des données que le programme demande.
<br>

![](/assets/images/pico2021/7.png) <br>

# L'exploitation

Le programme ajoute la valeur de l'adresse entrée avec 0x6034a0 avec l'instruction `add rdx, rax`, il faut donc entrer `0x602088 - 0x6034a0 = -5144` pour effectivement écrire à 0x602088.

Mais comment écrire l'adresse d'une zone avec le flag ? Nous n'avons droit qu'à un octet, il faut donc être très précis.
La valeur déjà en mémoire à 0x602088 est 0x603890.
<br>

![](/assets/images/pico2021/5.png)

La zone à 0x603800 est parfaite !
Il faut donc écrire un octet nul à 0x602088 qui va alors contenir 0x603800 au lieu de 0x603890

Essayons donc le payload suivant:
```sh
perl -e 'print "-5144\n\x00\n"' | ./heapedit
```
<br>

![](/assets/images/pico2021/8.png) <br>

Ok, ça marche en local, essayons à distance. <br>
![](/assets/images/pico2021/9.png)

# Flag
picoCTF{f2d58262f377f31fddf8576b59226f2a}
