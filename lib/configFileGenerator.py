# -*- coding: utf8 -*-
import getpass
import os
import sys

from baiduOperation import adminLogin
from stdlog import stdLog, errLog

def configFileGenerator(config):
	stdLog(u'启动配置文件生成工具', 'info')

	stdLog(u'请输入配置文件的文件名（按回车使用默认文件）：', 'info', ('console'), '')
	filename = raw_input()
	if filename == '':
		filename = 'config/default.json'
	else:
		filename = 'config/' + filename
	stdLog(u'使用配置文件 ' + filename, 'info', ('console'))

	while os.path.exists(filename):
		stdLog(u'文件已存在，本操作将覆盖此文件，是否继续？（y/n）：', 'info', ('console'), '')
		choose = raw_input()
		if choose in ['n', 'N']:
			stdLog(u'已取消', 'info', ('console'))
			sys.exit(0)
		elif choose in ['y', 'Y']:
			break

	while True:
		stdLog(u'请输入用户名：', 'info', ('console'), '')
		config['user']['username'] = raw_input().decode(config['stdincoding'])
		stdLog(u'请输入密码（无回显）', 'info', ('console'), '')
		config['user']['password'] = getpass.getpass(':')

		stdLog(u'登陆测试', 'info', ('console'))
		if not config['debug']:
			if adminLogin(config['user'], config = True):
				stdLog(u'登陆成功', 'success', ('console'))
				break
			else:
				stdLog(u'登陆失败', 'error', ('console'))
				while True:
					stdLog(u'是否继续尝试？（y/n）：', 'info', ('console'), '')
					choose = raw_input()
					if choose in ['n', 'N']:
						stdLog(u'程序退出，未作出任何更改', 'info', ('console'))
						sys.exit(0)
					elif choose in ['y', 'Y']:
						break
		else:
			stdLog(u'因调试而跳过登陆验证', 'debug', ('console'))
			break

	stdLog(u'请输入贴吧名（不带‘吧’，如c语言吧则输入‘c语言’）：', 'info', ('console'), '')
	config['forum']['kw'] = raw_input().decode(config['stdincoding'])
	stdLog(u'请输入API key(若没有请按回车)：', 'info', ('console'), '')
	config['apikey'] = raw_input()

	stdLog(u'-----------------', 'info', ('console'))
	stdLog(u'使用用户名：' + config['user']['username'], 'info', ('console'))
	stdLog(u'密码：' + '*' * len(config['user']['password']), 'info', ('console'))
	stdLog(u'管理贴吧：' + config['forum']['kw'], 'info', ('console'))
	if config['apikey']:
		stdLog(u'API key：' + config['apikey'], 'info', ('console'))
	while True:
		stdLog(u'请检查输入的信息是否正确？（y/n）：', 'info', ('console'), '')
		choose = raw_input()
		if choose in ['n', 'N']:
			stdLog(u'程序退出，未作出任何更改', 'info', ('console'))
			sys.exit(0)
		elif choose in ['y', 'Y']:
			try:
				f = open(filename, 'w')
				f.write('{\n')
				f.write('	"username": "' + config['user']['username'].encode('utf8') + '",\n')
				f.write('	"password": "' + config['user']['password'] + '",\n')
				f.write('	"kw": "' + config['forum']['kw'].encode('utf8') + '",\n')
				f.write('	"apikey": "' + config['apikey'] + '"\n')
				f.write('}')
			except Exception as e:
				errLog(200, pause = False)
				sys.exit(1)
			stdLog(u'写入成功', 'success', ('console'))
			if filename == 'config/default.json':
				stdLog(u'请使用 python2 TiebaAutoTool.py run 来使用本配置运行', 'info', ('console'))
			else:
				stdLog(u'请使用 python2 TiebaAutoTool.py run -c %s 来使用本配置运行' % filename, 'info', ('console'))
			break

if __name__ == '__main__':
	print u'本模块只应被导入执行'