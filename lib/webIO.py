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

def webIOInitialization(filename):
	global _cj
	_cj = cookielib.MozillaCookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(_cj))
	urllib2.install_opener(opener)

	if os.path.exists(filename):
		_cj.load(filename, True)

def getFid(forum):
	data = _genericGet('http://tieba.baidu.com/f?kw=' + forum['kw'])

	return re.search(r'.+"forum_info":{"forum_id":(?P<fid>\d*),.+', data).group('fid')

def adminLogin(user, filename = ''):
	if isLogined():
		return True
	else:
		postdata = {
			'token' : _getToken(),
			'tpl' : 'pp',
			'mem_pass' : 'on',
			'username' : user['username'],
			'password' : user['password'],
		}
		data = _genericPost('https://passport.baidu.com/v2/api/?login', postdata)
		err_code = int(re.search(r'error=(?P<err_code>\d+)', data).group('err_code'))

		if err_code == 0:
			if filename:
				_cj.save(filename, True)
			return True
		elif err_code == 257:
			#TODO: log request
			print 'need verify code'
			sys.exit()
		elif err_code == 4:
			#TODO: log request
			print 'wrong username or password'
			sys.exit()
		else:
			return False

def isLogined():
	data = _genericGet('http://tieba.baidu.com/dc/common/tbs')

	return True if json.loads(data)['is_login'] == 1 else False;

def deleteThread(thread, forum):
	postdata = {
		'tbs' : _getTbs(),
		'kw' : forum['kw'],
		'fid' : forum['fid'],
		'tid' : thread['tid'],
		'pid' : thread['pid'],
		'commit_fr' : 'pb',
		'ie' : 'utf-8',
		'is_vipdel' : '0',
		'is_finf' : 'false'
	}
	data = _genericPost('http://tieba.baidu.com/f/commit/post/delete', postdata)

	if data['err_code'] == 0:
		return True
	else:
		#TODO: log request save data
		return False

def blockID(author, forum, reason = ''):
	constantPid = '82459413573'
	postdata = {
		'tbs' : _getTbs(),
		'fid' : forum['fid'],
		'user_name[]' : author,
		'pids[]' : constantPid,
		'day' : '1',
		'ie' : 'utf-8'
	}
	if not reason:
		postdata['reason'] = '根据帖子标题或内容，判定出现 伸手，作业，课设，作弊，二级考试，广告，无意义水贴，不文明言行或对吧务工作造成干扰等（详见吧规）违反吧规的行为中的至少一种，给予封禁处罚。如有问题请使用贴吧的申诉功能。'
	data = _genericPost('http://tieba.baidu.com/pmc/blockid', postdata)

	if data['err_code'] == 0:
		return True
	else:
		#TODO: log request save data
		return False

def getThreadDataList(forum):
	data = _genericGet('http://tieba.baidu.com/f?kw=' + forum['kw'])

	# if there is a special utf-8 charactor in html that cannot decode to 'gbk' (eg. 🐶),
	# there will be a error occured when you trying to print threadData['abstract'] to console
	html = data.decode('utf8').encode('gbk','replace').decode('gbk')
	html = bs4.BeautifulSoup(html, 'html5lib')
	threadList = html.select('.j_thread_list')
	topThreadNum = len(html.select('.thread_top'))

	#multiprocessing spend 01:06
	pool = ThreadPool()
	threadDataList = pool.map(_parseThreadData, threadList[topThreadNum:])

	#single processing spend 01:27
	#threadDataList = []
	#for thread in threadList[topThreadNum:]:
	#	threadDataList.append(_parseThreadData(thread))

	return threadDataList

def _parseThreadData(thread):
	dataField = json.loads(thread['data-field'])
	threadData = {
		'thread' : {
			'title' : thread.select('a.j_th_tit')[0].string,
			'abstract' : str(thread.select('div.threadlist_abs')[0].string).decode('utf-8'),
			'tid' : dataField['id'],
			'pid' : dataField['first_post_id'],
			'goodThread' : dataField['is_good'],
			'topThread' : dataField['is_top'],
			'replyNum' : dataField['reply_num']
		},
		'author' : {
			'userName' : dataField['author_name']
		}
	}
	_getThreadDetail(threadData)

	return threadData

def _getThreadDetail(threadData):
	data = _genericGet('http://tieba.baidu.com/p/' + str(threadData['thread']['tid']))
	data = bs4.BeautifulSoup(data, 'html5lib')
	dataField = json.loads(data.select('.l_post')[0]['data-field'])
	threadData['author']['userId'] = dataField['author']['user_id']
	threadData['author']['userLevel'] = dataField['author']['level_id']
	threadData['thread']['threadDate'] = dataField['content']['date']
	threadData['thread']['content'] = data.select('#post_content_' + str(threadData['thread']['pid']))[0].text

def _genericPost(url, postdata):
	request = urllib2.Request(url, urllib.urlencode(postdata))
	request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	request.add_header('Accept-Encoding','gzip,deflate,sdch')
	request.add_header('Accept-Language','zh-CN,zh;q=0.8')
	request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36')
	request.add_header('Content-Type','application/x-www-form-urlencoded')

	return _decodeGzip(_genericGet(request))

def _genericGet(url):
	i = 0
	while i < 10:
		i += 1
		try:
			connection = urllib2.urlopen(url, timeout = 10)
		except Exception as e:
			#TODO: log request: internet error.Retry
			sys.sleep(i ** 2)
		else:
			if connection.getcode() == 200:
				return connection.read()
			else:
				sys.sleep(i ** 2)

	#TODO: log request: internet error
	sys.exit()

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
	data = _genericGet('http://tieba.baidu.com/dc/common/tbs')
	tbs = json.loads(data)['tbs']

	return tbs

def _getToken():
	data = _genericGet('https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&class=login')
	token = json.loads(data.replace('\'', '"'))['data']['token']

	return token
