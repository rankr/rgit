#coding: utf-8
'''
some general functions
'''
import os
import Queue

def dirSize(dirPath):
	'''
	ret in Byte
	'''
	if not os.path.isdir(dirPath):
		return -1
	q = Queue.Queue()
	q.put(dirPath)
	res = 0
	while not q.empty():
		a = q.get()
		b = os.listdir(a)
		for i in b:
			c = a+'/'+i
			if os.path.isdir(c):
				q.put(c)
			elif os.path.isfile(c):
				res += os.path.getsize(c)
			else:
				print c,'is not file or dir'
	return res