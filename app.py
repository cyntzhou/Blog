from flask import Flask,render_template,request

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    if request.method=="GET":
        return render_template("blog.html")
    else:
        button = request.form["submit"]
        title = request.form["title"]
        post = request.form["post"]
        if button=="Post!":
            f = open("posts.csv",'a')
            f.write(title+","+post+"\n")
            f.close()
            return render_template("blog.html")

@app.route("/<title>")
def title(title=None):
    return render_template("title.html",title=title)

if __name__=="__main__":
    app.debug=True
    app.run()
