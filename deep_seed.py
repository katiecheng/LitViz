from pyquery import PyQuery as pq
import update
import time
import re

def cycle():

    # map months to integers
    month_dict = {
        'Jan':1, 'January':1,
        'Feb':2, 'February':2,
        'Mar':3, 'March':3,
        'Apr':4, 'April':4,
        'May':5,
        'Jun':6, 'June':6,
        'Jul':7, 'July':7,
        'Aug':8, 'August':8,
        'Sep':9, 'Sept':9, 'September':9,
        'Oct':10, 'October':10,
        'Nov':11, 'November':11,
        'Dec':12, 'December':12
    }

    for group in range(2436,16526, 5):
    # for group in range(1,5,5):
        print "----------------",group,"----------------"

        for page in range(group, group+5):

            url = "http://eric.ed.gov/?q=education&ft=on&pg=%d" %page
            print url

            # get html for search results page
            html = pq(url=url)
            publications = html(".r_i")

            # process each of the 15 publications on a given search results page
            for i in range(0,15):

                # wait two seconds between every page request
                time.sleep(2)

                current_pub = publications.eq(i)

                # "deep url" goes in one more layer, to the detailed pub page
                deep_url = 'http://eric.ed.gov/' + current_pub.find('.r_t'
                    ).find('a').attr("href").encode('ascii', 'replace')
                deep_html = pq(url=deep_url)

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

                try:
                    int(year)
                    print eric_id, year
                except ValueError:
                    print eric_id, "year is not an integer"
                    continue

                # pull the full description from the detailed pub page
                # get rid of weird \r\n formatting
                u_deep_desc = deep_html.find('.abstract').text()
                deep_desc_split = u_deep_desc.split(u'\r\n')
                deep_desc = ''
                for part in deep_desc_split:
                    deep_desc += part

                # pull the full list of descriptors from the detailed pub page
                deep_descriptors_html = str(deep_html.find('.keywords').find('a'))
                pattern = r"<a href=.*?>(.*?)</a>"
                deep_descriptors = re.findall(pattern, deep_descriptors_html)

                # pull citation count from detailed pub page
                deep_citation_html = str(deep_html.find('div#r_colR'))
                pattern = r"<div><strong>Reference Count:</strong> (.*?)</div>"
                deep_citation_count_raw = re.findall(pattern, deep_citation_html)[0]
                
                try:
                    deep_citation_count = int(deep_citation_count_raw)
                except ValueError:
                    deep_citation_count = 0

                # pull volume, issue, page, and month from detailed pub page
                deep_info = deep_html('.r_a').text().encode('ascii', 'replace')
                volume_pattern = r" v(\d*?) "
                issue_pattern = r" n(\d*?) "
                page_pattern = r" p(\d*?)-(\d*?) "
                date_pattern = r".*? ([a-zA-Z]*) \d\d\d\d"

                volume_list = re.findall(volume_pattern, deep_info)
                issue_list = re.findall(issue_pattern, deep_info)
                pages_list = re.findall(page_pattern, deep_info)
                month_str_list = re.findall(date_pattern, deep_info)

                # populate the pub_dict
                if volume_list:
                    deep_volume = volume_list[0]
                    pub_dict["volume"] = deep_volume
                else:
                    pub_dict["volume"] = None

                if issue_list:
                    deep_issue = issue_list[0]
                    pub_dict["issue"] = deep_issue
                else:
                    pub_dict["issue"] = None

                if pages_list:
                    if len(pages_list[0])==2:
                        deep_start_page = pages_list[0][0]
                        deep_end_page = pages_list[0][1]
                        pub_dict["start_page"] = deep_start_page
                        pub_dict["end_page"] = deep_end_page
                    else:
                        deep_start_page = pages_list[0][0]
                        pub_dict["start_page"] = deep_start_page
                        pub_dict["end_page"] = None
                else:
                    pub_dict["start_page"] = None
                    pub_dict["end_page"] = None

                if month_str_list:
                    if month_str_list[0] in month_dict:
                        deep_month = month_dict[month_str_list[0]]
                        pub_dict["month"] = deep_month
                    else:
                        pub_dict["month"] = None

                pub_dict["eric_id"] = eric_id
                pub_dict["title"] = title[:500]
                pub_dict["url"] = link
                pub_dict["authors"] = authors
                pub_dict["source"] = source[:100]
                pub_dict["year"] = year
                pub_dict["full_desc"] = deep_desc[:5000]
                pub_dict["descriptors"] = deep_descriptors
                pub_dict["citation_count"] = deep_citation_count

                # add the publication entry (and all related info) to DB
                update.add_source(source[:100])
                update.add_publication(pub_dict)
                    
def main():
    cycle()

if __name__=="__main__":
    main()