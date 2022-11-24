import socket
import sys
import threading
import miscellaneous as misc
import function as func


# URL = "http://www.httpwatch.com/httpgallery/chunked/chunkedimage.aspx"

# URL = "http://web.stanford.edu/class/cs224w/slides/02-tradition-ml.pdf"

URL = "http://www.google.com/index.html"

port = 80
domain, path, filename, fileext = misc.extractInfo(URL)
print(misc.extractInfo(URL))

host = "Host: {}\r\n".format(domain)
connection = "Connection: Keep-Alive\r\n"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((domain, port))
s.settimeout(5.0)
print("Connected")

request = "GET /{} HTTP/1.1\r\n{}{}\r\n".format(path, host, connection)
s.send(request.encode())
print("Request is sent")

respond = func.getRespond(s, fileext)
data, size, type = func.removeHeader(respond, fileext)

if type == "chunked":
    while size != 0:
        respond = func.getRespond(s, fileext)
        data += b"".join(respond.split(b'\r\n')[1:])
        print(data)
        size = int(respond.split(b'\r\n')[-3], 16) #html
        # size = int(respond.split(b'\r\n')[0], 16) #aspx
        print(respond.split(b'\r\n')[0])

# print("\n\n")
# print(respond)


s.settimeout(None)
func.saveFile(data, filename)

s.close()

# https://stackoverflow.com/questions/52599656/how-to-send-files-in-chunks-by-socket
# https://bunny.net/academy/http/what-is-chunked-encoding/
# https://en.wikipedia.org/wiki/Chunked_transfer_encoding
# https://realpython.com/python-sockets/
# https://www.bogotobogo.com/python/python_network_programming_server_client_file_transfer.php