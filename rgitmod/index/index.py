#coding: utf-8

def findRepo(name, path):
	'''
	whether the repo have been managed by rgit
	ret 1 - existed
	ret 0 - not
	'''
	'''
	more powerful techniques should be used to improve the efficiency
	'''
	repoPathFile = open('repoPath', 'r')
	while True:
		line = repoPathFile.readline()
		if not line:
			return 0
		storeName, storePath = line.strip().split(',')
		if name == storeName and path == storePath:
			return 1


def addRepoPath(name, path):
	'''
	a new repo will be added to rgit to be managed
	ret 0: fail to add
	ret 1: success
	'''
	if findRepo(name, path):
		return 0
	indexFile = open('repoPath', 'a')
	indexFile.write(name + ',' + 'path' + '\n')
	indexFile.close()