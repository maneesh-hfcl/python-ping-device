import socket
import sys

def connSocket():
    try:
        print("connecting by socket")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        print("socket successfully created")
        clientIpAddr = "192.168.170.155"
        port = 1433
        s.connect((clientIpAddr, port))
        print("client connected by socket") 
        #print(s.recv(1024).decode())
        #ipbyhost = socket.gethostbyname("https://www.google.com")
        #print(ipbyhost)
    except socket.error as err:
        print(err)
        print("Error occured in creating socket")
    except ex as ex:
        print(ex)

if __name__ == "__main__":
    connSocket()