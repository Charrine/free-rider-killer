# -*- coding: utf8 -*-
import urllib2
import urllib
import cookielib
import bs4
import time
import sys, getopt
import json

#Set username and password

keywords = [u'求代码', u'求教', u'求助', u'在线等', u'求帮助', u'二级', u'帮做', u'大神', u'哪里错了', u'帮我看', u'小白求', u'为什么']

# 'generic' tieba request
def sendRequest(url, postdata):
	request = urllib2.Request(url, urllib.urlencode(postdata))

	request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8');

	request.add_header('Accept-Encoding','gzip,deflate,sdch');

	request.add_header('Accept-Language','zh-CN,zh;q=0.8');

	request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36');

	request.add_header('Content-Type','application/x-www-form-urlencoded');
	result = urllib2.urlopen(request)
	result.close()
	print '--- Done Request ---'
	return

# delete a post with its tid and pid 
def deletePost(threadData):
	print '--- Sending Delete Request ---'
	tbs = eval(urllib2.urlopen('http://tieba.baidu.com/dc/common/tbs').read())['tbs']
	postdata = {
		'commit_fr' : 'pb',
		'ie' : 'utf-8',
		'tbs' : tbs,
		'kw' : 'c%E8%AF%AD%E8%A8%80',
		'fid' : '22545',
		'tid' : threadData['tid'], #tie zi id: e.g.'4304106830'
		'is_vipdel' : '0',
		'pid' : threadData['pid'], #lou ceng id: e.g.'82457746974'
		'is_finf' : 'false'
	}
	sendRequest('http://tieba.baidu.com/f/commit/post/delete', postdata)
	logFile = open('log.txt', 'a')
	logFile.write('{\n')
	logFile.write('    "type" : "delete",\n')
	logFile.write('    "data" : {\n')
	logFile.write('        "time" : "' + time.asctime() + '",\n')
	logFile.write('        "title" : "' + threadData['title'].encode('utf-8') + '",\n')
	logFile.write('        "author" : "' + threadData['author'].encode('utf-8') + '",\n')
	logFile.write('        "abstract" : "' + threadData['abstract'].encode('utf-8') + '",\n')
	logFile.write('    }\n')
	logFile.write('},\n')
	logFile.close()
	return

# block list of user with their username and pid(pid may not be necessary)
def blockID(threadData):
	print '--- Sending Block Request ---'
	constantPid = '82459413573'
	tbs = eval(urllib2.urlopen('http://tieba.baidu.com/dc/common/tbs').read())['tbs']
	postdata = {
		'day' : '1',
		'fid' : '22545',
		'tbs' : tbs,
		'ie' : 'utf-8',
		'user_name[]': threadData['author'].encode('utf-8'),
		'pids[]' : constantPid, 
		'reason' : '根据帖子标题或内容，判定出现 伸手，作业，课设，作弊，二级考试，广告，无意义水贴，不文明言行或对吧务工作造成干扰等（详见吧规）违反吧规的行为中的至少一种，给予封禁处罚。如有问题请使用贴吧的申诉功能。'
	}
	sendRequest('http://tieba.baidu.com/pmc/blockid', postdata)
	logFile = open('log.txt', 'a')
	logFile.write('{\n')
	logFile.write('    "type" : "block",\n')
	logFile.write('    "data" : {\n')
	logFile.write('        "time" : "' + time.asctime() + '",\n')
	logFile.write('        "author" : "' + threadData['author'].encode('utf-8') + '",\n')
	logFile.write('    }\n')
	logFile.write('},\n')
	logFile.close()
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
	print '--- Sending Signin Request ---'
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
	print "Get argument: {0}".format(len(argv))
	if len(argv) != 2:
		print 'tiebaAutoTool.py <ID_OF_ADMIN> <PASSWORD>'
		sys.exit(2)

	username = sys.argv[1]
	password = sys.argv[2]
	print "Current username: " + username

	adminLogin(username, password)

	while(True):
		deleteCount = 0
		request = urllib2.Request('http://tieba.baidu.com/f?kw=c语言')
		connection = urllib2.urlopen(request)
		html = connection.read()
		connection.close()
		soup = bs4.BeautifulSoup(html, 'html.parser');
		threadList = soup.select('.j_thread_list')
		topThreadNum = len(soup.select('.thread_top'))

		for thread in threadList[topThreadNum:]:
			dataField = json.loads(thread['data-field'])
			threadData = {
				'title' : thread.select('a.j_th_tit')[0].string,
				'author' : dataField['author_name'],
				'abstract' : thread.select('div.threadlist_abs')[0].string,
				'tid' : dataField['id'],
				'pid' : dataField['first_post_id'],
				'goodThread' : dataField['is_good'],
				'topThread' : dataField['is_top'],
				'replyNum' : dataField['reply_num']
			}

			if threadData['goodThread'] == 0 and threadData['topThread'] == 0:
				if any(word in threadData['title'] for word in keywords) or ((threadData['abstract'] != None) and any(word in threadData['abstract'] for word in keywords)):
					deleteCount += 1
					print threadData['title']
					print threadData['author']
					print threadData['abstract']
					deletePost(threadData)
					#blockID(threadData)
					time.sleep(3)

		print 'Front Page Checked: {0} Post Deleted'.format(deleteCount)

	return

if __name__ == '__main__':
	main(sys.argv[1:])
