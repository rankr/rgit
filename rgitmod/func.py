#coding: utf-8
'''
some general functions
'''
import os
import Queue
import commands as cmd

def dirSize(dirPath):
	'''
	ret in Byte
	'''
	if not os.path.isdir(dirPath):
		return -1
	q = Queue.Queue()
	q.put(dirPath)
	res = 0
	while not q.empty():
		a = q.get()
		b = os.listdir(a)
		for i in b:
			c = a+'/'+i
			if os.path.isdir(c):
				q.put(c)
			elif os.path.isfile(c):
				res += os.path.getsize(c)
			else:
				print c,'is not file or dir'
	return res

def cmpSha(sha1, sha2):
	for i in xrange(0, len(sha1)):
		a = sha1[i]
		b = sha2[i]
		if a > b:
			return 1
		elif a < b:
			return -1
	return 0


def idxAna(idxPath):
	'''get a path of *.idx file, give all its objects'''
	status, output = cmd.getstatusoutput('cat %s | git show-index'%(idxPath))
	if status != 0:
		print 'git show-index failed in idxAna'
		exit()
	ret = output.split()[1::3]
	return ret

def getObjFromGit(repoPath):
	'''get all objects names from git repo'''
	rawPath = os.getcwd()
	os.chdir(repoPath)

	path = repoPath + '/.git/objects'
	dirs = os.listdir(path)
	ret = []
	for i in dirs:
		if i == 'info':
			continue
		elif i == 'pack':
			d = os.listdir(path + '/' + i)
			for j in d:
				if len(j) > 4 and j[-4:]=='.idx':
					ret += idxAna(path + '/pack/' + j)
		else:
			objs = os.listdir(path + '/' + i)
			ret += [i + x for x in objs]

	os.chdir(rawPath)
	return ret