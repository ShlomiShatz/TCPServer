# TCP Socket Server for HTTP File Requests using Python
This is a simple TCP socket server that handles HTTP requests for files and serves them to the requesting client in the browser using Python.

## How it Works
The server listens on a specified port for incoming connections. When a client connects, the server waits for an HTTP request. If the request is a GET request for a file, the server looks for the file in the specified directory. If the file is found, the server sends an HTTP response with the file contents. If the file is not found, the server sends an HTTP 404 error.

## Installation and Usage
To use the server, follow these steps:  
1. Clone the repository to your local machine.  
2. Start the server by running python3 server.py <port>.  
3. Open your web browser and navigate to http://localhost:<port>/file/path where <port> is the port number the server is listening on and /file/path is the path to the file you want to request.  

A folder containing files examples is within the repository.

### Enjoy!
