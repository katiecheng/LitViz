import model

### GET PUBLICATION INFO
def get_pub_source(pub_id):
	session = model.session

	pub = session.query(model.Publication).get(pub_id)
	source_id = pub.source_id
	source = session.query(model.Source).get(source_id)
	return source

def get_pub_journal():
	pass

def get_pub_references(pub_id):
	session = model.session

	pub = session.query(model.Publication).get(pub_id)
	refs = pub.references
	return refs

def get_pub_referenced_by(pub_id):
	session = model.session

	ref_by = session.query(model.references).filter_by(child_pub_id=pub_id)
	ref_by_ids = [ref.parent_pub_id for ref in ref_by]
	return ref_by_ids


def get_pub_authors(pub_id):
	session = model.session

	pub = session.query(model.Publication).get(pub_id)
	pub_auth_list = pub.pub_auth
	pub_auth_id_list = [pub_auth.auth_id for pub_auth in pub_auth_list]
	auths = [session.query(model.Author).get(auth_id) for auth_id in pub_auth_id_list]
	return auths

def get_pub_descriptors(pub_id):
	session = model.session

	pub = session.query(model.Publication).get(pub_id)
	pub_desc_list = pub.pub_desc
	pub_desc_id_list = [pub_desc.desc_id for pub_desc in pub_desc_list]
	descs = [session.query(model.Descriptor).get(desc_id) for desc_id in pub_desc_id_list]
	return descs

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
	return pubs

### GET DESCRIPTOR INFO
def get_desc_publications(desc_id):
	session = model.session

	desc = session.query(model.Descriptor).get(desc_id)
	pub_desc_list = desc.pub_desc
	pub_desc_id_list = [pub_desc.pub_id for pub_desc in pub_desc_list]
	pubs = [session.query(model.Publication).get(pub_id) for pub_id in pub_desc_id_list]
	return pubs

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
	

	return related_pubs

def get_shared_child_pub(pub_id_1, pub_id_2):

	pub1_references = get_pub_references(pub_id_1)
	pub2_references = get_pub_references(pub_id_2)

	in_both = []

	for ref in pub1_references:
		if ref in pub2_references:
			in_both.append(ref)

	return in_both