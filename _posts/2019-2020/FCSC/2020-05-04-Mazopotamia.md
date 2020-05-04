---
title: "Mazopotamia"
subtitle: "Challenge de Misc du FCSC 2020"
published: true
author: "Headorteil"
ctf: "FCSC"
annee: "2020"
---

# L'énoncé

Mazopotamia

Bienvenue en Mazopotamia ! Pour obtenir le flag, vous devrez vous échapper de plusieurs labyrinthes comme celui montré ci-dessous.

![](/assets/images/FCSC2020-mazopotamia.png)

Toutes les informations sont données ici :
nc challenges2.france-cybersecurity-challenge.fr 6002

# TL;DR

On nous donne accès à un netcat qui nous envoie des photos de labyrinthes et le but est de les résoudre et de renvoyer le chemin, au total on nous envoie 30 labyrinthes sachant que la particularité de ces labyrinthes est qu'ils ont des portes de couleurs qu'on ne peut emprunter que dans un certain ordre définit en haut de l'image (et cet ordre et le nombre de couleurs changent bien sûr) on applique donc un simple algorithme récursif de résolution de labyrinthe un peu adapté au problème.

# Parsing

Quand on ouvre une connexion netcat avec `nc challenges2.france-cybersecurity-challenge.fr 6002`, on obtient l'output suivant:

```
Hello stranger, welcome in Mazopotamia.
To check whether you are worthy to be here, please try to get out of our mazes.
I will send you a PNG maze as a base64-encoded string.
Send me how you would like to move within the maze:
  N to go North
  S to go South
  E to go East
  W to go West
Along your journey, you will encounter coloured doors: you can only cross them, but cannot stay on a cell with a door.
Important: you can only cross doors in a predetermined order, which is listed on top of each problem.
Try to escape all the mazes in less than 30 seconds!
I will give you a beautiful flag if you succeed ;-)

Here is an example:
------------------------ BEGIN MAZE ------------------------
iVBORw0KGgoAAAANSUhEUgAAAsAAAAOACAIAAAC7YlJgAAA44ElEQVR4nO3d
d2BVhd34/3tJQGQJCgqiFkStKAXFhVpnaSviQhwoarVa96q1oOVxAYK7tmot
...
AABhAgIACBMQAECYgAAAwgQEABAmIACAMAEBAIQJCAAgTEAAAGECAgAIExAA
QJiAAADCBAQAECYgAICw/wfUufMIea1K7gAAAABJRU5ErkJggg==
------------------------- END MAZE -------------------------
One solution to get ouf of this maze is: NENNWWNWWSSSES

Press a key when you are ready...
Here is a new maze as a PNG base64-encoded string.
------------------------ BEGIN MAZE ------------------------
iVBORw0KGgoAAAANSUhEUgAAA0AAAAQACAIAAABH/q73AAA+aklEQVR4nO3d
e4BVdb3w/72ZYbgLCJZICHgD0wOIPnIxFcu8JCZIKZqWt+h4O+YltTRRQAVN
...
AADBCDgAgGAEHABAMAIOACAYAQcAEIyAAwAIRsABAAQj4AAAgvn/AG9C+ggB
qjiOAAAAAElFTkSuQmCC
------------------------- END MAZE -------------------------
Now enter your solution:
>>> 
```

1ère étape : le parsing des données : on nous envoie un png encodé en base64, on va donc le décoder et le découper en morceaux élémentaires (ici en blocs de 64 * 64) afin d'avoir des données exploitables.

On extrait ensuite l'ordre des changements de couleur en faisant attention à pouvoir traiter les cas ou on aurait plusieurs couleurs possibles.
Pour gérer et stocker les couleurs, j'ai choisi de garder le valeur G du RGB qui est différente à chaque fois dans les couleurs proposées.

Puis on regarde où sont l'entrée et la sortie (pour ça j'ai extrait les blocs de flèches entrantes et sortantes dans un labyrinthe et j'enregistre leur position dans le labyrinthe actuel).

Enfin on construit le labyrinthe.

# Résolution

Une fois qu'on peut travailler avec des données propres, y'a plus qu'à!

J'ai fait un algo récursif qui gère les 8 cas suivants : il y'a une case blanche dans les 4 directions possibles ou une porte colorée dans les 4 directions possibles.

Si on est dans un de ces 8 cas, on emprunte le 1er possible qui vérifie les condition suivante :
  - La case à atteindre n'a pas encore été atteinte dans l'état dans lequel nous l'atteindront (par état j'entends dernière couleur empruntée) et 
  - Si le chemin est une porte de couleur, ai-je le droit de passer par cette porte?

Puis on rappelle la même fonction en ayant pris soin d'avoir actualisé notre marquage (sans oublier que pour chaque case du labyrinthe on peut avoir eu plusieurs états) ainsi que notre chemin déjà emprunté et la dernière couleur empruntée si on vient de passer par une porte.

Dès qu'on tombe sur la sortie, on stocke le chemin et on envoie la valeur.

# Le code

```python
#! /usr/bin/python3

import base64
import pwn
from PIL import Image
import io
import numpy


white = 255
black = 0

uparrow = list(Image.open("./uparrow.png").getdata())

downarrow = list(Image.open("./downarrow.png").getdata())


def img2pix(im):
    im_arr = numpy.frombuffer(im.tobytes(), dtype=numpy.uint8)
    im_arr = im_arr.reshape((im.size[1], im.size[0], 3))
    return im_arr[32][32][1]


def decode_img(msg):
    msg = base64.b64decode(msg)
    buf = io.BytesIO(msg)
    img = Image.open(buf)
    return img


def crop(im, height, width):
    total = []
    imgwidth, imgheight = im.size
    for i in range(imgheight//height):
        images = []
        for j in range(imgwidth//width):
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            images.append(im.crop(box))
        total.append(images)
    return total


def findcolors(images):
    colors = []
    i = 1
    cond = True
    while cond:
        pix = img2pix(images[1][2*i])
        if pix == white:
            break
        i += 1
        colors.append(pix)
    return colors


def purge_junk(images):
    useful_images = images[3:-1]
    pixels = []
    for i in useful_images:
        pixels.append([])
        for j in i[1:-1]:
            pixels[-1].append(img2pix(j))
    pixels.reverse()
    return pixels


def findentrance_exit(images):
    j = 1
    for i in images[-2][2:-2]:
        data = list(i.getdata())
        if data == uparrow:
            entrance = (j, 0)
        if data == downarrow:
            exit = (j, 0)
        j += 1
    return entrance, exit


def exploreMaze(maze, current_state, colors, path, explored, exit):
    global globalepath
    a, o, c = current_state
    explored[o][a].append(c)

    if a == exit[0] and o == exit[1]:
        globalepath = path
        return

    if maze[o][a + 1] == white and c not in explored[o][a + 1]:
        exploreMaze(maze, [a + 1, o, c], colors, path + "E", explored, exit)

    if maze[o][a - 1] == white and c not in explored[o][a - 1]:
        exploreMaze(maze, [a - 1, o, c], colors, path + "W", explored, exit)

    if maze[o + 1][a] == white and c not in explored[o + 1][a]:
        exploreMaze(maze, [a, o + 1, c], colors, path + "N", explored, exit)

    if maze[o - 1][a] == white and c not in explored[o - 1][a]:
        exploreMaze(maze, [a, o - 1, c], colors, path + "S", explored, exit)

    if (maze[o][a + 1] == colors[(c + 1) % len(colors)]) and ((c + 1) % len(
            colors) not in explored[o][a + 2]):

        exploreMaze(maze, [a + 2, o, (c + 1) % len(colors)],
                    colors, path + "E", explored, exit)

    if (maze[o][a - 1] == colors[(c + 1) % len(colors)]) and ((c + 1) % len(
            colors) not in explored[o][a - 2]):

        exploreMaze(maze, [a - 2, o, (c + 1) % len(colors)],
                    colors, path + "W", explored, exit)

    if (maze[o + 1][a] == colors[(c + 1) % len(colors)]) and ((c + 1) % len(
            colors) not in explored[o + 2][a]):

        exploreMaze(maze, [a, o + 2, (c + 1) % len(colors)],
                    colors, path + "N", explored, exit)

    if (maze[o - 1][a] == colors[(c + 1) % len(colors)]) and ((c + 1) % len(
            colors) not in explored[o - 2][a]):

        exploreMaze(maze, [a, o - 2, (c + 1) % len(colors)],
                    colors, path + "S", explored, exit)


if __name__ == "__main__":
    global globalepath
    a = pwn.remote("challenges2.france-cybersecurity-challenge.fr", 6002,
                   level="error")
    a.recvuntil(b"Press a key when you are ready...")
    a.sendline("")
    i = 0
    log = pwn.log.progress("Path")
    while i < 31:
        ctenu = a.recvuntil(b">>> ")
        maze = ctenu.decode().split(
            '------------------------')[2].replace("\n", "")
        img = decode_img(maze)
        images = crop(img, 64, 64)
        colors = findcolors(images)
        entrance, exit = findentrance_exit(images)
        pixels = purge_junk(images)
        firstcolor = colors.index(pixels[entrance[1] + 1][entrance[0]])
        pixels[entrance[1] + 1][entrance[0]] = black
        # print(colors)
        explored = [[[] for _ in range(len(pixels[0]))] for _ in
                    range(len(pixels))]
        globalepath = ""
        solve = exploreMaze(pixels, [entrance[0], entrance[1] + 2,
                                        firstcolor], colors, 'N',
                            explored, exit)
        log.status(str(i + 1) + " > " + globalepath)
        a.sendline(globalepath.encode())
        i += 1
    log.success(a.recv().decode())
```

# Flag

Et hop en quelques secondes on obtient le flag :
`Congratulations! Here is your flag: FCSC{a630a31265cdc8516f5926d636f62d4c38ed4bf743bc84db095f1cc78cd3fb7f}`
