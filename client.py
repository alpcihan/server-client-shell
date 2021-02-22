# region Imports

import socket, os, subprocess, threading, sys

# endregion Imports

# region Client Class

class Client:
    
    # region Public

    # region Constructor

    # constructor with host IP and Port parameters
    def __init__(self, HOST, PORT):
        self.__HOST = HOST
        self.__PORT = PORT
        self.__sckt = None
        self.__connected = False
    
    #endregion Constructor

    # region Public Methods

    # connect and run the client
    def run(self):

        # connect the client to the server
        self.__connected = self.__connectSocket()

        # main loop
        while self.__connected:
            
            # receive from the server as a thread
            thRecive = threading.Thread(target=self.__receiveBackground, daemon= True)
            thRecive.start()

            # get input
            try:
                cmd = input("> ")
            except: # if the client presses "ctr+c" then, exit
                self.__sckt.sendall("CTRL-C".encode())
                thRecive.join()
                self.__sckt.close()
                break

            # send the input
            if self.__connected:
                self.__sckt.sendall(cmd.encode())

            thRecive.join()

        # disattach the client socket
        self.__sckt.close()
    
    # endregion Public Methods

    # endregion Public

    # region Private 

    # region Private Methods

    # receive from the server
    def __receiveBackground(self):

        # receive data
        data = self.__sckt.recv(1024)
        
        # disconnect if the server is offline
        if data.decode('utf-8') == "DISCONNECT":
            print("Server disconnected. Press ENTER to exit.")
            self.__connected = False
            self.__sckt.close()
            self.__sckt.detach()
            return

        # print without 'EOFX'
        elif data.decode('utf-8') != 'EOFX':
            print(data.decode('utf-8'), end='') 
    
    # connect the socket to the server
    def __connectSocket(self):
        
        self.__sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            print("Trying to connect...")
            self.__sckt.connect((self.__HOST, self.__PORT))
            print("Connected to the server! (Press CTRL-C to exit.)")
            return True
        except:
            print("Could not connect to the server!")
            return False

    # endregion Private Methods

    # endregion Private

# endregion Client Class

# region Main Function

if __name__ == "__main__":

    client = Client(input("Enter an IP to connect: "), 5000)
    client.run()

# endregion Main Function