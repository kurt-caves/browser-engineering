import socket
import ssl
class URL:
    # __init__ is a class constructor
    # self is similar to this in Java
    def __init__(self, url):
        # self.scheme will have http, url will have what comes after
        # .split splits on one occurence of ://
        # https://browser.engineering/http.html
        # scheme will be https
        # url will be browser.engineering/http.html
        # we split on "one" (delimeter, 1) instance
        substring_link = "://"
        view_source_substring = "view-source"

        
        
        if substring_link in url:
            self.scheme, url = url.split("://", 1)
            # print("scheme: " + self.scheme)
        else:

            self.scheme, url = url.split(":", 1)
            
            # assert, if True the code runs else an Assertion error is raised
            assert self.scheme in ["http", "https", "file", "data", "view-source:https"]
        
       
        if self.scheme == "file":
            self.localFile = True
            self.data = False
            self.path = url
            self.host = None
            self.port = None
            self.viewsource = False
        elif self.scheme == "data":
            self.localFile = False
            self.data = True
            self.path = url
            self.host = None
            self.port = None
            self.viewsource = False
        elif self.scheme == "view-source:https":
            self.viewsource = True
            self.localFile = False
            self.data = False
            self.host, url = url.split("/", 1)
            self.path = "/" + url
            # print("self.host " , self.host)
            # print("self.path ", self.path)

        else:
            self.localFile = False
            self.data = False
            self.viewsource = False
            self.socket = None
            
            # seperate host from path
            # host comes before the first /
            # https://browser.engineering/http.html
            if "/" not in url:
                url = url + "/"
                # host will get browser.engineering
                # url will be http.html
            self.host, url = url.split("/", 1)
            self.path = "/" + url
            # print("self.host " , self.host)
            # print("self.path ", self.path)

            # if there is something like http://localhost:8000/
            # the port is 8000
            if ":" in self.host:
                
                self.host, port = self.host.split(":", 1)
                self.port = int(port)

    # connect to host
    # talk to another computer
    
    def request(self):
        # call the socket constructor the module we imported
        # address family - how to find the other computer
        # type - the type of conversation
        # protocol - how to establish a connection
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )

        if self.scheme == "http":
            self.port = 80
        elif self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)
            self.port = 443
        elif self.scheme == "view-source:https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)
            self.port = 443
        

        # connect to host through port
        if self.host or self.port:
            # print("here connect")
            # print("self.host: " + self.host)
            # print("self.port: " , self.port)
            s.connect((self.host, self.port))

            # modular request headers
            request_headers = {
                'get_request' : "GET {} HTTP/1.1\r\n".format(self.path),
                'host' : "Host: {}\r\n".format(self.host),
                'user-agent' : "User-Agent: Kurts Browser\r\n",
                'close-conn' : "Connection: close\r\n",
                'end-request' : "\r\n",
            }
            # we are doing the Method, Path and HTTP Version
            # request = "GET {} HTTP/1.1\r\n".format(self.path)
            request = request_headers["get_request"]
            request += request_headers["host"]
            request += request_headers["user-agent"]
            request += request_headers["close-conn"]
            request += request_headers["end-request"]
            # convert our string to bytes send the request
            s.send(request.encode("utf-8"))
            # treat socket like a file that contains bytes from the server
            response = s.makefile("r", encoding="utf8", newline="\r\n")
            print("response: " ,response)
            # return one line from the response
            # should 200 OK
            statusline = response.readline()
            print("status line: ", statusline)
            # split response
            version, status, explanation = statusline.split(" ", 2)

            # make a dicitionary of header value pairs, use lower case
            response_headers = {}
            while True:
                # read till "\r\n"
                line = response.readline()
                if line == "\r\n": break
                # header is before : value is after
                header, value = line.split(":", 1)
                # print("header: ", header)
                # print("value: ", value)
                # header becomes lowercase and white space is stripped
                response_headers[header.casefold()] = value.strip()
            print(response_headers)

            # prevent unusal headers?
            #chunked encoding
            assert "transfer-encoding" not in response_headers
            # no compression is used
            assert "content-encoding" not in response_headers

            # send data after headers
            # this is the actual body of the page
            content = response.read()
            s.close()
            # return the body
            return content
        
        if self.scheme == "file":
            try:
                file_path = self.path
                # print(file_path)
                # new_file_path = file_path.strip('/')
                # print(new_file_path)
                f = open(file_path, 'r')
                print(f.read())
                # f = open(file_path, 'r')
                # print(f.read())
            except Exception as e:
                print(f"Need the full relative path {e}")
        if self.scheme == "data":
            html_substring = "html"
            if html_substring in self.path:
                current_output = self.path.split(",", 1)
                makeHTML(current_output[1])
        

        
            

    # print the text not the tags
def show(body):
    in_tag = False
    entity = ""
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")
        # else:
        #     if c == "&":
        #             entity = "&"
        #     elif c == ";":
        #         entity = ""
        #     elif entity:
        #         entity += c
        #         if entity == "&lt":
        #             print("<", end="")
                    
        #         elif entity == "&gt":
        #             print(">", end="")
        #     else:
        #         print(c, end="")
            

        

def load(url):
    body = url.request()
    if url.localFile == False and url.data == False and url.viewsource == False: 
        show(body)
    if url.viewsource:
        print("here at show")
        viewSource(url)
def makeHTML(body):
    print("<html>")
    print("<body>" + body + "</body>")
    print("</html>")
def viewSource(url):
    body = url.request()
    for c in body:
        print(c, end="")
    

if __name__ == "__main__":
    # HTTP/1.1. Along with Host, send the Connection header in the request function with the value close
    import sys
    # the url is given from cli using sys
    # sys.argv[1] is an instance of URL
    # meaning it has access to all URL methods
    # so load(url) is an instance of URL which has access to
    # to the method request
    # we call load on it
    if len(sys.argv) > 1:
        load(URL(sys.argv[1]))  # Load the URL if provided
    else:
        error_path = ('error.html')
        f = open(error_path, 'r')
        print(f.read())
      