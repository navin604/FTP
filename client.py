"""
To run this program you can either specify 4 arguments in the CLI or just run the program.

Command can be "get" or "send"

 python .\client.py [host] [port] [command] [filename]
 or
 python .\client.py

"""

import sys
from socket import *

serverHost = 'localhost'
serverPort = 7005
ftpCommand = 'send'
file = 'Test.txt'

hostname = gethostname()
local_ip = gethostbyname(hostname)

def get(socket):
    """Receives file from server"""
    with open(file, "wb") as f:
        while True:
            fileReceive = socket.recv(1024)
            if not fileReceive:
                break
            f.write(fileReceive)
    print('File Received')
    socket.close()


def send(socket):
    """Sends file"""
    with open(file, "rb") as f:
        while True:
            binaryBytes = f.read(1024)
            if not binaryBytes:
                break
            socket.send(binaryBytes)
    print('File Sent')
    socket.close()


if __name__ == "__main__":
    """Handles stdin arguments"""
    if len(sys.argv) == 5:
        serverHost = sys.argv[1]
        serverPort = sys.argv[2]
        ftpCommand = sys.argv[3]
        file = sys.argv[4]

    serverPort = int(serverPort)
    ftp = ftpCommand.lower()

    """Creates socket and connects to server"""
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((serverHost, serverPort))
    s.send(f"{ftp}+{file}".encode())
    receivedData = s.recv(1024).decode()
    print(f'Connection Completed')
    s.close()

    """Receives data channel port from server"""
    arr = receivedData.split('+')
    dataPort = arr[1]

    """Creates socket and connects to data channel"""
    dataSocket = socket(AF_INET, SOCK_STREAM)
    dataSocket.connect((serverHost, int(dataPort)))
    print(f'Initiating Data Channel')

    if ftpCommand == 'get':
        get(dataSocket)
    else:
        send(dataSocket)
