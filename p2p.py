#!/usr/bin/env python
import socket, pickle
from multiprocessing import Process

contacts = pickle.load(open( "contacts.txt", "rb" ))

port = 6311


def main():
    action = raw_input('Chat or Contacts? ')
    if action == 'chat':
        chat()
    elif action == 'contacts':
         Contacts()
    else:
        print 'Not a valid action\n'
        main()


def chat():
    contact = raw_input("Chat w/: ")
    ip = contacts[contact]
    punch(ip)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', port))
    p1 = Process(target = Server, args = (ip, sock,))
    p1.start()
    Client(ip, sock)

def punch(host): ## UDP hole puch

    punch = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    punch.bind(('', port))
    punch.sendto('', (host, port))
    punch.close()

def Server(host, s): ## listens for incoming messages
    connected = False

    while True: 
        data, addr = s.recvfrom(1024)
        if connected == False:
            print 'Connected to %s' % host
            s.sendto('', (host, port))
            connected = True
        elif data == '':
            pass
        else:
            print '>> ' + data

def Client(host, s): ## send messages
    
    while True:
        message = raw_input()
        s.sendto(message, (host, port))


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

main()
