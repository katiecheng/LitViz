from pyquery import PyQuery as pq
import re

def cycle():
    # for group in range(1,16526, 5):
    for group in range(1,5,5):

        with open("json_files/pages_%d_%d.json"%(group, group+4), 'w') as f:
        
            f.write(""" "publications":[""")
            
        with open("json_files/pages_%d_%d.json"%(group, group+4), 'a') as f:
            for page in range(group, group+5):
                url = "http://eric.ed.gov/?q=education&ft=on&pg=%d" %page
                print url


                html = pq(url=url)
                publications = html(".r_i")

                for i in range(0,15):
                    current_pub = publications.eq(i)
                    pub_id = current_pub.attr("id")[2:].encode('ascii', 'replace')
                    title = current_pub.find('.r_t').text().encode('ascii', 'replace')
                    link = current_pub.find('.r_f').find('a').attr("href").encode('ascii', 'replace')

                    auth_src_yr = current_pub.find('.r_a').text()
                    auth_src_yr_split = auth_src_yr.split(u'\u2013 ')

                    if len(auth_src_yr_split) > 1:
                        authors = auth_src_yr_split[0].split('; ')

                        for auth in authors:
                            auth = auth.encode('ascii', 'replace')

                        source = auth_src_yr_split[1][:-7].encode('ascii', 'replace')
                        year = auth_src_yr_split[1][-4:].encode('ascii', 'replace')
                    else:
                        authors = 'NONE'
                        source = auth_src_yr_split[0][:-6].encode('ascii', 'replace')
                        year = auth_src_yr_split[0][-4:].encode('ascii', 'replace')

                    short_desc = current_pub.find('.r_d').text().encode('ascii', 'replace')
                    descriptors = current_pub.find('.keywords').text()[13:].encode('ascii', 'replace').split(', ')

                f.write("""
                        {
                            "pub_id": %s,
                            "title": %s,
                            "link": %s,
                            "authors": %s,
                            "source": %s,
                            "year": %s
                            "short_desc": %s
                            "descriptors": %s
                        },
                    """%(pub_id, title, link, authors, source, year, short_desc, descriptors)
                )

            f.write("""
                ]"""
            )
                    
def main():
    cycle()

if __name__=="__main__":
    main()