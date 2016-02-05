#--*-- coding:utf-8 --*--
import sys
import time
import colorama

__level__ = {
	'DEBUG'  : 50,
	'DEFAULT': 40,
	'SIMPLE' : 30,


	'INFO':40,
	'SUCCESS':40,
	'ERROR':30
}

class log(object):
	"""docstring for log"""
	def __init__(self, logmethod, logtype, level):
		self.method = logmethod
		self.level = level
		self.type = logtype

		if 'console' in logmethod:
			colorama.init(autoreset = True)

	def setLevel(self, level):
		self.level = __level__['level']

	def setOutputFile(self, filename):
		self.filename = filename

	def setMySQL(self, host, username, password, database):
		self.mysql['host'] = host
		self.mysql['username'] = username
		self.mysql['password'] = password
		self.mysql['database'] = database

	def log(self, message, level):
		if 'console' in self.method:
			self.__ToConsole__(message, level)

		if 'file' in self.method:
			self.__ToFile__(message, level)


	def __ToConsole__(self, message, level):
		if level == 'SUCCESS':
			sys.stdout.write(colorama.Style.BRIGHT + colorama.Fore.GREEN +  u'【调试】 ' + message)
			sys.stdout.write('\n')
			sys.stdout.flush()
		if level == 'DEBUG':
			sys.stdout.write(colorama.Style.BRIGHT + colorama.Fore.YELLOW +  u'【调试】 ' + message)
			sys.stdout.write('\n')
			sys.stdout.flush()
		if level == 'INFO':
			sys.stdout.write(colorama.Style.BRIGHT + colorama.Fore.WHITE + u'【信息】 ' + message)
			sys.stdout.write('\n')
			sys.stdout.flush()
		if level == 'ERROR':
			sys.stdout.write(colorama.Style.BRIGHT + colorama.Fore.RED + u'【错误】 ' + message)
			sys.stdout.write('\n')
			sys.stdout.flush()

	def __ToFile__(self, message, level):
		print '[FILE]' + message

	def __ToMySQL__(self, message, level):
		print u'当前版本暂不支持数据库'


test = log('console', 'INFO','DEFAULT')
test.log(u'这是普通信息', 'INFO')
test.log(u'这是错误信息', 'ERROR')
test.log(u'调试信息啊', 'DEBUG')
test.log(u'成功啦！！！', 'SUCCESS')

# def loginit(level = 'DEFAULT', method = ['console']):
# 	__logConfig__['LogLevel']     = level
# 	__logConfig__['OutputMethod'] = method

# 	if 


# def uniout(str = '', threadData = '', level = 0, method = 'STDOUT'):
# 	if method == 'STDOUT':
# 		_stdout(str, level)
# 	elif method == 'DELETE':
# 		_delete(threadData)
# 	elif method == 'BLOCK':
# 		_block(threadData)
# 	elif method == 'ERROR':
# 		_error(str)

# 	return

# def _stdout(str, level):
# 	_output(str)

# 	return

# def _delete(threadData):
# 	str = ''\
# 		+ '{\n'\
# 		+ '    "type" : "delete",\n'\
# 		+ '    "data" : {\n'\
# 		+ '        "time" : "' + time.asctime() + '",\n'\
# 		+ '        "title" : "' + threadData['title'].encode('utf-8') + '",\n'\
# 		+ '        "author" : "' + threadData['author'].encode('utf-8') + '",\n'\
# 		+ '        "abstract" : "' + threadData['abstract'].encode('utf-8') + '",\n'\
# 		+ '    }\n'\
# 		+ '},\n'

# 	_output(str, stream = 'HISTORY')

# 	return

# def _block(threadData):
# 	str = ''\
# 		+ '{\n'\
# 		+ '    "type" : "block",\n'\
# 		+ '    "data" : {\n'\
# 		+ '        "time" : "' + time.asctime() + '",\n'\
# 		+ '        "author" : "' + threadData['author'].encode('utf-8') + '",\n'\
# 		+ '    }\n'\
# 		+ '},\n'\

# 	_output(str, stream = 'HISTORY')

# 	return

# def _error(str):
# 	_output(str, stream = 'ERROR')

# 	return

# def _output(str, stream = 'STDOUT'):
# 	if stream == 'STDOUT':
# 		print str
# 	elif stream == 'HISTORY':
# 		with open('history.log', 'a') as f:
# 			f.write(str)
# 	elif stream == 'ERROR':
# 		with open('error.log', 'a') as f:
# 			f.write(str)

# 	return

# def test():
# 	stdStr = 'this is stdout'
# 	threadData = {
# 		'title' : 'title',
# 		'author' : 'author',
# 		'abstract' : 'abstract'
# 	}
# 	errorStr = 'this is error'

# 	#uniout(stdStr)
# 	uniout(threadData = threadData, method = 'HISTORY')
# 	#uniout(threadData = threadData, method = 'BLOCK')
# 	#uniout(errorStr, method = 'ERROR')

# test()
