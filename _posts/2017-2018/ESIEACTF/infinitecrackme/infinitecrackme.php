<br />
<a href="WRITEUPS/2017-2018/ESIEACTF/infinitecrackme/infinitecrackme.zip">download infinitecrackme.zip</a>
<br />
<a href="WRITEUPS/2017-2018/ESIEACTF/infinitecrackme/solve.sh">download solve.sh</a>
<br />
<br />
La commande ltrace permet d'observer sur chacun des binaires la "string compare: strcmp" qui est effectuée. Le mot de passe était à restituer sous la forme ESE{md5(pass_chall0+...+pass_chall19)}.
<br />
<br />
<pre><code class="hljs bash">
#! /bin/bash
passphrase=""
unzip infinitecrackme.zip
number=$(ls -l | grep chall | wc -l)
number=`expr $number - 1`
for i in `seq 0 $number`; do
  file="chall""$i"
  ltrace -o output ./$file "test" > /dev/null
  flag=$(cat output | grep strcmp | cut -d' ' -f2 | cut -d'"' -f2)
  echo $flag
  passphrase="$passphrase""$flag"
done
echo -n $passphrase > output
echo " "
echo "ESE{""$(md5sum output | cut -d' ' -f1)""}"
rm output
rm chall*

</code></pre>
