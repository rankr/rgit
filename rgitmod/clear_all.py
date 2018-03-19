#coding: utf-8
import rpath
from ObjRepo import *

def clear_all():
	a = rpath.readPathFile()

	for i in a:
		b = ObjRepo(i)
		b.clear()
