import model

def add_journal():
    pass

def add_source(source_string):
    session = model.session

    new_source = model.Source()
    new_source.name = source_string

    session.add(new_source)
    session.commit()

def add_publication(pub_dict):
    session = model.session

    new_pub = model.Publication()
    new_pub.eric_id = pub_dict["eric_id"]
    new_pub.title = pub_dict["title"]
    # new_pub.source_id = int(pub_dict["source_id"])
    new_pub.short_desc = pub_dict["short_desc"]
    new_pub.url = pub_dict["url"]
    # new_pub.abstract = pub_dict["abstract"]
    # new_pub.month = int(pub_dict["month"])
    new_pub.year = int(pub_dict["year"])
    # new_pub.ISSN = pub_dict["ISSN"]
    # new_pub.journal_id = int(pub_dict["journal_id"])
    # new_pub.volume = int(pub_dict["volume"])
    # new_pub.issue = int(pub_dict["issue"])
    # new_pub.start_page = int(pub_dict["start_page"])
    # new_pub.end_page = int(pub_dict["end_page"])

    session.add(new_pub)
    session.commit()

def add_authors(author_list):
    session = model.session

    for author in author_list:
        author_split = author.split(',')

        new_author = model.Author()
        new_author.last_name = author_split[0]
        new_author.first_name = author_split[1]

        if len(author_split) > 2:
            new_author.middle_name = author_split[2:]

        session.add(new_author)
        session.commit()

def add_descriptors(descriptor_list):
    session = model.session

    for descriptor in descriptor_list:
        new_desc = model.Descriptor()
        new_desc.phrase = descriptor

        session.add(new_desc)
        session.commit()

def add_keyword():
    pass

def add_common_word():
    pass

def add_institution():
    pass

def add_department():
    pass

def main():
    pass

if __name__ == "__main__":
    main()