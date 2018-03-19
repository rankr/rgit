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
from func import read_number_from_file, read_chunk_from_pack

MSBBIT = 1<<31

class OBJECT:
	def __init__(self, sha = '', type = '', raw_data = '', offset = -1, header_len = -1):
		self.sha1 = sha
		self.type = type
		self.raw_data = raw_data
		self.offset = offset #offset in packfile
		self.header_len = header_len #header_len in packfile

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

	def clear(self):
		a = raw_input("Are you sure to delete all the objs in Repo: %s ?"%(self.path))
		if not len(a) or  a.lower()[0]!='y':
			return
		a = raw_input("Really to delete all the objs in Repo: %s ?"%(self.path))
		if not len(a) or  a.lower()[0]!='y':
			return

		for i in xrange(0, 256):
			dirname = hex(i/16)[2] + hex(i%16)[2]
			for j in xrange(0, 256):
				filename = hex(j/16)[2] + hex(j%16)[2]
				dir_path = self.objPath + '/' + dirname + '/' + filename
				dirs = os.listdir(self.objPath + '/' + dirname + '/' + filename)
				for k in dirs:
					os.remove('/'.join([dir_path, k]))


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
		if len(objName) != 40:
			print 'length of SHA-1 should be 40, but the given value is not'
			raise ValueError
		store = '%s %s\0%s'%(type, len(Content), Content)
		toWrite = zlib.compress(store)

		toSavePath = '/'.join([self.objPath, objName[0:2], objName[2:4], objName[4:]])
		file = open(toSavePath, 'w')
		file.write(toWrite)
		file.close()
		return 1

	def addObjFromRawContent(self, rawContent, objName, type = 'blob'):
		if self.findObjBySha(objName):
			return 0
		if len(objName) != 40:
			print 'length of SHA-1 should be 40, but the given value is not'
			raise ValueError
		toWrite = rawContent

		toSavePath = '/'.join([self.objPath, objName[0:2], objName[2:4], objName[4:]])
		file = open(toSavePath, 'w')
		file.write(toWrite)
		file.close()
		return 1

	def addObjFromPack(self, idxPath, packPath):
		f_idx = open(idxPath, 'rb')
		f_idx.seek(4*257)

		#I dnt know if it's little endian
		obj_num = read_number_from_file(f_idx, 4)
		obj_list = []
		for i in xrange(0, obj_num):
			j = ""
			for k in xrange(0, 20):
				a = hex(ord(f_idx.read(1)))[2:]
				if len(a)==1:
					a = '0' + a
				j = j + a
			obj_list.append(j)

		f_idx.seek(4*258 + 24*obj_num, 0)
		#if offset is negative, then the offset is in layer5 not in layer4
		obj_offset_list = []
		layer5_list = []

		for i in xrange(0, obj_num):
			j = read_number_from_file(f_idx, 4)
			if not j&MSBBIT:
				obj_offset_list.append(j&(~MSBBIT))
			else:
				obj_offset_list.append(-1)
				layer5_list.append((i, j))

		def cmp_second(x, y):
			if x[1]>y[1]:
				return 1
			if x[1]<y[1]:
				return -1
			return 0
		layer5_list.sort(cmp_second)

		for index, offset_of_layer5 in layer5_list:
			obj_offset_list[index] = read_number_from_file(f_idx, 8, bigendian = False)

		f_idx.close()

		#now the offset of obj in packfile are well
		#I've prove the base object is before the deltaed object

		f_pack = open(packPath, 'rb')
		f_pack.seek(12, 0)
		
		obj_list = zip(obj_list, obj_offset_list)
		obj_list.sort(cmp_second)

		obj_hash = {}
		off2sha = {}
		for i, j in obj_list:
			#not need to store sha in offset
			obj_hash[i] = OBJECT(offset = j)
			obj_hash[i].sha = i
			off2sha[j] = i

		def handle_delta(string, idx, base_obj):
			string = zlib.decompress(string[idx:])
			tail_idx = len(string)
			#read two var-len int first
			idx = 0
			i = 7
			a = ord(string[idx])
			idx += 1
			src_size = a&0x7f
			while a&0x80:
				a = ord(string[idx])
				src_size |= (a&0x7f)<<i
				i += 7
				idx += 1
			if src_size != len(base_obj.raw_data):
				if src_size != len(base_obj.raw_data).size - 1 or base_obj.raw_data[-1] != "\n":
					print "Error in addObjFromPack:handle_delta: src_size != input_obj_size"
					print "former is %d, latter is %d"%(src_size, len(base_obj.raw_data))
					exit()

			tar_size = 0
			i = 0
			while True:
				#read two var-len int first
				a = ord(string[idx])
				tar_size |= (a&0x7f)<<i
				i += 7
				idx += 1
				if not a&(0x80):
						break
			#now deal with copy and insert command
			tar_data = ''
			while idx < tail_idx:
				a = ord(string[idx])
				idx += 1
				if a&(0x80):#copy
					offset = 0
					copy_len = 0
					if a&(1):
						offset = ord(string[idx])
						idx += 1
					if a&(2):
						offset |= ord(string[idx])<<8
						idx += 1
					if a&(4):
						offset |= ord(string[idx])<<16
						idx += 1
					if a&(8):
						offset |= ord(string[idx])<<24
						idx += 1
					if a&(0x10):
						copy_len = ord(string[idx])
						idx += 1
					if a&(0x20):
						copy_len |= ord(string[idx])<<8
						idx += 1
					if a&(0x40):
						copy_len |= ord(string[idx])<<16
						idx += 1
					if copy_len==0:
						copy_len = 0x10000
					
					tar_data += base_obj.raw_data[offset : offset + copy_len]
				else:#insert
					tar_data += string[idx:idx+a]
					idx += a
				if idx > tail_idx:
					print 'error in handle_delta, idx is bigger than string:\
 idx is %d, tail_idx is %d'%(idx, tail_idx)
					exit()
			return tar_data

		ret = []
		for i in xrange(0, len(obj_list)):
			#the type of base object and deltaed object is the same
			compressed_data = ''
			if i != len(obj_list) - 1:
				read_len = obj_list[i+1][1] - obj_list[i][1]
			else:
				read_len = -1

			obj_type, to_process, header_len = read_chunk_from_pack(f_pack, read_len)

			if obj_type == "ofs_delta":
				j = 1
				a = ord(to_process[0])
				base_real_offset = a&0x7f
				while a&0x80:#from the source code of git
					a = ord(to_process[j])
					base_real_offset = ((base_real_offset + 1)<<7) | (a&(0x7f))
					j += 1

				fk = off2sha.keys()
				fk.sort()
				base_obj_sha1 = off2sha[obj_list[i][1] - base_real_offset]
				obj_type = obj_hash[base_obj_sha1].type
				tar_data = handle_delta(to_process, j, obj_hash[base_obj_sha1])
			elif obj_type == "ref_delta":
				base_obj_sha1 = ''
				for k in xrange(0, 20):
					a = hex(ord(to_process[k]))[2:]
					if len(a)==1:
						a = '0' + a
					base_obj_sha1 = base_obj_sha1 + a
				obj_type = obj_hash[base_obj_sha1].type
				tar_data = handle_delta(to_process, 20, obj_hash[base_obj_sha1])
			elif obj_type == "not exists":
				print ("Error in addObjFromPack, objType is not exists")
				exit()
			else:
				tar_data = zlib.decompress(to_process)
			obj_hash[obj_list[i][0]].type = obj_type
			obj_hash[obj_list[i][0]].raw_data = tar_data
			obj_hash[obj_list[i][0]].header_len = header_len

		f_pack.close()

		for i in obj_hash:
			i = obj_hash[i]
			self.addObjFromContent(i.raw_data, i.sha, i.type)
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


