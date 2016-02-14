# -*- coding: utf8 -*-
import sys

from lib.initialization import initialization
from lib.configFileGenerator import configFileGenerator
from lib.autoTool import autoTool

reload(sys)
sys.setdefaultencoding( "utf-8" )

def main():
	config, keywords, outputLOG, postLOG = initialization()
	if config['workingType'] == 'config':
		configFileGenerator(config)
	elif config['workingType'] == 'autoTool':
		autoTool([config, keywords, outputLOG, postLOG])


if __name__ == '__main__':
	main()
