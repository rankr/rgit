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
	
	a = time.time()
	for i in xrange(0, 100):
		res2 = absorb.getObjFromGit2(path)
	b = time.time()
	
	print 'path is %s, getObjFromGit2 time is %f'%(path, b-a)

	w1 = open('test/getidx1.txt' ,'w')
	w1.write('\n'.join(res1))
	w1.close()
	w2 = open('test/getidx2.txt' ,'w')
	w2.write('\n'.join(res2))
	w2.close()
