<br />
<a href="WRITEUPS/2017-2018/ESIEACTF/emojimadness/file.js">download file.js</a>
<br />
<a href="WRITEUPS/2017-2018/ESIEACTF/emojimadness/solve.py">download solve.py</a>
<br />
<br />
il s'agit d'un challenge d'obfucation, cependant, rien ne sert d'essayer de comprendre le code, on décode toutes les chaines de caractères que l'on trouve dans le code et on obtient le flag
<br />
<br />
file.js
<pre><code class="hljs javascript">
eval("function 😀(😴){alert(😴)} function 😎(😴){return window.prompt(😴)}");eval("function 😬(😷, 😞){return 😷^😞;}");eval("😨 = '='");eval("😈 = 😨.charCodeAt(0).toString()[0];");eval("😶 = 😨.charCodeAt(0).toString()[1];");eval("function 😲(😷, 😞){return 😞^😷;}");eval("function 😚(😷){return btoa(😷);} function 😏(😷){return atob(😷);}");eval("function 😌(😷){var arr = [];for (var 😳 = (parseInt(😶)-parseInt(😶)), 😰 = 😷.length; 😳 < 😰; 😳 ++) {var 😭 = Number(😷.charCodeAt(😳)).toString(parseInt(😶+😈));arr.push(😭);}return arr.join('');}");eval("function 😘(😷){var 😭 = 😷.toString();var str = '';for (var 😕 = (parseInt(😶)-parseInt(😶)); 😕 < 😭.length; 😕 += (parseInt(😶)+parseInt(😶)))str += String.fromCharCode(parseInt(😭.substr(😕, (parseInt(😶)+parseInt(😶))), parseInt(😶+😈)));return str;}");eval("function 😇(){😒 = 😎(😘('456e7472657a206c65206d6f74206465207061737365202f20456e7465722070617373776f7264')); if(😌(😚(😒))=='52564e46653070545831526f4e48526652476c7964486c664a6c39544d33683558307730626d64314e47637a66513d3d'){😀(😏('R09PRCBKT0I='));}else{😀(😏('VE9PIEJBRA=='));}}");eval("function 😐(){😒 = 😎(😘('456e7472657a206c65206d6f74206465207061737365202f20456e7465722070617373776f7264')); if(😌(😚(😒))=='52564e46653164796232356e58305a7359576439'){😀(😏('R09PRCBKT0I='));}else{😀(😏('VE9PIEJBRA=='));}}");eval("😇()");eval("function 😆(){😒 = 😎(😘('456e7472657a206c65206d6f74206465207061737365202f20456e7465722070617373776f7264')); if(😌(😚(😒))=='52564e4665315279655639425a324670626934754c6935454f6e303d'){😀(😏('R09PRCBKT0I='));}else{😀(😏('VE9PIEJBRA=='));}}");eval("function 😪(😷){var arr = [];for (var 😳 = (parseInt(😶)-parseInt(😶)), 😰 = 😷.length; 😳 < 😰; 😳 ++) {var 😭 = Number(😷.charCodeAt(😳)).toString(parseInt(😶+😈));arr.push(😭);}return arr.join('');}");

</code></pre>
solve.py
<pre><code class="hljs python">
#! /usr/bin/env python3
import binascii
import base64

a="456e7472657a206c65206d6f74206465207061737365202f20456e7465722070617373776f7264"
b=binascii.unhexlify(a)
print(b)
c="52564e46653070545831526f4e48526652476c7964486c664a6c39544d33683558307730626d64314e47637a66513d3d"
d=binascii.unhexlify(c)
print(d)
#d="RVNFe0pTX1RoNHRfRGlydHlfJl9TM3h5X0w0bmd1NGczfQ=="
e=base64.b64decode(d)
print(e)

</code></pre>
