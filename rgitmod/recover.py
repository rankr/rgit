#coding: utf-8
import os
from RgitRepo import RgitRepo
from index import index
import re
from ObjRepo import *

def recovergit(RepoPath): 
	'''
	now it can only recover git into 
	'''
	RepoPath = os.path.abspath(RepoPath)
	print "RepoPath", RepoPath
	a = re.split(r"/|\\", RepoPath)
	
	if not index.findRepo(a[-1], '/'.join(a[0:-1])):
		print "not support recover to any directory now"
		return False
	repo = RgitRepo(RepoPath)

	shaArr = repo.getAllSha()
	for i in shaArr:
		repo.insertObj(i)
	return True