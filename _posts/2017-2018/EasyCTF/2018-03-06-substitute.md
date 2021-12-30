---
title: "Substitute"
ctf: "EasyCTF"
annee: "2018"
author: "zTeeed"
published: true
---
<br />
<a href="/writeup-scripts/2017-2018/EasyCTF/Substitute/solve.py">download solve.py</a>
<br />
<br />
```python
#! /usr/bin/python
chaine="FI! XJWCYIUSINLIGH QGLE TAMC A XCU NSAO NID EPC WEN AXM JL EIEASSF HDIGM IN JEL JXOCXGJEF. EPJL JL ASLI EPC LCWIXM HDIYSCT CZCD TAMC NID CALFWEN. PCDC: CALFWEN{EPJL_JL_AX_CALF_NSAO_EI_OGCLL} GLC WAHJEAS SCEECDL."
print "-------"
print chaine
print "-------"
"""
CALFWEN
EASYCTF
"""

alpha="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
sortie=["Z"]*len(alpha)
sortie[alpha.index('E')]='C'
sortie[alpha.index('A')]='A'
sortie[alpha.index('S')]='L'
sortie[alpha.index('Y')]='F'
sortie[alpha.index('C')]='W'
sortie[alpha.index('T')]='E'
sortie[alpha.index('F')]='N'
sortie[alpha.index('G')]='O'
sortie[alpha.index('U')]='G'
sortie[alpha.index('L')]='S'
sortie[alpha.index('O')]='I'
sortie[alpha.index('N')]='X'
sortie[alpha.index('W')]='U'
sortie[alpha.index('R')]='D'
sortie[alpha.index('P')]='H'
sortie[alpha.index('I')]='J'
sortie[alpha.index('D')]='M'
sortie[alpha.index('H')]='P'

flag=""
for i in range(len(chaine)):
    if chaine[i] not in alpha:
        flag+=chaine[i]
    else:
        try:
            indice=sortie.index(chaine[i])
            flag+=alpha[indice]
        except:
            flag+=chaine[i]
print flag
print "-------"

flag=flag[152:190].lower()
print flag
```
