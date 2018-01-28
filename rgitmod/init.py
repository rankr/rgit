#coding: utf-8
import os
import commands
from index import index

def initRepo(filePath):
	'''
	initialize a file into rgit format
	'''
	try:
		assert(os.path.exists(filePath))
	except AssertionError, e:
		print e
		print 'path not exists when initializing'
		exit()

	rawPath = os.getcwd()
	os.chdir(filePath)
	status, output = commands.getstatusoutput('git init')
	if status != 0:
		print output
		print 'failed when \'git init\''
		exit()
	os.chdir(rawPath)

	arr = filePath.split('/|\\')
	index.addRepoPath(arr[-1], '/'.join(arr[0:-1]))
	index.initObjIndex(filePath)
