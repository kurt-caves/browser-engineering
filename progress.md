run http: python3 download.py https://browser.engineering/examples/example1-simple.html
run file: python3 download.py file:///path/goes/here
run file: python3 download.py file:////home/klyell/projects/browser-engineering/progress.md
run no arg: python3 download.py
run data: python3 download.py data:text/html,Hello world

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


- recommended code:

def show(body):
    in_tag = False
    entity = ""  # Variable to collect entity characters
    for c in body:
        if c == "<":
            in_tag = True
            print("<", end="")
        elif c == ">":
            in_tag = False
            print(">", end="")
        elif in_tag:
            print(c, end="")
        else:
            if c == "&":  # Start of an entity
                entity = "&"
            elif c == ";":  # End of an entity
                entity += ";"
                # Handle the recognized entity
                if entity == "&lt;":
                    print("<", end="")
                elif entity == "&gt;":
                    print(">", end="")
                else:
                    print(entity, end="")  # Print unrecognized entities as is
                entity = ""  # Reset entity
            elif entity:  # If we are collecting an entity
                entity += c
            else:
                print(c, end="")

