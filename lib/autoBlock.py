# -*- coding: utf8 -*-
import datetime
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
	lastModifiedTime = os.path.getmtime('config/blacklist.txt')
	stdLog(u'黑名单初始化完毕', 'success')

	stdLog(u'登录中...', 'info')
	if adminLogin(config['user'], config['configFilename'][:-5] + '.co'):
		stdLog(u'登陆成功', 'success')
		while(True):
			if lastModifiedTime != os.path.getmtime('config/blacklist.txt'):
				stdLog(u'更新黑名单中...', 'info')
				blacklist = initBlacklist()
				lastModifiedTime = os.path.getmtime('config/blacklist.txt')
				stdLog(u'更新黑名单完毕', 'success')
			s = sched.scheduler(time.time, time.sleep)
			tomorrow = datetime.datetime.replace(datetime.datetime.now() + datetime.timedelta(days=1), hour=0, minute=0, second=0, microsecond=0)
			s.enter((tomorrow - datetime.datetime.now()).seconds, 1, _block, (config, blacklist))
			s.run()
	else:
		stdLog(u'登陆失败', 'error')
		sys.exit(1)

def _block(config, blacklist):
	for black in blacklist:
		blockID(black, config['forum'])
		sleep(5)