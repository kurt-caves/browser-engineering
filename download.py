import socket

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
        self.scheme, url = url.split("://", 1)
        # assert, if True the code runs else an Assertion error is raised
        assert self.scheme == "http"

        # seperate host from path
        # host comes before the first /
        # https://browser.engineering/http.html
        if "/" not in url:
            url = url + "/"
            # host will get browser.engineering
            # url will be http.html
            self.host, url = url.split("/", 1)
            self.path = "/" + url

    # connect to host
    # talk to another computer
    # address family - how to find the other computer
    # type - the type of conversation
    # protocol - how to establish a connection
    def request(self):
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )

        # connect to host through port
        s.connect((self.host, 80))
