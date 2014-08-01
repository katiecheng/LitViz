import simplejson as json
import test_query
import subprocess

def get_citation_count(title):

    try:
        num_citations = int(subprocess.check_output(["bash","citation.sh","%s" %title]))
    except ValueError:
        num_citations = 0
        print "Not listed in Google Scholar: %s" %title
    return num_citations

# def calculate_relatedness(pub_id):
#   """
#   for each publication
#   calculate how related it is to the target publication
#   based on shared keywords? references? referencers? authors? words in title? (though how to parse out the important words?)
#   based on # of citations (google scholar, scholar.py?)
#   return relatedness (to be added to the json dictionary of that pub)
#   """
#   pass

def get_viz_json(pub_id):

    # initialize a dictionary with the target publication's information
    pub_dict = test_query.get_pub(pub_id)
    pub_dict['google_citation_count'] = get_citation_count(pub_dict['title'])

    # create a second dictionary of information from all of the pub's references
    ref_dicts = test_query.get_pub_references(pub_id)

    # populate each of those reference dicts with their respective references
    for ref in ref_dicts:
        ref['google_citation_count'] = get_citation_count(ref['title'])
        ref['children'] = test_query.get_pub_references(ref["id"])

        for ref_child in ref['children']:
            ref_child['google_citation_count'] = get_citation_count(ref_child['title'])

    # create a third dictionary of information from all pubs that reference the target publication
    ref_by_dicts = test_query.get_pub_referenced_by(pub_id)

    # populate each of those referencing dicts with the pubs that reference them
    for ref_by in ref_by_dicts:
        ref_by['google_citation_count'] = get_citation_count(ref_by['title'])
        ref_by['children'] = test_query.get_pub_referenced_by(ref_by["id"])

        for ref_by_child in ref_by['children']:
            ref_by_child['google_citation_count'] = get_citation_count(ref_by_child['title'])

    # get the length of references vs. length of referencers
    num_refs = len(ref_dicts)
    num_ref_bys = len(ref_by_dicts)

    # interleave appending references & referencers to the target pub's children
    for i in range(min(num_refs, num_ref_bys)):
        if pub_dict.get('children'):
            pub_dict['children'].append(ref_dicts[i])
            pub_dict['children'].append(ref_by_dicts[i])
        else:
            pub_dict['children'] = []
            pub_dict['children'].append(ref_dicts[i])
            pub_dict['children'].append(ref_by_dicts[i])

    # once you've exhausted the ability to interleave, append the rest of the longer list
    diff = max(num_refs, num_ref_bys) - min(num_refs, num_ref_bys)

    for i in range(min(num_refs, num_ref_bys), max(num_refs, num_ref_bys)):
        if num_refs > num_ref_bys:
            pub_dict['children'].append(ref_dicts[i])
        else:
            pub_dict['children'].append(ref_by_dicts[i])

    # create a new json out of the pub_dict (which now has all of the info two 
    # layers up and down from the target pub)
    new_json = json.dumps([pub_dict], sort_keys=True)

    return (pub_dict, new_json)

def recursive_min(attr, mydict):
    if not mydict.get("children"):
        return mydict[attr]
    return min(mydict[attr], min([recursive_min(attr, child) for child in mydict["children"]]))

def recursive_max(attr, mydict):
    if not mydict.get("children"):
        return mydict[attr]
    return max(mydict[attr], max([recursive_max(attr, child) for child in mydict["children"]]))

def main(pub_id):

    # initialize pub_data dictionary
    pub_data = {}

    # populate pub_data dictionary to send back to app
    json_dict = get_viz_json(pub_id)
    pub_dict = json_dict[0]

    pub_data["json"] = json_dict[1]
    pub_data["year_min"] = recursive_min("year", pub_dict)
    pub_data["year_max"] = recursive_max("year", pub_dict)
    pub_data["citation_min"] = recursive_min("google_citation_count", pub_dict)
    pub_data["citation_max"] = recursive_max("google_citation_count", pub_dict)

    return pub_data

if __name__ == "__main__":
    main()