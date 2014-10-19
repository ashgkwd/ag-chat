ag-chat
=======

Chat application with client and server architecture. It is designed to work from command line.

Server is implemented in Python. Client is written in Java.

It is Many to Many chat app without authontication. It is possible to use "telnet" as a client.

To run Java client:
-------------------

java ClientAgChat 127.0.0.1 5000

To run telnet client:
---------------------

telnet localhost 5000

To run Python server:
---------------------

python server_ag_chat.py