# -*- coding: utf8 -*-

import os
import sys

__FILENAMELIST = dict()

def isFileUpdated(filename):
	"""判断某个文件是否更新，文件名应当包含路径
			当文件名是第一次判断时，返回值永远为True
			否则，当文件名对应的文件时间戳发生变化时，则返回True"""

	global __FILENAMELIST
	#当文件不存在时，返回False
	if not os.path.isfile(filename):
		return False


	#当文件名第一次出现时，获取文件时间戳并且储存与列表中
	if filename not in __FILENAMELIST:
		__FILENAMELIST[filename] = os.path.getmtime(filename)
		return True

	if __FILENAMELIST[filename] == os.path.getmtime(filename):
		return False

	else:
		__FILENAMELIST[filename] = os.path.getmtime(filename)
		return True