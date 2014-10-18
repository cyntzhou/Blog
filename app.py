from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("blog.html")

@app.route("/<title>")
def title(title=None):
    return render_template("title.html",title=title)

if __name__=="__main__":
    app.debug=True
    app.run()
