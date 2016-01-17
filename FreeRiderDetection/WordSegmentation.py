# -*- coding: utf8 -*-
import jieba
import sys

def main(argv):
	f = open('freeRiderData.txt')
	jieba.load_userdict('KeywordDictionary.txt')
	for line in f:
		# 精确模式
		seg_list = jieba.cut(line, cut_all=False)
		print("Default Mode: " + "/ ".join(seg_list))  	

	return

if __name__ == '__main__':
	main(sys.argv[1:])
