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
import os
import shutil
import zlib

class ObjRepo:
	def __init__(self, objRepoPath):
		self.path = objRepoPath
		self.objPath = objRepoPath + '/objects'
		self.indexPath = objRepoPath + '/index'
		if not os.path.exists(self.objPath):
			os.mkdir(self.objPath)
		if not os.path.exists(self.indexPath):
			os.mkdir(self.indexPath)

	def addObjFromPath(self, sourcePath, objName):
		if not os.path.exists(sourcePath):
			print 'source not exists when adding obj to rgit objrepo'
			raise OSError
		if len(objName) != 40:
			print 'length of SHA-1 should be 40, but the given value is not'
			raise ValueError

		#move raw object into objrepo
		objDir = os.listdir(self.objPath)
		if objName[0:2] not in objDir:
			os.mkdir(self.objPath + '/' + objName[0:2])
		toSavePath = '/'.join([self.objPath, objName[0:2], objname[2:]])
		if not os.path.exists(toSavePath):
			shutil.move(sourcePath, toSavePath)

	def addObjFromContent(self, Content, objName, type):
		store = '%s %s\0%s'%(type, len(Content), Content)
		toWrite = zlib.compress(store)
		objDir = os.listdir(self.objPath)
		if objName[0:2] not in objDir:
			os.mkdir(self.objPath + '/' + objName[0:2])
		toSavePath = '/'.join([self.objPath, objName[0:2], objName[2:]])
		if not os.path.exists(toSavePath):
			file = open(toSavePath, 'w')
			file.write(toWrite)
			file.close()

