---
title: "USB payload"
subtitle: "Challenge tiré du Cyberescape de la Sogeti"
author: "zTeeed"
team: "HackademINT"
ctf: "SogetiCyberEscape"
annee: "2019"

---

# L'énoncé

On nous donne le script qui vérifie le contenu des différents fichier contenu
sur une clé USB. Chaque fichier doit contenir `CDG`.

```bash
#!/bin/bash
key="123O321"
for file in /mnt/*.flight; do
  fn=$(basename -- "$file")
  f="${fn%.*}"
  re='^[0-9]{3}O[0-9]{3}'
  if [[ $f =~ $re ]]; then
    w=true
    for (( i=0; i<${#f}; i++ )); do
      h1=${f:$i:1}
      h2=${f:${#f}-$i-1:1}
      if ! [ "$h1" = "$h2" ]; then
        echo $f;
        w=false
      fi
    done
    if [[ $w = true && $f == "$key" ]]; then
      rr='^[A-Z]{3}$'
      d=$(cat $file)
      if [[ $d =~ $rr ]]; then
        echo $d;
        echo $f
        exit 0
      fi
    fi
  fi

done
```

# Solution

On monte la clé dans `/mnt` et on génère ces fichiers en bash:

```bash
for i in {000..999}; do touch /mnt/"$(echo $i | rev)"O"$i".flight; done
for i in $(ls /mnt/*flight); do echo -n "CDG" > $i; done 
```
