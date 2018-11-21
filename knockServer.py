import socket
import sys
import weblite
import config
import uuid
import hashlib
import datetime

def hashPW(pw):
    #salt = uuid.uuid4().hex #uuid lib to generate random number
    #return hashlib.sha256(salt.encode() + pw.encode()).hexdigest() + ':' + salt
    return hashlib.sha256(pw.encode()).hexdigest()

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    serverSock.bind((config.UDP_IP, config.UDP_PORT))
except socket.error as e:
    print(str(e))

print('starting up on %s port %d' % (config.UDP_IP, config.UDP_PORT))
serverHashKnock = None
knownIP = None

while True:
    print("Waiting to receive knocks...")
    data, addr = serverSock.recvfrom(1024) #receive a message from client
    dataDec = data.decode("utf-8") #decode client message (is back to string not bytes)
    print("Decoded client data: ", dataDec)
    
    
    if dataDec == "knock": #a general knock is received
        currTime = datetime.datetime.now().time()
        currTime = str(currTime)
        knownIP = addr

        print("current time is ", currTime)

        bytesTime = currTime.encode("utf-8")
        serverSock.sendto(bytesTime, addr) #send a reply of the current time to the ip that knocked
        serverHashKnock = hashPW(currTime+config.SECRET_KEY)
        print("current server hash is: ", serverHashKnock)
    else:
        if dataDec == serverHashKnock:
            print("a match in the hashes was found!")
            if addr == knownIP:
                serverHashKnock = None
                print("reset server hash knock")
                weblite.enableWeblite()
                
        else:
            print("invalid knocks")

    print("-RECEIVED-\nbytes: %d\nfrom: %s\nmessage: %s" % (len(data), addr, data))
    print()