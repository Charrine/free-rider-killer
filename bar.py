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
		sys.stdout.write(' '*(self.width + 6)+'\r')
		sys.stdout.flush()

	def flush(self):
		sys.stdout.write('\n')

def sleep(sleeptime):
	stat = bar(20, u'等待...', 's')
	x = sleeptime
	while x >= 0:
		stat.update(x, float(sleeptime - x) / sleeptime)
		time.sleep(1)
		x -= 1

	stat.flush()

sleep(60)
