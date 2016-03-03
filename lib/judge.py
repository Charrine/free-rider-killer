# -*- coding: utf8 -*-
import re

def judge(threadData, keywords):
	if threadData['thread']['goodThread'] == 0 and threadData['thread']['topThread'] == 0:
		grade(threadData, keywords)
		#only delete posts which has less than 10 replies
		if threadData['thread']['grade'] > 6 and threadData['thread']['replyNum'] < 10:
			return True

	return False

def grade(threadData, keywords):
	titleGrade   = 0
	previewGrade = 0
	threadData['thread']['keywords'] = []

	preview = (u'None' if threadData['thread']['abstract'] == None else threadData['thread']['abstract'])
	for keyword in keywords:
		arr = re.findall(keyword[2], threadData['thread']['title'])
		if len(arr):
			threadData['thread']['keywords'].append(keyword[0])
			titleGrade += len(arr) * keyword[1]

		arr = re.findall(keyword[2], preview)
		if len(arr):
			threadData['thread']['keywords'].append(keyword[0])
			previewGrade += len(arr) * keyword[1]

	grade = float(titleGrade) *0.8 / (len(threadData['thread']['title']) + len(preview) * 0.5) + float(previewGrade) * 1.2 / len(preview)

	threadData['thread']['grade'] = float('%.2f' % grade)

if __name__ == '__main__':
	print u'本模块只应被导入执行'
