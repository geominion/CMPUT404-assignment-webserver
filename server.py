import SocketServer
# coding: utf-8
import os
from os import curdir

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):

    
    def handle(self):

        self.data = self.request.recv(1024).strip()
        hold = self.data
        "".join(hold)
        parsed = hold.split()
        verify = False
        response = ""
        path = parsed[1]
        initial = "HTTP/1.1 ";
        conType  = "Content-Type: text/"
        webdir = "/www"
        default = "/index.html"
        check = "." + path
        for dirname, dirnames, filenames in os.walk("./www"):
            dirname = dirname.replace("/www", "")
            for subdirname in dirnames:
                dirpath = os.path.join(dirname, subdirname)
                if check == dirpath:
                    path = curdir + webdir + path
                    verify = True
                elif check == (dirpath + "/"):
                    path = curdir + webdir + "/" + path + default
                    verify = True
            for filename in filenames:
                if check == os.path.join(dirname, filename):
                    path = curdir + webdir + path
                    verify = True
        type = "css"
        if path.endswith(type) != True:
            type = "html"
        if parsed[0] == "GET":
            if path == "/":
                verify = True
                path = curdir + webdir + default
            if verify == True:
                f = open(path)
                page = f.read()
                f.close()
                response = initial + "200 OK\n" + conType + type + "\n\n\n" + page
            else:
                response = initial + "404 NOT FOUND\n" + conType + type + "\n\n" + "<h1>404 NOT FOUND</h1>"
        else:
            response = initial + "404 NOT FOUND\n" + conType + type + "\n\n" + "<h1>404 NOT FOUND</h1>"
        self.request.sendall(response)
                
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
