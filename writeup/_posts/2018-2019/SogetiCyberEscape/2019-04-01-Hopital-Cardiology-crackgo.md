---
title: "CrackGO"
subtitle: "Challenge tiré du Cyberescape de la Sogeti"
author: "zTeeed"
team: "HackademINT"
ctf: "SogetiCyberEscape"
annee: "2019"

---

# L'énoncé

On cherche à obtenir le bon mot de passe à partir du script GO ci-dessous (vous
pouvez télécharger ce script
[ici](/writeup-scripts/2018-2019/SogetiCyberEscape/gocrack/gocrack.go)).

L'objectif est de trouver les hashs correspondant à chacun des 25 caractères du
mot de passe afin de les casser et de reconstituer le mot de passe.

```go
package main

import (
    "bufio"
    "os"
    "crypto/md5"
    "strings"
)

func main() {
  reader := bufio.NewReader(os.Stdin)
  print("Enter password: ")
  password, _ := reader.ReadString('\n')
  password = strings.TrimSuffix(password, "\n")
  if len(password) != 25 {
    print("WRONG")
    return
  }

  var buffer [25*16]byte
  for i := 0; i < len(password); i++ {
    var sum = md5.Sum([]byte(password[i:i+1]))
    for j := 0; j < 16; j++ {
      buffer[16*i + j] = sum[j]
    }
	}

  expected := [...]byte{157, 94, 214, 120, 254, 87, 188, 202, 97, 1, 64, 149, 122, 250, 181, 113, 76, 97, 67, 96, 218, 147, 192, 160, 65, 178, 46, 83, 125, 225, 81, 235, 13, 97, 248, 55, 12, 173, 29, 65, 47, 128, 184, 77, 20, 62, 18, 87, 165, 243, 198, 161, 27, 3, 131, 157, 70, 175, 159, 180, 60, 151, 193, 136, 93, 188, 152, 220, 201, 131, 167, 7, 40, 189, 8, 45, 26, 71, 84, 110, 129, 84, 23, 38, 127, 118, 246, 244, 96, 164, 166, 31, 157, 183, 95, 219, 178, 245, 255, 71, 67, 102, 113, 182, 229, 51, 216, 220, 54, 20, 132, 93, 217, 86, 121, 117, 33, 52, 162, 217, 235, 97, 219, 215, 185, 28, 75, 204, 45, 185, 94, 142, 26, 146, 103, 183, 161, 24, 133, 86, 178, 1, 59, 51, 12, 193, 117, 185, 192, 241, 182, 168, 49, 195, 153, 226, 105, 119, 38, 97, 123, 139, 150, 90, 212, 188, 160, 228, 26, 181, 29, 231, 179, 19, 99, 161, 178, 245, 255, 71, 67, 102, 113, 182, 229, 51, 216, 220, 54, 20, 132, 93, 177, 74, 123, 128, 89, 217, 192, 85, 149, 76, 146, 103, 76, 230, 0, 50, 134, 92, 12, 11, 74, 176, 224, 99, 229, 202, 163, 56, 124, 26, 135, 65, 3, 199, 192, 172, 227, 149, 216, 1, 130, 219, 7, 174, 44, 48, 240, 52, 177, 74, 123, 128, 89, 217, 192, 85, 149, 76, 146, 103, 76, 230, 0, 50, 37, 16, 195, 144, 17, 197, 190, 112, 65, 130, 66, 62, 58, 105, 94, 145, 168, 127, 246, 121, 162, 243, 231, 29, 145, 129, 166, 123, 117, 66, 18, 44, 75, 67, 176, 174, 227, 86, 36, 205, 149, 185, 16, 24, 155, 61, 194, 49, 130, 119, 224, 145, 13, 117, 1, 149, 180, 72, 121, 118, 22, 224, 145, 173, 177, 74, 123, 128, 89, 217, 192, 85, 149, 76, 146, 103, 76, 230, 0, 50, 111, 143, 87, 113, 80, 144, 218, 38, 50, 69, 57, 136, 217, 161, 80, 27, 12, 193, 117, 185, 192, 241, 182, 168, 49, 195, 153, 226, 105, 119, 38, 97, 123, 139, 150, 90, 212, 188, 160, 228, 26, 181, 29, 231, 179, 19, 99, 161, 15, 189, 23, 118, 225, 173, 34, 197, 154, 112, 128, 211, 92, 127, 212, 219}
  if buffer == expected {
    print("Hell yeah!")
  } else {
    print ("WRONG")
  }
}
```

# Solution

## Dictionnaire de hash

On sait que chaque hash correspond à une lettre, on se crée un dictionnaire de
hash pour chaque caractère lisible

```python
dico = {}
for c in string.printable:
    dico[c] = hashlib.md5(c.encode()).hexdigest()
```

Ce qui nous donne:
```json
{"0": "cfcd208495d565ef66e7dff9f98764da", "1": "c4ca4238a0b923820dcc509a6f75849b", "2": "c81e728d9d4c2f636f067f89cc14862c", "3": "eccbc87e4b5ce2fe28308fd9f2a7baf3", "4": "a87ff679a2f3e71d9181a67b7542122c", "5": "e4da3b7fbbce2345d7772b0674a318d5", "6": "1679091c5a880faf6fb5e6087eb1b2dc", "7": "8f14e45fceea167a5a36dedd4bea2543", "8": "c9f0f895fb98ab9159f51fd0297e236d", "9": "45c48cce2e2d7fbdea1afc51c7c6ad26", "a": "0cc175b9c0f1b6a831c399e269772661", "b": "92eb5ffee6ae2fec3ad71c777531578f", "c": "4a8a08f09d37b73795649038408b5f33", "d": "8277e0910d750195b448797616e091ad", "e": "e1671797c52e15f763380b45e841ec32", "f": "8fa14cdd754f91cc6554c9e71929cce7", "g": "b2f5ff47436671b6e533d8dc3614845d", "h": "2510c39011c5be704182423e3a695e91", "i": "865c0c0b4ab0e063e5caa3387c1a8741", "j": "363b122c528f54df4a0446b6bab05515", "k": "8ce4b16b22b58894aa86c421e8759df3", "l": "2db95e8e1a9267b7a1188556b2013b33", "m": "6f8f57715090da2632453988d9a1501b", "n": "7b8b965ad4bca0e41ab51de7b31363a1", "o": "d95679752134a2d9eb61dbd7b91c4bcc", "p": "83878c91171338902e0fe0fb97a8c47a", "q": "7694f4a66316e53c8cdd9d9954bd611d", "r": "4b43b0aee35624cd95b910189b3dc231", "s": "03c7c0ace395d80182db07ae2c30f034", "t": "e358efa489f58062f10dd7316b65649e", "u": "7b774effe4a349c6dd82ad4f4f21d34c", "v": "9e3669d19b675bd57058fd4664205d2a", "w": "f1290186a5d0b1ceab27f4e77c0c5d68", "x": "9dd4e461268c8034f5c8564e155c67a6", "y": "415290769594460e2e485922904f345d", "z": "fbade9e36a3f36d3d676c1b808451dd7", "A": "7fc56270e7a70fa81a5935b72eacbe29", "B": "9d5ed678fe57bcca610140957afab571", "C": "0d61f8370cad1d412f80b84d143e1257", "D": "f623e75af30e62bbd73d6df5b50bb7b5", "E": "3a3ea00cfc35332cedf6e5e9a32e94da", "F": "800618943025315f869e4e1f09471012", "G": "dfcf28d0734569a6a693bc8194de62bf", "H": "c1d9f50f86825a1a2302ec2449c17196", "I": "dd7536794b63bf90eccfd37f9b147d7f", "J": "ff44570aca8241914870afbc310cdb85", "K": "a5f3c6a11b03839d46af9fb43c97c188", "L": "d20caec3b48a1eef164cb4ca81ba2587", "M": "69691c7bdcc3ce6d5d8a1361f22d04ac", "N": "8d9c307cb7f3c4a32822a51922d1ceaa", "O": "f186217753c37b9b9f958d906208506e", "P": "44c29edb103a2872f519ad0c9a0fdaaa", "Q": "f09564c9ca56850d4cd6b3319e541aee", "R": "e1e1d3d40573127e9ee0480caf1283d6", "S": "5dbc98dcc983a70728bd082d1a47546e", "T": "b9ece18c950afbfa6b0fdbfa4ff731d3", "U": "4c614360da93c0a041b22e537de151eb", "V": "5206560a306a2e085a437fd258eb57ce", "W": "61e9c06ea9a85a5088a499df6458d276", "X": "02129bb861061d1a052c592e2dc6b383", "Y": "57cec4137b614c87cb4e24a3d003a3e0", "Z": "21c2e59531c8710156d34a3c30ac81d5", "!": "9033e0e305f247c0c3c80d0c7848c8b3", "\"": "b15835f133ff2e27c7cb28117bfae8f4", "#": "01abfc750a0c942167651c40d088531d", "$": "c3e97dd6e97fb5125688c97f36720cbe", "%": "0bcef9c45bd8a48eda1b26eb0c61c869", "&": "6cff047854f19ac2aa52aac51bf3af4a", "'": "3590cb8af0bbb9e78c343b52b93773c9", "(": "84c40473414caf2ed4a7b1283e48bbf4", ")": "9371d7a2e3ae86a00aab4771e39d255d", "*": "3389dae361af79b04c9c8e7057f60cc6", "+": "26b17225b626fb9238849fd60eabdf60", ",": "c0cb5f0fcf239ab3d9c1fcd31fff1efc", "-": "336d5ebc5436534e61d16e63ddfca327", ".": "5058f1af8388633f609cadb75a75dc9d", "/": "6666cd76f96956469e7be39d750cc7d9", ":": "853ae90f0351324bd73ea615e6487517", ";": "9eecb7db59d16c80417c72d1e1f4fbf1", "<": "524a50782178998021a88b8cd4c8dcd8", "=": "43ec3e5dee6e706af7766fffea512721", ">": "cedf8da05466bb54708268b3c694a78f", "?": "d1457b72c3fb323a2671125aef3eab5d", "@": "518ed29525738cebdac49c49e60ea9d3", "[": "815417267f76f6f460a4a61f9db75fdb", "\\": "28d397e87306b8631f3ed80d858d35f0", "]": "0fbd1776e1ad22c59a7080d35c7fd4db", "^": "7e6a2afe551e067a75fafacf47a6d981", "_": "b14a7b8059d9c055954c92674ce60032", "`": "833344d5e1432da82ef02e1301477ce8", "{": "f95b70fdc3088560732a5ac135644506", "|": "b99834bc19bbad24580b3adfa04fb947", "}": "cbb184dd8e05c9709e5dcaedaa0495cf", "~": "4c761f170e016836ff84498202b99827", " ": "7215ee9c7d9dc229d2921a40e899ec5f", "\t": "5e732a1878be2342dbfeff5fe3ca5aa3", "\n": "68b329da9893e34099c7d8ad5cb9c940", "\r": "dcb9be2f604e5df91deb9659bed4748d", "\x0b": "13c8ffd977013703a701cf8e11deac65", "\x0c": "58c89562f58fd276f592420068db8c09"}
```

## Résolution

On commence par retrouver les 25 hashs correspondant aux 25 lettres du mot de passe. Puis on utilise le dictionnaire généré pour faire la correspondance entre les lettres et leurs hashs md5 correspondants.

script:
[solve.py](../../../writeup-scripts/2018-2019/SogetiCyberEscape/gocrack/solve.py)

```python
#!/usr/bin/python3

from binascii import hexlify
import hashlib, string

bytes_list = [157, 94, 214, 120, 254, 87, 188, 202, 97, 1, 64, 149, 122, 250, 181, 113, 76, 97, 67, 96, 218, 147, 192, 160, 65, 178, 46, 83, 125, 225, 81, 235, 13, 97, 248, 55, 12, 173, 29, 65, 47, 128, 184, 77, 20, 62, 18, 87, 165, 243, 198, 161, 27, 3, 131, 157, 70, 175, 159, 180, 60, 151, 193, 136, 93, 188, 152, 220, 201, 131, 167, 7, 40, 189, 8, 45, 26, 71, 84, 110, 129, 84, 23, 38, 127, 118, 246, 244, 96, 164, 166, 31, 157, 183, 95, 219, 178, 245, 255, 71, 67, 102, 113, 182, 229, 51, 216, 220, 54, 20, 132, 93, 217, 86, 121, 117, 33, 52, 162, 217, 235, 97, 219, 215, 185, 28, 75, 204, 45, 185, 94, 142, 26, 146, 103, 183, 161, 24, 133, 86, 178, 1, 59, 51, 12, 193, 117, 185, 192, 241, 182, 168, 49, 195, 153, 226, 105, 119, 38, 97, 123, 139, 150, 90, 212, 188, 160, 228, 26, 181, 29, 231, 179, 19, 99, 161, 178, 245, 255, 71, 67, 102, 113, 182, 229, 51, 216, 220, 54, 20, 132, 93, 177, 74, 123, 128, 89, 217, 192, 85, 149, 76, 146, 103, 76, 230, 0, 50, 134, 92, 12, 11, 74, 176, 224, 99, 229, 202, 163, 56, 124, 26, 135, 65, 3, 199, 192, 172, 227, 149, 216, 1, 130, 219, 7, 174, 44, 48, 240, 52, 177, 74, 123, 128, 89, 217, 192, 85, 149, 76, 146, 103, 76, 230, 0, 50, 37, 16, 195, 144, 17, 197, 190, 112, 65, 130, 66, 62, 58, 105, 94, 145, 168, 127, 246, 121, 162, 243, 231, 29, 145, 129, 166, 123, 117, 66, 18, 44, 75, 67, 176, 174, 227, 86, 36, 205, 149, 185, 16, 24, 155, 61, 194, 49, 130, 119, 224, 145, 13, 117, 1, 149, 180, 72, 121, 118, 22, 224, 145, 173, 177, 74, 123, 128, 89, 217, 192, 85, 149, 76, 146, 103, 76, 230, 0, 50, 111, 143, 87, 113, 80, 144, 218, 38, 50, 69, 57, 136, 217, 161, 80, 27, 12, 193, 117, 185, 192, 241, 182, 168, 49, 195, 153, 226, 105, 119, 38, 97, 123, 139, 150, 90, 212, 188, 160, 228, 26, 181, 29, 231, 179, 19, 99, 161, 15, 189, 23, 118, 225, 173, 34, 197, 154, 112, 128, 211, 92, 127, 212, 219]

""" Dictionnaire de hash pour chaque caractère lisible """
dico = {}
for c in string.printable:
    dico[c] = hashlib.md5(c.encode()).hexdigest()
""" """

def search_dict(value, dico):
    for key in dico:
        if dico[key] == value:
              return key
    return None


password = ''
length = 16
for i in range(0, len(bytes_list), length):
    part = bytes_list[i:i+length]
    raw_hash = b''.join([bytes([item]) for item in part])
    hex_hash = hexlify(raw_hash).decode()
    print(hex_hash)
    c = search_dict(hex_hash, dico)
    password += search_dict(hex_hash, dico)

print()
print(password)
```

On obtient:

```bash
9d5ed678fe57bcca610140957afab571
4c614360da93c0a041b22e537de151eb
0d61f8370cad1d412f80b84d143e1257
a5f3c6a11b03839d46af9fb43c97c188
5dbc98dcc983a70728bd082d1a47546e
815417267f76f6f460a4a61f9db75fdb
b2f5ff47436671b6e533d8dc3614845d
d95679752134a2d9eb61dbd7b91c4bcc
2db95e8e1a9267b7a1188556b2013b33
0cc175b9c0f1b6a831c399e269772661
7b8b965ad4bca0e41ab51de7b31363a1
b2f5ff47436671b6e533d8dc3614845d
b14a7b8059d9c055954c92674ce60032
865c0c0b4ab0e063e5caa3387c1a8741
03c7c0ace395d80182db07ae2c30f034
b14a7b8059d9c055954c92674ce60032
2510c39011c5be704182423e3a695e91
a87ff679a2f3e71d9181a67b7542122c
4b43b0aee35624cd95b910189b3dc231
8277e0910d750195b448797616e091ad
b14a7b8059d9c055954c92674ce60032
6f8f57715090da2632453988d9a1501b
0cc175b9c0f1b6a831c399e269772661
7b8b965ad4bca0e41ab51de7b31363a1
0fbd1776e1ad22c59a7080d35c7fd4db

BUCKS[golang_is_h4rd_man]
```
