# -*- coding: utf8 -*-
import datetime
from datetime import datetime
import json
import os
import sched
import sys
import time

from baiduOperation import adminLogin, blockID
from initialization import initBlacklist
from stdlog import stdLog

def autoBlock(config):
	stdLog(u'启动自动小黑屋', 'info')

	stdLog(u'黑名单初始化中...', 'info')
	blacklist = initBlacklist()
	stdLog(u'黑名单初始化完毕', 'success')

	stdLog(u'登录中...', 'info')
	if adminLogin(config['user'], config['configFilename'][:-5] + '.co'):
		stdLog(u'登陆成功', 'success')
		while(True):
			blacklist = initBlacklist()
			s = sched.scheduler(time.time, time.sleep)
			tomorrow = datetime.datetime.replace(datetime.datetime.now() +
												datetime.timedelta(days = 1),
												hour = 0,
												minute = 0,
												second = 0,
												microsecond = 0)
			s.enter((tomorrow - datetime.datetime.now()).seconds,
					1,
					_block,
					(config, blacklist))
			s.run()
			_saveBlacklist(blacklist)
	else:
		stdLog(u'登陆失败', 'error')
		sys.exit(1)

def _block(config, blacklist):
	for black in blacklist:
		if black['times'] > 0:
			print '%s %s' % (datetime.now().strftime('%y/%m/%d %H:%M:%S'), black['username'])
			blockID(black['username'], config['forum'])
			black['times'] -= 1
			time.sleep(5)
		else:
			del black

def _saveBlacklist(blacklist):
	with open('config/blacklist.txt', 'w') as f:
		f.write(json.dumps(blacklist,
							sort_keys = True,
							indent = 4,
							separators = (',', ': '))
				.decode('unicode-escape')
				.encode('utf8'))
