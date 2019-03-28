---
title: "TP Ressources HackademINT"
subtitle: "HackademINT, Comment ça marche ?"
author: "zTeeed"
team: "HackademINT"
titlepage: true
toc: true
toc-own-page: true
titlepage-color: "607D8B"
titlepage-text-color: "FFFFFF"
titlepage-rule-color: "FFFFFF"
titlepage-rule-height: 1
colorlinks: true
---

# La communication
## Facebook/Twitter
Objectif: Obtenir un fil d'actualité technique, être le plus actif possible pour
augmenter notre visibilité.\
\
![Facebook: Loïc Hackdemint](images/facebook.png)
![Twitter: HackademINT](images/twitter.png)

\pagebreak

## La Mailing List

Les mails servent uniquement à faire passer les informations les plus
importantes. La quantité de mails doit rester restreinte au maximum. On ne doit pas
avoir plus 3/4 mails dans la semaine. Les périodes de rentrée font évidemment exception.

## CTFTime

CTFTime est la plateforme qui recense l'activité des équipes de CTF sur le
plan international. Son intérêt majeur réside dans la visibilité des CTFs
organisés et dans notre visibilité personnelle. En effet, après avoir rédigé
des writeups sur le site, il faut ajouter une proposition de solution sur la
page qui concerne le CTF afin d'augmenter notre visibilité et le trafic sur
notre site web.
\
\
![Interface CTFTime](images/ctftime.png)

\pagebreak

## Discord

Discord est notre outil de communication en interne, on y établit toutes les
discussions en ce qui concerne notre travail sur les challenges de CTFs ou ceux
des autres plateformes dédiées à l'apprentissage de la sécurité informatique.
C'est notre meilleur outil pour s'entraider et c'est comme ça que l'on
Progresse. Il ne faut donc pas hésiter à être actif afin d'augmenter votre
interaction avec les autres membres. Cela vous profitera à tous.
\
\
![Interface Discord](images/discord.png)

\pagebreak

# Containers / Machines Virtuelles

- C'est quoi un hyperviseur ? \

> En informatique, un hyperviseur est une plate-forme de virtualisation qui
> permet à plusieurs systèmes d'exploitation de travailler sur une même machine
> physique en même temps.
\

- Ça sert à quoi ? \

> Théoriquement, c'est une couche logicielle très légère (en comparaison à un OS
> classique) qui permet d'allouer un maximum de ressources physiques aux
> containers / machines
> virtuelles.
\

- Quelle est la différence entre un container et une machine virtuelle ?
- Quelles sont leurs caractéristiques ? \

> À la différence de la machine virtuelle, le container partage le noyau de
> l'hôte. Du fait que les conteneurs nécessitent beaucoup moins de ressources, leur
> démarrage est rapide et leur déploiement est simple. La faible utilisation de
> ressources permet une densité plus élevée. Vous pouvez exécuter davantage de
> services sur la même unité matérielle et ainsi réduire vos coûts.
> L’exécution sur le même noyau entraîne une moins bonne isolation comparativement
> aux machines virtuelles.
\

![](images/ctvm.png)

\pagebreak

- Un noyau ?  \

> Un noyau de système d’exploitation, ou simplement noyau, ou kernel (de
> l'anglais), est une des parties fondamentales de certains systèmes
> d’exploitation. Il gère les ressources de l’ordinateur et permet aux différents
> composants — matériels et logiciels — de communiquer entre eux.

![](images/kernel.png)

\pagebreak

## Configuration

Les différents CTs/VMs sont sur un serveur au sein de l'infra MiNET. À
l'origine ils ne disposent pas d'**interface réseau publique** (à MiNET ça concerne
les IPs commençant par 157.159), seulement des **interfaces réseau privées** (par
convention les IPs commencent par 192.168) donc ces machines sont
seulement accessibles derrière le VPN MiNET. En vous connectant via **OpenVPN** au
VPN MiNET, vous êtes routés vers le sous-réseau ayant accès à ces machines.
L'ensemble des membres d'HackademINT n'étant pas forcément à MiNET, il a été
configuré sur ces machines des interfaces publiques.

Plutôt que d'administrer les CTs/VMs en vous connectant via **SSH** sur le noeud de
calcul et de tout faire en lignes de commandes, il existe **Proxmox**, une jolie
interface graphique pour la gestion "clic clic".\
\

![Illustration de l'interface Proxmox accessible à https://192.168.103.206:8006
](images/proxmox.png)

\pagebreak

Pour illustrer la suite de cette présentation, on prendra pour exemple le
container sur lequel est hébergé le site web hackademint.minet.net dont
la configuration est présenté plus bas. Une fois l'interface publique ajoutée, il faut modifier le
fichier de conf suivant:

```bash
[root@HackademINTWebsiteOfficial zteeed]# cat /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
        address 192.168.103.177
        netmask 255.255.255.0

auto eth1
iface eth1 inet static
        address 157.159.40.177
        netmask 255.255.255.192
        gateway 157.159.40.129


[root@HackademINTWebsiteOfficial zteeed]# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
241: eth0@if242: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether e6:0b:eb:ba:f2:f6 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.168.103.177/24 brd 192.168.103.255 scope global
eth0
       valid_lft forever preferred_lft forever
243: eth1@if244: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 06:02:b0:a5:13:df brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 157.159.40.177/26 brd 157.159.40.191 scope global eth1
       valid_lft forever preferred_lft forever
```

\pagebreak

## Quelles machines ?

> Site web hackademint.minet.net
- hackademint.minet.net
- **IP: 157.159.40.177**


> Site web secu.minet.net
- secu.minet.net
- **IP: 157.159.40.173**


> Plateforme de CTF starhackademint.minet.net dans /root
- starhackademint.minet.net
- **IP: 157.159.40.???**


> Site web webstarhackademint.minet.net / Une partie des challenges web et bases
> de données mysql
- webstarhackademint
- **IP: 157.159.40.163**

> Une partie des challenges web de starhackademint.minet.net / Chacun des
> challenge se trouve dans un lxc qui lui est dédié.
- webstarhackademint2
- **IP: 157.159.40.170**


\pagebreak

# Se connecter via SSH

Description du protocole réseau:\

> Secure Shell (SSH) est à la fois un programme informatique et un protocole de
> communication sécurisé. Le protocole de connexion impose un échange de clés de
> chiffrement en début de connexion. Par la suite, tous les segments TCP sont
> authentifiés et chiffrés. Il devient donc impossible d'utiliser un sniffer
> pour voir ce que fait l'utilisateur.

> Le protocole SSH a été conçu avec l'objectif de remplacer les différents
> protocoles non chiffrés comme rlogin, telnet, rcp et rsh.

## Authentification par mot de passe
```bash
ssh root@157.159.40.171
```

## Authentification par clé RSA

- Une clé RSA ?

> Quand vous travaillez avec des clés asymétriques, par principe, vous avez deux
> clés (on parle de paire de clés) : une clé publique, que vous pouvez diffuser
> librement, voire mettre à disposition sur un serveur de clés ; et une clé
> privée qui constitue véritablement votre « identité » et ne doit jamais être
> diffusée : elle reste simplement présente dans votre dépôt de clés
> personnelles.

- Comment créer une paire de clé ?

> www.aidoweb.com/tutoriaux/securiser-acces-ssh-paire-cles-rsa-generation-cles-application-serveur-646

```bash
ssh -i id_rsa zteeed@157.159.40.177 -p 2222
```
\pagebreak

## Utiliser ~/.ssh/config

Le fichier `~/.ssh/config` vous permet de créer des **alias** pour vous
connecter en SSH sans avoir à ressaisir toutes les options. Voici un exemple:

```bash
[zteeed@spider ~]$ cat ~/.ssh/config

Host hackademint.minet.net
  Hostname 157.159.40.177
  User zteeed
  IdentityFile /mnt/Data/Useful/SSH/id_rsa


[zteeed@spider ~]$ ssh hackademint.minet.net
```

# Réparer quand c'est cassé

Quand un challenge sur starhackademint.minet.net ne fonctionne plus c'est
souvent dû à plusieurs éléments:

-  Le serveur web a été coupé
```bash
systemctl status apache2
```
-  La connexion avec certaines bases de données a été rompue (mysql / postgresql)
```bash
systemctl status mysql
```
-  Certains containers (oui oui, un container dans un container) sont éteints (lxc)
```bash
systemctl status lxc
lxc-ls
lxc-info -n ping2
```

\pagebreak

# vim
```bash
sudo apt install vim
```

## C'est quoi ?

Vim est un éditeur de texte mais avec quelques plugins ça devient un vrai
**IDE**. La gestion des plugins de la configuration sont dans le fichier
`~/.vimrc`, vous pouvez piquer le mien sur mon **FTP**:
```bash
wget ftp://zteeed.fr/vimrc
mv vimrc ~/.vimrc`
```

Pour apprendre tous les bindings relatifs à vim, tapez `vimtutor` sur votre
terminal ou cherchez des tutos en ligne : vous allez rapidement devenir très
efficaces pour coder / éditer des fichiers rapidement.

## Comment installer des plugins ?
```bash
sudo apt install git curl
git clone https://github.com/junegunn/vim-plug.git
curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
  https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
vim ~/.vimrc
:PlugInstall
```

\pagebreak

# Mettre à jour le site web: faire du php

Le site fonctionne sans **framework**, l'idée est que vous puissiez comprendre
facilement et rapidement comment ça fonctionne sans que vous ayez à apprendre
tout le fonctionnement d'une structure web complexe.

Toutes les modifications sont locales. Un cron job ajoute vos modifications sur
le site tous les jours à 4h00. Voir la partie **git** pour envoyer vos modifications

Exemple pour cloner le site en local:
```
sudo apt install apache2
cd /var/www
rm -r html/
git clone https://github.com/zteeed/Cybersecurity-HackademINT.git
mv Cybersecurity-HackademINT html
firefox localhost
```

On passe à la modification du code php
vim /var/www/html/writeups.php
```php
<li>
  <a onclick="activate('AngstromCTF')">AngstromCTF</a>
  <div class="id" id="AngstromCTF">
    <?php include('/writeups/2017-2018/AngstromCTF/angstromctf.php') ?>
  </div>
</li>
```

/var/www/html/writeups/2017-2018/AngstromCTF/angstromctf.php
```php
<li><a onclick="activate('AngstromCTFintrotorsa')">introtorsa</a></li>
<div class="id" id="AngstromCTFintrotorsa">
  <?php include('introtorsa/introtorsa.php') ?>
</div>
```

/var/www/html/writeups/2017-2018/AngstromCTF/introtorsa
```php
// contenu du writeup
```

\pagebreak

# git

#### C'est quoi ça encore ?

git est un outil de versionning de code. Il faut vous créer un compte sur
https://github.com et que vous me donniez votre pseudo pour que je puisse vous
ajouter comme collaborateur sur le **répo** HackademINT.

## Commandes utiles (+Google)

Vérifier que vous maniez git avec votre user
```bash
git config --list
git config --global user.name "mon_user"
git config --global user.email "mon_user@mail.fr"
git status
git add fichier.php
git commit -m "super update"
git push
```

