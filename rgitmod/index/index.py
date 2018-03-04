#coding: utf-8
import sys
import os
from rgitmod import path
sys.path.append('../')
sys.path.append('../../conf')

def findRepo(name, repopath):
	'''
	whether the repo have been managed by rgit
	ret 1 - existed
	ret 0 - not
	'''
	'''
	more powerful techniques should be used to improve the efficiency
	'''
	pathList = path.readPathFile()

	repoPathFile = open('./rgitmod/index/repoList', 'r')
	while True:
		line = repoPathFile.readline()
		if not line:
			return 0
		storeName, storePath= line.strip().split(',')
		print "name:", name
		print "storename:", storeName
		print "repoPath:", repopath
		print "storePath:", storePath
		if name == storeName and repopath == storePath:
			return 1


def addRepoPath(name, path):
	'''
	a new repo will be added to rgit to be managed
	ret 0: fail to add
	ret 1: success
	'''
	if findRepo(name, path):
		return 0
	indexFile = open('repoList', 'a')
	indexFile.write(name + ',' + 'path' + '\n')
	indexFile.close()
	return 1

def initObjIndex(filePath):
	'''
	create related dir and files in repo, to store which objs the repo has
	'''
	os.mkdir(filePath + '/.rgit')
	f = open(filePath + '/.rgit/objects', 'w')
	f.close()

def findObjInObjRepo(objRepoPath, sha):
	pass
