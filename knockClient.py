import socket
import config
import hashlib

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


#grab timestmap 
clientSock.sendto(config.INIT_KNOCK.encode('utf-8'), (config.UDP_IP, config.UDP_PORT))
print("Sending '" + config.INIT_KNOCK + "' to port\n", config.UDP_PORT)

#grab server reply
replyFromServer = clientSock.recvfrom(1024)
print(replyFromServer)
timeFromServer = replyFromServer[0].decode('utf-8')
print("Server replied! Server says: ", timeFromServer)
print()

#hash
combo = timeFromServer + config.SECRET_KEY
clientHashKnock = hashlib.sha256(combo.encode()).hexdigest()
clientSock.sendto(clientHashKnock.encode('utf-8'), (config.UDP_IP, config.UDP_PORT))
print("Sending '" + combo + "' to port", config.UDP_PORT)
print("(HASHED) Sending '" + clientHashKnock + "' to port", config.UDP_PORT)




