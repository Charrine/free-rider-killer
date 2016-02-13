# -*- coding: utf8 -*-
import re

def judge(threadData, keywords):
	titleGrade   = 0
	previewGrade = 0

	preview = (u'None' if threadData['abstract'] == None else threadData['abstract'])
	for keyword in keywords:
		arr = re.findall(keyword[2], threadData['title'])
		if len(arr):
			threadData['keywords'].append(keyword[0])
			titleGrade += len(arr) * keyword[1]

		arr = re.findall(keyword[2], preview)
		if len(arr):
			threadData['keywords'].append(keyword[0])
			previewGrade += len(arr) * keyword[1]

	grade = float(titleGrade) *0.8 / (len(threadData['title']) + len(preview) * 0.5) + float(previewGrade) * 1.2 / len(preview)

	return grade
