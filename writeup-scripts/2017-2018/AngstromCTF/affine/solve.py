#! /usr/bin/python
# WARMUP
# Crypto , 10


def get_coeff_list(cipher,start,alpha):
    """ y = a*x + b """
    L=[]
    for i in range(len(alpha)):
        for j in range(len(alpha)):
            compt=0
            for p in range(len(start)):
                if (i*alpha.index(start[p])+j)%len(alpha)==alpha.index(cipher[p]):
                    compt+=1
            if compt==len(start):
                L.append([i,j])
    return L

def inv(a,alpha):
    for num in range(len(alpha)):
        if (a*num)%len(alpha)==1:
            return num
    return None

def get_plain(cipher,alpha,coeff):
    """
    modular inverse:
    a*a^-1 = 1 mod(p)
    y = a*x + b
    x = a^-1*y -b
    """
    [a,b]=coeff
    print ("coeff = "+str([a,b]))
    plain=""
    for i in range(len(cipher)):
        if cipher[i] not in "{_}":
            index=(inv(a,alpha)*(alpha.index(cipher[i])-b))%len(alpha)
            plain+=alpha[index]
        else:
            plain+=cipher[i]
    return plain

def main():
    alpha="abcdefghijklmnopqrstuvwxyz"
    cipher="myjd{ij_fkwizq}"
    start="actf"
    L=get_coeff_list(cipher,start,alpha)
    for coeff in L:
        print(get_plain(cipher,alpha,coeff))
    return

main()

