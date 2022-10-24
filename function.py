import socket

def getRespond(s:socket, fileext:str) -> str:
    if fileext == "html":
        respond = s.recv(512*1024)
    else:
        respond = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            respond += chunk
    return respond
def removeHeader(respond:str, fileext:str) -> str:
    if fileext == "html":
        encodeMethod = "UTF-8"
    else:
        encodeMethod = "latin1"
    data = "".join(respond.decode(encodeMethod).split("\r\n\r\n")[1:]).encode(encodeMethod)
    return data
def saveFile(data:str, filename:str) -> None:
    f = open(filename, "wb")
    f.write(data)
    f.close()