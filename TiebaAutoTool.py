# -*- coding: utf8 -*-
import sys
import time
from lib.bar import *
from lib.webIO import *
from lib.initialization import initialization
from lib.configFileGenerator import configFileGenerator
from lib.judge import judge
reload(sys)
sys.setdefaultencoding( "utf-8" )

def autoDelete():
	deleteCount = 0
	while(True):
		try:
			outputLOG.log(u'获取首页...', 'INFO')
			threadDataList = getThreadDataList(config['forum'])

			for threadData in threadDataList:
				if threadData['thread']['goodThread'] == 0 and threadData['thread']['topThread'] == 0:
					judge(threadData, keywords)

					#only delete posts which has less than 10 replies
					if threadData['thread']['grade'] > 6 and threadData['thread']['replyNum'] < 10:

						postLOG.PrintPost(threadData)
						if not config['debug']:
							outputLOG.log(u'正在删除帖子', 'INFO')
							if deleteThread(threadData['thread'], config['forum']):
								threadData['operation']['operation'] = 'delete'
								threadData['operation']['operationTime'] = getLogTime()
								outputLOG.log(u'删除成功', 'SUCCESS')
								outputLOG.log(u'操作时间：'+threadData['operation']['operationTime'], 'DEBUG')
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
								if deleteThread(threadData['thread'], config['forum']):
									threadData['operation']['operation'] = 'delete'
									threadData['operation']['operationTime'] = getLogTime()
									outputLOG.log(u'删除成功', 'SUCCESS')
									outputLOG.log(u'操作时间：'+threadData['operation']['operationTime'], 'DEBUG')

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
		configFileGenerator(config)
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
