#coding: utf-8
import sys
import random
import commands as cmd
import os
sys.path.append('../')
from rgitmod.func import getObjFromGit, cmpSha

def ifrepo_same(path1, path2):
	a = getObjFromGit(path1)
	b = getObjFromGit(path2)
	a.sort(cmpSha)
	b.sort(cmpSha)
	n = len(a)

	if n != len(b) or a != b:
		print 'test ifrepo_same: not same'
		return False

	testSha = []
	for i in xrange(0, 100):
		testSha.append(random.randint(0, n))

	rawPath = os.getcwd()
	for i in testSha:
		os.chdir(path1)
		status1, output1 = cmd.getstatusoutput('git cat-file -p %s'%(i))
		os.chdir(path2)
		status2, output2 = cmd.getstatusoutput('git cat-file -p %s'%(i))
		if status1 != 0 or status2 != 0 or output1 != output2:
			print 'test ifrepo_same: not same'
			return False
	print 'test ifrepo_same: same, yeah'
	return True

a = raw_input('path1:')
b = raw_input('path2:')
r = ifrepo_same(a, b)


