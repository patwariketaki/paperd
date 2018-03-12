import cookielib 
import urllib2 
import mechanize
from time import sleep
import os
import cgi

# A routine to download a file from a link, by simulating a click on it
def downloadlink(linkUrl, referer):
    r = br.click_link(linkUrl)
    r.add_header("Referer", referer) # add a referer header, just in case
    response = br.open(r)
    
    #get filename from the response headers if possible
    cdheader = response.info().getheader('Content-Disposition')
    if cdheader:
        value, params = cgi.parse_header(cdheader)
        filename  = params["filename"]
    else:
        # if not use the link's basename
        filename = os.path.basename(linkUrl.url)

    f = open(filename, "w") #TODO: perhaps ensure that file doesn't already exist?
    f.write(response.read()) # write the response content to disk
    print filename," has been downloaded"
    br.back()

# Make a Browser (think of this as chrome or firefox etc)
br = mechanize.Browser()

# Enable cookie support for urllib2 
cookiejar = cookielib.LWPCookieJar() 
br.set_cookiejar( cookiejar ) 

# Broser options 
br.set_handle_equiv( True ) 
br.set_handle_gzip( True ) 
br.set_handle_redirect( True ) 
br.set_handle_referer( True ) 
br.set_handle_robots( False ) 
br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 1 ) 
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')] # masquerade as a real browser. this is not nice to do though.

print "Get all PDF links\n"
for z in range(0,9):
# Open your site
	mypageUrl = 'http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=831061'+str(z)
	br.open(mypageUrl)

	
	filetypes=["pdf", "PDF"] # pattern matching for links, can add more kinds here
	myfiles=[]
	for l in br.links():
    #check if this link has the file extension or text we want
    		myfiles.extend([l for t in filetypes if t in l.url or t in l.text])

	for l in myfiles:
# for index, l in zip(range(100), myfiles): # <--- uncomment this line (and coment the one above) to download 100 links.
    #sleep(1) # uncomment to throttle downloads, so you dont hammer the site
		downloadlink(l, mypageUrl)
