import sqlite3
from flask import Flask,render_template,request

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    if request.method=="GET":
        titles = [];
        titles = retTitles();
        return render_template("blog.html",titles = titles)
    else:
        button = request.form["submit"]
        title = request.form["title"]
        post = request.form["post"]
        if button=="Post!":
            f = open("posts.csv",'a')
            f.write(title+","+post+"\n")
            f.close()
            titles = retTitles();
            return render_template("blog.html", titles = titles)

@app.route("/<title>")
def title(title=None):
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    q = '''
    select post
    from posts where title == "'''
    #print title
    q+=title
    q+='"'
    print(q)
    post = c.execute(q)
    for r in post:
        print r
        return render_template("title.html",title=title,text = r[0])

def retTitles():
    conn = sqlite3.connect("test.db")
    
    c = conn.cursor()
    q = """
    select title
    from posts
    """
    #print(q)
    result = c.execute(q)
    ret = []
    for r in result:
        ret.append(r[0])
    return ret

        

if __name__=="__main__":
    app.debug=True
    app.run()
