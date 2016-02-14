# -*- coding: utf8 -*-
import argparse
import json
import re
import sys

from baiduOperation import webIOInitialization, getFid
from log import log

outputLOG = None

def initialization():
	global outputLOG

	outputLOG = log(['console', 'file'], 'STRING', 'DEFAULT')
	outputLOG.setOutputFile('log/console.log')

	outputLOG.log(u'初始化中...', 'INFO')

	outputLOG.log(u'配置初始化中...', 'INFO')
	config = _initConfig()
	outputLOG.log(u'配置初始化完毕', 'SUCCESS')

	outputLOG.log(u'网络初始化中...', 'INFO')
	webIOInitialization(config['configFilename'][:-5] + '.co')
	outputLOG.log(u'网络初始化完毕', 'SUCCESS')

	keywords = []
	postLOG = None
	if config['workingType'] == 'autoTool':
		outputLOG.log(u'关键词初始化中...', 'INFO')
		keywords = _initKeywords()
		outputLOG.log(u'关键词初始化完毕', 'SUCCESS')

		outputLOG.log(u'用户配置文件初始化中...', 'INFO')
		_initUserConfigration(config)
		outputLOG.log(u'用户配置文件初始化完毕', 'SUCCESS')

		postLOG = log(('file', 'cloud'), 'POST', key = config['apikey'])
		postLOG.setOutputFile('log/record.log')

	outputLOG.log(u'初始化完毕', 'SUCCESS')

	return [config, keywords, outputLOG, postLOG]

def _initConfig():
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

	_parseArgument(config)

	if config['debug']:
		outputLOG.setLevel('DEBUG')
		outputLOG.log(u'已启用调试模式', 'DEBUG')

	_getStdinCoding(config)
	outputLOG.log(u'输入编码为：' + config['stdincoding'], 'DEBUG')

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

def _initKeywords():
	keywords = _getKeywords()
	outputLOG.log(u'获取关键词成功', 'SUCCESS')
	_compileKeywords(keywords)
	outputLOG.log(u'编译关键词成功', 'SUCCESS')

	return keywords

def _getKeywords():
	try:
		with open('config/keywords.txt', 'r') as f:
			keywords = eval(f.read().decode('utf8'))
		return keywords
	except Exception as e:
		outputLOG.log(u'无法得到 keywords，文件可能不存在或者格式可能不对', 'ERROR')
		sys.exit(1)

def _compileKeywords(keywords):
	for i in range(len(keywords)):
		keywords[i].append(re.compile(keywords[i][0], re.I))

def _initUserConfigration(config):
	outputLOG.log(u'用户配置文件：%s' % config['configFilename'], 'INFO')
	_getUserConfigration(config)
	outputLOG.log(u'获取用户配置文件成功', 'SUCCESS')
	config['forum']['fid'] = getFid(config['forum'])
	outputLOG.log(u'获取贴吧fid成功', 'SUCCESS')
	outputLOG.log(u'使用用户名：%s' % config['user']['username'], 'INFO')
	outputLOG.log(u'管理贴吧：%s(%s)' % (config['forum']['kw'], config['forum']['fid']), 'INFO')
	if config['apikey']:
		outputLOG.log(u'使用apikey：%s' % config['apikey'], 'INFO')

def _getUserConfigration(config):
	try:
		with open(config['configFilename'], 'r') as f:
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
		print u'无法得到 config，文件可能不存在或者格式可能不对'
		sys.exit(1)
