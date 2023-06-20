import socket

localIP = "127.0.0.1"
localPort = 9999
bufferSize = 1024

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print(f"Server is up and listening on {localIP}:{localPort}")


while True:
    res = UDPServerSocket.recvfrom(bufferSize)
    res = str(res[0]) + ", " + str(res[1])
    print(res)
