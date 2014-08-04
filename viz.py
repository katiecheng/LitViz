import query
import subprocess

# def get_citation_count(title):
#     try:
#         num_citations = int(subprocess.check_output(["bash","citation.sh","%s" %title]))
#     except ValueError:
#         num_citations = 0
#         print "Not listed in Google Scholar: %s" %title
#     return num_citations

def get_viz_data(pub_id):

    # initialize dict with the target pub's info
    pub_dict = query.get_pub(pub_id)

    # create 2nd dict of info from all of the pub's refs
    ref_dicts = query.get_pub_references(pub_id)

    # populate each reference dict with their respective refs
    for ref in ref_dicts:
        ref['children'] = query.get_pub_references(ref["id"])

    # create 3rd dict of info from all pubs that reference the target pub
    ref_by_dicts = query.get_pub_referenced_by(pub_id)

    # populate each referencing dict with the pubs that reference them
    for ref_by in ref_by_dicts:
        ref_by['children'] = query.get_pub_referenced_by(ref_by["id"])

    # get the length of refs vs. length of referencers
    num_refs = len(ref_dicts)
    num_ref_bys = len(ref_by_dicts)

    # interleave appending refs & referencers to the target pub's children
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
        elif num_refs < num_ref_bys:
            pub_dict['children'].append(ref_by_dicts[i])

    # pub_dict now has all of the info two layers up and down from the target pub
    return pub_dict

def recursive_min(attr, mydict):
    if not mydict.get("children"):
        return mydict[attr]
    return min(mydict[attr], min([recursive_min(attr, child) for child in mydict["children"]]))

def recursive_max(attr, mydict):
    if not mydict.get("children"):
        return mydict[attr]
    return max(mydict[attr], max([recursive_max(attr, child) for child in mydict["children"]]))

def main(pub_id):

    # initialize pub_data dict
    pub_data = {}

    # populate pub_data dict to send back to app
    pub_dict = get_viz_data(pub_id)
    pub_data["data"] = [pub_dict]
    pub_data["year_min"] = recursive_min("year", pub_dict)
    pub_data["year_max"] = recursive_max("year", pub_dict)
    pub_data["citation_min"] = recursive_min("citation_count", pub_dict)
    pub_data["citation_max"] = recursive_max("citation_count", pub_dict)

    return pub_data

if __name__ == "__main__":
    main()