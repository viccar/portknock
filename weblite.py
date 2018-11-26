import socket
import time
import config

def enableWeblite(addr):
    print("addr connected from knockServer is: ", addr)

    #create server socket
    serveSock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serveSock.bind((config.WEB_HOST,config.WEB_PORT))
    serveSock.listen(10) 
    print("Weblite is active and is listening!")

    serveSock.settimeout(10) #timeout is 10 seconds
    while True:
        try:
            print("Weblite waiting for connection requests")
            csock, caddr = serveSock.accept() #client socket, client address
            if caddr[0] not in config.KNOWN_IP: #lets just validate and make sure this IP is known
                print("this IP is not known to weblite or knockserver. breaking")
                break

            clientData = str(csock.recv(config.BUF_SIZE).decode())
            command, fileName = clientData.split()[:2] #grabs the http command plus filename
            fileName = fileName[1:]
            fileTitle, fileType = fileName.split('.')
            print("commmand: %s\nhtml: %s\n" % (command, fileName))
            print("file title: %s\nfile type: %s\n" % (fileName, fileType))

            if command != "GET":
                print("ERROR - Not a GET --- received command = '%s' \n" % command)
                break
            if fileType != "html":
                print("incorrect file type, disabling weblite")
                break

            try:
                fileO = open(fileName, 'r') #we skip the first character to cause of "/"
            except IOError:
                print("could not open file")
                break
    
            csock.send(config.OK_TEXT.encode())
            with fileO:
                content = fileO.read()
                print(content)
                csock.send(content.encode())
            
            
            #print("---received GET----")
            #print("Processed result: {}".format(clientData))
            #print("-------------------")

        except socket.timeout as err:
            print(err)
            break


    serveSock.close()
    print("weblite disabled\n")
