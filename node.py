#!/usr/bin/env python

import socket, sys, pickle, select, Queue
from Crypto.PublicKey import RSA
from Crypto import Random
#from threading import Thread

peers = pickle.load(open("peers.txt", "rb"))
peer_conn = dict.fromkeys(peers, False) # creates dict from hosts in peers.txt and status defaults
                                        # to offline

port = 31460
sPort = 6312


def node(d, a, s):
    print "Connection: %s" % a

    if "STATUS" in d:
        if "online" in d:
            if a in peers: # checks to see if hosts is a known peer
                peer_conn[a] = True # sets status to online
            else:
                peers.append(a) # adds host to known peer list
                pickle.dump(peers, open("peers.txt", "wb"))
                peer_conn[a] = True
                print peer_conn
        elif "offline" in d:
            peer_conn[a] = False # sets status to offline
    elif data == "GET aval_peers":
        aval_peers = pickle.dumps(peer_conn)
        s.sendto(aval_peers, (a, sPort)) # sends list of known peers

    


if __name__ == "__main__":
#    threads = [] # list of operational threads
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", port))

    while True:
#        for thread in threads:
#            if thread.isAlive() == False: # joins and removes thread if unused
#                thread.join() 
#                threads.remove(thread)
        data, addr = sock.recvfrom(1024)
#        t = Thread(target=node, args=(data, addr[0], sock))
#        t.start() # starts thread
#        threads.append(t)
        node(data, addr[0], sock)

