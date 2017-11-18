# p2py
Completely decentralized cli-based P2P chat

## About
This program uses Python 2.7 and its built-in sockets module. In order to achieve total decentralization, no rendezvous server mediates the connection between the two computers. Rather, each computer attempts to directly connect to each other using their respective external IP addresses.

P2P protocol is acheived by implementing UDP hole punching, simultaneously eliminating the need for a centralized server and port forwarding.

This program uses 2048 bit RSA encryption, and no party except you has access to your private key.

Currently only functioning on Linux. 

## Usage
You must know each other's external IP address. You can retrieve your own by running `dig +short myip.opendns.com @resolver1.opendns.com` in a shell. 

Run `keygen.py` to create a keyfile.

To exit out of a chat, simply type "exit". 

## Issues
* Message overlap
* Inability to easily exit out of an attempted connection

## To-Do
* Contacts
* Curses CLI and GUI
* Offline message reception
* Group chats
* File-sharing
