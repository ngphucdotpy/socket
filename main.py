import socket
import miscellaneous as misc
import function as func

URL = "http://www.google.com/"

# URL = "http://www.httpwatch.com/httpgallery/chunked/chunkedimage.aspx"

# URL = "http://anglesharp.azurewebsites.net/Chunked"

port = 80
domain, path, filename, fileext = misc.extractInfo(URL)
print(misc.extractInfo(URL))

host = "Host: {}\r\n".format(domain)
connection = "Connection: Keep-Alive\r\n"

t = socket.gethostbyname(domain) #

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((domain, port))
s.settimeout(3.0)
print("{} {}".format(t, port))
print("Connected")

request = "GET /{} HTTP/1.1\r\n{}{}\r\n".format(path, host, connection)
s.send(request.encode())
print("Request is sent")

respond = func.getRespond(s, fileext)
data, size, type = func.removeHeader(respond, fileext)

# if type == "chunked":
#     while size != 0:
#     # for i in range(0, 33):
#         respond = func.getRespond(s, fileext)
#         if not respond:
#             break
#         data += b"".join(respond.split(b'\r\n')[1:])
#         print(respond)
#         print(" ")
#         size = int(respond.split(b'\r\n')[0], 16)
#         # print(size)

if type == "chunked":
    # while size != 0:
    for i in range(0, 26):
        print("1")
        respond = func.getRespond(s, fileext)
print(respond)

# print(respond)
s.settimeout(None)
func.saveFile(data, filename)

s.close()

# https://stackoverflow.com/questions/52599656/how-to-send-files-in-chunks-by-socket
# https://bunny.net/academy/http/what-is-chunked-encoding/
# https://en.wikipedia.org/wiki/Chunked_transfer_encoding