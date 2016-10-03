#!/usr/bin/env python

import socket, sys, pickle, select, Queue
from Crypto.PublicKey import RSA
from Crypto import Random
from termcolor import colored
from threading import Thread

peers = pickle.load(open("peers.txt", "rb"))
peer_conn = dict.fromkeys(peers, False) # creates dict from hosts in peers.txt and status defaults
                                        # to offline

def node():
    print "Connection: %s" % addr[0]

    while True:
        data = conn.recv(1024)
        if "STATUS" in data:
            if "online" in data:
                if addr[0] in peers: # checks to see if hosts is a known peer
                    peer_conn[addr[0]] = True # sets status to online
                else:
                    peers.append(addr[0]) # adds host to known peer list
                    pickle.dump(peers, open("peers.txt", "wb"))
                    peer_conn[addr[0]] = True
            elif "offline" in data:
                peer_conn[addr[0]] = False # sets status to offline
                break
        elif data == "GET aval_peers":
            aval_peers = pickle.dumps(peer_conn)
            conn.send(aval_peers) # sends list of known peers
    conn.close() # closes socket
    


if __name__ == "__main__":
    threads = [] # list of operational threads
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("", 31459))

    while True:
        for thread in threads:
            if thread.isAlive() == False: # joins and removes thread if unused
                thread.join() 
                threads.remove(thread)
        s.listen(1)
        print "Waiting..."
        conn, addr = s.accept() 
        t = Thread(target=node)
        t.start() # starts thread
        threads.append(t)

