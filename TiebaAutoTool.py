# -*- coding: utf8 -*-
import getpass
import json
import os
import re
import sys
import time
from bar import *
from webIO import *

reload(sys)
sys.setdefaultencoding( "utf-8" )

def judge(threadData):
	titleGrade   = 0
	previewGrade = 0

	preview = (u'None' if threadData['abstract'] == None else threadData['abstract'])
	for keyword in keywords:
		arr = re.findall(keyword[0], threadData['title'])
		if len(arr):
			titleGrade += len(arr) * keyword[1]

		arr = re.findall(keyword[0], preview)
		if len(arr):
			previewGrade += len(arr) * keyword[1]

	grade = float(titleGrade) / len(threadData['title']) + float(previewGrade) / len(preview) * 1.1

	return grade

def parseArgument():
	import argparse

	parser = argparse.ArgumentParser()

	parser.add_argument('workingType', choices = ['run', 'config'], help = u'使用 "run" 来运行删帖机，使用 "config" 来生成一个用户配置文件', default = 'run')
	parser.add_argument('-c', '--configfile',      help = u'json 格式的 user 配置文件的路径，若未给出则默认为default.json', dest = 'configFilename', default = 'default.json')
	parser.add_argument('-d',  '--debug' ,        help = u'添加此参数即开启调试模式，删贴机将只对页面进行检测，而不会发送删帖/封禁请求', action = "store_true")
	parser.add_argument('-v',  '--version' ,      help = u'显示版本信息并退出', action = "version", version = '0.1')
	args = parser.parse_args()


	if args.workingType == 'run':
		config['workingType'] = 'autoTool'
		config['configFilename'] = args.configFilename
	else:
		config['workingType'] = 'config'

	config['debug'] = args.debug

	return

def configFileGenerator():
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
		if inputs not in ['y', 'Y']:
			print u'已取消'
			sys.exit(0)

	isLogined = False
	while isLogined == False:
		print u'请输入用户名:',
		config['user']['username'] = raw_input()

		print u'请输入密码（无回显）',
		config['user']['password'] = getpass.getpass(':')

		print u'-----登陆测试-----'
		if not config['debug']:

			isLogined = adminLogin(config['user'])
			if isLogined == False:
				print u'登陆失败...按q可退出,回车继续尝试'
				inputs = raw_input()
				if inputs in ['q', 'Q']:
					print u'程序退出，未作出任何更改...'
					sys.exit(0)
			else:
				print u'-----登陆成功！-----'
		else:
			isLogined = True
			print u'\n因调试而跳过登陆验证\n'

	print u'请输入贴吧名（不带‘吧’，如c语言吧则输入‘c语言’）'
	config['forum']['kw'] = raw_input()

	# decode into unicode
	config['user']['username'] = config['user']['username'].decode(config['stdincoding'])
	config['forum']['kw']      = config['forum']['kw'].decode(config['stdincoding'])
	print u'-----------------\n请检查输入的信息是否正确'
	print u'使用用户名：{0}\n密码：{1}\n管理贴吧{2}\n输入yes将会写入用户配置文件:'.format(config['user']['username'], '*'*len(config['user']['password']), config['forum']['kw']), 
	inputs = raw_input()

	if inputs == 'yes':
		with open(filename, "w") as configfile:
			configfile.write('{\n')
			configfile.write('    "username" : "' + config['user']['username'].encode('utf8') + '",\n')
			configfile.write('    "password" : "' + config['user']['password'] + '",\n')
			configfile.write('    "kw" : "' + config['forum']['kw'].encode('utf8') + '",\n')
			configfile.write('}')
		print u'-----写入成功-----'
		print u'请使用python2 TiebaAutoTool.py run -c %s 来使用本配置运行' % config['configFilename']

	else:
		print u'已取消，未做任何更改'
	return


def autoDelete():
	deleteCount = 0
	while(True):
		try:
			print u'获取首页...'
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


						if not config['debug']:
							deleteThread(threadData, config['forum'])
							deleteCount += 1
							sleep(5)

						else:
							print u'请确认是否删除（按y删除）：',
							if raw_input() == 'y':
								deleteThread(threadData, config['forum'])
								deleteCount += 1				
							else:
								print u'因为调试跳过删帖'

						#blockID(threadData, config['forum'])
						
						
		except Exception, e:
			print e
			logFile = open('error.log', 'a')
			logFile.write(time.asctime() + '\n')
			logFile.write(str(e) + '\n\n')
			logFile.close()
			time.sleep(10)
		else:
			if deleteCount != 0:
				print u'已检查首页: 已删除{0} 个帖子'.format(deleteCount)
			else:
				print u'等待更多新帖...'
				sleep(60)
			deleteCount = 0

	return


def main():
	if config['workingType'] == 'config':
		configFileGenerator()
	elif config['workingType'] == 'autoTool':
		print u'使用用户名：' + config['user']['username']
		isLogined = adminLogin(config['user'])
		if isLogined:
			autoDelete()
		else:
			print u'登陆失败'
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
		'debug' : False,
		'workingType' : 'autoTool',
		'configFilename' : 'default.json',
		'stdincoding' : 'utf8'
	}
	getStdinCoding(config)
	parseArgument()
	webIOInitialization()
	if config['debug']:
		print u'调试已开启'
	
	if config['workingType'] == 'autoTool':
		getKeywords()
		getUserConfigration()
		config['forum']['fid'] = getFid(config['forum'])
		print config['forum']['fid']
	return

def getUserConfigration():
	print u'使用配置文件：' + config['configFilename']+ '...\n'

	try:
		f = file(config['configFilename'])
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
			if 'username' in jsonObj and 'password' in jsonObj and 'kw' in jsonObj:
				config['user']['username'] = jsonObj['username'].decode('utf8')
				config['user']['password'] = jsonObj['password'].decode('utf8')
				config['forum']['kw']      = jsonObj['kw'].decode('utf8')

			else:
				print u'无效的配置文件，请使用 TiebaAutoTool.py config 来生成配置文件'
				sys.exit(1)
	finally:
		f.close()

	return

def getCookie():
	loadCookie(config['loginType'])
	return

def getKeywords():
	print u'获取关键词...'
	global keywords
	try:
		f = file('keywords.txt')
	except IOError, e:
		print u'无法打开 keywords 配置文件，文件可能不存在'
		sys.exit(1)
	else:
		try:
			
			keywords = eval(f.read().decode('utf8'))
		except Exception, e:
			print u'无法解析配置文件，文件格式可能不对'
			sys.exit(1)
	finally:
		f.close()

	return

def getStdinCoding(config):
	if sys.stdin.encoding == 'cp936':
		config['stdincoding'] = 'gbk'
	else:
		config['stdincoding'] = 'utf8'

if __name__ == '__main__':
	init()
	main()