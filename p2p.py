#!/usr/bin/env python

import socket, pickle, sys, os
from Crypto.PublicKey import RSA
from Crypto import Random
from multiprocessing import Process
from termcolor import colored

def main():
    while True:
        l = input('Choose an action:\n1 | Chat\n2 | Exit\n')
        if l == 1:
            chat()
        elif l == 2:
            sys.exit()
        else:
            print "Not valid.\n"

def chat():
    ip = raw_input("Enter an IP address: ")

    print "Connecting..."
    
    punch(ip) 
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", port))
    hostPubKey = keyExchange(sock, ip)
    serverProcess = Process(target=server, args=(ip, sock,)) # creates server subprocess
    serverProcess.start()
    client(ip, sock, hostPubKey, serverProcess)

def punch(host): # UDP Hole Punching

    p = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    p.bind(("", port))
    p.sendto("", (host, port))
    p.close()

def keyExchange(s, host): # exchanges public keys with remote host
    
    keyReceived = False
    while keyReceived == False:
        s.sendto(pubKey.exportKey(), (host, port)) # sends own public key
        data = s.recv(1024)
        try: # verifies if data is a public key
            hostKey = RSA.importKey(data)
            keyReceived = True
        except:
            pass

    return hostKey

def server(host, s):
    
    Random.atfork()
    connected = False

    s.sendto("", (host, port)) # attempts connection

    while True:
        data = s.recv(1024)
        if connected == False: # no previous data received
            print "Connected to %s\n" % host
            s.sendto("", (host, port)) 
            connected = True
        elif data == "":
            pass
        else:
            dec = privKey.decrypt(data) # decrypts data
            if dec == "exit":
                print "User disconnected. Type 'exit' to exit."
                break
            else:
                print colored("%s: "% host, "red") + dec

def client(host, s, hostPubKey, serverProcess):

    while True:
        m = raw_input()
        enc = hostPubKey.encrypt(m, 32)[0] # encrypts message
        s.sendto(str(enc), (host, port)) # sends message
        if m == "exit":
            serverProcess.terminate() 
            s.close()
            main()
            
if __name__ == "__main__":

    port = 6311
    HOME = os.environ['HOME']

    keys = pickle.load(open(HOME + "/.p2py/keys", "rb")) # loads keys from keyfile
    privKey = RSA.importKey(keys[0])
    pubKey = RSA.importKey(keys[1])

    main()
