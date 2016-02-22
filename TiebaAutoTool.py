# -*- coding: utf8 -*-
import sys

from lib.initialization import initialization
from lib.configFileGenerator import configFileGenerator
from lib.autoDelete import autoDelete

reload(sys)
sys.setdefaultencoding( "utf-8" )

def main():
	config = initialization()
	if config['workingType'] == 'config':
		configFileGenerator(config)
	elif config['workingType'] == 'autoDelete':
		autoDelete(config)

if __name__ == '__main__':
	main()
