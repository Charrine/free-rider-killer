# -*- coding: utf8 -*-
import bs4
import cookielib
import gzip
import json
import os
import re
import sys
import StringIO
import time
import urllib
import urllib2

from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

_cj = None

def baiduInitialization(filename):
	global _cj
	_cj = cookielib.MozillaCookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(_cj))
	urllib2.install_opener(opener)

	if os.path.exists(filename):
		_cj.load(filename, True)

def getFid(forum):
	data = _request('http://tieba.baidu.com/f?kw=' + forum['kw'])

	return re.search(r'.+"forum_info":{"forum_id":(?P<fid>\d*),.+', data).group('fid')

def adminLogin(user, filename = '', config = False):
	if not config and isLogined():
		return True
	else:
		postdata = {
			'token' : _getToken(),
			'tpl' : 'pp',
			'mem_pass' : 'on',
			'username' : user['username'],
			'password' : user['password'],
		}
		data = _request('https://passport.baidu.com/v2/api/?login', postdata)
		err_code = int(re.search(r'error=(?P<err_code>\d+)', data).group('err_code'))

		if err_code == 0:
			if filename:
				_cj.save(filename, True)
			return True
		else:
			return False
#		elif err_code == 257:
#			print 'need verify code'
#			sys.exit()
#		elif err_code == 4:
#			print 'wrong username or password'
#			sys.exit()

def isLogined():
	data = _request('http://tieba.baidu.com/dc/common/tbs')

	return True if json.loads(data)['is_login'] == 1 else False;

def deleteThread(thread, forum):
	postdata = {
		'tbs': _getTbs(),
		'kw': forum['kw'],
		'fid': forum['fid'],
		'tid': thread['tid'],
		'pid': thread['pid'],
		'commit_fr': 'pb',
		'ie': 'utf-8',
		'is_vipdel': '0',
		'is_finf': 'false'
	}
	data = _request('http://tieba.baidu.com/f/commit/post/delete', postdata)
	data = json.loads(data)

	if data['err_code'] == 0:
		return True
	else:
		return False

def blockID(author, forum, reason = ''):
	constantPid = '82459413573'
	postdata = {
		'tbs': _getTbs(),
		'fid': forum['fid'],
		'user_name[]': author,
		'pids[]': constantPid,
		'day': '1',
		'ie': 'utf-8',
		'reason': reason
	}
	if not reason:
		postdata['reason'] = '根据帖子标题或内容，判定出现 伸手，作业，课设，作弊，二级考试，广告，无意义水贴，不文明言行或对吧务工作造成干扰等（详见吧规）违反吧规的行为中的至少一种，给予封禁处罚。如有问题请使用贴吧的申诉功能。'
	data = _request('http://tieba.baidu.com/pmc/blockid', postdata)
	data = json.loads(data)

	if data['errno'] == 0:
		return True
	else:
		return False
#	elif data['err_code'] == 74:
#		print 'user doesn't exist'
#		sys.exit()

def getThreadDataList(forum):
	data = _request('http://tieba.baidu.com/f?kw=' + forum['kw'] + '&pn=0&apage=1')

	# if there is a special utf-8 charactor in html that cannot decode to 'gbk' (eg. 🐶),
	# there will be a error occured when you trying to print threadData['abstract'] to console
	html = data.decode('utf8').encode('gbk','replace').decode('gbk')
	html = bs4.BeautifulSoup(html, 'html5lib')
	threadList = html.select('.j_thread_list')
	topThreadNum = len(html.select('.thread_top'))

	pool = ThreadPool()
	threadDataList = pool.map(_parseThreadData, threadList[topThreadNum:])

	return threadDataList

def _parseThreadData(thread):
	dataField = json.loads(thread['data-field'])
	threadData = {
		'thread': {
			'title': thread.select('a.j_th_tit')[0].string,
			'abstract': str(thread.select('div.threadlist_abs')[0].string).decode('utf-8'),
			'tid': dataField['id'],
			'pid': dataField['first_post_id'],
			'goodThread': dataField['is_good'],
			'topThread': dataField['is_top'],
			'replyNum': dataField['reply_num']
		},
		'author': {
			'userName': dataField['author_name']
		},
		'operation': {}
	}
	#_getThreadDetail(threadData)

	return threadData

def _getThreadDetail(threadData):
	data = _request('http://tieba.baidu.com/p/' + str(threadData['thread']['tid']) + '?pn=1&ajax=1')
	data = bs4.BeautifulSoup(data, 'html5lib')
	dataField = json.loads(data.select('.l_post')[0]['data-field'])
	if dataField['content']['is_anonym'] == 1:
		threadData['author']['is_anonym'] = True
		threadData['author']['userLevel'] = '0'
		threadData['author']['userLevel'] = '0'
		threadData['thread']['threadDate'] = dataField['content']['date']
		threadData['thread']['content'] = data.select('#post_content_' + str(threadData['thread']['pid']))[0].text
	else:
		threadData['author']['is_anonym'] = False
		threadData['author']['userLevel'] = dataField['author']['level_id']
		threadData['author']['userLevel'] = dataField['author']['user_id']
		threadData['thread']['threadDate'] = dataField['content']['date']
		threadData['thread']['content'] = data.select('#post_content_' + str(threadData['thread']['pid']))[0].text

def _request(url, postdata = ''):
	if postdata:
		request = urllib2.Request(url, urllib.urlencode(postdata))
	else:
		request = urllib2.Request(url)

	request.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0')
	request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	request.add_header('Accept-Language', 'zh-CN,zh;q=0.8')
	request.add_header('Accept-Encoding', 'gzip, deflate')

	return _decodeGzip(_urlopen(request))

def _urlopen(request):
	i = 0
	while i < 10:
		i += 1
		try:
			connection = urllib2.urlopen(request, timeout = 10)
		except Exception as e:
			time.sleep(i ** 2)
		else:
			if connection.getcode() == 200:
				return connection.read()
			else:
				time.sleep(i ** 2)

def _decodeGzip(data):
	try:
		fileObj = StringIO.StringIO(data)
		gzipObj = gzip.GzipFile(fileobj = fileObj)
		data = gzipObj.read()
	except IOError, e:
		pass
	finally:
		fileObj.close()
		gzipObj.close()

	return data

def _getTbs():
	data = _request('http://tieba.baidu.com/dc/common/tbs')
	tbs = json.loads(data)['tbs']

	return tbs

def _getToken():
	data = _request('https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&class=login')
	token = json.loads(data.replace('\'', '"'))['data']['token']

	return token

if __name__ == '__main__':
	print u'本模块只应被导入执行'
