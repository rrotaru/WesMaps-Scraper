import urllib2, urlparse, datetime, time
from bs4 import BeautifulSoup, NavigableString

print "The scraper is now running. Please wait while it fetches all of the web pages and creates its lists."
print "Also, be sure to check your internet connection if the scraper does not work or throws an Errno 8"

# Create a soup from the HTML on the main page of wesmaps
dept_soup = BeautifulSoup(urllib2.urlopen('https://iasext.wesleyan.edu/regprod/!wesmaps_page.html'))
# Find all <a></a> tags on wesmaps with the href attribute (aka all the links)
links = dept_soup.findAll('a', href=True)

# Create two empty lists.
linkslist = []
depts = []

# Calculate the current term. The term for 2012 is 1129 and each following term
# will be that number plus 10
term = str(1129 + 10*(datetime.datetime.now().year - 2012))

# Take each link from above and select all those that include the string "subj_page" 
# (aka all links to a department's courses) and append the value of the subj_page parameter to the list linkslist
# (This will be things such as ARHA, BIOL, etc.
# This is done using the automatic url parsing from the urlparse lib
for link in links:
    href = link['href']
    url = urlparse.urlparse(href)
    params = urlparse.parse_qs(url.query)
    if 'subj_page' in params:
        depts.append(params['subj_page'][0])
        linkslist.append(link)

# Create 5 empty lists
course_list = []
coursename_list = []
prof_list = []
url_list = []
desc_list = [] # Currently unused because the function is unfinished.

# Construct a link to the "Courses Offered" page for each department this term and create a soup from the html of the page.
for dept in depts:
    html = 'https://iasext.wesleyan.edu/regprod/!wesmaps_page.html?crse_list=' + dept + '&term=' + term + '&offered=Y'
    course_soup = BeautifulSoup(urllib2.urlopen(html))
    
    # For each course found by invoking course_soup.findAll(etc), append the course to course_list and append the URL to the course's description page to url_list
    # soup.findAll searches for a <td></td> tag with a width parameter of 5% (which happens to exist only for the tags which contain the course names (such as BIOL-140-01))
    for course in course_soup.findAll('td', width = "5%"):
        course_list.append(course.a.string)
        course_html = 'https://iasext.wesleyan.edu/regprod/' + course.a['href']
        url_list.append(course_html)

# For scraping course description. DO NOT UNCOMMENT. Feature is not yet finished, maybe someone can add it. 
#        courseinfo_soup = BeautifulSoup(urllib2.urlopen(course_html))
#        for info in courseinfo_soup.findall(

    # For each coursename, append it to coursename_list
    # soup.findAll searches for <td></td> tags with width = 55% (only exists for course names, such as "Classic Studies in Animal Behavior")
    for coursename in course_soup.findAll('td', width = "55%"):
        coursename_list.append(coursename.string)

    # For each professor name, append it to prof_list
    # soup.findAll uses same method as above, with width = 40%
    # Some courses do not have a professor text available, which throws an AttributeError that is caught. A lot of these errors will print when the scraper is run.
    for prof in course_soup.findAll('td', width = "40%"):
        try:
            prof_list.append(prof.a.string)
        except AttributeError, e:
            # Some courses have "STAFF" listed, which doesn't correspond to an <a></a> tag, but to an html break.
            # So we catch AttributeError exceptions where prof.a doesn't have a string attribute and just stick "STAFF" in our list instead.
            prof_list.append(u"STAFF")

print "The scraper has finished. All of the courses can be found in 'info_tuple'"
print "You can run 'for i in info_tuple: print i' to view the list."
# zip takes the four lists and combines them into one tuple in order
# (i.e. lists [1,2,3,4] [a,b,c,d] and [A,B,C,D] would combine into [(1,a,A),(2,b,B),(3,c,C),(4,d,D)]
info_tuple = zip(course_list, coursename_list, prof_list, url_list)







