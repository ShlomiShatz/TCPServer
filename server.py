# Created by: Shlomo Shatz 316093202

# Importing relevant libraries
import socket, sys, os

# Setting up the server to IPv4, TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Gets the port number from commandline arguments, then listens to 5 clients at most
server.bind(('', int(sys.argv[1])))
server.listen(5)

# Loop that accepts clients and work with them
while True:
    # Accepts client
    client_socket, client_address = server.accept()
    # Loop that run for a specific client, and breaks when the client is closed so a new client can be accepted
    while True:
        # Sets the timeout to 1 second
        client_socket.settimeout(1.0)
        try:
            # Tries to accept the client's message
            data = client_socket.recv(4096)
        except:
            # If it took more than one second and timed out, closes the client and breaks the loop
            client_socket.close()
            break
        # If data is recieved successfully, decodes it from bytes to string
        data = data.decode()
        # If the message is empty, closes the socket and breaks the loop
        if len(data) == 0: 
            client_socket.close()
            break
        # Prints the data that was recieved
        print(data)
        # Splits the data by lines
        clientReq = data.split('\r\n')
        # Seperates the connection type (e.g. keep-alive, close) and file name/path
        connectionType = clientReq[2][12:]
        fileName = clientReq[0].split(' ')[1]
        # If the file is '/', switch it to index.html
        if fileName == '/': fileName = '/index.html'
        # If the file requested is redirect, sends appropriate message, closes the socket and breaks the loop
        if fileName == '/redirect':
            package = "HTTP/1.1 301 Moved Permanently\r\nConnection: close\r\nLocation: /result.html\r\n\r\n"
            client_socket.send(package.encode())
            client_socket.close()
            break
        # Completes the file name to a full path taken from the OS
        fpath = os.getcwd() + '/files' + fileName
        # Checks if the file exists
        if os.path.isfile(fpath):
            # If it does, gets its size
            fileSize = os.path.getsize(fpath)
            # Then opens it, sends the header and the file itself
            with open(fpath, 'rb') as f:
                package = "HTTP/1.1 200 OK\r\nConnection: " + connectionType + "\r\nContent-Length: " + str(fileSize) + "\r\n\r\n"
                client_socket.send(package.encode())
                client_socket.sendfile(f)
                # If the type is 'keep-alive', continues the loop with the current client
                if connectionType == 'keep-alive': continue
        # If the file does not exists, send and appropriate message, closes the socket and breaks the loop
        else:
            package = "HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n"
            client_socket.send(package.encode())
            client_socket.close()
            break