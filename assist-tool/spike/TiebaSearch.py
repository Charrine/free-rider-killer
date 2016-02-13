# -*- coding: utf8 -*-
import urllib2
import urllib
import sys
import bs4
import json

keywords = [u'跪求', u'急', u'助攻', u'在线等']

def main(argv):
	request = urllib2.Request('http://tieba.baidu.com/f?kw=c语言')
	html = urllib2.urlopen(request).read()
	print html 
	soup = bs4.BeautifulSoup(html, 'html.parser');
	threadList = soup.select('.j_thread_list')

	for thread in threadList[2:]:
		dataField = json.loads(thread['data-field'])
		author = dataField['author_name']
		tid = dataField['id']
		pid = dataField['first_post_id']
		title = thread.select('a.j_th_tit')[0].string
		if any(word in title for word in keywords):
			print title
			print author
	return

if __name__ == '__main__':
	main(sys.argv[1:])

