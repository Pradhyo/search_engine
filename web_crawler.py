# Build a web crawler

import string
index = {}
graph = {}

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
	if keyword in index:
		if url not in index[keyword]:
			index[keyword].append(url)
	else:
		index[keyword] = [url]

def lookup(index,keyword):
	"""Lookup keyword in index and return correspoding urls """
	if keyword in index:
		return index[keyword]
	return None

def split_string(source,splitlist):
	"""Better split function to extract keywords from a page"""
	spaces = " " * len(splitlist)
	transtable = string.maketrans(splitlist, spaces)
	source = string.translate(source, transtable)
	return source.split()


def add_page_to_index(index,url,content):
	"""Add given content as correspoding to given url into index """
	keywords = split_string(content,".,-!<>/=\"")
	for keyword in keywords:
		add_to_index(index,keyword,url)
	
def rank_pages(graph):
	damping_factor = 0.8
	loops = 10
	ranks = {}

	npages = len(graph)
	for page in graph:
		ranks[page] = 1.0 / npages

	for i in range(0):
		newranks = {}
		for page in graph:
			newrank = (1 - d) / npages

			newranks[page] = newrank
		ranks = newranks
	return ranks


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
			content = get_page(link)
			add_page_to_index(index, link, content)
			outlinks = get_all_links(content)
			graph[link] = outlinks
			union(next_depth, outlinks)
			crawled.append(link)			 
		if not to_crawl:
			to_crawl, next_depth = next_depth, []
			current_depth += 1

	return index, graph


seed = "https://www.udacity.com/cs101x/index.html"
'''page = get_page("http://xkcd.com/353/")
page = get_page("https://www.udacity.com/cs101x/index.html")'''

print web_crawler(seed,3)[1]
print lookup(index,"a")