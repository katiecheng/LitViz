from pyquery import PyQuery as pq
import update
import time

def cycle():
    # for group in range(1,16526, 5):
    for group in range(1,5,5):
        print "----------------",group,"----------------"

        for page in range(group, group+5):

            # wait two seconds between every page request
            time.sleep(2)

            url = "http://eric.ed.gov/?q=education&ft=on&pg=%d" %page
            print url

            # get html for search results page
            html = pq(url=url)
            publications = html(".r_i")

            # process each of the 15 publications on a given search results page
            for i in range(0,15):

                current_pub = publications.eq(i)

                # initialize pub_dict to hold all of the pub's data
                pub_dict = {}

                # get eric_id, title, and pdf link from search results page
                eric_id = current_pub.attr("id")[2:].encode('ascii', 'replace')
                title = current_pub.find('.r_t').text().encode('ascii', 'replace')
                link = current_pub.find('.r_f').find('a').attr("href").encode('ascii', 'replace')

                # get authors and source/year (split on hyphen)
                auth_src_yr = current_pub.find('.r_a').text()
                auth_src_yr_split = auth_src_yr.split(u'\u2013 ')

                # if there is a hyphen, process the portion before the hyphen
                # to get a list of authors (split on semicolons)
                if len(auth_src_yr_split) > 1:
                    u_authors = auth_src_yr_split[0].split('; ')

                    authors = []
                    for u_auth in u_authors:
                        auth = u_auth.encode('ascii', 'replace')
                        auth = auth.strip()
                        authors.append(auth)
                    # process line after the hyphen to get source and year
                    source = auth_src_yr_split[1][:-6].encode('ascii', 'replace')
                    year = auth_src_yr_split[1][-4:].encode('ascii', 'replace')

                # if there is not a hyphen, authors is empty
                # process line to get source and year
                else:
                    authors = []
                    source = auth_src_yr_split[0][:-6].encode('ascii', 'replace')
                    year = auth_src_yr_split[0][-4:].encode('ascii', 'replace')

                # pull the short description from the search results page
                # get rid of weird \r\n formatting, and fix ellipses at the end
                u_short_desc = current_pub.find('.r_d').text()
                u_short_desc_split = u_short_desc.split(u'\r\n')
                u_short_desc = ''
                for item in u_short_desc_split:
                    u_short_desc += ' ' + item

                if u_short_desc[-1:] == u'\u2026':
                    short_desc = u_short_desc[:-1].encode('ascii', 'replace') + '...'
                else:
                    short_desc = u_short_desc.encode('ascii', 'replace')

                # pull the short list of descriptors from the search results page
                descriptors = current_pub.find('.keywords').text()[13:].encode('ascii', 'replace').split(', ')

                # populate the pub_dict
                pub_dict["eric_id"] = eric_id
                pub_dict["title"] = title
                pub_dict["url"] = link
                pub_dict["authors"] = authors
                pub_dict["source"] = source
                pub_dict["year"] = year
                pub_dict["short_desc"] = short_desc
                pub_dict["descriptors"] = descriptors

                # add the publication entry (and all related info) to DB
                update.add_source(source)
                update.add_publication(pub_dict)
                    
def main():
    cycle()

if __name__=="__main__":
    main()