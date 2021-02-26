# Server-Client Shell

The purpose of the project is to create a shell-based server-client system where a single or multiple clients can redirect their shell commands to the server module simultaneously. Then the server executes the commands at the running machine and redirects the outputs to the related client.

Each client can work on a different directory on the same target machine.

## Table of contents
* [How to run](#how-to-run)
* [How to use](#how-to-use)
* [Sample run](#sample-run)
* [License](#license)

## How to run
### Run the server
- Run the following shell command on the target machine. 

      $ python3 server.py

### Run a client
- Run the following shell command on any machine to access from.

      $ python3 client.py

## How to use
1) Run the “server.py” on the target machine, then enter a valid IP to listen to. If the server starts it will display “Server is listening... {IP} {PORT}”. Else it will terminate.
2) Run the “client.py” on any machine to instantiate a new client.
3) Client program will ask for an IP to connect. Enter the IP that is displayed at the server
program. If the connection is not successful the client program will display “Could not connect to the server!” and terminate. If the connection is successful the client program will “Connected to the server!” and the server program will display “New client has connected {IP} {Port of the client connection} ”
4) If the connection is successful the client can begin to enter commands (ex: pwd, cd a, mkdir -p /a/b/c, git init, etc.)
5) The same process could be applied with multiple client programs simultaneously.
6) Press "CTRL+C" key to close the server or a client.

## Sample run

- Here is a sample run where:

  - **S$** denotes the server

  - **Cn$** denotes the client n (ex: C1$ is the client 1)

  - **Bold texts** are the inputs (“ex: S$ **python3 server.py**” is the input of the server)

  - **Regular texts** are the outputs (“ex: C2$ Trying to connect...” is the output of the client 2)

--------------------------------------
   S$ **python3 server.py**

   S$ Server is listening...
   
   S$ Enter the HOST IP: **0.0.0.0**

   S$ IP:127.0.0.1 Port: 500

   C1$ **python3 client.py**

   C1$ Enter an IP to connect: **999.999.999**

   C1$ Trying to connect...

   C1$ Could not connect to the server!

   C1$ **python3 client.py**

   C1$ Enter an IP to connect: **127.0.0.1**

   C1$ Connected to the server! (Press CTRL-C to exit.)

   S$ New client has connected: (‘127.0.0.1’, 51474)

   C1$ > **pwd**

   C1$ /Users/alp/Documents/client-server/server

   C2$ **python3 client.py**

   C2$ Enter an IP to connect: **127.0.0.1**

   C2$ Connected to the server! (Press CTRL-C to exit.)

   S$ New client has connected: (‘127.0.0.1’, 51489)

   C2$ > **pwd**

   C2$ /Users/alp/Documents/client-server/server

   C2$ > **cd ..**

   C2$ > **cd ..**

   C2$ > **pwd**

   C2$ /Users/alp/Documents

   C1$ > **cd ..**

   C1$ > **pwd**

   C1$ /Users/alp/Documents/client-server

   C1$ **mkdir -p /a/b/c**

   C1$ mkdir: /a/b/c: Read-only file system

   C1$ **mkdir -p a/b/c**

   C2$ **cd client-server/a/b/c**

   C2$ **pwd**

   C2$ /Users/alp/Documents/client-server/a/b/c

   C2$ **^C**

   S$ A client has disconnected: (127.0.0.1, 51474)

   C1$ **^C**

   S$ A client has disconnected: (127.0.0.1, 51489)

   C3$ **python3 client.py**

   C3$ Enter an IP to connect: **127.0.0.1**

   C3$ Connected to the server! (Press CTRL-C to exit.)

   S$ New client has connected: (‘127.0.0.1’, 51552)

   C4$ **python3 client.py**

   C4$ Enter an IP to connect: **127.0.0.1**

   C4$ Connected to the server! (Press CTRL-C to exit.)

   S$ New client has connected: (‘127.0.0.1’, 51557)

   S$ **^C**

   C3$ Server disconnected. Press Enter to exit.

   C4$ Server disconnected. Press Enter to exit.

   C3$ **Enter keypress**

   C4$ **Enter keypress**
    
 -------------------
 
 ## License
 [MIT](./LICENSE)
