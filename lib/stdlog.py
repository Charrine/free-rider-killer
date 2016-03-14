# -*- coding: utf8 -*-
import colorama
from datetime import datetime
import json
import traceback
import sys
import urllib
import urllib2


#日志等级
__LOGLEVEL = {
	'debug': 0,
	'middle': 10,
	'less': 20
}

#日志类型
__LOGTYPE = {
	'debug': [0, u'【调试】', colorama.Style.BRIGHT+colorama.Fore.YELLOW],
	'info': [10, u'【信息】', colorama.Style.BRIGHT+colorama.Fore.WHITE],
	'success': [10, u'【成功】', colorama.Style.BRIGHT+colorama.Fore.GREEN],
	'error': [20, u'【错误】', colorama.Style.BRIGHT+colorama.Fore.RED]
}

#默认为10
__STDLEVEL = 10

#默认标准输出的结果将被记录到控制台窗口和文件中
#此处的值可以设为'console'：记录到控制台
#'file'：记录到文件
__STDMETHOD = ('console', 'file')

#默认的日志输出方法
#console： 输出到控制台窗口
#file： 输出到指定文件
#cloud： 输出到云
__POSTMETHOD = ('console', 'file')

#错误输出方法，默认为终端和文件
__ERRMETHON = ('console', 'file')

#默认的输出文件名
__LOGFILENAME = {
	'log': 'log/default.log',
	'post': 'log/record.log',
	'error': 'log/error.log'
}

__ERRORNUMBER = {
	100: u'网络错误：无法解析域名',
	101: u'网络错误：无法获取网页',
	102: u'网络日志错误，发送日志失败',

	200: u'无法打开文件，可能是文件不存在或没有权限？',
	201: u'无法打开文件用于写入，没有权限或文件所处路径无效？',

	300: u'解析配置文件时发生错误，不是有效的配置文件',
	301: u'解析关键词时发生错误，可能不是有效的关键词，或文件包含BOM'
}

#设置输出文件名
def setOutputFile(log = '', post = '', error = ''):
	if log != '':
		__LOGFILENAME['log'] = log

	if post != '':
		__LOGFILENAME['post'] = post

	if error != '':
		__LOGFILENAME['error'] = error

def setStdLevel(level):
	"""设置标准日志输出等级
		level为等级，其值可以为'debug', 'middle', 'less'
		debug: 调试等级，将输出所有信息
		middle： 中等等级，输出调试信息以外的信息。此等级为默认等级
		less： 精简等级，只会输出错误信息。使用此等级不会向终端输出帖子信息，
			但其它方式的帖子记录没有影响"""
	global __STDLEVEL
	__STDLEVEL = __LOGLEVEL[level]
	stdLog(u'设置日志等级为%s' % level, 'debug')

def stdLog(message, logtype, method = None, end = '\n'):
	"""标准日志输出
		参数为 message 和 level，message 为将要输出的信息，level 为日志等级，
		当日志等级高于当前设置的等级时，将向对应的设备输出信息
		使用此函数不会记录调用栈"""
	if not method:
		method = __STDMETHOD
	if __LOGTYPE[logtype][0] >= __STDLEVEL:
		logtime = getLogTime()
		if 'console' in method:
			__logToConsole(message, logtype, end)

		if 'file' in method:
			__logToFile(message, logtype, logtime, end)

def __logToConsole(message, logtype, end):
	sys.stdout.write(__LOGTYPE[logtype][2] + __LOGTYPE[logtype][1] + message + end)

def __logToFile(message, logtype, time, end):
	try:
		with open(__LOGFILENAME['log'], mode = 'a') as f:
			f.write(time + __LOGTYPE[logtype][1] + message + end)
	except IOError, e:
		__errToConsole(201, getStack(), getLogTime(), True)

def getStack():
	"""获取调用栈，将返回一个格式化过的调用栈字符串"""
	callStack = traceback.format_stack()

	#最后2行为自身，无意义
	callStack.pop(-1)
	callStack.pop(-1)

	return callStack


def __errToConsole(errorNumber, stack, time, pause):
	print colorama.Style.BRIGHT + colorama.Fore.RED +\
		u'--------------------发生错误--------------------\n' +\
		u'时间：{0}\n错误：{1}'.format(time, __ERRORNUMBER[errorNumber])
	print u'调用跟踪：'
	for line in stack:
		sys.stdout.write(colorama.Fore.YELLOW + colorama.Style.BRIGHT + line)
	print colorama.Style.BRIGHT + colorama.Fore.RED +\
		u'------------------------------------------------'

	if pause:
		print u'按回车继续...',
		raw_input()

def __errToFile(errorNumber, stack, time):
	try:
		with open(__LOGFILENAME['error'], mode = 'a') as f:
			f.write((u'时间：{0}\n错误：{1}\n调用跟踪：\n'.format(time, __ERRORNUMBER[errorNumber])).encode('utf8'))
			for line in stack:
				f.write(line)
	except IOError, e:
		__errToConsole(201, getStack(), getLogTime(), True)

def errLog(errorNumber, pause = True):
	"""错误日志函数，使用此函数记录错误时会同时记录调用栈
		errorNumber： 错误号，应当为数字
		pause： 是否在输出错误后暂停，仅对终端输出时有效"""
	stack = getStack()
	logtime = getLogTime()

	if 'console' in __ERRMETHON:
		__errToConsole(errorNumber, stack, logtime, pause)
	if 'file' in __ERRMETHON:
		__errToFile(errorNumber, stack, logtime)

def getLogTime():
	return datetime.now().strftime('%y/%m/%d %H:%M:%S.') + datetime.now().strftime('%f')[:2]

def postLog(threadData, method = None, APIKey = ''):
	if not method:
		method = __POSTMETHOD

	if 'file' in method:
		__postToFile(threadData)
	if APIKey != '' and 'cloud' in method:
		#发送日志并判断是否成功
		if not __postToCloud(threadData, APIKey):
			#失败时输出错误信息
			errLog(102, pause = False)
	if 'console' in method:
		__postToConsole(threadData)

def __postToConsole(threadData):
	print u'------------------------------------------'
	print u'|作者：' + threadData['author']['userName']
	print u'|帖子标题：' + threadData['thread']['title']
	print u'|帖子预览：' + threadData['thread']['abstract']
	print u'|回复数：' + str(threadData['thread']['replyNum'])
	print u'|关键词：' + ','.join(threadData['thread']['keywords'])
	print u'|得分：%f' % threadData['thread']['grade']
	print u'-------------------------------------------'

def __postToFile(threadData):
	try:
		with open(__LOGFILENAME['post'], mode = 'a') as f:
			string = ''+\
				'{\n'+\
				'    "forum": "' + threadData['forum'] +'",\n'+\
				'    "data": {\n'+\
				'        "time": "' + threadData['operation']['operationTime'] + '",\n'+\
				'        "tid": "' + str(threadData['thread']['tid']) + '",\n'+\
				'        "pid": "' + str(threadData['thread']['pid']) + '",\n'+\
				'        "title": "' + threadData['thread']['title'].encode('utf-8') + '",\n'+\
				'        "author": "' + threadData['author']['userName'].encode('utf-8') + '",\n'+\
				'        "abstract": "' + threadData['thread']['abstract'].encode('utf-8') + '",\n'+\
				'        "replyNum": "' + str(threadData['thread']['replyNum']) + '",\n'+\
				'        "keywords": "' + ', '.join(threadData['thread']['keywords']) + '"\n'+\
				'    },\n'+\
				'    "grade": "' + str(threadData['thread']['grade']) + '"\n'+\
				'},\n'
			f.write(string)
	except IOError, e:
		__errToConsole(201, getStack(), getLogTime(), True)

def __postToCloud(threadData, APIKey):
	postdata = {
		'title': threadData['thread']['title'].encode('utf8'),
		'author': threadData['author']['userName'].encode('utf8'),
		'abstract': threadData['thread']['abstract'].encode('utf8'),
		'tid': threadData['thread']['tid'],
		'pid': threadData['thread']['pid'],
		'replyNum': threadData['thread']['replyNum'],
		'operationTime': threadData['operation']['operationTime'],
		'grade': threadData['thread']['grade'],
		'keywords': ', '.join(threadData['thread']['keywords']).encode('utf8'),
		'forum': threadData['forum'].encode('utf8'),
		'operator': APIKey
	}
	#"http://log.tiebamanager.xyz/create.php"
	#"http://localhost/tieba/create.php"
	request = urllib2.Request("http://log.tiebamanager.xyz/create.php", urllib.urlencode(postdata))
	connection = urllib2.urlopen(request, timeout = 10)
	code = json.loads(connection.read())['code']
	if code == 0:
		return True
	else:
		return False

#在导入时进行些许初始化工作
def logInitialization():
	colorama.init(autoreset = True)



if __name__ == '__main__':
	print u'本模块只应被导入执行'

#下面为测试数据，如果你要进行测试，请将下列代码解除注释
#threadData = {
#	'forum': 'c语言',
#	'operation': {
#		'operationTime': '16/02/22 21:44:44.66',
#	},
#	'thread': {
#		'tid': 4368741082,
#		'pid': 84471389607,
#		'title': '新手，求大神',
#		'abstract': 'NicoNicoNi',
#		'replyNum': 233,
#		'grade': 23.1,
#		'keywords': ['asd', 'asd']
#	},
#	'author': {
#		'userName': 'YukiSora'
#	}
#}
#下面为测试代码
# def f1():
# 	f2()

# def f2():
# 	f3()

# def f3():
# 	stdLog('这是错误信息', 'error')
# 	stdLog('普通信息', 'info')
# 	stdLog('调试信息', 'debug')
# 	stdLog('成功了会这样', 'success')
# colorama.init(autoreset = True)
# f1()

# setStdLevel('debug')
# f1()
