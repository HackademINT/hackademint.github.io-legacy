#! /usr/bin/python
chaine="22 14 6 9 26 7 9 14 19 22 29 8 7 17 13 0 78 42 18 12 7 48 27 31 14 44 9 69 2 38 29 95 6 64 12 1 12 70 47 87 93 65 8"
L=chaine.split(" ")
for i in range(len(L)):
    L[i]=int(L[i])
print (L)

def process(b,L):
    maxi=max(len(L),len(b))
    liste=[]
    for i in range(maxi):
        ca = L[i % len(L)]
        cb = ord(b[i % len(b)])
        liste.append(ca ^ cb)
    return liste

b="soupy"
X=process(b,L)
#flag ^ key = cipher
#cipher ^ key = flag
# cipher ^ flag = key
s=""
for u in X:
    s+=str(chr(u))
print s
