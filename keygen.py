#!/usr/bin/env python
import os.path, pickle
from os.path import expanduser
from Crypto.PublicKey import RSA
from Crypto import Random


home = expanduser("~")
config_dir = home + "/.p2py"
keyfile = config_dir + "/keys"

if not os.path.exists(config_dir):
    os.makedirs(config_dir)
    print "Config directory created at ~/.p2py."

if not os.path.isfile(keyfile):
    randomGen = Random.new().read
    privKey = RSA.generate(2048, randomGen)
    pubKey = privKey.publickey()
    keys = [privKey.exportKey(), pubKey.exportKey()]
    pickle.dump(keys, open(keyfile, "wb"))
    print "Keyfile created at ~/.p2py/keys"

