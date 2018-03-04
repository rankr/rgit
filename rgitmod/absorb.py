import path
import os
from func import getObjFromGit, dirSize
from index.index import *
from ObjRepo import *
import commands as cmd
from RgitRepo import *
import time

def absorb(gitRepoPath):
	objList = getObjFromGit(gitRepoPath)
	#considering the packed size is almost 0.5 of raw objects
	needed = dirSize(gitRepoPath + '/.git') * 2
	objPath = path.getObjPath(needed)
	objrepo = ObjRepo(objPath)
	rgitRepo = RgitRepo(gitRepoPath)

	rawPath = os.getcwd()
	os.chdir(gitRepoPath)
	
	for sha in objList:
		status1, objType = cmd.getstatusoutput('git cat-file -t %s'%(sha))
		status2, objRawContent = cmd.getstatusoutput('git cat-file -p %s'%(sha))
		if status1 + status2 > 0:
			print 'git cat-file commands failed'
			raise Exception
		objrepo.addObjFromContent(objRawContent, sha, objType)
	
	rgitRepo.storeObjSha_lot(objList)
	rgitRepo.delGitFile()
	os.chdir(rawPath)

	temp = gitRepoPath.split("\\|/")
	addRepoPath(temp[-1], '/'.join(temp[0:-1]))