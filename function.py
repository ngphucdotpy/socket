def removeHeader(respond:str, fileext:str) -> str:
    if fileext == "html":
        data = "".join(respond.decode().split("\r\n\r\n")[1:])
    else:
        data = "".join(respond.decode("latin1").split("\r\n\r\n")[1:])
    return data
def saveFile(data:str, filename:str, fileext:str) -> None:
    if fileext == "html":
        f = open(filename, "w")
        f.write(data)
    else:
        f = open(filename, "wb")
        f.write(data.encode("latin1"))