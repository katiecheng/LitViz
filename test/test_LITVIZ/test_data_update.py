import test_model

def add_publication(pub_dict):
    session = test_model.session

    new_pub = test_model.Publication()
    new_pub.title = pub_dict["title"]
    new_pub.year = int(pub_dict["year"])

    session.add(new_pub)
    session.commit()

def add_references(ref_tuple):
    session = test_model.session
    session.execute(test_model.references.insert().values(ref_tuple))
    session.commit()

pubs_list = [
    { "title":"pub1", "year":1980},
    { "title":"pub2", "year":1970},
    { "title":"pub3", "year":1975},
    { "title":"pub4", "year":1960},
    { "title":"pub5", "year":1940},
    { "title":"pub6", "year":1950},
    { "title":"pub7", "year":1990},
    { "title":"pub8", "year":1995},
    { "title":"pub9", "year":2000},
    { "title":"pub10", "year":2015},
    { "title":"pub11", "year":2009},
]

refs_list = [
    (1,7),
    (1,8),
    (7,9),
    (8,10),
    (8,11),
    (3,1),
    (2,1),
    (4,1),
    (5,2),
    (6,2),
]

def main():

    for pub in pubs_list:
        add_publication(pub)

    for ref in refs_list:
        add_references(ref)

if __name__ == "__main__":
    main()