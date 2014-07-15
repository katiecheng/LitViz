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
    if session.get("search_text") and session.get("search_type"):
        search_text = session.get("search_text")
        search_type = session.get("search_type")

    else:
        session["search_text"] = request.form.get("search_text")
        session["search_type"] = request.form.get("search_type")
        search_text = session.get("search_text")
        search_type = session.get("search_type")

    if search_type == "Title":
        query_list = model.session.query(model.Publication
            ).filter(model.Publication.title.ilike("%" + search_text + "%")
            ).all()
    elif search_type == "Author":
        query_list = model.session.query(model.Author
            ).filter(model.Author.last_name.ilike("%" + search_text + "%")
            ).all()
    elif search_type == "Keyword":
        query_list = model.session.query(model.Publication
            ).filter(model.Publication.full_desc.ilike("%" + search_text + "%")
            ).all()
    else:
            query_list = ['this sucks 1']
    
    return render_template("results.html", 
                            search_text = search_text,
                            search_type = search_type,
                            results = query_list)

@app.route("/viz", methods=["GET","POST"])
def viz():
    search_text = session.get("search_text")
    search_type = session.get("search_type")
    return render_template("viz.html", 
                            search_text = search_text,
                            search_type = search_type)

@app.route("/submit", methods=["POST"])
def submit():
    search_text = request.form.get("search_text")
    search_type = request.form.get("search_type")
    session["search_text"] = search_text
    session["search_type"] = search_type

    if request.form['btn'] == "Search":
        return redirect("/results")
    elif request.form['btn'] == "Visualize Data!":
        return redirect("/viz")

if __name__ == '__main__':
    # Note that in production, you would want to disable debugging
    app.run(debug=True)