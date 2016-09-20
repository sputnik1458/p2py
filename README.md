# p2p-chat
Completely decentralized cli-based P2P chat

## About
This program uses Python 2.7 and its built-in sockets module. In order to achieve total decentralization, no rendezvous server mediates the connection between the two computers. Rather, each computer attempts to directly connect to each other using their respective external IP addresses.

P2P protocol is acheived by implementing UDP hole punching, simultaneously eliminating the need for a centralized server and port forwarding.

This program uses 2048 bit RSA encryption, and no party except you has access to your private key.

## Usage
You must know each other's external IP address. You can retrieve your own by running `dig +short myip.opendns.com @resolver1.opendns.com`

You may either create a Contacts entry for the computer you are trying to communicate with, or you can just directly enter the IP address or hostname.

Because there is no defined UI, messages that you receive and messages that you are typing will overlap with each other. This will be fixed with the implementation of Curses as a CLI and the development of a GUI.  

To exit out of a chat, simply type "exit". This will currently only work if you are already connected. If you are still connecting and wish to exit, you must completely exit the program with Ctrl-c.
## To-Do
* Add Curses CLI and GUI
* Implement missed message saving
* Create an executable for Windows
* Implement group chats
* Implement file-sharing
