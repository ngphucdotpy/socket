def extractInfo(URL:str):
	tmpURL = URL.split("://")
	tmppath = tmpURL[1].split("/")
	domain = tmppath[0]
	path = "/".join(tmppath[1:])
	if (path != ""):
		filename = domain + "_" + tmppath[-1]
	else:
		path = "index.html"
		filename = domain + "_index.html"
	fileext = filename.split(".")[-1]
	# fileext = tmppath[-1].split(".")[-1]
	return domain, path, filename, fileext

# print(extractInfo("http://www.bing.com/"))