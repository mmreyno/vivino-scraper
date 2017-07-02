# -*- coding: utf-8 -*-
import requests
import urllib
import urllib2
import json
from BeautifulSoup import BeautifulSoup
import unicodedata

# Open the file with the list of top wineries
def opener():
	with open('allwineries.csv') as infile:
		for line in infile:
			search_term = line.split(',')[0]
			
			number = line.split(',')[2]

			number = float(number)
			if (number < 10):
				continue
			else:
				winery_id = id_finder(search_term)
				row = wine_lister(winery_id) 
				


def id_finder(search_term):
# 	print search_term
	search_term = urllib.quote_plus(search_term)

	url = 'https://www.vivino.com/search/wineries?q='+search_term
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
	req = urllib2.Request(url,headers=hdr)
	page = urllib2.urlopen(req)
	html = page.read()
	soup = BeautifulSoup(html)

	loc = soup.find('a',{'class' : 'bold link-color-alt-grey'})
	
	link = loc['href']
	
# 	try:
# 		link = loc['href']
# 	except TypeError:
# 		winery_id = 
# 		return winery_id

	winery_url = 'https://www.vivino.com'+link
	req = urllib2.Request(winery_url,headers=hdr)
	page = urllib2.urlopen(req)
	html = page.read()
	soup = BeautifulSoup(html)

	loc = soup.find('meta',{'name' : 'twitter:app:url:iphone'})
	winery_id = loc['content'].split('=')[1]
	return winery_id



def wine_lister(winery_id):
	# Url with the wine id
	url = 'https://www.vivino.com/api/wineries/%s/wines' % winery_id

	# Search parameters
	params = {'start_from' : '0',
			  'limit' : '20',
			  'sort' : 'popular'}

	# Search headers
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
			   'Accept' : 'application/json, text/javascript, */*; q=0.01',
			   'Accept-Encoding' : 'gzip, deflate, sdch, br',
			   'Accept-Language' : 'en-US,en;q=0.8,pt;q=0.6',
			   'Referer' : 'https://www.vivino.com/wineries/albert-boxler',
			   'X-Requested-With': 'XMLHttpRequest',
			   'X-Csrf-Token' : 'qEU5USXTrOHI5IkO07nhwfDN6mMQE1w2WNfaSp0+R+37CFKQzf/3+r2n2t+WLwI+6MtoTa7bg+ICC8nZyn7Szw==',
			   'X-Newrelic-Id' : 'Vw8OVFVTGwADVFBWBAU=',
			   'If-None-Match' : 'W/"f9050af48a0e6c907e030a160a3dd802"',
			   'Cookie' : 'PAPVisitorId=794d253f5f29f20f5bb03glnI4DfXFzL; push_down=true; icid=Top rated wines from region-region-page; visited_wine_styles=%7B%2247%22%3A1%2C%22248%22%3A1%2C%22181%22%3A3%2C%22128%22%3A3%2C%227%22%3A3%2C%22130%22%3A1%2C%225%22%3A1%2C%2273%22%3A2%2C%2283%22%3A2%2C%22131%22%3A1%2C%22139%22%3A1%2C%2294%22%3A3%7D; eeny_meeny_related_wines_for_user_v3=CvNu2h29PENAWhw316bLadlHUotbFbftYnCbBy8L4WNLanJQ2NTawx1UrB5WsNjVEaSNn67PBoTiolMnpOazmA%3D%3D; __asc=ef33061015c01a20c0a62f47871; __auc=0a1ba21315be3e2ea4bfcf74de6; _ga=GA1.2.2143981093.1494176950; _gid=GA1.2.1989317754.1494676577; _gat_vivinoTracker=1; _ruby-web_session=VWRMbENKN2JMSElNbFNjVjlHR2FKN2hja3JwdnNabTA5ZlJ6dWplZWRUN2lQYk5qbERscjMrVmtSYXFXWmZXcVlsSStKaW9GcmhQOVlUN2FHL3Q4aXQ3VzZ0S3lmZ0FDNVNuNzlMb0VXLzVvckZNd1FlOTZyNTBxZW5TY0UzNno3Z3d6VHg1RWdLeE1hem9zMHhiOFZ1WTZ3MUF4QXhES0ZoUkdzR3Fub0p0WldnamQ2Wjl6V1c2ZHFkTDVlbE9hc3lZajd0ajNjYXJ3eVUwWFdGN0FNUjhoei9ZMEhITDVSNVU3TDJIZTBFNXJySTJSVDJzNjE3MW0zdTBXK0ZpWDN0L3hIWVFSbWtleFErdUFmbDY5eE15WG5CUnp4K25WK3VERTJWY1lSV3RyQ0JUakhPUEo5Qk94UnlFQ0FjM09yKzlGK01NMkhUa2ltSHdGL0xQbkN3PT0tLWJ0Vm9ENnowdmkvUFJWM3R3U0VrQ3c9PQ%3D%3D--9f1948a8048746dabe15f5739abe94919b5cb877'
			   }

	# Make the request
	r = requests.get(url, params=params, headers=headers)

	# Get as a json and parse
	json_list = r.text
	parsed = json.loads(json_list)
	number_of_wines = len(parsed['wines'])

	# Iterate over and find all the wines with more than 30 rankings
	for i in range(number_of_wines):
		loc = parsed['wines'][i]
	
		# Find the number of ratings
		num_ratings = loc['statistics']['ratings_count']
		if (num_ratings > 30 or num_ratings < 10):
			continue
		num_ratings = str(num_ratings)
	
		# Find the average rating
		avg_rating = loc['statistics']['ratings_average']
		if avg_rating < 3.6:
			continue
		avg_rating = str(avg_rating)
	
		# Find the name of the wine and the winery
		name = loc['name']		
		winery = loc['winery']['name']
	
		# Make into a row so it can be printed
		row = "%s, %s, %s, %s" % (winery, name, avg_rating, num_ratings)
		print row.encode('utf-8')
	
		
	
if __name__ == "__main__":
	opener()
	
	
	
	
	
	

	
	
	
	