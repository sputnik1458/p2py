#!/usr/bin/env python3

import socket, pickle, sys, os
from Crypto.PublicKey import RSA
from Crypto import Random
from multiprocessing import Process
from termcolor import colored

def main():
    while True:
        mode = int(input('Choose an action:\n1 | Chat\n2 | Exit\n'))
        if mode == 1:
            chat()
        elif mode == 2:
            sys.exit()
        else:
            print("Not valid.\n")

def chat():
    ip = input("Enter an IP address to connect to: ")
    print("Connecting...")
    punch(ip)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", port))
    hostPubKey = keyExchange(sock, ip)
    serverProcess = Process(target=server, args=(ip, sock,)) # creates server subprocess
    serverProcess.start()
    client(ip, sock, hostPubKey, serverProcess)

def punch(host): # UDP Hole Punching
    p = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    p.bind((b'', port))
    p.sendto(b'', (host, port))
    p.close()

def keyExchange(s, host): # exchanges public keys with remote host
    keyReceived = False
    while keyReceived == False:
        s.sendto(pubKey.exportKey(), (host, port)) # sends own pblic key
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

    s.sendto(b"", (host, port)) # attempts connection

    while True:
        data = s.recv(1024)
        if connected == False: # no previous data received
            print("Connected to %s\n" % host)
            s.sendto(b"", (host, port))
            connected = True
        elif data == "":
            pass
        else:
            dec = privKey.decrypt(data)
            if dec == "exit":
                print("User disconnected. Type 'exit' to exit.")
                break
            else:
                print(colored("%s: "% host, "red") + dec.decode("UTF-8"))

def client(host, s, hostPubKey, serverProcess):
    while True:
        m = str(input())
        enc = hostPubKey.encrypt(m.encode("UTF-8"), 32)[0] # encrypts message
        s.sendto(enc, (host, port)) # sends message
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
