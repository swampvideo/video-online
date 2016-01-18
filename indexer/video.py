import config, element
import re
import locale
import sys
import string


class VideoClass:
	def __init__(self):
		"initialization"
		#load configs
		#print "OTSTOYYY"
		sss = config.Config()
		self.config = sss.LoadAll()
		del sss
		self.ECache = self.load_hash("ECache")
		self.VCCache = self.load_hash("VCCache")
		self.VCSCache = self.load_hash("VCSCache")
		self.SVCCache = self.load_hash("SVCCache")
		self.OCCache = self.load_hash("OCCache")

		self.Element = element.Element()
		locale.setlocale(locale.LC_ALL, 'ru')
		self.debug_level = 0
		self.st = {}
		self.st['cr'] = 0
		self.st['ncr'] = 0
		self.st['vcc'] = 0
		self.st['vcnc'] = 0
		pass

	def __del__(self):
		#print "PIZDAAAAAAAAAAAAAAAAAAAAAa"
		b = open("ignore.txt", "r")
		c = b.readline()
		b.close()
		if c:
			print "Ignoring. Invalidating caches..."
			a = open("ignore.txt", "w")
			a.close()
			return

		self.save_hash("ECache", self.ECache)
		self.save_hash("VCCache", self.VCCache)
		self.save_hash("VCSCache", self.VCSCache)
		self.save_hash("SVCCache", self.SVCCache)
		self.save_hash("OCCache", self.SVCCache)
		
		#print "Chached req = %s, nonCached = %s" % (self.st['cr'], self.st['ncr'])
		#print "ChachedVC req = %s, nonCachedVC = %s" % (self.st['vcc'], self.st['vcnc'])

	def save_hash(self, name, hash):
		f = open(name + ".txt", "wb")
		lines = []
		for i in hash.keys():
			lines.append(str(i) + "|" + str(hash[i]) + "\n")
		f.writelines(lines)

	def load_hash(self, name):
		hash = {}
		lines = open(name + ".txt", "r").readlines()
		for i in lines:
			(key, value) = i.split("|")
			hash[key] = value.strip()
		#print "loaded %d lines" % (len(hash.keys()))
		return hash


	def out(self, string, level):
		if self.debug_level >= level :
			#sys.stdout.write(string)
			pass


	def ReMatch(self, element, pattern):
		"match the element to pattern"
		element = self.Element.Normalize(element)
		a = re.compile(pattern, re.LOCALE).search(element)
		self.out(" ->[element: %s, pattern: %s]" % (element, pattern), 2)
		if a != None:
			self.out(" ->(found: %s)\n" % [a.group()], 2)
			return 1
		else:
			self.out(" ->(not found)\n", 2)
			return 0

	def ClearList(self, list):
		"Clearing the list"
		pass

	def GetVideoClass1(self, element):
		"get the element class"
		for alias in self.config["VideoClass"]:
			if element == alias:
				return 1
		return 0


	def GetVideoClass(self, element):
		#print "GetVC"
		"get the element class"
		#print "\t getting"
		cl = 0
		if self.VCCache.has_key(element):
			self.st['vcc'] += 1
			return int(self.VCCache[element])
		self.out("element: %s" % element, 2)
		for alias in self.config["VideoClass"][0]:
			if self.ReMatch(element, alias):
				cl = 1
				self.out(" ->classefied as video",2)
				for skip in self.config["VideoClass"][1]:
					if self.ReMatch(element, skip):
						self.out(" ->video skipped",2)
						cl = 0
						self.out("\n",2)
						return 0
					else:
						cl = 1
		self.out("\n",2)
		self.VCCache[element] = str(cl)
		self.st['vcnc'] += 1
		#print "\t done"
		return cl

	def GetSubVideoClass(self, element):
		#print "Get SubVC"
		"get the element class"
		if self.SVCCache.has_key(element):
			return int(self.SVCCache[element])

		cl = 0
		self.out("element: %s" % element, 2)
		for alias in self.config["SubVideoClass"][0]:
			if self.ReMatch(element, alias):
				cl = 1
				self.out(" ->classefied as SUBvideo",2)
				for skip in self.config["SubVideoClass"][1]:
					if self.ReMatch(element, skip):
						self.out(" ->SUBvideo skipped",2)
						cl = 0
						self.out("\n",2)
						return 0
					else:
						cl = 1
		self.out("\n",2)
		self.SVCCache[element] = str(cl)
		return cl

	def GetOtherClass(self, element):
		"get the element class"
		#print "Get Other"
		#print "[Getting Video Class (%s)]" % element.encode("cp866")
		if self.OCCache.has_key(element):
			return int(self.OCCache[element])

		cl = 0
		self.out("element: %s" % element, 2)
		for alias in self.config["OtherClass"][0]:
			if self.ReMatch(element, alias):
				cl = 1
				self.out(" ->classefied as Other",2)
				for skip in self.config["OtherClass"][1]:
					if self.ReMatch(element, skip):
						self.out(" ->Other Class skipped",2)
						cl = 0
						self.out("\n",2)
						return 0
					else:
						cl = 1
		self.out("\n",2)
		self.OCCache[element] = str(cl)
		return cl

	def GetVideoCatalogSkip(self, element):
		"get the element class"
		#print "Get VCS"
		cl = 0
		self.out("element: %s" % element, 2)

		if self.VCSCache.has_key(element):
			return int(self.VCSCache[element])


		for alias in self.config["VideoCatalogSkip"][0]:
			if self.ReMatch(element, alias):
				cl = 1
				self.out(" ->classefied as VideoCatalogSkip",2)
				for skip in self.config["VideoCatalogSkip"][1]:
					if self.ReMatch(element, skip):
						self.out(" ->VideoCatalogSkip skipped",2)
						cl = 0
						self.out("\n",2)
						return 0
					else:
						cl = 1
		self.out("\n",2)
		#print "Done VCS"
		self.VCSCache[element] = str(cl)
		return cl

	def del_space(self, element):
		#print "Del_Space"
		res = [';', '_', '-', '>', '<', '!', '&', '$', '%', '^', "'", "+", ".", ",", "@",")","(","=", "]", "["]
		for i in res:
			element = string.replace(element, i, ' ')
		while 1:
			x = element
			element = string.replace(element, '  ', ' ')
			if x == element:
				break
			
		return element
		
	
	def proc_el(self, element, pattern):
		#print "ProcEl"
		#res = re.compile("\([\w\s]*\)", re.LOCALE).findall(element)
		res = re.compile(pattern, re.LOCALE).findall(element)
		if res:
			for i in res:
				element = string.replace(element, i, '')
		return element

	def ClearElement(self, element):
		#element = self.del_skobki(element)
		#print "Clear"
		if self.ECache.has_key(element):
			self.st['cr'] += 1
			return self.ECache[element]
		
		self.st['ncr'] += 1
		cl = 0
		old_element = element
		element = element.lower()
		element = self.del_space(element)
		for pattern in self.config["FromElementDel"][0]:
			element = self.proc_el(element, pattern)
		element = string.strip(element)
		self.ECache[old_element] = element
		return element
	
	def Test(self, element):
		for i in self.config.keys():
			print i, len(self.config[i])
		print self.Element.Normalize(element)

#a = VideoClass()
#print a.del_space("->Fight Club (film) DVD QUALITY-<")
#print [a.ClearElement("The_Best__Of___ The   Best+++ !!! (ахуенное кино) DVD quality ")]