# Build a web crawler


def get_next_target(page):
	start_link = page.find('<a href=')
	if start_link == -1:
		return None,0
	url_start = page.find('"',start_link)
	url_end = page.find('"',url_start+1)
	url= page[url_start+1:url_end]
	return url, url_end

def get_all_links(page):
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
	import urllib2
	source = urllib2.urlopen(page)
	return source.read()

def web_crawler(seed):
	to_crawl = [seed]
	crawled = []
	#links = get_all_links(page)

	while to_crawl:
		link = to_crawl[0]
		if link not in crawled:
			links = get_all_links(get_page(link))
			crawled.append(link)
			to_crawl += links
		to_crawl.remove(link)

	return crawled

seed = "https://www.udacity.com/cs101x/index.html"
'''page = get_page("http://xkcd.com/353/")
page = get_page("https://www.udacity.com/cs101x/index.html")'''

print web_crawler(seed)
