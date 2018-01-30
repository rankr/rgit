from dulwich.repo import Repo
from dulwich.objects import *
import path
import os
from func import *
from ObjRepo import *
import commands as cmd
from RgitRepo import *

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
					ret += idxAna2(path + '/pack/' + j)
		else:
			objs = os.listdir(path + '/' + i)
			ret += [i + x for x in objs]

	os.chdir(rawPath)
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
	os.chdir(rawPath)