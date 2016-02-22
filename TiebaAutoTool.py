# -*- coding: utf8 -*-
import sys

from lib.autoBlock import autoBlock
from lib.autoDelete import autoDelete
from lib.configFileGenerator import configFileGenerator
from lib.initialization import initialization

reload(sys)
sys.setdefaultencoding( "utf-8" )

def main():
	config = initialization()
	if config['workingType'] == 'config':
		configFileGenerator(config)
	elif config['workingType'] == 'autoDelete':
		autoDelete(config)
	elif config['workingType'] == 'autoBlock':
		autoBlock(config)

if __name__ == '__main__':
	main()
