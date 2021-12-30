---
title: "MISC.Iheardyoulikefiles"
ctf: "TamuCTF"
annee: "2019"
published: true
author: "Bdenneu"
---
# Description
On a accés à une image.

![iheard1](/assets/images/TamuCTF2019/tamuctf2019_iheard1.png)

# Solution

La première étape consiste à extraire des données de l'image avec binwalk.
En fouillant un peu, on tombe dans word/media une image suspecte.

![iheard2](/assets/images/TamuCTF2019/tamuctf2019_iheard2.png)

A la fin de l'image, il y a la base64 du flag: ZmxhZ3tQMGxZdEByX0QwX3kwdV9HM3RfSXRfTjB3P30K

# Le flag

On obtient: flag{P0lYt@r_D0_y0u_G3t_It_N0w?}

