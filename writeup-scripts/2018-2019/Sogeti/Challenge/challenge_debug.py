import random
import hashlib
import string
import time
from Crypto.Cipher import AES

CHALLENGE = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(64))

FLAG = "SCE{DEMO PROGRAM - NOTHING HERE}"

class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def pprint(message, level="INFO"):
    if level == "INFO":
        print("[" + bcolors.OKBLUE + "*" + bcolors.ENDC + "] " + message)
    elif level == "WARNING":
        print("[" + bcolors.WARNING + "!" + bcolors.ENDC + "] " + message)
    elif level == "FAIL":
        print("[" + bcolors.FAIL + "X" + bcolors.ENDC + "] " + message)
    elif level == "SUCCESS":
        print("[" + bcolors.OKGREEN + "+" + bcolors.ENDC + "] " + message)

pprint("Random initialization vector", "INFO")
random.seed(random.randint(1,10000))
pprint("Seed generated !", "SUCCESS")

key = 0xffffffff 

pprint("Generating secret key", "INFO")
for i in range(10):
   key ^= random.randint(0x00000000, 0xffffffff)
pprint("Secret key generated !", "SUCCESS")


secret = hashlib.sha256(str(key))

# @TODO REMOVE THIS IN PRODUCTION !
pprint("DEBUG - Secret key is %s...%s" % (secret.hexdigest()[:15], secret.hexdigest()[-15:]), "WARNING")

encryption_suite = AES.new(secret.digest(), AES.MODE_CBC, 'LmQHJ6G6QnE5LxbV')
cipher_text = encryption_suite.encrypt(CHALLENGE)

pprint("Encrypted Challenge : " + cipher_text.encode("hex"), "SUCCESS")

current_time = time.time()
USER_CHALLENGE = raw_input("Give me the challenge (2s) > ")

if time.time() - current_time > 2:
    pprint("You were too slow", "FAIL")
else:
    if USER_CHALLENGE == CHALLENGE:
        pprint("Here is your flag : " + FLAG, "SUCCESS")
    else:
        pprint("Incorrect challenge", "FAIL")
