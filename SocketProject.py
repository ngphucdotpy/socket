import socket

class SocketProject:
    def __init__(self, URL:str):
        self.URL = URL
        self.domain = self.URL.split("://")[1].split("/")[0]
        self.path = list(filter(None, self.URL.split("://")[1].split("/")[1:]))
        if len(self.path) > 0:
            self.fileName = self.domain + "_" + self.path[-1]
        else:
            self.path.append("index.html")
            self.fileName = self.domain + "_" + self.path[0]
        self.path = "/".join(self.path)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5.0)

        # main
        self.__connect()
        self.__request()
        self.__receive()

        self.socket.close()
    
    def __connect(self):
        try:
            print("Connecting")
            self.socket.connect((self.domain, 80))
            print("Successful")
        except socket.error as er:
            print("Error: {}".format(er))
            self.socket.close()

    def __request(self):
        host = "Host: {}\r\n".format(self.domain)
        connection = "Connection: Keep-Alive\r\n"
        request = "GET /{} HTTP/1.1\r\n{}{}\r\n".format(self.path, host, connection)
        self.socket.send(request.encode())       

    def __removeHeader(self, respond):
        return respond.split(b"\r\n\r\n")[1]

    def __getContentLength(self, respond):
        if respond.find(b"Content-Length:") != -1:
            return int(respond.split(b"Content-Length:")[1].split(b"\r\n")[0])
        return -1

    def __getChunkLength(self, data):
        raw = data.split(b"\r\n")
        if len(raw) >= 2:
            return b"\r\n".join(raw[1:]), int(raw[0], 16)
        if len(raw) == 0:
            return b'', 0
        return raw[0], 0

    def __receiveContentLength(self, respond, size):
        f = open(self.fileName, "wb")
        data = self.__removeHeader(respond)
        f.write(data)
        rsize = size - len(data)
        try:
            while True:
                if (not data) or rsize <= 0:
                    break
                data = self.socket.recv(32)
                rsize -= 32
                f.write(data)
        except socket.error as er:
            print("Error: {} or server disconnected. Terminated.".format(er))
            self.socket.close()
        f.close()

    def __receiveChunk(self, respond):
        f = open(self.fileName, "wb")
        data, size = self.__getChunkLength(self.__removeHeader(respond))
        try:
            while True:
                if data == b"0" or size == 0:
                    break
                f.write(data)
                remainChunkSize = size - len(data)
                while remainChunkSize > 0:
                    if remainChunkSize < 32:
                        data = self.socket.recv(remainChunkSize + 2)
                    else:
                        data = self.socket.recv(32)
                    remainChunkSize -= 32
                    f.write(data)
                data, size = self.__getChunkLength((self.socket.recv(32)))
        except socket.error as er:
            print("Error: {} or server disconnected. Terminated.".format(er))
            self.socket.close()
        f.close()

    def __receive(self):
        respond = self.socket.recv(1024)
        size = self.__getContentLength(respond)
        if size != -1:
            self.__receiveContentLength(respond, size)
        else:
            self.__receiveChunk(respond)

SocketProject("http://www.httpwatch.com/httpgallery/chunked/chunkedimage.aspx")
# SocketProject("http://www.google.com")
# SocketProject("http://web.stanford.edu/class/cs224w/slides/")

# print(a.URL)
# print(a.domain)
# print(a.path)
# print(a.fileName)