# -*- coding: utf8 -*-
import getpass
import os
import sys
import time
from lib.bar import *
from lib.webIO import *
from lib.initialization import initialization
from lib.judge import judge
reload(sys)
sys.setdefaultencoding( "utf-8" )


def configFileGenerator():
	print u'请输入配置文件的文件名（按回车使用默认文件）: ',
	filename = raw_input()
	if filename == '':
		filename = 'config/default.json'
		print u'使用默认配置文件config/default.json'
	else:
		filename = 'config/' + filename
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

	print u'请输入API key: ',
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
		try:
			outputLOG.log(u'获取首页...', 'INFO')
			threadDataList = getThreadDataList(config['forum'])

			for threadData in threadDataList:
				if threadData['goodThread'] == 0 and threadData['topThread'] == 0:
					threadData['keywords'] = []
					threadData['grade'] = float('%.2f'%judge(threadData, keywords))

					#only delete posts which has less than 10 replies
					if threadData['grade'] > 6 and threadData['replyNum'] < 10:

						postLOG.PrintPost(threadData)
						if not config['debug']:
							outputLOG.log(u'正在删除帖子', 'INFO')
							if deleteThread(threadData, config['forum']):
								outputLOG.log(u'删除成功', 'SUCCESS')
								outputLOG.log(u'操作时间：'+threadData['operationTime'], 'DEBUG')
								postLOG.log(threadData)

								if postLOG.getLastError():
									outputLOG.log(postLOG.errorMessage, 'ERROR')

								deleteCount += 1
							else:
								outputLOG.log(u'删除失败', 'ERROR')
							sleep(5)
						# in debug mode
						else:
							print u'请确认是否删除（按y删除）:',
							if raw_input() == 'y':
								outputLOG.log(u'已确认删除帖子...', 'DEBUG')
								outputLOG.log(u'正在删除', 'INFO')
								if deleteThread(threadData, config['forum']):
									outputLOG.log(u'删除成功', 'SUCCESS')
									outputLOG.log(u'操作时间：'+threadData['operationTime'], 'DEBUG')

									postLOG.log(threadData)
									if postLOG.getLastError():
										outputLOG.log(postLOG.errorMessage, 'ERROR')
									deleteCount += 1
								else:
									outputLOG.log(u'删除失败', 'ERROR')
							else:
								outputLOG.log(u'跳过删帖', 'DEBUG')



		except Exception, e:
			print e
			logFile = open('log/error.log', 'a')
			logFile.write(time.asctime() + '\n')
			logFile.write(str(e) + '\n\n')
			logFile.close()
			time.sleep(10)
		else:
			if deleteCount != 0:
				outputLOG.log(u'已检查首页: 已删除{0} 个帖子'.format(deleteCount), 'INFO')
			elif config['debug']:
				outputLOG.log(u'等待更多新帖...', 'INFO')
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
	global keywords
	config, keywords, outputLOG, postLOG = initialization()

if __name__ == '__main__':
	init()
	main()
