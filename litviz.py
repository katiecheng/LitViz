from flask import Flask
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import session
import model
import query
import viz as viz_mod
import simplejson as json

# Create a Flask web app
app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'

# @app.route("/")
# def d3_page():
#     return render_template("d3.html")


# Render the home page
@app.route("/", methods=["GET", "POST"])
def show_front_page():
    if request.method == "GET":
        return render_template("index.html")

@app.route("/results", methods=["GET", "POST"])
def results():
    search_text = session.get("search_text")
    search_type = session.get("search_type")

    if search_type == "Title":
        index = 0
        query_list = query.get_pubs(search_text, "title", index)

        pub_list = [pub["id"] for pub in query_list]
        source_list = [query.get_pub_source(pub["id"]) for pub in query_list]
        auth_list = [query.get_pub_authors(pub["id"]) for pub in query_list]
        desc_list = [query.get_pub_descriptors(pub["id"]) for pub in query_list]
        ref_list = [query.get_pub_references(pub["id"]) for pub in query_list]

    elif search_type == "Author":
        auth_list = model.session.query(model.Author
            ).filter(model.Author.last_name.ilike("%" + search_text + "%")
            ).all()

        auth_id_list = [auth.id for auth in auth_list]
        auth_pubs_list = [query.get_auth_publications(auth_id) for auth_id in auth_id_list]
        query_list = []
        for auth_pubs in auth_pubs_list:
            for auth_pub in auth_pubs:
                query_list.append(auth_pub)

        pub_list = [pub["id"] for pub in query_list]
        source_list = [query.get_pub_source(pub["id"]) for pub in query_list]
        auth_list = [query.get_pub_authors(pub["id"]) for pub in query_list]
        desc_list = [query.get_pub_descriptors(pub["id"]) for pub in query_list]
        ref_list = [query.get_pub_references(pub["id"]) for pub in query_list]

    elif search_type == "Keyword":
        index = 0
        query_list = query.get_pubs(search_text, "full_desc", index)

        pub_list = [pub["id"] for pub in query_list]
        source_list = [query.get_pub_source(pub["id"]) for pub in query_list]
        auth_list = [query.get_pub_authors(pub["id"]) for pub in query_list]
        desc_list = [query.get_pub_descriptors(pub["id"]) for pub in query_list]
        ref_list = [query.get_pub_references(pub["id"]) for pub in query_list]

    else:
        query_list = ['-']
        pub_list = [0]
        source_list = ['-']
        desc_list = ['-']
        ref_list = ['-']
        auth_list = ['-']

    return render_template("results.html", 
                            search_text = search_text,
                            search_type = search_type,
                            length = len(query_list),
                            results = query_list,
                            publist = pub_list,
                            sources = source_list,
                            authors = auth_list,
                            descriptors = desc_list,
                            references = ref_list)

@app.route("/viz", methods=["GET","POST"])
def viz():
    search_text = session.get("search_text")
    search_type = session.get("search_type")
    pub_id = session.get("pub_id")
    pub_data = json.dumps(viz_mod.main(pub_id))
    return render_template("viz.html", 
                            search_text = search_text,
                            search_type = search_type,
                            data = pub_data)

@app.route("/lazyload")
def lazyload():
    pass

@app.route("/update")
def update():
    pub_id = int(request.args.get("pub_id").encode("utf-8"))
    pub_data = json.dumps(viz_mod.main(pub_id))
    return pub_data

@app.route("/submit", methods=["POST"])
def submit():
    if request.form.get("search_button"):
        session["search_text"] = request.form.get("search_text")
        session["search_type"] = request.form.get("search_type")
        return redirect ("/results")
    elif request.form.get("viz_button"):
        session["search_text"] = request.form.get("search_text")
        session["search_type"] = request.form.get("search_type")
        session["pub_id"] = request.form.get("hidden_id")
        return redirect ("/viz")

if __name__ == '__main__':
    # Note that in production, you would want to disable debugging
    app.run(debug=True)