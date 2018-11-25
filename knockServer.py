import socket
import sys
import weblite
import config
import uuid
import hashlib
import datetime
import time
import _thread


def hashPW(pw):
    #salt = uuid.uuid4().hex #uuid lib to generate random number
    #return hashlib.sha256(salt.encode() + pw.encode()).hexdigest() + ':' + salt
    return hashlib.sha256(pw.encode()).hexdigest()


def enableKnockServer():
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        serverSock.bind((config.UDP_IP, config.UDP_PORT))
    except socket.error as e:
        print(e)

    print('starting up on %s port %d' % (config.UDP_IP, config.UDP_PORT))
    serverHashKnock = None
    deny = None
    
    while True:
        print("[ Still waiting to receive knocks on UDP server...]")
        data, addr = serverSock.recvfrom(1024) #receive a message from client
        currTime = str(datetime.datetime.now().time().replace(microsecond=0)) 
        print("curr time when data RECEIVED from CLIENT: ", currTime)
        dataDec = data.decode("utf-8") #decode client message (is back to string not bytes)
        print("Decoded client data: ", dataDec)
        
        serverHashKnock = hashPW(currTime+config.SECRET_KEY)
        print("server hash: ", serverHashKnock)
        if dataDec == serverHashKnock:
            print("a match in the hashes was found!")

            serverHashKnock = None
            print("reset server hash knock")
            print("weblite enabled!\n")
            if config.numClient < config.MAX_CLIENT:
                _thread.start_new_thread(weblite.enableWeblite,(addr,))
                config.numClient = config.numClient + 1
            else:
                print("reached max number of user to connect to knockServer")

            #weblite.enableWeblite(addr)
                
        else:
                print("invalid knock found")
                deny = True
                break

        #print("-RECEIVED-\nbytes: %d\nfrom: %s\nmessage: %s" % (len(data), addr, data))
        print()

    if deny == True:
        serverSock.close()
        print("Server will now disable for 10 sec to avoid DOS")
        time.sleep(10)
        print("Socket will start again now\n")
        deny = False
        enableKnockServer()

#main
enableKnockServer()

