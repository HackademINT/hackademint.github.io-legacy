<br />
<a href="WRITEUPS/2017-2018/EasyCTF/IntroReverseEngineering/solve.py">download solve.py</a>
<br />
<br />
<pre><code class="hljs python">
#!/usr/bin/env python3
import binascii
key = "JDClkFeX"
def mystery(s):
    r = ""
    for i, c in enumerate(s):
        #print ((i,c))
        r += chr(ord(c) ^ ((i * ord(key[i % len(key)])) % 256))
        #print (binascii.hexlify(bytes(r, "utf-8")).decode("utf-8"))
        #print (len((binascii.hexlify(bytes(r, "utf-8")).decode("utf-8"))))
    return binascii.hexlify(bytes(r, "utf-8"))

#print (mystery("easyctf{"))

cipherhex="6525c3b53dc38f2a3813330cc3bfc3965bc3acc3bf77c383c3acc3977603c3b8c3aac390c294c3a0c2a819"
key = "JDClkFeX"

def resolve(cipherhex,key):
    flag=""
    rang=1
    i=0
    while rang&lt;len(cipherhex):
        test1=cipherhex[rang-1:rang+1]
        test2=cipherhex[rang-1:rang+3]
        test=False
        number=0
        while test==False:
            r=chr(number ^ ((i * ord(key[i % len(key)])) % 256))
            x=binascii.hexlify(bytes(r, "utf-8")).decode("utf-8")
            number+=1
            if x==test1:
                rang+=2
                i+=1
                flag+=chr(number-1)
                test=True
            elif x==test2:
                rang+=4
                i+=1
                flag+=chr(number-1)
                test=True
            elif number==257:
                return "erreur"
    return flag

print (resolve(cipherhex,key))

</code></pre>
