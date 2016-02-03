# -*- coding: utf8 -*-
import json
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

def parseArgument(config):
	import argparse
	
	parser = argparse.ArgumentParser()

	parser.add_argument('choices', choices = ['run', 'config'], help = u'使用"run"来运行删帖机，使用"config"来生成一个配置文件')
	parser.add_argument('-c', help = u'json格式的配置文件名，若未给出则默认为default.json', dest = 'filename', default = 'default.json')
	parser.add_argument('-u', '--username', help = u'指定登陆的用户名')
	parser.add_argument('-p', '--password', help = u'密码，必须和上一项结合使用')
	parser.add_argument('-n'              , help = u'贴吧名，不包含‘吧’', default = u'c语言')
	# parser.add_argument('--fid',          , help = u'fid', )
	parser.add_argument('-d', '--debug'   , help = u'调试模式，只对页面进行检测，而不会发送删帖/封禁请求', action = "store_true")
	parser.add_argument('-v', '--version' , help = u'显示版本信息并退出', action = "version", version = '0.1')
	args = parser.parse_args()

	config['debug'] = args.debug

	if args.choices == 'run':
		if args.username != None:
			config['username'] = args.username.decode(config['stdincoding'])
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
	import os
	import getpass

	isLogined = False

	print u'请输入配置文件的文件名按回车使用默认文件:',
	config['filename'] = raw_input()
	if config['filename'] == '':
		print u'使用默认配置文件default.json'
		config['filename'] = 'default.json'
	print u'-----将使用:%s -----' %(config['filename'])
	if os.path.exists(config['filename']):
		print u'文件已存在，本操作将覆盖此文件，是否继续？(y继续操作)'
		inputs = raw_input()
		if inputs != 'y' and inputs != 'Y':
			print u'已取消'
			sys.exit(0)	

	while isLogined == False:
		print u'请输入用户名:',
		config['username'] = raw_input()

		print u'请输入密码（无回显）',

		config['password'] = getpass.getpass(':')

		print u'-----登陆测试-----'
		if config['debug'] == False:
			isLogined = adminLogin(config['username'], config['password'])
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

	print u'请输入贴吧名称（不带‘吧’，如希望管理c语言吧，则输入‘c语言’）'
	config['kw'] = raw_input()



	print u'请输入fid：',
	config['fid'] = raw_input()

	config['kw']     = config['kw'].decode(config['stdincoding'])
	config['username'] = config['username'].decode(config['stdincoding'])
	with open(config['filename'], "w") as configfile:
		configfile.write('{\n')
		configfile.write('    "username":"' + config['username'].encode('utf8') + '",\n')
		configfile.write('    "password":"' + config['password'] + '",\n')
		configfile.write('    "kw":"' + config['kw'].encode('utf8') + '",\n')
		configfile.write('    "fid":' + config['fid'] + '\n')
		configfile.write('}')
	print u'-----写入成功-----'
	print u'请使用python TiebaAutoTool.py run -c %s 来使用本配置运行' % config['filename']
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

	if 'username' in jsonobj and 'password' in jsonobj and 'kw' in jsonobj and 'fid' in jsonobj:
		config['username'] = jsonobj['username']
		config['password'] = jsonobj['password']
		config['kw']     = jsonobj['kw']
		config['fid']	   = jsonobj['fid']

	else:
		print u'无效的配置文件，请使用TiebaAutoTool.py config来生成配置文件'
		sys.exit(2)



def main():

	deleteCount = 0
	while(True):
		try:
			threadDataList = getThreadDataList(config)

			for threadData in threadDataList:
				if threadData['goodThread'] == 0 and threadData['topThread'] == 0:
					grade = judge(threadData)
					if grade > 6:
						print u'------------------------------------------\n|作者：' + threadData['author']
						print u'\n|帖子标题：' + threadData['title'] 
						print u'\n|帖子预览：' + threadData['abstract']
						print u'\n|得分：%f' % grade
						print u'\n-------------------------------------------\n\n'

						if config['debug'] == False:
							deleteThread(threadData, config)
						#blockID(threadData, config)
						deleteCount += 1
						sleep(5)
		except Exception, e:
			print e
			logFile = open('error.log', 'a')
			logFile.write(time.asctime() + '\n')
			logFile.write(str(e) + '\n\n')
			logFile.close()
			time.sleep(10)
		else:
			if deleteCount != 0:
				print '已检查首页: 已删除{0} 个帖子'.format(deleteCount)
			print '等待更多新帖...'
			sleep(60)
			deleteCount = 0

	return

# do some initialization work
def init():

	

	global config 
	config = {}
	

	if sys.stdin.encoding == 'cp936':
		config['stdincoding'] = 'gbk'
	else:
		config['stdincoding'] = 'utf8'

	parseArgument(config)

	print '--- Initializing ---'
	if config['debug']:
		print u'调试模式已开启！'


	if config['type'] == 'config':
		configure()
		sys.exit(0)
	elif config['type'] == 'json':
		getConfigrations(config)


	try:
		global keywords
		f = file('keywords.conf')
		keywords = json.load(f)
	except IOError, e:
		print u'无法打开 keywords 配置文件，文件可能不存在'
		sys.exit(1)
	finally:
		f.close()


	print u'使用用户名：' + config['username']


	isLogined = adminLogin(config)

	if isLogined == False:
		sys.exit(1)

	print "--- Initialize succeessful ---"

if __name__ == '__main__':

	init()
	main()