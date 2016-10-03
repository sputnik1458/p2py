# p2p-chat
Completely decentralized cli-based P2P chat

## About
This program uses Python 2.7 and its built-in sockets module. In order to achieve total decentralization, no rendezvous server mediates the connection between the two computers. Rather, each computer attempts to directly connect to each other using their respective external IP addresses.

P2P protocol is acheived by implementing UDP hole punching, simultaneously eliminating the need for a centralized server and port forwarding.

This program uses 2048 bit RSA encryption, and no party except you has access to your private key.

This program communicates with nodes for the purpose of keeping track of who is online.

## Usage
You must know each other's external IP address. You can retrieve your own by running `dig +short myip.opendns.com @resolver1.opendns.com` in a shell. 

You may either create a Contacts entry for the computer you are trying to communicate with, or you can just directly enter the IP address or hostname.

To exit out of a chat, simply type "exit". 

## Issues
* Message overlap
* Node software interfering with client if ran together
* Inability to easily exit out of an attempted connection

## To-Do
* Curses CLI and GUI
* Offline message reception
* Windows executable
* Group chats
* File-sharing
* Node communication opt-out
