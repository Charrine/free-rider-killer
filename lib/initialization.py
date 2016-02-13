# -*- coding: utf8 -*-
import json
import sys

from lib.webIO import *
from lib.log import log

def initialization():
	global config
	global outputLOG
	global postLOG
	global keywords

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
		'configFilename' : 'config/default.json',
		'stdincoding' : 'utf8',
		'loglevel':'DEFAULT'
	}
	outputLOG = log(['console', 'file'], 'STRING', config['loglevel'])
	outputLOG.setOutputFile('config/log.log')
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
		outputLOG.log(u'编译关键词中...', 'INFO')
		compileKeywords(keywords)
		outputLOG.log(u'编译成功', 'INFO')

		outputLOG.log(u'获取配置文件：%s ...' %config['configFilename'], 'INFO')
		getUserConfigration()
		outputLOG.log(u'获取贴吧fid', 'DEBUG')
		config['forum']['fid'] = getFid(config['forum'])
		outputLOG.log(u'使用用户名： ' + config['user']['username'], 'INFO')
		outputLOG.log(u'管理贴吧： ' + config['forum']['kw'] + u'(' + config['forum']['fid'] + u')', 'INFO')

		postLOG = log(('file', 'cloud'), 'POST', key = config['apikey'])
		postLOG.setOutputFile('log/history.log')
		outputLOG.log(u'使用apikey:' + config['apikey'])
		outputLOG.log(u'初始化完毕', 'SUCCESS')

	return {
		'config' : config,
		'outputLOG' : outputLOG,
		'postLOG' : postLOG,
		'keywords' : keywords
	}

def getUserConfigration():
	try:
		with open(config['configFilename'], 'r') as f:
			jsonObj = json.load(f)
			# print type(jsonObj)
			# if all(x in jsonObj for x in ['username', 'password', 'kw', 'apikey'])
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
		with open('config/keywords.txt', 'r') as f:
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

def parseArgument():
	import argparse

	parser = argparse.ArgumentParser()

	parser.add_argument('workingType', choices = ['run', 'config'], help = u'使用 "run" 来运行删帖机，使用 "config" 来生成一个用户配置文件')
	parser.add_argument('-c', '--configfile', help = u'json 格式的 user 配置文件的路径，若未给出则默认为config/default.json', dest = 'configFilename', default = 'config/default.json')
	parser.add_argument('-d', '--debug' ,     help = u'添加此参数即开启调试模式，删贴机将只对页面进行检测，而不会发送删帖/封禁请求', action = "store_true")
	parser.add_argument('-v', '--version' ,   help = u'显示此版本信息并退出', action = "version", version = '1.0')
	args = parser.parse_args()

	if args.workingType == 'run':
		config['workingType'] = 'autoTool'
		config['configFilename'] = args.configFilename
	else:
		config['workingType'] = 'config'

	config['debug'] = args.debug

	return

def compileKeywords(keywords):
	for i in range(len(keywords)):
		keywords[i].append(re.compile(keywords[i][0],re.I))
