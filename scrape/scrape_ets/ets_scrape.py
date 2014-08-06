import re
import urllib2

# f = open('ets_file.txt').read()
# pattern = r'<li><a href="(http://www.informatik.uni-trier.de/~ley/db/journals/ets/ets.*?.html)">(.*?)</a></li>'
# matches = re.findall(pattern, f)

# for link, name in matches:
# 	print "Requesting source from %s" %name
# 	try:
# 		source = urllib2.urlopen(link).read()

# 		pdf_pattern = r'<a href="(http://www.ifets.info/download_pdf.php?.*?);a_id=(.*?)">'
# 		pdf_matches = re.findall(pdf_pattern, source)

		# for link, name in pdf_matches:
		# 	print "Requesting file %s from %s" %(name, link)
		# 	html = urllib2.urlopen(link).read()
		# 	f = open('/Volumes/Backup Katie MacAir/Scrape/ETS/%s.pdf' %name, 'wb')
		# 	f.write(html)
		# 	f.close()

# go into each Volume, get source, search for XML links

f = open('ets_file.txt').read()
vol_pattern = r'<li><a href="(http://www.informatik.uni-trier.de/~ley/db/journals/ets/ets.*?.html)">(.*?)</a></li>'
vol_matches = re.findall(vol_pattern, f)

for link, name in vol_matches:
	print "Requesting source from %s" %name
	vol_source = urllib2.urlopen(link).read()
	xml_pattern = r'BibTeX</a></li><li><a href="(http://dblp.uni-trier.de/rec/bibtex/journals/ets/.*?.xml)">'
	xml_matches = re.findall(xml_pattern, vol_source)

	# go into each XML link, search for PDF link
	art_number= 0
	for xml_link in xml_matches:
		art_number +=1
		print "Requesting xml information from %s" %xml_link
		xml_source = urllib2.urlopen(xml_link).read()
		pub_pattern = r'<ee>(.*?)</ee>'
		pub_matches = re.findall(pub_pattern, xml_source)
		vol_pattern = r'<volume>(.*?)</volume>'
		vol_matches = re.findall(vol_pattern, xml_source)
		num_pattern = r'<number>(.*?)</number>'
		num_matches = re.findall(num_pattern, xml_source)

		for pub_link in pub_matches:
			if pub_link.split('.')[-1] == 'pdf':
				print "Requesting file, Volume %s Number %s Article %d from %s" %(vol_matches[0], num_matches[0], art_number, pub_link)
				html = urllib2.urlopen(link).read()
				f = open('/Volumes/Backup Katie MacAir/Scrape_ETS/Vol%s_Num%s_%d.pdf' %(vol_matches[0], num_matches[0], art_number), 'wb')
				f.write(html)
				f.close()


# http://www.ifets.info/journals/7_1/1.pdf
# http://www.ifets.info/journals/7_4/24.pdf

# http://www.ifets.info/journals/8_1/3.pdf
# http://www.ifets.info/journals/8_4/24.pdf
