import socket
import time

#constants
host = ''
port = 8080
buff = 4096
          

def enableWeblite():
    #create server socket
    serveSock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveSock.bind((host,port))
    serveSock.listen(10) #can listen to up to 10, listen also begins accept connections
    print("Weblite is active and is listening!")

    serveSock.settimeout(10)
    while True:
        try:
            print("Weblite waiting for connection requests")
            csock, caddr = serveSock.accept() #client socket, client address
            print("Connected from client: ", caddr)

            #serveSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #not sure what this does but looks important
            clientData = csock.recv(buff).decode()
            print("Processed result: {}".format(clientData))
            csock.send("received, thank u -weblite".encode("utf-8"))

        except socket.timeout as err:
            print(err)
            break


    serveSock.close()
    print("weblite disabled")