#--*-- coding:utf-8 --*--
import sys
import time
import colorama

__LOGLEVEL__ = {
	'DEBUG':0,
	'DEFAULT':10,
	'SIMPLE':20
}

__LOGTYPE__ = {
	'POST':[25],
	'SUCCESS':[10, u'【成功】 ', colorama.Style.BRIGHT + colorama.Fore.GREEN],
	'INFO':[10, u'【信息】 ', colorama.Style.BRIGHT + colorama.Fore.WHITE],
	'ERROR':[30,u'【错误】 ', colorama.Style.BRIGHT + colorama.Fore.RED],
	'DEBUG':[5,u'【调试】 ', colorama.Style.BRIGHT + colorama.Fore.YELLOW]
}


class log(object):
	"""This class provide you a simple interface to output or store logs"""
	def __init__(self, logmethod, logtype, level = 'DEFAULT'):
		"""logmethod will specify the place where logs will be stored or displaied
				it's value could be 'console', 'file', 'cloud' or 'mysql'
					'console' means the log data will display on the console
					'file' means logs will be stored in a specified file, you must specify the filename by setOutputFile method
					'cloud' if you want to stored logs on a cloud, you should use this value
					'mysql' you can use mysql to save your logs if you have a mysql server on localhost or on a remote server
			logtype specify the log's type, you can you 'POST' or 'STRING'
				'STRING' 
				"""
		self.method = logmethod
		self.level = __LOGLEVEL__[level]
		self.type = logtype

		if 'console' in logmethod:
			colorama.init(autoreset = True)

	def setLevel(self, level):
		"""This function will set log level

				You may use 'DEBUG', 'DEFAULT' or 'SIMPLE' to define which type of log will be displaied or stored
				'DEBUG' level is the highest log level which means it will recoder everything happened in this program, 
					so it may help you debug
					Once you use -d to enable debug mod, this log level should be set by default and conldn't be modified
				'DEFAULT' level will be set when you run this program without using debug mode"""
		self.level = __LOGLEVEL__[level]

	def setOutputFile(self, filename):
		self.filename = filename

	def setMySQL(self, host, username, password, database):
		self.mysql['host'] = host
		self.mysql['username'] = username
		self.mysql['password'] = password
		self.mysql['database'] = database

	def log(self, message, types = 'INFO'):
		if 'console' in self.method:
			if __LOGTYPE__[types][0] >= self.level:
				self.__ToConsole__(message, types)

		if 'file' in self.method:
			self.__ToFile__(message, types)


	def __ToConsole__(self, message, types):

		if self.type == 'POST':
			self.__PrintPost__(message)

		else:
			sys.stdout.write(__LOGTYPE__[types][2] + __LOGTYPE__[types][1] + message + '\n')
			sys.stdout.flush()

	def __ToFile__(self, message, types):
		if self.type == 'POST':
			self.__PostToFile__(message)

		else:
			with open(self.filename, 'a') as f:
				f.write(__LOGTYPE__[types][1] + message + '\n')

	def __ToMySQL__(self, message, level):
		print u'当前版本暂不支持数据库'

	def PrintPost(self, threadData):
		print u'------------------------------------------'
		print u'\n|作者：' + threadData['author']
		print u'\n|帖子标题：' + threadData['title']
		print u'\n|帖子预览：' + threadData['abstract']
		print u'\n|得分：%f' % threadData['grade']
		print u'\n-------------------------------------------\n\n'

	def __PostToFile__(self, threadData):
		string = ''\
			+ '{\n'\
			+ '    "type" : "' + threadData['operation'] +'",\n'\
			+ '    "data" : {\n'\
			+ '        "time" : "' + threadData['time'] + '",\n'\
			+ '        "title" : "' + threadData['title'].encode('utf-8') + '",\n'\
			+ '        "author" : "' + threadData['author'].encode('utf-8') + '",\n'\
			+ '        "abstract" : "' + threadData['abstract'].encode('utf-8') + '",\n'\
			+ '    },\n'\
			+ '    "grade" : ' + str(threadData['grade']) + '\n'\
			+ '},\n'
		with open(self.filename, 'a') as f:
			f.write(string)

	
# test = log('console', 'INFO','SIMPLE')
# test.log(u'这是普通信息', 'INFO')
# test.log(u'这是错误信息', 'ERROR')
# test.log(u'调试信息啊', 'DEBUG')
# test.log(u'成功啦！！！', 'SUCCESS')


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
