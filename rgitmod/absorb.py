from dulwich.repo import Repo
from dulwich.objects import *
import path
import os
from func import *
from ObjRepo import *
import commands as cmd
from RgitRepo import *


def num2Chr(a):
	if a < 10:
		return chr(ord('0') + a)
	else:
		return chr(ord('a') + a - 10)

def idxAna(idxPath):#get obj from index file
	#checking file
	f = open(idxPath, 'rb')
	assert(f)

	#checking .idx
	size = 4 + 4
	header = [255, 116, 79, 99, 0, 0, 0, 2]
	L = []
	for i in xrange(0, size):
		temp = f.read(1)
		L.append(ord(temp))
	assert(L == header)

	L = []
	for i in xrange(0, 256):
		a = ord(f.read(1))
		b = ord(f.read(1))
		c = ord(f.read(1))
		d = ord(f.read(1))
		temp = a*256**3 + b*256**2 + c*256 + d#tested, this's right
		L.append(temp)
	objNum = L[255]
	ret = []
	for i in xrange(0, objNum):
		s = ''
		for j in xrange(0, 20):
			temp = ord(f.read(1))
			a = temp/16
			b = temp%16
			s += num2Chr(a) + num2Chr(b)
		ret.append(s)
	return ret

def getObjFromGit(repoPath):
	'''get all object names from git repo'''
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
	return ret


def absorb(gitRepoPath):
	repo = Repo(gitRepoPath)

	objList = getObjFromGit(gitRepoPath)
	#considering the packed size is almost 0.5 of raw objects
	needed = dirSize(gitRepoPath + '/.git') * 2
	objPath = path.getObjPath(needed)
	objrepo = ObjRepo(objPath)
	rgitRepo = RgitRepo(gitRepoPath)
	'''
	dulwich:
	1 - commit
	2 - tree
	3 - blob
	4 - tag
	'''
	rawPath = os.getcwd()
	os.chdir(gitRepoPath)
	for sha in objList:
		status1, objType = cmd.getstatusoutput('git cat-file -t %s'%(sha))
		status2, objRawContent = cmd.getstatusoutput('git cat-file -p %s'%(sha))
		if status1 + status2 > 0:
			print 'git cat-file commands failed'
			raise Exception
		objrepo.addObjFromContent(objRawContent, sha, objType)
		rgitRepo.storeObjName(sha)
	rgitRepo.delGitFile()