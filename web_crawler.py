# Build a web crawler


def get_next_target(page):
	start_link = page.find('<a href=')
	url_start = page.find('"',start_link)
	url_end = page.find('"',url_start+1)
	url= page[url_start+1:url_end]
	return url, url_end

page =('<div id="top_bin"><div id="top_content" class="width960">'
'<div class="udacity float-left"><a href="http://udacity.com">')
url, end_pos = get_next_target(page)
print url