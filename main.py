import socket
import miscellaneous as misc
import function as func

URL = "http://example.com/index.html"

#URL = "http://web.stanford.edu/dept/its/support/techtraining/techbriefing-media/Intro_Net_91407.ppt"

port = 80
domain, path, filename, fileext = misc.extractInfo(URL)
print(misc.extractInfo(URL))

host = "Host: {}\r\n".format(domain)
connection = "Connection: Keep-Alive\r\n"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((domain, port))
print("Connected")

request = "GET /{} HTTP/1.1\r\n{}{}\r\n".format(path, host, connection)
s.send(request.encode())
print("Request is sent")

respond = func.getRespond(s, fileext)
data, size = func.removeHeader(respond, fileext)
func.saveFile(data, filename)

print(respond.decode().split("\r\n\r\n")[0])
print(size)

s.close()