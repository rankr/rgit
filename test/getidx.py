#coding: utf-8
from rgitmod import absorb
import time
import sys

def testgetidx():
	path = '/Users/file4/ijkplayer'
	a = time.time()
	for i in xrange(0, 100):
		res1 = absorb.getObjFromGit(path)
	b = time.time()
	
	print 'path is %s, getObjFromGit time is %f'%(path, b-a)

