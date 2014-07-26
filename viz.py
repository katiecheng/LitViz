import simplejson as json
import test_query

def get_viz_json(pub_id):

	pub_dict = test_query.get_pub(pub_id)

	ref_dicts = test_query.get_pub_references(pub_id)

	for ref in ref_dicts:
		ref['children'] = test_query.get_pub_references(ref["id"])

	ref_by_dicts = test_query.get_pub_referenced_by(pub_id)

	for ref_by in ref_by_dicts:
		ref_by['children'] = test_query.get_pub_referenced_by(ref_by["id"])

	num_refs = len(ref_dicts)
	num_ref_bys = len(ref_by_dicts)

	
	for i in range(min(num_refs, num_ref_bys)):
		if pub_dict.get('children'):
			pub_dict['children'].append(ref_dicts[i])
			pub_dict['children'].append(ref_by_dicts[i])
		else:
			pub_dict['children'] = []
			pub_dict['children'].append(ref_dicts[i])
			pub_dict['children'].append(ref_by_dicts[i])

	diff = max(num_refs, num_ref_bys) - min(num_refs, num_ref_bys)

	for i in range(min(num_refs, num_ref_bys), max(num_refs, num_ref_bys)):
		if num_refs > num_ref_bys:
			pub_dict['children'].append(ref_dicts[i])
		else:
			pub_dict['children'].append(ref_by_dicts[i])
	# for ref, ref_by in ref_dicts, ref_by_dicts:
	# 	if pub_dict.get('children'):
	# 		pub_dict['children'].append(ref)
	# 		pub_dict['children'].append(ref_by)
	# 		print 'okay'
	# 	else:
	# 		pub_dict['children'] = []
	# 		pub_dict['children'].append(ref)
	# 		pub_dict['children'].append(ref_by)
	# 		print 'yes'

	# pub_dict['children'] = ref_dicts + ref_by_dicts

	new_json = json.dumps([pub_dict], sort_keys=True, indent=4*' ')

	f = open("test.json", "w")
	f.write(new_json)

def main():
	pass

if __name__ == "__main__":
	main()