import sqlite3
import time
from flask import Flask,render_template,request

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    if request.method=="POST":
        button = request.form["submit"]
        title = request.form["title"]
        post = request.form["post"]
        if button=="Post!":
            try:
                conn = sqlite3.connect('test.db')
                c = conn.cursor()
                localtime = time.asctime( time.localtime(time.time()) )
                q = "insert into posts values('" + title + "', '" + post + "', '"+localtime+"');"
                print q
                #f = open("posts.csv",'a')
                #f.write(title+","+post+"\n")
                #f.close()
                c.execute(q)
                conn.commit()
            except sqlite3.Error, e:
                print "Error %s:" %e.args[0]
    titles = retPost();
    return render_template("blog.html", titles = titles,)

@app.route("/<title>", methods=["GET","POST"])
def title(title=None):
    if request.method=="POST":
        button = request.form["submit"]
        name = request.form["name"]
        comment = request.form["comment"]
        conn = sqlite3.connect("test.db")
        c = conn.cursor()
        localtime = time.asctime( time.localtime(time.time()) )
        q = "insert into comments values('"+title+"','"+comment+"','"+name+"', '"+localtime+"');"
        print q
        c.execute(q)
        conn.commit()
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    q = '''
    select post,time
    from posts where title == "'''
    q+=title
    q+='"'
    post = c.execute(q)
    comments = retComments(title)
    for r in post:
        #print r
        return render_template("title.html",title=title, post=r[0], time = r[1], comments = comments)
        
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
