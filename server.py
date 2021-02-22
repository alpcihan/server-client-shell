# region Imports

import socket, os, subprocess, threading

# endregion imports

# region Server Class

class Server:
    
    # region Public

    # region Constructor

    # constructor with the port input
    def __init__(self, PORT):
        #self.__HOST = socket.gethostbyname( # Listen on this host
        #              socket.gethostname())  
        self.__HOST = input("Enter the HOST IP: ")
        self.__PORT = PORT                  # Main port to listen on
        self.__sckt = None                  # Main socket
        self.__paths = {}                   # Current working directory of each client
        self.__clients = {}                 # Sockets of the clients
    
    # endregion Constructor

    # region Public Methods 

    # run the server
    def run(self):

        # configure the socket
        try:
            self.__socketConfigure()
        except:
            print("Failed to connect.")

        try:
            # main loop
            while True:
                # accept new client
                conn, address = self.__sckt.accept() 

                # create and start a new thread for the accepted client
                thread = threading.Thread( target= self.__clientHandle,
                                        args= (conn, address, ),
                                        daemon= True )
                thread.start()
        except:
            # if the server disconnects, remove all the clients and make them terminate
            self.__removeAllSockets()
            return
   
    # endregion Public Methods
    
    # endregion Public

    # region Private

    # region Private Methods

    # disconnect the server and the clients
    def __removeAllSockets(self):

        # send remove message to the clients and detach them
        for port in self.__clients:
            client = self.__clients[port]
            client.sendall("DISCONNECT".encode())
            client.detach()

        # close the server socket
        self.__sckt.close()

    # configure the socket then, make it bind and listen
    def __socketConfigure(self):
        self.__sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sckt.bind((self.__HOST, self.__PORT))
        self.__sckt.listen(1)
        print("Server is listening...\nIP:", self.__HOST, "Port:", self.__PORT, "\n")
    
    # thread function for each client
    def __clientHandle(self, conn, address): 
        
        print("New client has connected:", address)

        # Store the working directory and socket of the client
        cPort = address[1] # port of the client as a key value
        self.__paths[cPort] = os.getcwd() # store the working dir
        self.__clients[cPort] = conn # store the socket

        while True:
            
            # receive data
            data = conn.recv(1024)

            # if the client has disconnected
            if data.decode() == "CTRL-C": break

            # handle command cd
            if data.decode().split(' ')[0] == "cd":
                try: 
                    path = os.path.join(self.__paths[cPort], data.decode()[3:])
                    os.chdir(path)
                    self.__paths[cPort] = os.getcwd()
                    conn.sendall("EOFX".encode())
                except: 
                    conn.sendall("Invalid cd command.\n".encode())
            
            # handle other inputs
            else:
                proc = subprocess.Popen( data.decode(),
                                        cwd= self.__paths[cPort],
                                        shell= True,
                                        stdout= subprocess.PIPE,
                                        stderr= subprocess.PIPE,
                                        stdin= subprocess.PIPE )
                stdoutput = proc.stdout.read() + proc.stderr.read()
                
                if stdoutput.decode() == '':
                    stdoutput = "EOFX".encode()

                conn.sendall(stdoutput)
            
        # disconnect
        print("A client has disconnected:", address)
        del self.__clients[cPort] # remove the client from the dictionary
        conn.close()

    # endregion Private Methods
    
    # endregion private

# endregion Server Class

# region Main Function

if __name__ == "__main__":
    server = Server(5000)
    server.run()

# endregion Main Function