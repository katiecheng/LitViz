import model

### CONVERT ROWS TO DICTIONARIES
def row2dict(row):
    d = {}
    for column in row.__table__.columns:

        # when possible, convert unicode string to ascii
        if isinstance(getattr(row, column.name), unicode):
            d[column.name] = getattr(row, column.name).encode('utf-8')
        else:
            d[column.name] = getattr(row, column.name)
    return d

### GET PUBLICATION INFO
def get_pub_source(pub_id):
    session = model.session

    pub = session.query(model.Publication).get(pub_id)
    source_id = pub.source_id
    source = session.query(model.Source).get(source_id)
    return row2dict(source)

def get_pub_journal():
    pass

def get_pub_references(pub_id):
    session = model.session

    pub = session.query(model.Publication).get(pub_id)
    refs = pub.references
    ref_dicts = []
    for ref in refs:
        ref_dicts.append(row2dict(ref))
    return ref_dicts

def get_pub_referenced_by(pub_id):
    session = model.session

    ref_by = session.query(model.references).filter_by(child_pub_id=pub_id)
    ref_by_ids = [ref.parent_pub_id for ref in ref_by]

    ref_by_dicts = []
    for ref_by_id in ref_by_ids:
        ref_by = session.query(model.Publication).get(ref_by_id)
        ref_by_dicts.append(row2dict(ref_by))
    return ref_by_dicts

def get_pub(pub_id):
    session = model.session

    pub = session.query(model.Publication).get(pub_id)
    return row2dict(pub)

def get_pubs_count(search_text, column):
    session = model.session 
    if column == "title":
        pubs = (session.query(model.Publication)
                .filter(model.Publication
                .title.ilike("%" + search_text + "%")))
        count = pubs.count()
    elif column == "full_desc":
        pubs = (session.query(model.Publication)
                .filter(model.Publication
                .full_desc.ilike("% " + search_text + " %")))
        count = pubs.count()
    return count

def get_pubs(search_text, column, index):
    session = model.session 
    if column == "title":
        pubs = (session.query(model.Publication)
                .filter(model.Publication.title.ilike("%" + search_text + "%"))
                .order_by(model.Publication.citation_count.desc())
                .slice(index*10, index*10+10))
    elif column == "full_desc":
        pubs = (session.query(model.Publication)
                .filter(model.Publication.full_desc.ilike("% " + search_text + " %"))
                .order_by(model.Publication.citation_count.desc())
                .slice(index*10, index*10+10))
    pub_dicts = []
    for pub in pubs:
        pub_dict = PubResultsInfo(pub.id, pub.title, pub.url, pub.full_desc, pub.citation_count).__dict__
        pub_dicts.append(pub_dict)
    return pub_dicts

class PubResultsInfo(object):
    pub_id = 0
    title = ""
    url = ""
    authors = [""]
    full_desc = ""
    descriptors = [""]
    citation_count = 0

    def __init__(self, pub_id, title, url, full_desc, citation_count):
        self.pub_id = pub_id
        self.title = title
        self.url = url
        self.full_desc = full_desc
        if citation_count:
            self.citation_count = citation_count
        self.authors = get_pub_authors(pub_id)
        self.descriptors = get_pub_descriptors(pub_id)


def get_pub_authors(pub_id):
    session = model.session

    pub = session.query(model.Publication).get(pub_id)
    pub_auth_list = pub.pub_auth
    pub_auth_id_list = [pub_auth.auth_id for pub_auth in pub_auth_list]
    auths = [session.query(model.Author).get(auth_id) for auth_id in pub_auth_id_list]

    auth_dicts = []
    for auth in auths:
        auth_dicts.append(row2dict(auth))

    string_auths = ""
    for auth_dict in auth_dicts:
        author_string = ''
        author_string += (auth_dict['last_name'] + ', ' + 
                          auth_dict['first_name'] + ' ' + 
                          auth_dict['middle_name'])

        if auth_dict == auth_dicts[0]:
            string_auths += author_string
        else:
            string_auths += "; %s" %author_string

    return string_auths

def get_pub_descriptors(pub_id):
    session = model.session

    pub = session.query(model.Publication).get(pub_id)
    pub_desc_list = pub.pub_desc
    pub_desc_id_list = [pub_desc.desc_id for pub_desc in pub_desc_list]
    descs = [session.query(model.Descriptor).get(desc_id) for desc_id in pub_desc_id_list]
    desc_dicts = []
    for desc in descs:
        desc_dicts.append(row2dict(desc))

    string_descs = ""
    for desc_dict in desc_dicts:
        desc_string = ''
        desc_string += (desc_dict['phrase'])
        
        if desc_dict == desc_dicts[0]:
            string_descs += desc_string
        else:
            string_descs += ", %s" %desc_string

    return string_descs

def get_pub_desc_ids(pub_id):
    session = model.session

    pub = session.query(model.Publication).get(pub_id)
    pub_desc_list = pub.pub_desc
    pub_desc_id_list = [pub_desc.desc_id for pub_desc in pub_desc_list]
    return pub_desc_id_list

def get_pub_keywords():
    pass

def get_pub_commonwords():
    pass

### GET AUTHOR INFO
def get_auth_publications(auth_id):
    session = model.session

    auth = session.query(model.Author).get(auth_id)
    pub_auth_list = auth.pub_auth
    pub_auth_id_list = [pub_auth.pub_id for pub_auth in pub_auth_list]
    pubs = [session.query(model.Publication).get(pub_id) for pub_id in pub_auth_id_list]
    pub_dicts = []
    for pub in pubs:
        pub_dict = PubResultsInfo(pub.id, pub.title, pub.url, pub.full_desc, pub.citation_count).__dict__
        pub_dicts.append(pub_dict)
    return pub_dicts

### GET DESCRIPTOR INFO
def get_desc_publications(desc_id):
    session = model.session

    desc = session.query(model.Descriptor).get(desc_id)
    pub_desc_list = desc.pub_desc
    pub_desc_id_list = [pub_desc.pub_id for pub_desc in pub_desc_list]
    pubs = [session.query(model.Publication).get(pub_id) for pub_id in pub_desc_id_list]
    pub_dicts = []
    for pub in pubs:
        pub_dicts.append(row2dict(pub))
    return pub_dicts

### GET KEYWORD INFO
def get_key_publications():
    pass

### GET COMMON WORD INFO
def get_comm_publications():
    pass

### GET INSTITUTION INFO
def get_inst_authors():
    pass

### GET DEPARTMENT INFO
def get_dept_authors():
    pass


### GET RELATED PUBLICATIONS


def get_related_pubs(pub_id):
    related_pubs = {}

    # add number of shared descriptors
    descriptor_ids = get_pub_desc_ids(pub_id)
    for desc_id in descriptor_ids:
        for pub in get_desc_publications(desc_id):
            if pub.id != pub_id:
                if related_pubs.get(pub.id):
                    related_pubs[pub.id]["relatedness"] += 1
                else:
                    related_pubs[pub.id] = {"year":pub.year, "title":pub.title, "relatedness":1}
    related_pub_dicts = []
    for pub in related_pubs:
        related_pub_dicts.append(row2dict(pub))
    return related_pub_dicts

def get_shared_child_pub(pub_id_1, pub_id_2):

    pub1_references = get_pub_references(pub_id_1)
    pub2_references = get_pub_references(pub_id_2)

    in_both = []

    for ref in pub1_references:
        if ref in pub2_references:
            in_both.append(ref)
    in_both_dicts = []
    for pub in in_both:
        in_both_dicts.append(row2dict(pub))
    return in_both_dicts