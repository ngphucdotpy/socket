import socket


def getRespond(s:socket, fileext:str) -> str:
    if fileext == "html" or fileext == "aspx":
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
        type = "content-length"
    # if respond.split(b"\r\n\r\n")[0].find(b"Transfer-Encoding: chunked") != -1: 
    #     size = "chunked"
    elif respond.split(b"\r\n\r\n")[0].find(b"Transfer-Encoding: chunked") != -1:
        tmp = respond.split(b'\r\n\r\n')
        data = b"".join(tmp[1].split(b'\r\n')[1:])
        type = "chunked"
        size = int(tmp[1].split(b'\r\n')[0].decode(), 16)
    return data, size, type

def saveFile(data:str, filename:str) -> None:
    f = open(filename, "wb")
    f.write(data)
    f.close()