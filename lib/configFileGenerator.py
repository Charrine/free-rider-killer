# -*- coding: utf8 -*-
import getpass
import os
import sys

from lib.webIO import adminLogin

def configFileGenerator(config):
	print u'请输入配置文件的文件名（按回车使用默认文件）：',
	filename = raw_input()
	if filename == '':
		filename = 'config/default.json'
		print u'使用默认配置文件config/default.json'
	else:
		filename = 'config/' + filename
		print u'-----将使用：%s-----' % filename

	if os.path.exists(filename):
		print u'文件已存在，本操作将覆盖此文件，是否继续？（y继续操作）：',
		inputs = raw_input()
		if inputs not in ['y', 'Y']:
			print u'已取消'
			sys.exit(0)

	isLogined = False
	while not isLogined:
		print u'请输入用户名：',
		config['user']['username'] = raw_input().decode(config['stdincoding'])
		print u'请输入密码（无回显）',
		config['user']['password'] = getpass.getpass(u'：')

		print u'-----登陆测试-----'
		if not config['debug']:
			isLogined = adminLogin(config['user'])
			if not isLogined:
				print u'-----登陆失败-----\n按q可退出,回车继续尝试：',
				inputs = raw_input()
				if inputs in ['q', 'Q']:
					print u'程序退出，未作出任何更改...'
					sys.exit(0)
			else:
				print u'-----登陆成功！-----'
		else:
			isLogined = True
			print u'\n因调试而跳过登陆验证\n'
	print u'请输入贴吧名（不带‘吧’，如c语言吧则输入‘c语言’）：',
	config['forum']['kw'] = raw_input().decode(config['stdincoding'])

	print u'请输入API key：(若没有请按回车)',
	config['apikey'] = raw_input()

	print u'-----------------'
	print u'请检查输入的信息是否正确'
	print u'使用用户名：' + config['user']['username']
	print u'密码：' + '*' * len(config['user']['password'])
	print u'管理贴吧：' + config['forum']['kw']
	if config['apikey']:
		print u'API key：' + config['apikey']
	print u'输入yes将会写入用户配置文件：'
	inputs = raw_input()

	if inputs == 'yes':
		with open(filename, 'w') as configfile:
			configfile.write('{\n')
			configfile.write('	"username" : "' + config['user']['username'].encode('utf8') + '",\n')
			configfile.write('	"password" : "' + config['user']['password'] + '",\n')
			configfile.write('	"kw" : "' + config['forum']['kw'].encode('utf8') + '",\n')
			configfile.write('	"apikey" : "' + config['apikey'] + '"\n')
			configfile.write('}')
		print u'-----写入成功-----'
		if filename == 'config/default.json':
			print u'请使用 python2 TiebaAutoTool.py run 来使用本配置运行'
		else:
			print u'请使用 python2 TiebaAutoTool.py run -c %s 来使用本配置运行' % filename
	else:
		print u'已取消，未做任何更改'
