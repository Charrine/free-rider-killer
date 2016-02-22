# -*- coding: utf8 -*-
import argparse
import json
import re
import sys

from baiduOperation import webIOInitialization, getFid
from stdlog import logInitialization, stdLog, errLog, setStdLevel

def initialization():
	logInitialization()
	stdLog(u'初始化中...', 'info')

	stdLog(u'配置初始化中...', 'info')
	config = _initConfig()
	stdLog(u'配置初始化完毕', 'success')

	stdLog(u'网络初始化中...', 'info')
	webIOInitialization(config['configFilename'][:-5] + '.co')
	stdLog(u'网络初始化完毕', 'success')

	if config['workingType'] == 'autoTool':
		stdLog(u'关键词初始化中...', 'info')
		keywords = initKeywords()
		stdLog(u'关键词初始化完毕', 'success')

		stdLog(u'用户配置文件初始化中...', 'info')
		_initUserConfigration(config)
		stdLog(u'用户配置文件初始化完毕', 'success')

	stdLog(u'初始化完毕', 'success')

	return [config, keywords]

def _initConfig():
	config = {
		'user': {
			'username': 'username',
			'password': 'password'
		},
		'forum': {
			'kw': u'c语言',
			'fid': 22545
		},
		'debug': False,
		'workingType': 'autoTool',
		'configFilename': 'config/default.json',
		'stdincoding': 'utf8'
	}

	_parseArgument(config)

	if config['debug']:
		setStdLevel('debug')
		stdLog(u'已启用调试模式', 'debug')

	_getStdinCoding(config)
	stdLog(u'输入编码为：' + config['stdincoding'], 'debug')

	return config

def _parseArgument(config):
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

def _getStdinCoding(config):
	if sys.stdin.encoding == 'cp936':
		config['stdincoding'] = 'gbk'
	else:
		config['stdincoding'] = 'utf8'

def initKeywords():
	keywords = _getKeywords()
	stdLog(u'获取关键词成功', 'success')
	_compileKeywords(keywords)
	stdLog(u'编译关键词成功', 'success')

	return keywords

def _getKeywords():
	try:
		f = open('config/keywords.txt', 'r')
		try:
			keywords = eval(f.read().decode('utf8'))
		except Exception as e:
			errLog(300, pause = False)
			sys.exit(1)
	except Exception as e:
		errLog(200, pause = False)
		sys.exit(1)

	return keywords

def _compileKeywords(keywords):
	for i in range(len(keywords)):
		keywords[i].append(re.compile(keywords[i][0], re.I))

def _initUserConfigration(config):
	stdLog(u'用户配置文件：%s' % config['configFilename'], 'info')
	_getUserConfigration(config)
	stdLog(u'获取用户配置文件成功', 'success')
	config['forum']['fid'] = getFid(config['forum'])
	stdLog(u'获取贴吧fid成功', 'success')
	stdLog(u'使用用户名：%s' % config['user']['username'], 'info')
	stdLog(u'管理贴吧：%s(%s)' % (config['forum']['kw'], config['forum']['fid']), 'info')
	if config['apikey']:
		stdLog(u'使用apikey：%s' % config['apikey'], 'info')

def _getUserConfigration(config):
	try:
		f = open(config['configFilename'], 'r')
		try:
			jsonObj = json.load(f)
			if ['apikey', 'kw', 'password', 'username'] == sorted(jsonObj.keys()):
				config['user']['username'] = jsonObj['username'].decode('utf8')
				config['user']['password'] = jsonObj['password'].decode('utf8')
				config['forum']['kw']      = jsonObj['kw'].decode('utf8')
				config['apikey']           = jsonObj['apikey'].decode('utf8')
			else:
				print u'无效的配置文件，请使用 TiebaAutoTool.py config 来生成配置文件'
				sys.exit(1)
		except Exception as e:
			errLog(300, pause = False)
			sys.exit(1)
	except Exception as e:
		errLog(200, pause = False)
		sys.exit(1)
