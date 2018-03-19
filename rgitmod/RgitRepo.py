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
import shutil
from func import cmpSha
import rpath


'''
structure to store what obj one repo have
.rgit
	-00
		00.sha
		01.sha
		...
		ff.sha
	-01
	...
	-ff
'''
class RgitRepo:
	def __init__(self, path):
		self.gitPath = path + '/.git'
		self.path = path + '/.rgit'
		if not os.path.exists(self.path):
			os.mkdir(self.path)
			for i in xrange(0, 256):
				dirname = hex(i/16)[2] + hex(i%16)[2]
				os.mkdir(self.path + '/' + dirname)
				for j in xrange(0, 256):
					filename = hex(j/16)[2] + hex(j%16)[2]
					f = open('%s/%s/%s'%(self.path, dirname, filename), 'w')
					f.close()

	def storeObjSha(self, sha):
		'''
		ret 0: already exists, so not insert
		ret 1: insert successfully
		ret -1: other
		'''
		print 'sha is',sha
		dirname = sha[0:2]
		filename = sha[2:4]
		sha = sha[4:]

		finalPath = "%s/%s/%s"%(self.path, dirname, filename)
		f = open(finalPath, 'r')
		shaArr = [x.strip() for x in f.readlines()]
		f.close()

		if sha in shaArr:
			return 0
		else:
			f = open(finalPath, 'a')
			f.write(sha + '\n')
			f.close()
			return 1

	def storeObjSha_lot(self, ShaArr):
		'''
		ret 1: insert successfully
		ret -1: other
		'''
		n = len(ShaArr)
		print 'n is',n
		if n < 20000:
			for i in ShaArr:
				res = self.storeObjSha(i)
				if res == -1:
					return -1
			return 1

		ShaArr.sort(cmpSha)#ascend now
		print ShaArr[0:10]
		#when len(ShaArr) > 200
		for i in xrange(255, -1, -1):
			dirname = hex(i/16)[2] + hex(i%16)[2]

			for j in xrange(255, -1, -1):
				filename = hex(j/16)[2] + hex(j%16)[2]
				prefix = dirname + filename
				if not ShaArr:
					return 1

				if ShaArr[-1][0:4] != prefix:
					continue
				nowPath = "%s/%s/%s"%(self.path, dirname, filename)
				f = open(nowPath)
				fileCont = [x.strip() for x in f.readlines()]
				f.close()

				while ShaArr and ShaArr[-1][0:4] == prefix:
					fileCont.append(ShaArr.pop()[4:])
				fileCont = list(set(fileCont))
				f = open(nowPath, 'w')
				f.writelines([x + '\n' for x in fileCont])
				f.close()
		return 1


	def delGitFile(self):
		status, output = cmd.getstatusoutput('rm -rf %s/%s'%(self.gitPath, 'objects'))
		if status != 0:
			print 'error when delete .git directory'
			raise Exception

	def getAllSha(self):
		ret = []

		for i in xrange(0, 256):
			dirname = hex(i/16)[2] + hex(i%16)[2]
			if not os.path.exists(self.path + '/' + dirname):
				os.mkdir(self.path + '/' + dirname)
			for j in xrange(0, 256):
				filename = hex(j/16)[2] + hex(j%16)[2]
				f = open('%s/%s/%s'%(self.path, dirname, filename))
				ret += [ dirname + filename + x.strip() for x in f.readlines()]
		return ret

	def createGit(self):
		if not os.path.exists(self.gitPath):
			os.mkdir(self.gitPath)
			os.mkdir(self.gitPath + '/objects')


	def insertObj_lot(self, shaArr):
		'''
		this should be modified to improve efficiency
		'''
		pass
		return -1
		self.createGit()
		for i in shaArr:
			self.insertObj(i)

	def insertObj(self, sha):
		p = rpath.shaFilePath(sha)
		if not p:
			print "repo wrecked, obj %s is disappeared"%(sha)
			raise ValueError
		storePath = "%s/%s/%s"%(self.gitPath, 'objects', sha[0:2])
		if not os.path.exists(self.gitPath + '/objects'):
			os.mkdir(self.gitPath + '/objects')
		if not os.path.exists(storePath):
			os.mkdir(storePath)
		shutil.copy(p, storePath + '/' + sha[2:])





