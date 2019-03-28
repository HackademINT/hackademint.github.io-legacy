#! /bin/bash

while true; do
    pattern=$(cat pattern.txt | sed s/a/?l/g | sed s/A/?u/g | sed s/0/?d/g)
    hashcat -a3 -m100 -w3 -o recovered.txt --outfile-format=2 hash.txt "$pattern"
    tail -n1 recovered.txt
    unzip -o -P $(tail -n1 recovered.txt) ../$(cat filename.txt)
done
