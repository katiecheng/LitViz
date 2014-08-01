mylist = [{'year': 1920,
  'children': [{'year': 1930}, 
			   {'year': 1940,
				'children': [{'year': 1950}] }]}]

def recursive_min(attr, mydict):
	if "children" not in mydict:
		return mydict[attr]
	return min(mydict[attr], min([recursive_min(attr, child) for child in mydict["children"]]))

mydict = mylist[0]
print recursive_min("year", mydict)