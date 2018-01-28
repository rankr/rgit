#coding: utf-8

'''
structure of RgitRepo:
root of Repo
	-.rgit
		-objects
		-index
	-.git
'''
import os
import commands as cmd

class RgitRepo:
	def __init__(self, path):
		self.gitPath = path + '/.git'
		self.path = path + '/.rgit'
		self.objNamePath = self.path + '/objName'
		if not os.path.exists(self.objNamePath):
			if not os.path.exists(self.path):
				os.mkdir(self.path)
			f = open(self.objNamePath, 'w')
			f.close()

	def storeObjName(self, sha):
		f = open(self.objNamePath, 'a')
		f.write(sha + '\n')
		f.close()

	def delGitFile(self):
		status, output = cmd.getstatusoutput('rm -rf %s'%(self.gitPath))
		if status != 0:
			print 'error when delete .git directory'
			raise Exception

