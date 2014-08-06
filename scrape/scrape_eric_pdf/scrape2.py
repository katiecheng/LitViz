import re
import urllib2

pattern = r'<a href="(http://files.eric.ed.gov/fulltext/(.+?).pdf)" target="_blank">'

for page in range(10657,16526):
	
	print "Requesting source from page %d" %page
	url = 'http://eric.ed.gov/?q=education&ft=on&pg=%d' %page
	source = urllib2.urlopen(url).read()

	matches = re.findall(pattern, source)

	for link, name in matches:
		print "Requesting file %s from %s" %(name, link)
		html = urllib2.urlopen(link).read()
		f = open('/Volumes/Backup Katie MacAir/Scrape/%s.pdf' %name, 'wb')
		f.write(html)
		f.close()