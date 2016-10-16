#!/usr/bin/env python
import socket, pickle, sys
from Crypto.PublicKey import RSA
from Crypto import Random
from multiprocessing import Process
from termcolor import colored

contacts = pickle.load(open("contacts.txt", "rb"))
hosts = contacts.values()
port = 6311
port2 = 6312
node = ("99.38.224.215", 31460)

def main():
    action = raw_input('Chat, contacts, view, or exit? ')
    if action == 'chat':
        chat()
    elif action == 'contacts':
         Contacts()
    elif action == 'exit':
        c.sendto("STATUS offline", node)
        sys.exit()
    elif action == "view":
        peers()
        main()
    else:
        print 'Not a valid action\n'
        main()

def peers(): # gets a list of available peers
        c.sendto("GET aval_peers", node)
        data = c.recv(1024)
    
        peer_list = pickle.loads(data) # loads peer list
        for peer in peer_list:
            if peer in hosts: # checks to see if peer in known
                if peer_list[peer] == True: # online
                    print "%s: " % contacts.keys()[contacts.values().index(peer)] + colored('online', 'green')
                elif peer_list[peer] == False: # offline
                    print "%s: " % contacts.keys()[contacts.values().index(peer)] + colored('offline', 'red')
                else:
                    print "n/a"
        print ''

def gen_key(): ## generates 2048 bit RSA key
    random_gen = Random.new().read
    key = RSA.generate(2048, random_gen)
    return key

def chat():
    contact = raw_input("Chat w/: ")
    if contact in contacts:
        ip = contacts[contact] 
    else:
        ip = contact
    print "Connecting..."
    punch(ip)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # creates UDP socket object
    sock.bind(('', port))
    host_pubkey = key_exchange(sock, ip)
    process = Process(target = server, args = (ip, sock, contact,)) # creates Server subprocess  
    process.start() # starts Server subprocess
    client(ip, sock, host_pubkey, process)

def key_exchange(s, host): ## exchanges public keys with remote host
    host_pubkey_received = False
    test = False
    while host_pubkey_received == False:
        s.sendto(public_key.exportKey(), (host, port))
        data = s.recv(1024)
        try:
            host_key = RSA.importKey(data) # checks to see if data is a RSA public key
            host_pubkey_received = True
        except:
            pass

    return host_key
        
        
def punch(host): ## UDP hole puch

    punch = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    punch.bind(('', port))
    punch.sendto('', (host, port))
    punch.close()

def server(host, s, con): ## listens for incoming messages
    Random.atfork()
    connected = False
    
    s.sendto('', (host, port))

    while True: 
        data = s.recv(1024)
        if connected == False:
            print 'Connected to %s\n' % host
            s.sendto('', (host, port))
            connected = True
        elif data == '':
            pass
        else:
            dec = private_key.decrypt(data)
            if dec == 'exit':
                print 'User disconnected. Type "exit" to exit.'
                break
            else:
                 print colored("%s: " % con, 'red') + dec

def client(host, s, pk, server_process): ## send messages
    
    while True:
        message = raw_input()
        enc = pk.encrypt(message, 32)[0]
        s.sendto(str(enc), (host, port))
        if message == "exit":
            server_process.terminate()  # terminates the Server subprocess
            s.close()  # closes socket 
            main()


def Contacts():
    
    choice = raw_input('Add, remove, edit, view or return? ')    
    
    if choice == 'add':
        name = raw_input('Name: ')
        host = raw_input('IP/Hostname: ')
        contacts[name] = host
    elif choice == 'remove':
        name = raw_input("Name: ")
        contacts.pop(name, None)
    elif choice == 'edit':
        contact = raw_input('Enter contact name: ')
        host = contacts[contact]
        choice2 = raw_input('Edit name or IP? ').lower()
        if choice2 == 'name':
            newName = raw_input('Enter new name: ')
            contacts[newName] = contacts.pop(contact)
        elif choice2 == 'ip':
            newIP = raw_input('Enter new IP: ')
            contacts.pop(contact, None)
            contacts[contact] = newIP
    elif choice == 'view':
        print ''
        for contact in contacts:
            print '%s: %s' % (contact, contacts[contact])
        print ''
    elif choice == 'return':
        main()
    else:
        print 'Not a valid action.'
        Contacts()
    if choice != 'view':
        pickle.dump(contacts, open("contacts.txt", "wb"))
        print 'Contacts saved.'
    Contacts()


if __name__ == "__main__":
    c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # this socket is for node communication
    c.bind(("", port2))
    c.sendto("STATUS online", node) # broadcast that this peer is online to node
    private_key = gen_key() # generates keys
    public_key = private_key.publickey()
    main()
