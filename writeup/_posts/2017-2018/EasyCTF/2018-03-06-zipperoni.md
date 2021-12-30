---
title: "zipperoni"
ctf: "EasyCTF"
annee: "2018"
author: "zTeeed"
published: true
type: crypto
---
<br />
<a href="/writeup-scripts/2017-2018/EasyCTF/zipperoni/9a894176201a4b9a76c7ebe224239e127e3071bf2d3f2a7ecf974dcd26f96dfa_zip_files.tar">download zipfiles</a>
<br />
<a href="/writeup-scripts/2017-2018/EasyCTF/zipperoni/solve.sh">download solve.sh</a>
<br />
<br />
Using hashcat - Simple code
<br />
The variable 'pattern' is just here to translate the pattern format from pattern.txt (ex : '00aA0') so it matches hashcat's one ( '?d?d?l?U?d').
<br />
Just unzip begin.zip before you execute this script.
<br />
<br />
```bash
#! /bin/bash

while true; do
    pattern=$(cat pattern.txt | sed s/a/?l/g | sed s/A/?u/g | sed s/0/?d/g)
    hashcat -a3 -m100 -w3 -o recovered.txt --outfile-format=2 hash.txt "$pattern"
    tail -n1 recovered.txt
    unzip -o -P $(tail -n1 recovered.txt) ../$(cat filename.txt)
done
```

Just wait for 2 or 3 minutes until the file flag.txt appears
<br />
<br />
