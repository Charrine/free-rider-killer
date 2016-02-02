# -*- coding: utf8 -*-
import json
import os
import re
import sys
import time

from webIO import *

reload(sys)
sys.setdefaultencoding( "utf-8" )

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

	parser = argparse.ArgumentParser()

	#TODO: forum
	#TODO: how to set default for choices
	parser.add_argument('workingType', choices = ['run', 'config-user', 'config-cookie'], help = u'使用 "run" 来运行删帖机，使用 "config-user" 来生成一个用户配置文件，使用 "config-cookie" 来生成一个 cookie 配置文件', default = u'run')
	parser.add_argument('-l', '--login-type',     help = u'使用 argument 来登陆，使用 json 来登陆，使用 cookie 来登陆', dest = 'loginType', default = u'json')#choices = ['argument', 'json', 'cookie'],
	parser.add_argument('-c', '--user-path',     help = u'json 格式的 user 配置文件的路径，若未给出则默认为default.json', dest = 'userFilename', default = 'default.json')
	parser.add_argument('-k', '--cookie-path',   help = u'cookie 文件的路径，若未给出则默认为cookie.txt', dest = 'cookieFilename', default = 'cookie.txt')
	parser.add_argument('-u',  '--username',      help = u'指定登陆的用户名')
	parser.add_argument('-p',  '--password',      help = u'密码，必须和上一项结合使用')
	#parser.add_argument('-f',  '--forum'          help = u'贴吧名，不包含‘吧’', default = u'c语言')
	parser.add_argument('-d',  '--debug' ,        help = u'调试模式，只对页面进行检测，而不会发送删帖/封禁请求', action = "store_true")
	parser.add_argument('-v',  '--version' ,      help = u'显示版本信息并退出', action = "version", version = '0.1')
	args = parser.parse_args()

	if args.workingType == 'run':
		config['workingType'] = 'autoDelete'
		if args.loginType == 'argument':
			config['loginType']['type'] = 'argument'
			if args.username != None and args.password != None:
				config['user']['username'] = args.username.decode(config['stdincoding'])
				config['user']['password'] = args.password
			else:
				print u'错误：未指定用户名或者密码，-u选项必须和-p选项连用\n'
				parser.print_help()
				sys.exit(1)
		elif args.loginType == 'json':
			config['loginType']['type'] = 'json'
			config['loginType']['filename'] = args.userFilename
		elif args.loginType == 'cookie':
			config['loginType']['type'] = 'cookie'
			config['loginType']['filename'] = args.cookieFilename
		else:
			print u'错误：错误参数\n'
			parser.print_help()
			sys.exit(1)
	elif args.workingType == 'config-user':
		config['workingType'] = 'configUser'
	elif args.workingType == 'config-cookie':
		config['workingType'] = 'configCookie'

	#config['forum']['kw'] = args.forum
	#config['forum']['fid'] = getFid(config['forum']['kw'])

	if args.debug:
		config['workingMode'] = 'debug'
		print u'调试模式已开启！'

	return

def configureUser():
	import getpass

	print u'请输入配置文件的文件名(按回车使用默认文件):',
	filename = raw_input()
	if filename == '':
		filename = 'default.json'
		print u'使用默认配置文件default.json'
	else:
		print u'-----将使用:%s -----' %(filename)

	if os.path.exists(filename):
		print u'文件已存在，本操作将覆盖此文件，是否继续？(y继续操作)'
		inputs = raw_input()
		if inputs != 'y' and inputs != 'Y':
			print u'已取消'
			sys.exit(0)

	isLogined = False
	while isLogined == False:
		print u'请输入用户名:',
		config['user']['username'] = raw_input()

		print u'请输入密码（无回显）',
		config['user']['password'] = getpass.getpass(':')

		print u'-----登陆测试-----'
		if config['workingMode'] != 'debug':
			isLogined = adminLogin(config['user'])
			if isLogined == False:
				print u'登陆失败...按q可退出,回车继续尝试'
				inputs = raw_input()
				if inputs == 'q' or inputs == 'Q':
					print u'程序退出，未作出任何更改...'
					sys.exit(0)
			else:
				print u'-----登陆成功！-----'
		else:
			isLogined = True
			print u'\n因调试而跳过登陆验证\n'

	config['user']['username'] = config['user']['username'].decode(config['stdincoding'])
	with open(filename, "w") as configfile:
		configfile.write('{\n')
		configfile.write('    "username" : "' + config['user']['username'].encode('utf8') + '",\n')
		configfile.write('    "password" : "' + config['user']['password'] + '",\n')
		configfile.write('}')
	print u'-----写入成功-----'
	print u'请使用python2 TiebaAutoTool.py run -c %s 来使用本配置运行' % config['filename']

def configureCookie():
	import getpass

	print u'请输入 cookie 文件的文件名(按回车使用默认文件):',
	filename = raw_input()
	if filename == '':
		filename = 'cookie.txt'
		print u'使用默认配置文件cookie.txt'
	else:
		print u'-----将使用:%s -----' %(filename)

	if os.path.exists(filename):
		print u'文件已存在，本操作将覆盖此文件，是否继续？(y继续操作)'
		inputs = raw_input()
		if inputs != 'y' and inputs != 'Y':
			print u'已取消'
			sys.exit(0)

	isLogined = False
	while isLogined == False:
		print u'请输入用户名:',
		config['user']['username'] = raw_input()

		print u'请输入密码（无回显）',
		config['user']['password'] = getpass.getpass(':')

		print u'-----登陆测试-----'
		if config['workingMode'] != 'debug':
			isLogined = adminLogin(config['user'])
			if isLogined == False:
				print u'登陆失败...按q可退出,回车继续尝试'
				inputs = raw_input()
				if inputs == 'q' or inputs == 'Q':
					print u'程序退出，未作出任何更改...'
					sys.exit(0)
			else:
				print u'-----登陆成功！-----'
		else:
			isLogined = True
			print u'\n因调试而跳过登陆验证\n'

	saveCookie(filename)

	return

def autoDelete():
	deleteCount = 0
	while(True):
		try:
			threadDataList = getThreadDataList(config['forum'])

			for threadData in threadDataList:
				if threadData['goodThread'] == 0 and threadData['topThread'] == 0:
					grade = judge(threadData)
					if grade > 6:
						print u'------------------------------------------\n|作者：' + threadData['author']
						print u'\n|帖子标题：' + threadData['title'] 
						print u'\n|帖子预览：' + threadData['abstract']
						print u'\n|得分：%f' % grade
						print u'\n-------------------------------------------\n\n'

						if config['workingMode'] != 'debug':
							deleteThread(threadData, config['forum'])
						#blockID(threadData, config['forum'])
						deleteCount += 1
						time.sleep(5)
		except Exception, e:
			print e
			logFile = open('error.log', 'a')
			logFile.write(time.asctime() + '\n')
			logFile.write(str(e) + '\n\n')
			logFile.close()
			time.sleep(10)
		else:
			if deleteCount != 0:
				print 'Front Page Checked: {0} Post Deleted'.format(deleteCount)
			print 'Waiting for more post...'
			time.sleep(60)
			deleteCount = 0

	return

def main():
	if config['workingType'] == 'configUser':
		configureUser()
	elif config['workingType'] == 'configCookie':
		configureCookie()
	elif config['workingType'] == 'autoDelete':
		print u'使用用户名：' + config['user']['username']
		isLogined = adminLogin(config['user'])
		if isLogined:
			autoDelete()
		else:
			sys.exit(1)

	return

# do some initialization work
def init():
	global config 
	config = {
		'user' : {
			'username' : 'username',
			'password' : 'password'
		},
		'forum' : {
			'kw' : 'c语言',
			'fid' : 22545
		},
		'workingMode' : 'normal',
		'workingType' : 'autoDelete',
		'loginType' : {
			'type' : 'none',
			'filename' : ''
		},
		'stdincoding' : 'utf8'
	}

	if sys.stdin.encoding == 'cp936':
		config['stdincoding'] = 'gbk'
	else:
		config['stdincoding'] = 'utf8'

	parseArgument()

	print '--- Initializing ---'
	webIOInitialization()
	if config['workingType'] == 'autoDelete':
		getKeywords()
		if config['loginType']['type'] == 'json':
			getUserConfigration()
		elif config['loginType']['type'] == 'cookie':
			getCookie()

	return

def getUserConfigration():
	print u'使用配置文件：' + config['loginType']['filename'] + '...\n'

	try:
		f = file(config['loginType']['filename'])
	except IOError, e:
		print u'无法打开配置文件，文件可能不存在'
		sys.exit(1)
	else:
		try:
			jsonObj = json.load(f)
		except Exception, e:
			print u'无法解析配置文件，文件格式可能不对'
			sys.exit(1)
		else:
			if 'username' in jsonObj and 'password' in jsonObj:
				config['user']['username'] = jsonObj['username']
				config['user']['password'] = jsonObj['password']
			else:
				print u'无效的配置文件，请使用 TiebaAutoTool.py user-config 来生成配置文件'
				sys.exit(1)
	finally:
		f.close()

	return

def getCookie():
	loadCookie(config['loginType'])

	return

def getKeywords():
	try:
		f = file('keywords.conf')
	except IOError, e:
		print u'无法打开 keywords 配置文件，文件可能不存在'
		sys.exit(1)
	else:
		try:
			global keywords
			keywords = json.load(f)
		except Exception, e:
			print u'无法解析配置文件，文件格式可能不对'
			sys.exit(1)
	finally:
		f.close()

	return

if __name__ == '__main__':
	init()
	main()