# -*- coding: utf8 -*-
import sys
import time

from bar import sleep
from baiduOperation import adminLogin, getThreadDataList, deleteThread
from judge import judge
from stdlog import getLogTime

def autoTool(params):
	global config
	global outputLOG
	global postLOG
	global keywords

	config, keywords, outputLOG, postLOG = params

	if adminLogin(config['user'], config['configFilename'][:-5] + '.co'):
		outputLOG.log(u'登陆成功', 'SUCCESS')
		autoDelete()
		#autoBlock
	else:
		outputLOG.log(u'登陆失败', 'ERROR')
		sys.exit(1)

def autoDelete():
	deleteCount = 0
	while(True):
		try:
			outputLOG.log(u'获取首页...', 'INFO')
			threadDataList = getThreadDataList(config['forum'])
			for threadData in threadDataList:
				deleteCount += _analyzeThread(threadData)
		except Exception, e:
			print e
			logFile = open('log/error.log', 'a')
			logFile.write(time.asctime() + '\n')
			logFile.write(str(e) + '\n\n')
			logFile.close()
			sleep(10)
		else:
			if deleteCount != 0:
				outputLOG.log(u'删除 {0} 个帖子'.format(deleteCount), 'INFO')
			else:
				outputLOG.log(u'等待更多新帖...', 'INFO')
				sleep(60)
			deleteCount = 0

def _analyzeThread(threadData):
	if threadData['thread']['goodThread'] == 0 and threadData['thread']['topThread'] == 0:
		judge(threadData, keywords)
		#only delete posts which has less than 10 replies
		if threadData['thread']['grade'] > 6 and threadData['thread']['replyNum'] < 10:
			postLOG.PrintPost(threadData)
			if not config['debug']:
				return _deleteThread(threadData)
				sleep(5)
			else:
				print u'请确认是否删除（按y删除）:',
				if raw_input() == 'y':
					outputLOG.log(u'已确认删除帖子...', 'DEBUG')
					return _deleteThread(threadData)
				else:
					outputLOG.log(u'跳过删帖', 'DEBUG')
	return 0

def _deleteThread(threadData):
	outputLOG.log(u'正在删除帖子', 'INFO')
	if deleteThread(threadData['thread'], config['forum']):
		threadData['operation']['operation'] = 'delete'
		threadData['operation']['operationTime'] = getLogTime()
		outputLOG.log(u'删除成功', 'SUCCESS')
		outputLOG.log(u'操作时间：'+threadData['operation']['operationTime'], 'DEBUG')
		postLOG.log(threadData)

		if postLOG.getLastError():
			outputLOG.log(postLOG.errorMessage, 'ERROR')
		return 1
	else:
		outputLOG.log(u'删除失败', 'ERROR')
		return 0

def autoBlock():
	pass
