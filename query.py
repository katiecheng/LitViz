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

def get_pub_referenced_by():
	pass

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

