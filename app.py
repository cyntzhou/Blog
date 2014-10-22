import sqlite3
import time
from flask import Flask,render_template,request

app = Flask(__name__)

def urls():
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    q = "SELECT title, time FROM posts"
    results = c.execute(q)
    urls = [(str("%20".join(t[0].split(' '))), t[1]) for t in results]
    return urls

@app.route("/", methods=["GET","POST"])
def home():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    if request.method=="POST":
        button = request.form["submit"]
        title = request.form["title"]
        post = request.form["post"]
        if button=="Post!":
            try:
                localtime = time.strftime("%d/%m/%Y")
                q = "insert into posts values('" + title + "', '" + post + "', '"+localtime+"');"
                c.execute(q)
                conn.commit()
            except sqlite3.Error, e:
                print "Error %s:" %e.args[0]
    q2 = "SELECT * FROM posts ORDER BY title DESC LIMIT 1;"
    newest = [elem for elem in c.execute(q2)]
    urltuples = urls();
    return render_template("blog.html", urls = urltuples, new = newest)

@app.route("/<title>", methods=["GET","POST"])
def title(title=None):
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    if request.method=="POST":
        button = request.form["submit"]
        name = request.form["name"]
        comment = request.form["comment"]
        localtime = time.strftime("%d/%m/%Y")
        q = "insert into comments values('"+title+"','"+comment+"','"+name+"', '"+localtime+"');"
        c.execute(q)
        conn.commit()
    q = '''
    select post,time
    from posts where title == "'''
    q+=title
    q+='"'
    post = c.execute(q)
    comments = retComments(title)
    q2 = 'SELECT title, post, time FROM posts WHERE title =="' + title + '"'
    display = [elem for elem in c.execute(q2)]
    urltuples = urls();
    comments = retComments(title)
    return render_template("blog.html", urls = urltuples, new = display, comments = comments)
        
def retPost():
    conn = sqlite3.connect("test.db")    
    c = conn.cursor()
    q = """
    select title,time
    from posts
    """
    #print(q)
    result = c.execute(q)
    ret = []
    for r in result:
        #print r
        ret.append(r)
    return ret

def retComments(title):
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    q = '''
    select comment,name,time
    from comments where title == "'''
    q+=title
    q+='"'
    comments = c.execute(q)
    return comments

if __name__=="__main__":
    app.debug=True
    app.run()
