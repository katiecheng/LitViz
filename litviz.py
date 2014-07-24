from flask import Flask
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import session
import model
import query

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
        query_list = model.session.query(model.Publication
            ).filter(model.Publication.title.ilike("%" + search_text + "%")
            ).all()

        source_list = [query.get_pub_source(pub.id) for pub in query_list]
        auth_list = [query.get_pub_authors(pub.id) for pub in query_list]
        desc_list = [query.get_pub_descriptors(pub.id) for pub in query_list]
        ref_list = [query.get_pub_references(pub.id) for pub in query_list]

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

        source_list = [query.get_pub_source(pub.id) for pub in query_list]
        auth_list = [query.get_pub_authors(pub.id) for pub in query_list]
        desc_list = [query.get_pub_descriptors(pub.id) for pub in query_list]
        ref_list = [query.get_pub_references(pub.id) for pub in query_list]

    elif search_type == "Keyword":
        query_list = model.session.query(model.Publication
            ).filter(model.Publication.full_desc.ilike("%" + search_text + "%")
            ).all()

        source_list = [query.get_pub_source(pub.id) for pub in query_list]
        auth_list = [query.get_pub_authors(pub.id) for pub in query_list]
        desc_list = [query.get_pub_descriptors(pub.id) for pub in query_list]
        ref_list = [query.get_pub_references(pub.id) for pub in query_list]

    else:
        query_list = ['uhg']
        source_list = ['boo']
        desc_list = ['no']
        ref_list = ['stop']
        auth_list = ['get out']
    # [(auth.first_name, auth.middle_name, auth.last_name) for auth in auth_list]
    # desc_phrase = [desc.phrase for desc in desc_list]
    # ref_titles = [ref.title for ref in ref_list]

    return render_template("results.html", 
                            search_text = search_text,
                            search_type = search_type,
                            length = len(query_list),
                            results = query_list,
                            sources = source_list,
                            authors = auth_list,
                            descriptors = desc_list,
                            references = ref_list)

@app.route("/viz", methods=["GET","POST"])
def viz():
    search_text = session.get("search_text")
    search_type = session.get("search_type")
    return render_template("viz.html", 
                            search_text = search_text,
                            search_type = search_type)

@app.route("/submit", methods=["POST"])
def submit():
    if request.form.get("search_button"):
        session["search_text"] = request.form.get("search_text")
        session["search_type"] = request.form.get("search_type")
        return redirect ("/results")
    elif request.form.get("viz_button"):
        session["search_text"] = request.form.get("search_text")
        session["search_type"] = request.form.get("search_type")
        return redirect ("/viz")

if __name__ == '__main__':
    # Note that in production, you would want to disable debugging
    app.run(debug=True)