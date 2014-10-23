import sqlite3
import time
from flask import Flask,render_template,request, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    q2 = "SELECT * FROM posts ORDER BY title DESC LIMIT 1;"
    newest = [elem for elem in c.execute(q2)][0]
    urltuples = urls();
    if request.method=="POST":
        button = request.form["submit"]
        localtime = time.strftime("%m/%d/%Y")
        if button == "Comment!":
            name = request.form["name"]
            comment = request.form["comment"]
            c.execute("insert into comments values(?, ?, ?,?)", (str(newest[0]), comment, name,localtime))
            #c.execute(q)
            conn.commit()
        if button == "Post!":
            title = request.form["title"]
            post = request.form["post"]
            #q = "insert into posts values('" + title + "', '" + post + "', '"+localtime+"');"
            c.execute("insert into posts values(?,?,?)",(title,post,localtime))
            conn.commit()
            return redirect("/"+title)
    comments = retComments(str(newest[0]))
    return render_template("blog.html", urls = urltuples, new = newest, comments=comments)

@app.route("/<title>", methods=["GET","POST"])
def title(title=None):
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    if request.method=="POST":
        button = request.form["submit"]
        localtime = time.strftime("%m/%d/%Y")
        if button == "Comment!":
            name = request.form["name"]
            comment = request.form["comment"]
            c.execute("insert into comments values(?, ?, ?,?)", (title, comment, name,localtime))
            conn.commit()
        if button == "Post!":
            title = request.form["title"]
            post = request.form["post"]
            #q = "insert into posts values('" + title + "', '" + post + "', '"+localtime+"');"
            c.execute("insert into posts values(?,?,?)",(title,post,localtime))
            conn.commit()
            return redirect("/"+title)
    comments = retComments(title)
    q = 'SELECT title, post, time FROM posts WHERE title =="' + title + '"'
    display = [elem for elem in c.execute(q)][0]
    urltuples = urls();
    comments = retComments(title)
    return render_template("blog.html", urls = urltuples, new = display, comments = comments)
       
def urls():
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    q = "SELECT title, time FROM posts"
    results = c.execute(q)
    urls = [(str("%20".join(t[0].split(' '))), t[1]) for t in results]
    return urls
 
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
