from flask import Flask
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import session

# Create a Flask web app
app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'

# Render the home page
@app.route("/", methods=["GET", "POST"])
def show_front_page():
    if request.method == "GET":
        print 'showing front page'
        return render_template("index.html")
    elif request.method == "POST":
        if request.form.get("search_button"):
            session["search_text"] = request.form.get("search_text")
            session["search_type"] = request.form.get("search_type")
            return redirect ("/results")
        elif request.form.get("viz_button"):
            session["search_text"] = request.form.get("search_text")
            session["search_type"] = request.form.get("search_type")
            return redirect ("/viz")

@app.route("/results")
def results():
    print 'showing results page'
    search_text = session.get("search_text")
    search_type = session.get("search_type")
    return render_template("results.html",
                            search_text = search_text,
                            search_type = search_type)

@app.route("/viz")
def viz():
    print 'showing viz page'
    search_text = session.get("search_text")
    search_type = session.get("search_type")
    return render_template("viz.html",
                            search_text = search_text,
                            search_type = search_type)

if __name__ == '__main__':
    # Note that in production, you would want to disable debugging
    app.run(debug=True)