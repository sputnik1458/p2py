#!/usr/bin/env python
import socket, pickle, sys
from Crypto.PublicKey import RSA
from Crypto import Random
from multiprocessing import Process
from termcolor import colored

contacts = pickle.load(open("contacts.txt", "rb"))

port = 6311

def main():
    action = raw_input('Chat, contacts, or exit? ')
    if action == 'chat':
        chat()
    elif action == 'contacts':
         Contacts()
    elif action == 'exit':
        sys.exit()
    else:
        print 'Not a valid action\n'
        main()

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
        elif data == 'exitcode':
            print 'User disconnected. Type "exit" to exit.'
            break
        else:
            dec = private_key.decrypt(data)
            print colored("%s: " % con, 'red') + dec

def client(host, s, pk, server_process): ## send messages
    
    while True:
        message = raw_input()
        if message == 'exit':
            s.sendto('exitcode', (host, port))
            server_process.terminate() # terminates the Server subprocess
            s.close() # closes socket 
            main()
        else:
            enc = pk.encrypt(message, 32)[0]
            s.sendto(str(enc), (host, port))


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

    private_key = gen_key()
    public_key = private_key.publickey()
    main()
