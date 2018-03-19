#coding: utf-8

import os
import commands
from time import time
import commands as cmd

opath = "/Users/file4/毕设/testZone/redis"

#换不同的absorb然后进行时间的比较

from rgitmod import absorb
from rgitmod import clear_all

clear_all.clear_all()

src = "/Users/file4/redis"

'''
a = time()
absorb.absorb(opath)
b = time()
clear_all.clear_all()
print "time of absorb: ", b - a

#result of absorb: 1739.1521492s
'''
'''
cmd.getstatusoutput("rm -rf /Users/file4/毕设/testZone/redis")
cmd.getstatusoutput("cp -r /Users/file4/redis /Users/file4/毕设/testZone/redis")
a = time()
absorb.absorb1(opath)
b = time()
clear_all.clear_all()
print "time of absorb1: ", b - a
#result of absorb1: 1666.12460899
'''

cmd.getstatusoutput("rm -rf /Users/file4/毕设/testZone/redis")
cmd.getstatusoutput("cp -r /Users/file4/redis /Users/file4/毕设/testZone/redis")
a = time()
absorb.absorb2(opath)
b = time()
clear_all.clear_all()
print "time of absorb2: ", b - a
'''
710.064494848
'''


cmd.getstatusoutput("rm -rf /Users/file4/毕设/testZone/redis")
cmd.getstatusoutput("cp -r /Users/file4/redis /Users/file4/毕设/testZone/redis")
