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
def removeHeader(respond:str, fileext:str):
    data = b"".join(respond.split(b'\r\n\r\n')[1:])
    if respond.split(b"\r\n\r\n")[0].find(b"Content-Length:") != -1:
        size = int(respond.split(b"\r\n\r\n")[0].split(b"Content-Length:")[1])
    if respond.split(b"\r\n\r\n")[0].find(b"Transfer-Encoding: chunked") != -1: 
        size = "chunked"
    return data, size
def saveFile(data:str, filename:str) -> None:
    f = open(filename, "wb")
    f.write(data)
    f.close()