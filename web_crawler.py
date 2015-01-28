# Build a web crawler

index = []

def get_next_target(page):
	"""Return starting and ending positions of next url in 'page'"""
	start_link = page.find('<a href=')
	if start_link == -1:
		return None,0
	url_start = page.find('"',start_link)
	url_end = page.find('"',url_start+1)
	url= page[url_start+1:url_end]
	return url, url_end

def get_all_links(page):
	"""Return all urls in 'page' as a list"""
	links = []
	while True:
		url, end_pos = get_next_target(page)
		if url:
			links.append(url)
			page = page[end_pos:]
		else:
			break
	return links

def get_page(page):
	"""Return the content of 'page' as a string"""
	import urllib2
	source = urllib2.urlopen(page)
	return source.read()

def union(p,q):
	"""Store the union of p and q in p"""
	for e in q:
		if e not in p:
			p.append(e)


def add_to_index(index,keyword,url):
    """Add keyword and correspoding url to index"""
    for entry in index: 
        if keyword == entry[0]:
            entry[1].append(url)
            return index
    index.append([keyword,[url]])

def lookup(index,keyword):
	"""Lookup keyword in index and return correspoding urls """
    for entry in index:
        if keyword == entry[0]:
            return entry[1]
    return []

    

def web_crawler(seed, max_depth):
	"""Return all crawled links starting with seed page never 
	exceeding max_depth number of links"""
	to_crawl = [seed]
	crawled = []
	next_depth = []
	current_depth = 0
	
	while to_crawl and current_depth <= max_depth:
		link = to_crawl.pop(0)
		if link not in crawled:
			union(next_depth, get_all_links(get_page(link)))
			crawled.append(link)			 
		if not to_crawl:
			to_crawl, next_depth = next_depth, []
			current_depth += 1

	return crawled


seed = "https://www.udacity.com/cs101x/index.html"
'''page = get_page("http://xkcd.com/353/")
page = get_page("https://www.udacity.com/cs101x/index.html")'''

print web_crawler(seed,3)
