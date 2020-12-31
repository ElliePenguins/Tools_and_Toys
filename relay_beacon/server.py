#!/bin/python3

import subprocess
import socket
import sys
import pyotp 

class NetManager:

    # NOTE, gen a new key before using.
    key = "3232323232323232";
    local_addr = "0.0.0.0"
    remote_addr = "127.0.0.1";
    port = 0 
    data = ""
    script = "";

    def __init__(self, port, script = ""):
#        self.setAddress();
        self.script = script;
        self.port = int(port)
        print();
        print("key:\t" + self.key);
        print("LADDR:\t" + self.local_addr);
        print("RADDR:\t" + self.remote_addr);
        print("PORT:\t" + str(self.port));
        print();

    def genKey(self):
        self.key = pyotp.random_base32();

    def getKey(self):
        return self.key;

    def setKey(self, key):
        self.key = key;

    def genPass(self):
        totp = pyotp.TOTP(self.key);
        self.data = totp.now()

    def setAddress(self):
        self.local_addr = socket.gethostbyname(
                socket.gethostname());

    def createSocket(self):
        try:
            s = socket.socket()
            s.setsockopt(socket.SOL_SOCKET, 
                    socket.SO_REUSEADDR, 1);
            s.bind(('',self.port));
            s.listen();

            while(True):
                c, addr = s.accept()
                self.genPass();
                if self.isAccepted(
                        c.recv(1024).decode()):
                    self.runScript(str(addr[0]));
                # Should it reply with a status?
        except:
            print("\nProgram, stop.");
            s.close();

    def isAccepted(self, passwd):
        if passwd == self.data:
            return True;
        else:
            return False;

    def checkScript(self):
        if len(self.script) > 0:
            return True;
        else:
            return False;

    def runScript(self, address):
        if self.checkScript():
            subprocess.call(
                    "./" + self.script +
                    " " + address, shell=True);


# Port, run-script
if len(sys.argv) == 2:
    run = NetManager(sys.argv[1]);
    run.createSocket();
elif len(sys.argv) == 3:
    run = NetManager(sys.argv[1], sys.argv[2]);
    run.createSocket();
else:
    print("usage: ./server <port> [script]\n");

