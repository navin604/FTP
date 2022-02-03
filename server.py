from socket import *

hostname = gethostname()
ip = gethostbyname(hostname)
host = ''
port = 7005
dataport=7007
command = None


def send(socket):
    """Sends file to client"""
    global command
    with open(file, "rb") as f:
        while True:
            binaryBytes = f.read(1024)
            if not binaryBytes:
                break
            socket.send(binaryBytes)
    socket.close()
    command = None

def receive(socket):
    """Receives file from client"""
    global command
    with open(file, "wb") as f:
        while True:
            fileReceive = socket.recv(1024)
            if not fileReceive:
                break
            f.write(fileReceive)
    socket.close()
    command = None


"""Creates and binds socket"""
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.listen(5)

while True:
    """Accepts new connections and receives FTP request"""
    clientSocket, address = serverSocket.accept()
    print(f" {address} has connected ")

    while True:
        data = clientSocket.recv(1024).decode()
        if not data:
            break
        arr = data.split('+')
        command = arr[0]
        file = arr[1]
        print(f"Received a {command} request")
        clientSocket.send(f"{ip}+{dataport}".encode())
        print(f"Sending data channel information")

        """Initializes data channel"""
        dataChannel = socket(AF_INET, SOCK_STREAM)
        dataChannel.bind((host, dataport))
        dataChannel.listen(5)
        dataClient, dataAddress = dataChannel.accept()
        if command == 'get':
            send(dataClient)
        elif command == 'send':
            receive(dataClient)
    clientSocket.close()






