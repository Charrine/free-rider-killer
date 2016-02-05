import sys
import time

def uniout(str = '', threadData = '', level = 0, method = 'STDOUT'):
	if method == 'STDOUT':
		_stdout(str, level)
	elif method == 'DELETE':
		_delete(threadData)
	elif method == 'BLOCK':
		_block(threadData)
	elif method == 'ERROR':
		_error(str)

	return

def _stdout(str, level):
	_output(str)

	return

def _delete(threadData):
	str = ''\
		+ '{\n'\
		+ '    "type" : "delete",\n'\
		+ '    "data" : {\n'\
		+ '        "time" : "' + time.asctime() + '",\n'\
		+ '        "title" : "' + threadData['title'].encode('utf-8') + '",\n'\
		+ '        "author" : "' + threadData['author'].encode('utf-8') + '",\n'\
		+ '        "abstract" : "' + threadData['abstract'].encode('utf-8') + '",\n'\
		+ '    }\n'\
		+ '},\n'

	_output(str, stream = 'HISTORY')

	return

def _block(threadData):
	str = ''\
		+ '{\n'\
		+ '    "type" : "block",\n'\
		+ '    "data" : {\n'\
		+ '        "time" : "' + time.asctime() + '",\n'\
		+ '        "author" : "' + threadData['author'].encode('utf-8') + '",\n'\
		+ '    }\n'\
		+ '},\n'\

	_output(str, stream = 'HISTORY')

	return

def _error(str):
	_output(str, stream = 'ERROR')

	return

def _output(str, stream = 'STDOUT'):
	if stream == 'STDOUT':
		print str
	elif stream == 'HISTORY':
		with open('history.log', 'a') as f:
			f.write(str)
	elif stream == 'ERROR':
		with open('error.log', 'a') as f:
			f.write(str)

	return

def test():
	stdStr = 'this is stdout'
	threadData = {
		'title' : 'title',
		'author' : 'author',
		'abstract' : 'abstract'
	}
	errorStr = 'this is error'

	#uniout(stdStr)
	uniout(threadData = threadData, method = 'HISTORY')
	#uniout(threadData = threadData, method = 'BLOCK')
	#uniout(errorStr, method = 'ERROR')

test()
