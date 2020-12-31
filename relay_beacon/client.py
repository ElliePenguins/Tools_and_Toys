#!/sbin/python3

import sys
import socket
import pyotp

# Create passwd/key managment class. 
# Maybe base class of common attr.

# TODO, need ssl/tls 
# TODO, remove debug statements.
# TODO, modify classes to use inheritance.

class NetManager:

    # NOTE, gen a new key before using.
    key = "3232323232323232";
    local_addr = "0.0.0.0"
    remote_addr = "127.0.0.1";
    data = ""
    port = 0; 

    def __init__(self, server_addr, port):
        self.setAddress();
        self.remote_addr = server_addr;
        self.port = int(port);
        print();
        print("key:\t" + self.key);
        print("LADDR:\t" + self.local_addr);
        print("RADDR:\t" + str(self.remote_addr));
        print();

    # Create new key.
    def genKey(self):
        self.key = pyotp.random_base32();

    # Set pre-generated key, eg. sync server/client.
    def setKey(self, key):
        self.key = key;

    # Output the current key, or maybe save it
    # to a file to use on other machine.
    def getKey(self):
        return self.key;

    def genPass(self):
        totp = pyotp.TOTP(self.key);
        self.data = totp.now()

    def setAddress(self):
        self.local_addr = socket.gethostbyname(
                socket.gethostname());

    def createSocket(self):
        s = socket.socket(socket.AF_INET, 
                socket.SOCK_STREAM);
        s.connect((self.remote_addr,
            self.port));
        self.genPass();
        s.sendall(self.data.encode());

        print("sent");


# port number
if len(sys.argv) > 2:
    run = NetManager(sys.argv[1], sys.argv[2]);
    run.createSocket();
else:
    print("./client.py <ip addr> <port>");
