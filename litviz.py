from flask import Flask
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import session
import model

# Create a Flask web app
app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'

# Render the home page
@app.route("/", methods=["GET", "POST"])
def index():
    session["search_text"]=''
    return render_template("index.html")

@app.route("/results", methods=["GET", "POST"])
def results():
    if session.get("search_text"):
        search_text = session.get("search_text")
    else:
        session["search_text"] = request.form.get("search_text")
        search_text = session.get("search_text")
    return render_template("results.html", 
                            search_text = search_text)

@app.route("/viz", methods=["GET","POST"])
def viz():
    search_text = session.get("search_text")
    return render_template("viz.html", 
                            search_text = search_text)

@app.route("/submit", methods=["POST"])
def submit():
    search_text = request.form.get("search_text")
    session["search_text"] = search_text
    if session["search_text"]:
        if request.form['btn'] == "Search":
            return redirect("/results")
        elif request.form['btn'] == "Visualize Data!":
            return redirect("/viz")
    else:
        return render_template("results.html", 
                                search_text = search_text)

if __name__ == '__main__':
    # Note that in production, you would want to disable debugging
    app.run(debug=True)