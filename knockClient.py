import socket
import config
import hashlib
import datetime

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

currTime = str(datetime.datetime.now().time().replace(microsecond=0)) #get time w/o millisec
#combo = currTime + config.TEST_KEY #will fail
combo = currTime + config.SECRET_KEY #concatenate time + share secret
clientHashKnock = hashlib.sha256(combo.encode()).hexdigest() #hash the new key
clientSock.sendto(clientHashKnock.encode('utf-8'), (config.UDP_IP, config.UDP_PORT)) #sends code
print("current time when data SENT to SERVER: ", currTime)
print("Sending '" + combo + "' to port", config.UDP_PORT)
print("(HASHED) Sending '" + clientHashKnock + "' to port", config.UDP_PORT)




