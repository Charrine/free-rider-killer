# -*- coding: utf8 -*-
import bs4
import cookielib
import getopt
import gzip
import json
import re
import StringIO
import sys
import time
import urllib
import urllib2





reload(sys)
sys.setdefaultencoding( "utf-8" )

keywords=[
	[u'求',		40],
	[u'写c',	50],
	[u'求助',	100],
	[u'新人',	50],
	[u'小白',	50],
	[u'新手',	40],
	[u'出错了',	50],
	[u'求资源',	200],
	[u'题',		50],
	[u'大神', 	100],
	[u'求大神',	200],
	[u'求高手',	100],
	[u'请大神',	100],
	[u'帮忙',	50],
	[u'考试',	40],
	[u'作业',	40],
	[u'谁来帮我',400],
	[u'？？',	100],
	[u'！！！',	100],
	[u'为什么',	50],
	[u'帮我',	100],
	[u'二级',	100],
	[u'计算机二级', 500],
	[u'跪求',	500],
	[u'在线等',	500],
	[u'救急',	15],
	[u'题库',	200],
	[u'不会',	30],
	[u'2级',	100],
	[u'安装包',	100],
	[u'include', 100],
	[u'怎么改', 100],
	[u'助攻',	100],
	[u'挂科', 	50],
	[u'资料',	50],
	[u'谁有',	200],
	[u'win10',	100],
	[u'win8',	100],
	[u'vc', 	200],
	[u'VC',		200],
	[u'dev',	-200],
	[u'入门',	50],
	[u'tc',	50],
	[u'答案',	50]
]

# 'generic' tieba request
def genericPost(url, postdata):
	request = urllib2.Request(url, urllib.urlencode(postdata))

	request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8');
	request.add_header('Accept-Encoding','gzip,deflate,sdch');
	request.add_header('Accept-Language','zh-CN,zh;q=0.8');
	request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36');
	request.add_header('Content-Type','application/x-www-form-urlencoded');

	data = genericGet(request)

	return data

def genericGet(url):
	connection = urllib2.urlopen(url)
	data = connection.read()
	connection.close()

	return data


# delete a post with its tid and pid 
def deleteThread(threadData):
	print '--- Deleting ---'

	data = genericGet('http://tieba.baidu.com/dc/common/tbs')
	tbs = json.loads(data)['tbs']

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
	data = genericPost('http://tieba.baidu.com/f/commit/post/delete', postdata)

	#Decode gzip
	data = StringIO.StringIO(data)
	gzipper = gzip.GzipFile(fileobj = data)
	gzipData = gzipper.read()
	err_code = json.loads(gzipData)['err_code']

	if err_code == 0:
		print '--- Delete succeessful ---'
		writeLog(threadData, 'delete')
		return True
	else:
		print '--- Delete failed ---'
		print gzipdata
		#exit for testing
		sys.exit(3)
		return False

# block list of user with their username and pid(pid may not be necessary)
def blockID(threadData):
	print '--- Blocking ---'

	constantPid = '82459413573'

	data = genericGet('http://tieba.baidu.com/dc/common/tbs')
	tbs = json.loads(data)['tbs']

	postdata = {
		'day' : '1',
		'fid' : '22545',
		'tbs' : tbs,
		'ie' : 'utf-8',
		'user_name[]' : threadData['author'].encode('utf-8'),
		'pids[]' : constantPid, 
		'reason' : '根据帖子标题或内容，判定出现 伸手，作业，课设，作弊，二级考试，广告，无意义水贴，不文明言行或对吧务工作造成干扰等（详见吧规）违反吧规的行为中的至少一种，给予封禁处罚。如有问题请使用贴吧的申诉功能。'
	}
	data = genericPost('http://tieba.baidu.com/pmc/blockid', postdata)

	#Decode gzip
	data = StringIO.StringIO(data)
	gzipper = gzip.GzipFile(fileobj = data)
	gzipData = gzipper.read()
	err_code = json.loads(gzipData)['err_code']

	if err_code == 0:
		print '--- Block succeessful ---'
		writeLog(threadData, 'block')
		return True
	else:
		print '--- Block failed ---'
		print gzipData
		#exit for testing
		sys.exit(4)
		return False

# tieba admin user login
def adminLogin(username, password):
	print '--- Initializing ---'
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	urllib2.install_opener(opener)

	#Geting Cookie
	genericGet('http://www.baidu.com/')

	#Geting Token
	data = genericGet('https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&class=login')
	token = json.loads(data.replace('\'', '"'))['data']['token']

	print '--- Logining ---'
	postdata = {
		'token' : token,
		'tpl' : 'pp',
		'username' : username,
		'password' : password,
	}
	genericPost('https://passport.baidu.com/v2/api/?login', postdata)

	if 'BDUSS' in str(cj):
		print "--- Login succeessful ---"
		return True
	else:
		print "--- Login failed ---"
		return False

def writeLog(threadData, logType):
	logFile = open('log.txt', 'a')

	if logType == 'delete':
		logFile.write('{\n')
		logFile.write('    "type" : "delete",\n')
		logFile.write('    "data" : {\n')
		logFile.write('        "time" : "' + time.asctime() + '",\n')
		logFile.write('        "title" : "' + threadData['title'].encode('utf-8') + '",\n')
		logFile.write('        "author" : "' + threadData['author'].encode('utf-8') + '",\n')
		logFile.write('        "abstract" : "' + threadData['abstract'].encode('utf-8') + '",\n')
		logFile.write('    }\n')
		logFile.write('},\n')
	elif logType == 'block':
		logFile.write('{\n')
		logFile.write('    "type" : "block",\n')
		logFile.write('    "data" : {\n')
		logFile.write('        "time" : "' + time.asctime() + '",\n')
		logFile.write('        "author" : "' + threadData['author'].encode('utf-8') + '",\n')
		logFile.write('    }\n')
		logFile.write('},\n')

	logFile.close()

def judge(threadData):
	titleGrade   = 0
	previewGrade = 0

	preview = (u'None' if threadData['abstract'] == None else threadData['abstract'])
	# print keywords[1][0]
	for keyword in keywords:
		arr = re.findall(keyword[0], threadData['title'])
		if len(arr):
			titleGrade += len(arr) * keyword[1]

		arr = re.findall(keyword[0], preview)
		if len(arr):
			previewGrade += len(arr) * keyword[1]

	grade = titleGrade / len(threadData['title']) + previewGrade / len(preview) * 1.2

	return grade

def parseArgument():
	import argparse
	config = {}
	parser = argparse.ArgumentParser()

	parser.add_argument('choices', choices = ['run', 'config'], help = u'使用"run"来运行删帖机，使用"config"来生成一个配置文件')
	parser.add_argument('-c', help = u'json格式的配置文件名，若未给出则默认为tieba.json', dest = 'filename', default = 'tieba.json')
	parser.add_argument('-u', '--username', help = u'指定登陆的用户名')
	parser.add_argument('-p', '--password', help = u'密码，必须和上一项结合使用')
	parser.add_argument('-v', '--version', action = "version", help = u'显示版本信息并退出', version = '0.1')
	args = parser.parse_args()

	if args.choices == 'run':
		if args.username != None:
			config['username'] = args.username
			if args.password == None:
				print u'错误：未指定密码，-u选项必须和-p选项连用\n'
				parser.print_help()
				sys.exit(1)

			config['password'] = args.password
			config['type'] = 'argument'
		else:
			config['filename'] = args.filename
			config['type'] = 'json'
	else:
		config['type'] = 'config'

	return config

def configure():
	print u'请输入配置文件名'
	#Todo 根据用户的输入生成配置文件


def getConfigrations(config):
	print u'使用配置文件：' + config['filename'] + '...\n'
	

	try:
		f = file(config['filename'])
	except IOError, e:
		print u'无法打开配置文件，文件可能不存在'
		sys.exit(1)
	finally:
		pass
	jsonobj = json.load(f)
	f.close()

	if 'username' in jsonobj and 'password' in jsonobj:
		config['username'] = jsonobj['username']
		config['password'] = jsonobj['password']

	else:
		print u'无效的配置文件，请使用TiebaAutoTool.py config来生成配置文件'
		sys.exit(2)



def main(argv):
	grade = 0
	config = parseArgument()
	if config['type'] == 'config':
		configure()
		sys.exit(0)

	if config['type'] == 'json':
		getConfigrations(config)

	print u'使用用户名：' + config['username']

	isLogined = adminLogin(config['username'], config['password'])

	while(isLogined):
		deleteCount = 0
		data = genericGet('http://tieba.baidu.com/f?kw=c语言')

		# if there is a special utf-8 charactor in html that cannot decode to 'gbk' (eg. 🐶), 
		# there will be a error occured when you trying to print threadData['abstract'] to console

		html = data.decode('utf8').encode('gbk','replace').decode('gbk')
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

			#threadData['abstract'] maybe None, and this may cause a lot of problems!!!

			threadData['abstract'] = (u'None' if threadData['abstract'] == None else threadData['abstract'])
			if threadData['goodThread'] == 0 and threadData['topThread'] == 0:
				grade = judge(threadData)
				if grade > 6:
					# print type(threadData['abstract'])
					print u'------------------------------------------\n|作者：' + threadData['author']
					print u'\n|帖子标题：' + threadData['title'] 
					print u'\n|帖子预览：' + threadData['abstract']
					print u'\n|得分：%f' % grade
					print u'\n-------------------------------------------\n\n'
				# if any(word in threadData['title'] for word in keywords) or u'求' in threadData['title'][0] or ((threadData['abstract'] != None) and u'求' in threadData['abstract'][0]) \
				# or ((threadData['abstract'] != None) and any(word in threadData['abstract'] for word in keywords)):
					deleteCount += 1
					deleteThread(threadData)
					#blockID(threadData)
					time.sleep(5)

		print 'Front Page Checked: {0} Post Deleted'.format(deleteCount)

		if deleteCount == 0:
			print 'Waiting for more post...'
			time.sleep(60)

	return

if __name__ == '__main__':
	main(sys.argv[1:])
