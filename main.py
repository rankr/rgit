#coding: utf-8
import argparse
import sys
from rgitmod import init
from rgitmod.index import

def initParse():
	parser = argparse.ArgumentParser()

	#initializing a empty file with rgit format, exec in the empty file
	parser.add_argument('-i', '--init')

	#absorb a raw git repository into rgit store, argu is the path
	parser.add_argument('-a', '--absorb')

	#update a repository with a git repository, argu is the path
	parser.add_argument('-u', '--update')

	return parser


if __name__ == '__main__':
	#parsing the argus
	parser = initParse()
	args = getArgs()
	args = vars(parser.parse_args(args))

	if 'init' in args:
		init.initFile(args['init'])
		exit()
	if 'absorb' in args:
		pass
		exit()
	if 'update' in args:
		pass
		exit()