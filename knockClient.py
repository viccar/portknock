import socket
import config
import hashlib
import datetime

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #set up socket

currTime = str(datetime.datetime.now().time().replace(microsecond=0)) #get current time w/o millisec
#combo = currTime + config.TEST_KEY #a test case, this will fail
combo = currTime + config.SECRET_KEY #concatenate time + share secret
seqHash = hashlib.sha256(config.SECRET_KNOCK.encode()).hexdigest()
clientHashKnock = hashlib.sha256(combo.encode()).hexdigest() #hash the new key
concatKnock = seqHash + ":" + clientHashKnock
clientSock.sendto(concatKnock.encode(), (config.UDP_IP, config.UDP_PORT)) #send code

#print statements
print("current time when data SENT to SERVER: ", currTime)
print("Sending '(" + combo + ") +" + config.SECRET_KNOCK + "' to port", config.UDP_PORT)
print("(HASHED) Sending '" + concatKnock + "' to port", config.UDP_PORT)




