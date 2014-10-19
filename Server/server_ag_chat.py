#!/usr/bin/env python

"""
A simple chat server by Ashish Gaikwad <ash.gkwd@gmail.com>
"""

import socket, select

# Function to have custom names set by clients
def getUserName (sock):
  if sock.getpeername() in nice_names:
    return str(nice_names[sock.getpeername()])
  else:
    return str(sock.getpeername())

#Function to broadcast chat messages to all connected clients
def broadcast_data (sock, message):
  #Do not send the message to master socket and the client who has send us the message
  for socket in CONNECTION_LIST:
    if socket != server_socket and socket != sock :
      try :
        socket.send(message)
        socket.send("_> ")
      except :
        # broken socket connection may be, chat client pressed ctrl+c for example
        socket.close()
        if socket in CONNECTION_LIST:
          CONNECTION_LIST.remove(socket)

if __name__ == "__main__":
  nice_names = dict() # nice names set by clients
  # List to keep track of socket descriptors
  CONNECTION_LIST = []
  RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
  PORT = 5000

  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # this has no effect, why ?
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server_socket.bind(("0.0.0.0", PORT))
  server_socket.listen(10)

  # Add server socket to the list of readable connections
  CONNECTION_LIST.append(server_socket)

  print "Chat server started on port " + str(PORT)

  while 1:
    # Get the list sockets which are ready to be read through select
    read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])

    for sock in read_sockets:
      #New connection
      if sock == server_socket:
        # Handle the case in which there is a new connection recieved through server_socket
        sockfd, addr = server_socket.accept()
        CONNECTION_LIST.append(sockfd)
        print "Client (%s, %s) connected" % addr

        broadcast_data(sockfd, "[%s:%s] entered room\n" % addr)

      #Some incoming message from a client
      else:
        # Data recieved from client, process it
        try:
          #In Windows, sometimes when a TCP program closes abruptly,
          # a "Connection reset by peer" exception will be thrown
          data = sock.recv(RECV_BUFFER)
          if data:
            if data[0:5] == ":name" and len(data) > 7:
              new_name = data.split()
              nice_names[sock.getpeername()] = new_name[1]
              broadcast_data(sock, "\r" + '[Renamed] <' + str(sock.getpeername()) + '> to "' + getUserName(sock) + '"')
            else:
              broadcast_data(sock, "\r" + '<' + getUserName(sock) + '> ' + data)

        except Exception as e:
          broadcast_data(sock, "Client (%s, %s) is offline \r" % addr)
          print "Client (%s, %s) is offline" % addr
          sock.close()
          if sock in CONNECTION_LIST:
            CONNECTION_LIST.remove(sock)
          print e
          continue

  server_socket.close()