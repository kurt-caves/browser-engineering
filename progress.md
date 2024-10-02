run http: python3 download.py https://browser.engineering/examples/example1-simple.html
run file: python3 download.py file:///path/goes/here
run file: python3 download.py file:////home/klyell/projects/browser-engineering/progress.md
run no arg: python3 download.py
run data: python3 download.py data:text/html,Hello world

# Links:
https://developer.mozilla.org/en-US/docs/Glossary/Request_header

# Headers:
GET /home.html HTTP/1.1
Host: developer.mozilla.org
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://developer.mozilla.org/testpage.html
Connection: keep-alive
Upgrade-Insecure-Requests: 1
If-Modified-Since: Mon, 18 Jul 2016 02:36:04 GMT
If-None-Match: "c561c68d0ba92bbeb8b0fff2a9199f722e3a621a"
Cache-Control: max-age=0


# 1-2 File Urls
### setup in main handling of no argument given
### setup file handling
- self.localFile handles schemes with file
- since I will be working on this on both my work pc and personal I need use only relative paths.

# 1-3 data
### data:
- going to "data:text/html,Hello world" outputs in HTML "Hello world"
- going to "data:text,Hello world!" outputs in text "Hello world!"
- need to wrap whatever is being put in for data in quotes, because of sys.argv[1]
- the output from data:text/html,"Hello world" should be
    - <html>
    -   <body> Hello world </body>
    - </html>

# 1-4 entities
&lt;div&gt;Hello&lt;/div&gt;
-> <div>Hello</div>


# 1-5 Keep Alive

