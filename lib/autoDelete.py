# -*- coding: utf8 -*-
import os
import sys
import time

from bar import sleep
from baiduOperation import adminLogin, getThreadDataList, deleteThread
from initialization import initKeywords
from judge import judge
from stdlog import stdLog, postLog, getLogTime

__LASTDELETENUMBER__ = 0

#延时单位为分钟
__SLEEPLEVEL__ = [0.5, 1, 2, 3, 5, 10]

#当前延时等级
__CURRENTSLEEPLEVEL__ = 0


def autoDelete(config):
	stdLog(u'启动自动删贴机', 'info')

	stdLog(u'关键词初始化中...', 'info')
	keywords = initKeywords()
	lastModifiedTime = os.path.getmtime('config/keywords.txt')
	stdLog(u'关键词初始化完毕', 'success')

	stdLog(u'登录中...', 'info')
	if adminLogin(config['user'], config['configFilename'][:-5] + '.co'):
		stdLog(u'登陆成功', 'success')
		while(True):
			if lastModifiedTime != os.path.getmtime('config/keywords.txt'):
				stdLog(u'更新关键词中...', 'info')
				keywords = initKeywords()
				lastModifiedTime = os.path.getmtime('config/keywords.txt')
				stdLog(u'更新关键词完毕', 'success')
			_delete(config, keywords)
	else:
		stdLog(u'登陆失败', 'error')
		sys.exit(1)

def _delete(config, keywords):
	deleteCount = 0
	stdLog(u'获取首页...', 'info')
	threadDataList = getThreadDataList(config['forum'])
	for threadData in threadDataList:
		if _judgeThread(threadData, config, keywords):
			if _deleteThread(threadData, config):
				deleteCount += 1
				if not config['debug']:
					sleep(5)
			else:
				sleep(5)
				return

	if deleteCount != 0:
		stdLog(u'删除 {0} 个帖子'.format(deleteCount), 'info')
	stdLog(u'等待更多新帖...', 'info')
	_smartSleep(deleteCount)

def _judgeThread(threadData, config, keywords):
	if judge(threadData, keywords):
		postLog(threadData, ('console'))
		if not config['debug']:
			return True
		else:
			stdLog(u'请确认是否删除（按y删除）:', 'info', ('console'), '')
			if raw_input() == 'y':
				stdLog(u'已确认删除帖子...', 'debug')
				return True
			else:
				stdLog(u'跳过删帖', 'debug')

	return False

def _deleteThread(threadData, config):
	stdLog(u'正在删除帖子', 'info')
	if deleteThread(threadData['thread'], config['forum']):
		threadData['operation']['operation'] = 'delete'
		threadData['operation']['operationTime'] = getLogTime()
		stdLog(u'删除成功', 'success')
		stdLog(u'操作时间：' + threadData['operation']['operationTime'], 'debug')
		postLog(threadData, ('file'), config['apikey'])
		return True
	else:
		stdLog(u'删除失败', 'error')
		return False



def _smartSleep(deleteNumber):
	global __LASTDELETENUMBER__, __SLEEPLEVEL__, __CURRENTSLEEPLEVEL__
	#当上一次和本次删帖数都为0时，增大等待时间
	if __LASTDELETENUMBER__ == 0 and deleteNumber == 0 and __CURRENTSLEEPLEVEL__ != 5:
		__CURRENTSLEEPLEVEL__ += 1

	if __LASTDELETENUMBER__ != 0:
		#本次删帖数增加超过30%，就减少等待时间
		if (deleteNumber - __LASTDELETENUMBER__) / float(__LASTDELETENUMBER__) > 0.5:
			if __CURRENTSLEEPLEVEL__ != 0:
				__CURRENTSLEEPLEVEL__ -= 1

		#同理，删帖数降低则增大等待时间
		elif (__LASTDELETENUMBER__ - deleteNumber) / float(__LASTDELETENUMBER__) > 0.5:
			if __CURRENTSLEEPLEVEL__ != 5:
				__CURRENTSLEEPLEVEL__ +=1


	__LASTDELETENUMBER__ = deleteNumber

	sleep(int(60 * __SLEEPLEVEL__[__CURRENTSLEEPLEVEL__]))

if __name__ == '__main__':
	print u'本模块只应被导入执行'
