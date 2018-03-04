'''
file where rgit store objects for rgit repos -- defined as obj-repo
users can specify many files
structure of obj-repo directory:
root
	-objects
		-many directories with begining two char of objects
	-index
		-some files to speed up
'''
#from rgitmodindex import index
import os
import shutil
import zlib

class ObjRepo:
	'''
	now it use filesystem to store objs, I'll modify it soon
	'''
	def __init__(self, objRepoPath):
		self.path = os.path.abspath(objRepoPath)
		self.objPath = objRepoPath + '/objects'
		self.indexPath = objRepoPath + '/index'
		if not os.path.exists(self.objPath):
			os.mkdir(self.objPath)
			for i in xrange(0, 256):
				dirname = hex(i/16)[2] + hex(i%16)[2]
				os.mkdir(self.objPath + '/' + dirname)
				for j in xrange(0, 256):
					filename = hex(j/16)[2] + hex(j%16)[2]
					os.mkdir(self.objPath + '/' + dirname + '/' + filename)
		if not os.path.exists(self.indexPath):
			os.mkdir(self.indexPath)

	def addObjFromPath(self, sourcePath, objName):
		if not os.path.exists(sourcePath):
			print 'source not exists when adding obj to rgit objrepo'
			raise OSError
		if len(objName) != 40:
			print 'length of SHA-1 should be 40, but the given value is not'
			raise ValueError
		if self.findObjBySha(objName):
			return 0

		#move raw object into objrepo
		toSavePath = '/'.join([self.objPath, objName[0:2], objname[2:4], objname[4:]])
		shutil.move(sourcePath, toSavePath)

	def addObjFromContent(self, Content, objName, type):
		if self.findObjBySha(objName):
			return 0
		store = '%s %s\0%s'%(type, len(Content), Content)
		toWrite = zlib.compress(store)

		toSavePath = '/'.join([self.objPath, objName[0:2], objName[2:4], objName[4:]])
		file = open(toSavePath, 'w')
		file.write(toWrite)
		file.close()
		return 1

	def findObjBySha(self, sha):
		if os.path.exists("%s/%s/%s/%s"%(self.objPath, sha[0:2], sha[2:4], sha[4:])):
			return 1
		return 0

	def objPathBySha(self, sha):
		p = "%s/%s/%s/%s"%(self.objPath, sha[0:2], sha[2:4], sha[4:])
		if os.path.exists(p):
			return p
		return ''


