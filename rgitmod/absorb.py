#coding: utf-8
import rpath
import os
from func import getObjFromGit, dirSize, idxAna
from index.index import *
from ObjRepo import *
import commands as cmd
from RgitRepo import *
import time
import shutil
'''
	absorb:
		得到所有sha1, 根据sha1利用cat-file提取内容，然后用md5算法存起来
	absorb1:
		遍历objects文件夹，未打包的就直接move过去；
		打包的利用git show-index（详见func.py，idxAna函数）得到sha1，然后挨个cat-file送过去
	absorb2:
		遍历objects文件夹，未打包直接move
		打包的自行解析idx和对应pack，把所有的内容都送过去
		好处是不用还原出来原来文件，过去之后也不用MD5再次压缩；而且packfile一起解析，而不是一个一个obj地处理
		坏处是自己编写的函数可能比git自带的效率低
	'''
"""
def absorb(gitRepoPath):
	objList = getObjFromGit(gitRepoPath)
	#considering the packed size is almost 0.5 of raw objects
	needed = dirSize(gitRepoPath + '/.git') * 2
	objPath = rpath.getObjPath(needed)
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

def absorb1(gitRepoPath):
	#considering the packed size is almost 0.5 of raw objects
	needed = dirSize(gitRepoPath + '/.git') * 2
	dstPath = rpath.getObjPath(needed)
	objrepo = ObjRepo(dstPath)
	rgitRepo = RgitRepo(gitRepoPath)

	unpacked_objList = []
	packed_objList = []

	rawPath = os.getcwd()
	git_objPath = gitRepoPath + '/.git/objects'
	os.chdir(git_objPath)
	dirs = os.listdir(git_objPath)
	for i in dirs:
		if i == 'info':
			continue
		elif i == 'pack':
			d = os.listdir(git_objPath + '/' + i)
			for j in d:
				if len(j) > 4 and j[-4:]=='.idx':
					packed_objList += idxAna(git_objPath + '/pack/' + j)
		else:
			objs = os.listdir(git_objPath + '/' + i)
			unpacked_objList += [i + x for x in objs]
			for j in objs:
				objrepo.addObjFromPath(os.path.join(git_objPath, i, j), i + j)
	
	for sha in packed_objList:
		status1, objType = cmd.getstatusoutput('git cat-file -t %s'%(sha))
		status2, objRawContent = cmd.getstatusoutput('git cat-file -p %s'%(sha))
		if status1 + status2 > 0:
			print 'git cat-file commands failed'
			raise Exception
		objrepo.addObjFromContent(objRawContent, sha, objType)
	
	rgitRepo.storeObjSha_lot(packed_objList + unpacked_objList)
	rgitRepo.delGitFile()
	os.chdir(rawPath)

	temp = gitRepoPath.split("\\|/")
	addRepoPath(temp[-1], '/'.join(temp[0:-1]))
"""

def absorb(gitRepoPath):
	'''
	for each seperated object, move it
	for each packfile, get each obj from it and store
	'''
	needed = dirSize(gitRepoPath + '/.git') * 2
	dstPath = rpath.getObjPath(needed)
	objrepo = ObjRepo(dstPath)
	rgitRepo = RgitRepo(gitRepoPath)

	unpacked_objList = []
	packed_objList = []

	rawPath = os.getcwd()
	git_objPath = gitRepoPath + '/.git/objects'
	os.chdir(git_objPath)
	dirs = os.listdir(git_objPath)
	for i in dirs:
		if i == 'info':
			continue
		elif i == 'pack':
			d = os.listdir(git_objPath + '/' + i)
			for j in d:
				if len(j) > 4 and j[-4:]=='.idx':
					idx_path = os.path.join(git_objPath, 'pack', j)
					pack_path = os.path.join(git_objPath, 'pack', j[:-4] + '.pack')
					packed_objList += idxAna(idx_path)
					objrepo.addObjFromPack(idx_path, pack_path)
		else:
			objs = os.listdir(git_objPath + '/' + i)
			unpacked_objList += [i + x for x in objs]
			for j in objs:
				objrepo.addObjFromPath(os.path.join(git_objPath, i, j), i + j)
	
	rgitRepo.storeObjSha_lot(packed_objList + unpacked_objList)
	rgitRepo.delGitFile()
	os.chdir(rawPath)

	temp = gitRepoPath.split("\\|/")
	addRepoPath(temp[-1], '/'.join(temp[0:-1]))