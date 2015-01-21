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

page =('<div id="top_bin"><div id="top_content" class="width960">'
'<div class="udacity float-left"><a href="http://udacity.com">')
page = get_page("http://xkcd.com/353/")
links = get_all_links(page)
for i in links:
	print i