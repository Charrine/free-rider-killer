# -*- coding: utf8 -*-
import urllib2
import urllib
import cookielib
import sys
import bs4
import json
import codecs

# 'generic' tieba request
def sendRequest(url, postdata):
	request = urllib2.Request(url, urllib.urlencode(postdata))

	request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8');

	request.add_header('Accept-Encoding','gzip,deflate,sdch');

	request.add_header('Accept-Language','zh-CN,zh;q=0.8');

	request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36');

	request.add_header('Content-Type','application/x-www-form-urlencoded');
	result = urllib2.urlopen(request)
	print result.read()
	result.close()
	print '--- Done Request ---'
	return

# tieba admin user login
def adminLogin(username, password):
	print '--- Initializing ---'
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	urllib2.install_opener(opener)
	print '--- Geting Cookie ---'
	link = urllib2.urlopen('http://www.baidu.com/')
	print '--- Geting Token ---'
	token = eval(urllib2.urlopen('https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&class=login').read())['data']['token']
	print "Token: " + token
	print '--- Sign In Posting ---'
	postdata = {
		'token' : token,
		'tpl' : 'pp',
		'username' : username,
		'password' : password,
	}
	sendRequest('https://passport.baidu.com/v2/api/?login', postdata)
	link.close()
	return

def main(argv):
	print len(argv)
	if len(argv) != 2:
		print 'tiebaAutoTool.py <ID_OF_ADMIN> <PASSWORD>'
		sys.exit(2)

	username = sys.argv[1]
	password = sys.argv[2]
	print username
	adminLogin(username, password)
	f = codecs.open('freeRiderData.txt', 'w', encoding='utf8')
	with codecs.open('noisyData.txt', 'r', encoding='utf8') as fnoise:
		dataNoisy = fnoise.readlines()

	datalink = 'http://tieba.baidu.com/bawu2/platform/listPostLog?stype=&svalue=&begin=&end=&op_type=&word=c%D3%EF%D1%D4&pn='

	for i in range(100,200):
		datalink+str(i)
		request = urllib2.Request(datalink+str(i))
		connection = urllib2.urlopen(request)
		html = connection.read()
		connection.close()
		soup = bs4.BeautifulSoup(html, 'html.parser');
		threadList = soup.select('.post_content')
		for thread in threadList[1:]:
			links = thread.find_all('a')
			for link in links:
				title = link.get('title')
				print title
				f.write(title)
				f.write('\n')
				'''
				if title != None and not any(data in title for data in dataNoisy):
					print title
					f.write(title)
					f.write('\n')
				'''
	return

if __name__ == '__main__':
	main(sys.argv[1:])
