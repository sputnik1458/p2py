#!/usr/bin/env python
import socket
from multiprocessing import Process

port = 6311
ip = 'Enter remote host: '



def main():
    #remoteHost = raw_input("Remote Host: ")
    punch(ip)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', port))
    p1 = Process(target = Server, args = (sock,))
    p1.start()
    while True:
        message = raw_input()
        p2 = Process(target = Client, args = (message, sock,))
        p2.start()

def punch(host):

    hole = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hole.bind(('', port))
    hole.sendto('', (host, port))
    hole.close()

def Server(s):

    while True: 
        data, addr = s.recvfrom(1024)
        print '>> ' + data

def Client(m, s):
   # print 'client'
    
   # while True:
    #    try:
     #       message = raw_input()
      #      s.sendto(message, (ip, port))
       # except EOFError:
        #    pass
    s.sendto(m, (ip ,port))

main()
