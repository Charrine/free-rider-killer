# -*- coding: utf8 -*-
import os
import sys
import time

from bar import sleep
from baiduOperation import adminLogin, getThreadDataList, deleteThread
from initialization import initKeywords
from judge import judge
from stdlog import stdLog, postLog, getLogTime

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
	sleep(60)

def _judgeThread(threadData, config, keywords):
	if threadData['thread']['goodThread'] == 0 and threadData['thread']['topThread'] == 0:
		judge(threadData, keywords)
		#only delete posts which has less than 10 replies
		if threadData['thread']['grade'] > 6 and threadData['thread']['replyNum'] < 10:
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
		postLog(threadData, ('file, cloud'), config['apikey'])
		return True
	else:
		stdLog(u'删除失败', 'error')
		return False

if __name__ == '__main__':
	print u'本模块只应被导入执行'