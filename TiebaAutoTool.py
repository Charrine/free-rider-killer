# -*- coding: utf8 -*-
import getpass
import json
import os
import re
import sys
import time
from bar import *
from webIO import *
from log import log
reload(sys)
sys.setdefaultencoding( "utf-8" )

config = {}

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

	parser.add_argument('workingType', choices = ['run', 'config'], help = u'使用 "run" 来运行删帖机，使用 "config" 来生成一个用户配置文件')
	parser.add_argument('-c', '--configfile', help = u'json 格式的 user 配置文件的路径，若未给出则默认为default.json', dest = 'configFilename', default = 'default.json')
	parser.add_argument('-d', '--debug' ,     help = u'添加此参数即开启调试模式，删贴机将只对页面进行检测，而不会发送删帖/封禁请求', action = "store_true")
	parser.add_argument('-v', '--version' ,   help = u'显示版本信息并退出', action = "version", version = '0.1')
	args = parser.parse_args()

	if args.workingType == 'run':
		config['workingType'] = 'autoTool'
		config['configFilename'] = args.configFilename
	else:
		config['workingType'] = 'config'

	config['debug'] = args.debug

	return

def configFileGenerator():
	print u'请输入配置文件的文件名（按回车使用默认文件）: ',
	filename = raw_input()
	if filename == '':
		filename = 'default.json'
		print u'使用默认配置文件default.json'
	else:
		print u'-----将使用: %s-----' % filename

	if os.path.exists(filename):
		print u'文件已存在，本操作将覆盖此文件，是否继续？（y继续操作）: ',
		inputs = raw_input()
		if inputs not in ['y', 'Y']:
			print u'已取消'
			sys.exit(0)

	isLogined = False
	while not isLogined:
		print u'请输入用户名: ',
		config['user']['username'] = raw_input().decode(config['stdincoding'])
		print u'请输入密码（无回显）',
		config['user']['password'] = getpass.getpass(':')

		print u'-----登陆测试-----'
		if not config['debug']:
			isLogined = adminLogin(config['user'])
			if not isLogined:
				print u'-----登陆失败-----\n按q可退出,回车继续尝试: ',
				inputs = raw_input()
				if inputs in ['q', 'Q']:
					print u'程序退出，未作出任何更改...'
					sys.exit(0)
			else:
				print u'-----登陆成功！-----'
		else:
			isLogined = True
			print u'\n因调试而跳过登陆验证\n'
	print u'请输入贴吧名（不带‘吧’，如c语言吧则输入‘c语言’）: ',
	config['forum']['kw'] = raw_input().decode(config['stdincoding'])

	print u'请输入API key：',
	config['apikey'] = raw_input()

	print u'-----------------\n请检查输入的信息是否正确'
	print u'使用用户名：{0}\n密码：{1}\n管理贴吧：{2}'.format(config['user']['username'],\
		'*' * len(config['user']['password']), config['forum']['kw'])
	print 'API key:' + config['apikey']
	print u'输入yes将会写入用户配置文件: '
	inputs = raw_input()

	if inputs == 'yes':
		with open(filename, 'w') as configfile:
			configfile.write('{\n')
			configfile.write('    "username" : "' + config['user']['username'].encode('utf8') + '",\n')
			configfile.write('    "password" : "' + config['user']['password'] + '",\n')
			configfile.write('    "kw" : "' + config['forum']['kw'].encode('utf8') + '",\n')
			configfile.write('    "apikey" : "' + config['apikey'] + '"\n')
			configfile.write('}')
		print u'-----写入成功-----'
		print u'请使用python2 TiebaAutoTool.py run -c %s 来使用本配置运行' % filename
	else:
		print u'已取消，未做任何更改'

	return

def autoDelete():
	deleteCount = 0
	while(True):
		# try:
			outputLOG.log(u'获取首页...', 'INFO')
			threadDataList = getThreadDataList(config['forum'])

			for threadData in threadDataList:
				if threadData['goodThread'] == 0 and threadData['topThread'] == 0:
					threadData['grade'] = judge(threadData)
					if threadData['grade'] > 6:
						postLOG.PrintPost(threadData)

						if not config['debug']:
							outputLOG.log(u'正在删除帖子', 'INFO')
							if deleteThread(threadData, config['forum']):							
								outputLOG(u'删除成功', 'SUCCESS')
								postLOG.log(threadData)
								deleteCount += 1
							else:
								outputLOG.log(u'删除失败', 'ERROR')
							sleep(5)
						else:
							print u'请确认是否删除（按y删除）:',
							if raw_input() == 'y':
								outputLOG.log(u'已确认删除帖子...', 'DEBUG')
								outputLOG.log(u'正在删除', 'INFO')
								if deleteThread(threadData, config['forum']):
									outputLOG.log(u'删除成功', 'SUCCESS')
									postLOG.log(threadData)
									deleteCount += 1
								else:
									outputLOG.log(u'删除失败', 'ERROR')
							else:
								outputLOG.log(u'跳过删帖', 'DEBUG')

						

		# except Exception, e:
		# 	print e
		# 	logFile = open('error.log', 'a')
		# 	logFile.write(time.asctime() + '\n')
		# 	logFile.write(str(e) + '\n\n')
		# 	logFile.close()
		# 	time.sleep(10)
		# else:
			if deleteCount != 0:
				outputLOG.log(u'已检查首页: 已删除{0} 个帖子'.format(deleteCount), 'INFO')
			else:
				outputLOG(u'等待更多新帖...', 'INFO')
				sleep(60)
			deleteCount = 0

	return


def main():
	if config['workingType'] == 'config':
		configFileGenerator()
	elif config['workingType'] == 'autoTool':
		isLogined = adminLogin(config['user'], config['configFilename'][:-5] + '.co')
		if isLogined:
			outputLOG.log(u'登陆成功', 'SUCCESS')
			autoDelete()
		else:
			outputLOG.log(u'登陆失败', 'ERROR')
			sys.exit(1)
	return

def init():
	global config
	global outputLOG
	global postLOG
	postLOG = log('file', 'POST')
	postLOG.setOutputFile('history.log')
	config = {
		'user' : {
			'username' : 'username',
			'password' : 'password'
		},
		'forum' : {
			'kw' : u'c语言',
			'fid' : 22545
		},
		'debug' : False,
		'workingType' : 'autoTool',
		'configFilename' : 'default.json',
		'stdincoding' : 'utf8',
		'loglevel':'DEFAULT'
	}
	outputLOG = log(['console', 'file'], 'STRING', config['loglevel'])
	outputLOG.setOutputFile('log.log')
	parseArgument()
	if config['debug']:
		outputLOG.setLevel('DEBUG')
		outputLOG.log(u'已启用调试模式', 'DEBUG')


	outputLOG.log(u'初始化中...', 'INFO')
	outputLOG.log(u'获取输入编码', 'DEBUG')
	getStdinCoding()
	outputLOG.log(u'输入编码为：' + config['stdincoding'], 'DEBUG')
	outputLOG.log(u'网络初始化中', 'INFO')
	webIOInitialization(config['configFilename'][:-5] + '.co')
	outputLOG.log(u'网络初始化完毕', 'SUCCESS')

	if config['workingType'] == 'autoTool':
		outputLOG.log(u'获取关键词中', 'INFO')
		getKeywords()
		outputLOG.log(u'获取关键词成功', 'SUCCESS')
		outputLOG.log(u'获取配置文件：%s ...' %config['configFilename'], 'INFO')
		getUserConfigration()
		outputLOG.log(u'获取贴吧fid', 'DEBUG')
		config['forum']['fid'] = getFid(config['forum'])
		outputLOG.log(u'使用用户名： ' + config['user']['username'], 'INFO')
		outputLOG.log(u'管理贴吧： ' + config['forum']['kw'] + u'(' + config['forum']['fid'] + u')', 'INFO')
	outputLOG.log(u'初始化完毕', 'SUCCESS')
	return

def getUserConfigration():
	try:
		with open(config['configFilename'], 'r') as f:
			jsonObj = json.load(f)
			if 'username' in jsonObj and 'password' in jsonObj and 'kw' in jsonObj and 'apikey' in jsonObj:
				config['user']['username'] = jsonObj['username'].decode('utf8')
				config['user']['password'] = jsonObj['password'].decode('utf8')
				config['forum']['kw']      = jsonObj['kw'].decode('utf8')
				config['apikey']           = jsonObj['apikey']
			else:
				print u'无效的配置文件，请使用 TiebaAutoTool.py config 来生成配置文件'
				sys.exit(1)
	except Exception as e:
		print u'无法得到 config，文件可能不存在或者格式可能不对'
		sys.exit(1)

	return

def getKeywords():
	global keywords
	try:
		with open('keywords.txt', 'r') as f:
			keywords = eval(f.read().decode('utf8'))
	except Exception as e:
		outputLOG.log(u'无法得到 keywords，文件可能不存在或者格式可能不对', 'ERROR')
		sys.exit(1)
	return

def getStdinCoding():

	if sys.stdin.encoding == 'cp936':
		config['stdincoding'] = 'gbk'
	else:
		config['stdincoding'] = 'utf8'
	return

if __name__ == '__main__':
	init()
	main()
