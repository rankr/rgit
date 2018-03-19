#in
import os
import platform
import ctypes
import sys

#I'm not sure if it appropriate to import this
from ObjRepo import *

def getFreeSpaceMb(folder):
    """ 
    Return folder/drive free space (in Byte)
    """
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize

def readPathFile():
	'''
	get paths specified by user to store objects
	there's a list
	'''
	ret = []
	pathFile = open('./rgitmod/index/repoPath')
	while 1:
		line = pathFile.readline()
		if not line:
			break
		ret.append(line.strip())
	return ret

def getObjPath(size):
	'''
	argu: space needed (in Byte)
	detect which path to store
	'''
	pathList = readPathFile()
	for path in pathList:
		try:
			assert(os.path.exists(path))
		except AssertionError, e:
			print e.message
			print 'path not exists'
			exit()
		else:
			freeSpace = getFreeSpaceMb(path)
 			if freeSpace > size:
 				return path
 	print 'no space left'
 	exit()
 	return ''

def shaFilePath(sha):
	'''
	find a obj's store path if exists
	'''

	pathList = readPathFile()
	for path in pathList:
		repo = ObjRepo(path)
		r = repo.objPathBySha(sha)
		if r:
			return r
	return ''

