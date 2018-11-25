#CONSTANTS
UDP_IP = ''
UDP_PORT = 5005
WEB_HOST = ''
WEB_PORT = 8080
BUF_SIZE = 4096
MAX_CLIENT = 10
SECRET_KEY = 'Nintendo' #shared secret, should work
TEST_KEY = 'Sega' #will not work
numClient = 0

#for HTML stuff
OK_IMAGE = "HTTP/1.0 200 OK\r\nContent-Type:image/gif\r\n\r\n"
OK_TEXT = "HTTP/1.0 200 OK\r\nContent-Type:text/html\r\n\r\n"
NOTOK_404 = "HTTP/1.0 404 Not Found\r\nContent-Type:text/html\r\n\r\n"
MESS_404 = "<html><body><h1>FILE NOT FOUND</h1></body></html>"
