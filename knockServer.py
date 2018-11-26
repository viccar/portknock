import socket
import sys
import weblite
import config
import uuid
import hashlib
import datetime
import time
import _thread


def hashPW(pw): #hashing
    #salt = uuid.uuid4().hex #uuid lib to generate random number
    #return hashlib.sha256(salt.encode() + pw.encode()).hexdigest() + ':' + salt
    return hashlib.sha256(pw.encode()).hexdigest()


def enableKnockServer():
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #set up server
    serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #exception handling for UDP server listen
    try: 
        serverSock.bind((config.UDP_IP, config.UDP_PORT))
    except socket.error as e:
        print(e)

    print('starting up on %s port %d' % (config.UDP_IP, config.UDP_PORT))
    serverHashKnock = None #temp var of hash key
    deny = None #check if knock is correct
    
    while True: #while listening
        print("[ Still waiting to receive knocks on UDP server...]")
        
        data, addr = serverSock.recvfrom(1024) #receive a message from client
        currTime = datetime.datetime.now().replace(microsecond=0) #when messaged is received, get current time
        #print("actual time recevied: ", currTime)
        #currTime = currTime + datetime.timedelta(seconds=1)
        currTime = str(currTime)
        print("curr time when data RECEIVED from CLIENT: ", currTime)
        
        
        dataDec = data.decode() #decode client message (is back to string not bytes)
        dataSplit = dataDec.split(":")
        
        print("\n-RECEIVED-\nbytes: %d\nfrom: %s\nmessage: %s" % (len(data), addr, data)) #the message received

        
        serverHashKnock = hashPW(currTime+config.SECRET_KEY) #now hash time+key
        print("server hash: ", serverHashKnock)

        if dataSplit[0] == hashPW(config.SECRET_KNOCK): #if a match is found
           
            print("correct knock sequence")
            
            if dataSplit[1] == serverHashKnock:
                
                print("and correct secret")

                if addr[0] not in config.KNOWN_IP:
                    config.KNOWN_IP.append(addr[0]) #remember this host as a known ip
                
                serverHashKnock = None #reset key to none as it will always change depending on time

                print("weblite enabled by client %s!\n" % addr[0])
                
                if config.numClient < config.MAX_CLIENT: #while number of available client does not exceed 10
                    _thread.start_new_thread(weblite.enableWeblite,(addr,)) #start a new thread of weblite
                    config.numClient = config.numClient + 1 #increment num of known clients
                else:
                    print("reached max number of user to connect to knockServer")
                    break #else cant connect

            else:
                print("but incorrect key")
                serverHashKnock = None 
                deny = True
                break
                
        else: #if match is wrong, an invalid knock has occured
                print("invalid knock found")
                deny = True #deny retry and break from listening
                break
        print()

    if deny == True: #deny second attempt by timeout
        serverSock.close()
        print("Server will now disable for 10 sec to avoid DOS")
        time.sleep(10)
        print("Socket will start again now\n")
        deny = False #restart
        enableKnockServer()

#main
enableKnockServer()

