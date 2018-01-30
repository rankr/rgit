#coding: utf-8
import os
import argparse
import sys
from rgitmod import init
from rgitmod import absorb
from test import getidx

def initParse():

	parser = argparse.ArgumentParser()
	#initializing a empty file with rgit format, exec in the empty file
	parser.add_argument('-i', '--init')

	#absorb a raw git repository into rgit store, argu is the path
	parser.add_argument('-a', '--absorb')

	#update a repository with a git repository, argu is the path
	parser.add_argument('-u', '--update')

	#for developer's testing
	parser.add_argument('-t', '--test')

	return parser


if __name__ == '__main__':
	#parsing the argus
	parser = initParse()
	args = vars(parser.parse_args())

	if args['test']:
		if args['test'] == 'getidx':
			getidx.testgetidx()
		exit()
	if args['init']:
		init.initRepo(os.path.abspath(args['init']))
		exit()
	if args['absorb']:
		absorb.absorb(os.path.abspath(args['absorb']))
		exit()
	if args['update']:
		pass
		exit()