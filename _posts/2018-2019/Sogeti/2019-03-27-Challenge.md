---
title: "Challenge Accepted !"
subtitle: "Challenge tiré du CTF de qualification pour le Cyberescape de Sogeti"
author: "patate"
ctf: "Sogeti"
team: "HackademINT"
---

# Enoncé

Serez-vous capable de battre la machine ? Celle-ci est programmée pour vous envoyer un message chiffré. Votre tâche est de déchiffrer ce challenge et le renvoyer à la machine en moins de 2 secondes.

Une copie du programme vous est fournie.

nc quals.shadow-league.org 5887


# Analyse du problème

## But du challenge

Le but du challenge est de se connecter à une machine distante afin d’y récupérer un message chiffré et de renvoyer le message déchiffré en moins de 2 secondes. 

Voici une capture de la connection au challenge:

![Test connexion](/assets/images/Challenge1.png)

## Comprendre le fonctionnement côté serveur

On dispose d’une copie du programme côté serveur [ici](/writeup-scripts/Sogeti/challenge_debug.py) pour comprendre le fonctionnement du chiffrement.

On observe que le programme commence par générer le message aléatoire de longueur 64 constitué de lettres et de chiffres. Une clé secrète est ensuite générée, le hash SHA256 de cette clé secrète est utilisé en tant que clé pour chiffrer en AES CBC le message initialement généré. Le programme nous affiche l’hexa du message ainsi chiffré. Enfin, le programme vérifie que le message que nous lui envoyons correspond bien à celui qui a été généré et nous donne le flag le cas échéant.


# Résolution

On comprend que le point clé du challenge est de retrouver la clé secrète utilisée pour chiffrer le message en AES CBC (il n’y a pas d'autre problème puisque le vecteur d’initialisation est donné dans le script).

## Des nombres aléatoires?

Pour cela, on s’intéresse tout d’abord à l’étape de génération de la clé secrète. On comprend que la clé secrète, initialement à la valeur 0xffffffff,  est xorée avec dix valeurs générées aléatoirement. Toutefois, on observe que la fonction random.seed() est utilisée pour initialiser le générateur de nombres pseudo-aléatoires. Chaque seed entrainant une certaine séquence de nombres “aléatoires” définis et le seed étant défini ici par une valeur aléatoire entre 1 et 10000, il n’y a donc que dix mille possibilités différentes pour la séquence de dix nombres “aléatoires” générés pour xorer la clé secrète.

## Un affichage oublié !!

Il faudrait donc qu’on retrouve ce seed mais il semble a priori impossible de savoir quelle valeur de seed a été utilisée. C'est là que les lignes
```
# @TODO REMOVE THIS IN PRODUCTION !
pprint("DEBUG - Secret key is %s...%s" % (secret.hexdigest()[:15], secret.hexdigest()[-15:]), "WARNING")
```
doivent attirer notre attention. 

Cet affichage, malencontreusement oublié là par la production, nous permet de déterminer le seed qui a été utilisé. Il suffit alors de tester chaque valeur de seed entre 1 et 10000 jusqu’à trouver celle qui nous permet de trouver une clé secrète dont le début et la fin correspondent aux morceaux affichés. On peut ainsi obtenir la clé secrète en entier !


# Proposition de solution

## Script

Voici une proposition de [script](/writeup-scripts/Sogeti/challenge.py) pour résoudre ce challenge:
```
#!/usr/bin/python2

import pwn
import random
import hashlib
from Crypto.Cipher import AES

r = pwn.remote('quals.shadow-league.org', 5002)

print(r.recvuntil('key is ').decode())
secretkey = r.recvline()
print(secretkey.decode())
deb = secretkey[:15].decode()
fin = secretkey[-17:-2].decode()

for s in range(1, 10000):
    random.seed(s)
    key = 0xffffffff
    for i in range(10):
        key ^= random.randint(0x00000000, 0xffffffff)
    secret = hashlib.sha256(str(key))
    skey = secret.hexdigest().decode()
    if skey[:15] == deb and skey[-15:] == fin:
        break

print(r.recvuntil('Challenge : '))
challenge = r.recvline()[:-2].decode('hex')

encryption_suite = AES.new(secret.digest(), AES.MODE_CBC, 'LmQHJ6G6QnE5LxbV')
decrypted_challenge = encryption_suite.decrypt(challenge)

r.sendline(decrypted_challenge.encode())
print(r.recvuntil('}'))
```
## Exécution

L’exécution renvoie:
```
$ ./prog.py
[+] Opening connection to quals.shadow-league.org on port 5002: Done
[*] Random initialization vector
[+] Seed generated !
[*] Generating secret key
[+] Secret key generated !
[!] DEBUG - Secret key is 
3d3fffde0f03d49...a8507c459068ea6

[+] Encrypted Challenge : 
Give me the challenge (2s) > ufkQQpGmif4mQxKXxeePYtpGXZSB2ldeQDvlXQNvfyvY1yG84ZIK8qXgyMaoZmgR
[+] Here is your flag : SCE{Str0ng_s3eds_are_adv1s3d...}
[*] Closed connection to quals.shadow-league.org port 5002
```

## Flag

On récupère le flag: SCE{Str0ng_s3eds_are_adv1s3d...}
