# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
import urllib2
import unicodedata



# Set headers, which are unexpectedly strict
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}



# Open the pages that will be parsed
def page_opener():
	
	# Vivino currently has 10 wines per page, so divide the number of wineries in the region by 10
	for i in range(1,176):
		
		# Url for the region's wineries
		url = 'http://www.vivino.com/wine-regions/alsace/wineries?page='+str(i)

		# Soup it
		req = urllib2.Request(url, headers=hdr)
		page = urllib2.urlopen(req)
		html = page.read()
		soup = BeautifulSoup(html)
		
		# Send the info to the page reader
		page_reader(soup)



# Read the page and extract the relevant info
def page_reader(soup):
	
	# Parse the page to find the tag we want
	for loc in soup.findAll("div", { "class" : "winery-card" }):
	
		# Find the name of the wine and clean it
		name = loc.div.text
		name = name.replace("'","")
		name = name.replace(",","")
		name = name.replace("[0xc2]","")
		name = name.replace(u'œ',u'')
		name = unicodedata.normalize('NFKD', unicode(name))
		name = u"".join([c for c in name if not unicodedata.combining(c)])
		name = name.replace('&amp;','and')
		print name,',',

		# Find the average rating of the winery
		try:
			rating = loc.div.nextSibling.nextSibling.div.nextSibling.nextSibling.div.text
			rating = float(rating)
			print rating,',',
	
			# Find the number of ratings for the winery
			num_ratings = loc.div.nextSibling.nextSibling.div.nextSibling.nextSibling.div.nextSibling.nextSibling.text
			num_ratings = num_ratings.split(' ')[0]
			print num_ratings,',',
		
		# The number of wines isn't always listed, so we deal with that here
		except AttributeError:
			rating = loc.find("div", { "class" : "text-inline-block light info__number" }).text
			rating = float(rating)
			print rating,',',
		
			num_ratings = loc.find( "p", {"class" : "text-micro" }).text
			num_ratings = num_ratings.split(' ')[0]
			print num_ratings,',',

		# We want the websites of the good wineries so we can contact them 
		if rating < 3.8:
			print '\n'
		else:
			link = loc.a['href']
			winery_website_finder(link)
	
	
# Get the websites of the good wineries			
def winery_website_finder(link):
	url = 'https://www.vivino.com'+link

	# Soup it
	req = urllib2.Request(url, headers=hdr)
	page = urllib2.urlopen(req)
	html = page.read()
	soup = BeautifulSoup(html)
	page_reader(soup)			
	
	# Find the info for the website
	try:
		winery_online = soup("a", { "class" : "winery-page__location__contact__online__item" })[-1]
		print 'http://www.'+winery_online.contents[2][1:]
	except IndexError:
		print '\n'


	
		
if __name__ == "__main__":
	page_opener()
	

