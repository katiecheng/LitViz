from pyquery import PyQuery as pq
import update
import time

def cycle():
    # for group in range(16521,16526, 5):
    for group in range(1,5,5):
        print "----------------",group,"----------------"

        for page in range(group, group+5):

            time.sleep(2)

            url = "http://eric.ed.gov/?q=education&ft=on&pg=%d" %page
            print url

            html = pq(url=url)
            publications = html(".r_i")

            for i in range(0,15):

                pub_dict = {}

                current_pub = publications.eq(i)
                eric_id = current_pub.attr("id")[2:].encode('ascii', 'replace')
                title = current_pub.find('.r_t').text().encode('ascii', 'replace')
                link = current_pub.find('.r_f').find('a').attr("href").encode('ascii', 'replace')

                auth_src_yr = current_pub.find('.r_a').text()
                auth_src_yr_split = auth_src_yr.split(u'\u2013 ')

                if len(auth_src_yr_split) > 1:
                    u_authors = auth_src_yr_split[0].split('; ')

                    authors = []
                    for u_auth in u_authors:
                        auth = u_auth.encode('ascii', 'replace')
                        auth = auth.strip()
                        authors.append(auth)

                    source = auth_src_yr_split[1][:-6].encode('ascii', 'replace')
                    year = auth_src_yr_split[1][-4:].encode('ascii', 'replace')
                else:
                    authors = []
                    source = auth_src_yr_split[0][:-6].encode('ascii', 'replace')
                    year = auth_src_yr_split[0][-4:].encode('ascii', 'replace')

                u_short_desc = current_pub.find('.r_d').text()

                u_short_desc_split = u_short_desc.split(u'\r\n')
                u_short_desc = ''
                for item in u_short_desc_split:
                    u_short_desc += ' ' + item

                if u_short_desc[-1:] == u'\u2026':
                    short_desc = u_short_desc[:-1].encode('ascii', 'replace') + '...'
                else:
                    short_desc = u_short_desc.encode('ascii', 'replace')

                descriptors = current_pub.find('.keywords').text()[13:].encode('ascii', 'replace').split(', ')

                pub_dict["eric_id"] = eric_id
                pub_dict["title"] = title
                pub_dict["url"] = link
                pub_dict["authors"] = authors
                pub_dict["source"] = source
                pub_dict["year"] = year
                pub_dict["short_desc"] = short_desc
                pub_dict["descriptors"] = descriptors

                update.add_source(source)
                update.add_publication(pub_dict)
                    
def main():
    cycle()

if __name__=="__main__":
    main()