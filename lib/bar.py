# -*- coding: utf8 -*-

import time
import sys

class bar(object):
	def __init__(self, width, message, symbol = '%'):
		self.message = message
		self.width = width
		self.symbol = symbol

	def update(self, number, percent):
		length = int(self.width * percent)
		sys.stdout.write(self.message+'{0:>3}{3}[{1:=>{2}}]\r'.format(number, ' '*(self.width-length), self.width, self.symbol))
		sys.stdout.flush()

	def wipe(self):
		sys.stdout.write(' '*(self.width + 15)+'\r')
		sys.stdout.flush()

	def flush(self):
		sys.stdout.write('\n')

def sleep(sleeptime, newline = None):
	if newline == None:
		newline = True

	stat = bar(60, u'等待...', 's')
	x = sleeptime
	while x >= 0:
		stat.update(x, float(sleeptime - x) / sleeptime)
		time.sleep(1)
		x -= 1

	if newline:
		stat.flush()
	else:
		stat.wipe()

# 直接运行则显示提示并退出
if __name__ == '__main__':
	print u'本模块只应被导入执行'