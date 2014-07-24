import model

def add_journal():
    pass

def add_source(source_string):
    session = model.session

    exists = session.query(model.Source).filter_by(name=source_string).all()

    if exists:
        pass
    else:
        new_source = model.Source()
        new_source.name = source_string

        session.add(new_source)
        session.commit()

def add_publication(pub_dict):
    session = model.session

    exists = session.query(model.Publication).filter_by(eric_id=pub_dict["eric_id"]).all()

    if exists:
        pass
    else:
        # get source id of publication's source
        source = session.query(model.Source).filter_by(name=pub_dict["source"]).one()
        source_id = source.id

        new_pub = model.Publication()
        new_pub.eric_id = pub_dict["eric_id"]
        new_pub.title = pub_dict["title"]
        new_pub.source_id = int(source_id)
        new_pub.full_desc = pub_dict["full_desc"]
        new_pub.url = pub_dict["url"]
        # new_pub.abstract = pub_dict["abstract"]
        if pub_dict.get("month"):
            new_pub.month = int(pub_dict["month"])
        if pub_dict.get("year"):
            new_pub.year = int(pub_dict["year"])
        # new_pub.journal_id = int(pub_dict["journal_id"])
        if pub_dict.get("volume"):
            new_pub.volume = int(pub_dict["volume"])
        if pub_dict.get("issue"):
            new_pub.issue = int(pub_dict["issue"])
        if pub_dict.get("start_page"):
            new_pub.start_page = int(pub_dict["start_page"])
        if pub_dict.get("end_page"):
            new_pub.end_page = int(pub_dict["end_page"])

        session.add(new_pub)
        session.commit()

        new_pub = session.query(model.Publication).filter_by(eric_id=new_pub.eric_id).one()
        new_pub_id = new_pub.id

        add_authors(session, pub_dict["authors"], new_pub_id)
        add_descriptors(session, pub_dict["descriptors"], new_pub_id)

def add_authors(session, author_list, pub_id):

    for author in author_list:
        author_split = author.split(', ')

        if len(author_split) > 1:
            author_split_again = author_split[1].split(' ')

            last_name = author_split[0][:30]
            first_name = author_split_again[0]
            middle_name = ''

            if len(author_split_again) > 1:
                
                for part in author_split_again[1:]:
                    if part == '{" Ed."}':
                        pass
                    else:
                        middle_name += part + ' '
            middle_name = middle_name.strip()[:30]

            exists = session.query(model.Author).filter_by(first_name=first_name,
                                                            middle_name=middle_name,
                                                            last_name=last_name).all()

            if exists:
                pass
            else:
                new_author = model.Author()
                new_author.last_name = last_name
                new_author.first_name = first_name
                new_author.middle_name = middle_name

                session.add(new_author)
                session.commit()

            auth = session.query(model.Author).filter_by(first_name=first_name,
                                                            middle_name=middle_name,
                                                            last_name=last_name).one()
            auth_id = auth.id
            add_pubAuth(session, pub_id, auth_id)

def add_descriptors(session, descriptor_list, pub_id):
    session = model.session

    for descriptor in descriptor_list:

        exists = session.query(model.Descriptor).filter_by(phrase=descriptor).all()

        if exists:
            pass
        else:
            new_desc = model.Descriptor()
            new_desc.phrase = descriptor

            session.add(new_desc)
            session.commit()

        desc = session.query(model.Descriptor).filter_by(phrase=descriptor).one()
        desc_id = desc.id
        add_pubDesc(session, pub_id, desc_id)

def add_keyword():
    pass

def add_common_word():
    pass

def add_institution():
    pass

def add_department():
    pass

### Pivot Tables

def add_reference():
    exists = session.query(model.pubAuth).filter_by(pub_id=pub_id,
                                                    auth_id=auth_id).all()

    if exists:
        pass
    else:
        new_pubAuth = model.pubAuth()
        new_pubAuth.pub_id = pub_id
        new_pubAuth.auth_id = auth_id
        session.add(new_pubAuth)
        session.commit()

def add_pubAuth(session, pub_id, auth_id):

    exists = session.query(model.pubAuth).filter_by(pub_id=pub_id,
                                                    auth_id=auth_id).all()

    if exists:
        pass
    else:
        new_pubAuth = model.pubAuth()
        new_pubAuth.pub_id = pub_id
        new_pubAuth.auth_id = auth_id
        session.add(new_pubAuth)
        session.commit()

def add_pubDesc(session, pub_id, desc_id):
    
    exists = session.query(model.pubDesc).filter_by(pub_id=pub_id,
                                                    desc_id=desc_id).all()

    if exists:
        pass
    else:
        new_pubDesc = model.pubDesc()
        new_pubDesc.pub_id = pub_id
        new_pubDesc.desc_id = desc_id
        session.add(new_pubDesc)
        session.commit()

def add_pubKey():
    pass

def add_pubCommon():
    pass



def main():
    pass

if __name__ == "__main__":
    main()