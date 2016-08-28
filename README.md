# p2p-chat
Completely decentralized cli-based P2P chat

## About
The program uses Python 2.7 and its built-in sockets module. In order to achieve total decentralization, no rendezvous server mediates the connection between the two computers. Rather, each computer attempts to directly connect to each other using their respective external IP addresses.

P2P protocol is acheived by implementing UDP hole punching, simultaneously eliminating the need for a centralized server and port forwarding.

## Usage
You must know each other's external IP address. You can retrieve your own by running `dig +short myip.opendns.com @resolver1.opendns.com`

As of now, both users must run the program within a short time period (< 3 minutes) of each other in order to connect.


## To-Do
* Add a "Connected" message when the computers connect to each other. 
* Fix message overwrite bug
* Add a contact system
* Add end-to-end encryption
* Implement missed message saving
* Create an executable for Windows
* Implement group chats
* Implement file-sharing
