import config, element
import re
import locale
import sys
import string


class VideoClass:
	def __init__(self):
		"initialization"
		#load configs
		self.config = config.Config().LoadAll()
		self.Element = element.Element()
		locale.setlocale(locale.LC_ALL, 'ru')
		self.debug_level = 0
		pass

	def out(self, string, level):
		if self.debug_level >= level :
			sys.stdout.write(string)


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
		"get the element class"
		#print "\t getting"
		cl = 0
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
		#print "\t done"
		return cl

	def GetSubVideoClass(self, element):
		"get the element class"
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
		return cl

	def GetOtherClass(self, element):
		"get the element class"
		print "[Getting Video Class (%s)]" % element.encode("cp866")
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
		return cl

	def GetVideoCatalogSkip(self, element):
		"get the element class"
		cl = 0
		self.out("element: %s" % element, 2)
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
		return cl

	def del_space(self, element):
		res = ['_', '-', '>', '<', '!', '&', '$', '%', '^', "'", "+", ".", ","]
		for i in res:
			element = string.replace(element, i, ' ')
		while 1:
			x = element
			element = string.replace(element, '  ', ' ')
			if x == element:
				break
			
		return element
		
	
	def proc_el(self, element, pattern):
		#res = re.compile("\([\w\s]*\)", re.LOCALE).findall(element)
		res = re.compile(pattern, re.LOCALE).findall(element)
		if res:
			for i in res:
				element = string.replace(element, i, '')
		return element

	def ClearElement(self, element):
		#element = self.del_skobki(element)
		cl = 0
		element = element.lower()
		element = self.del_space(element)
		for pattern in self.config["FromElementDel"][0]:
			element = self.proc_el(element, pattern)
		element = string.strip(element)
		return element
	
	def Test(self, element):
		for i in self.config.keys():
			print i, len(self.config[i])
		print self.Element.Normalize(element)

#a = VideoClass()
#print a.del_space("->Fight Club (film) DVD QUALITY-<")
#print [a.ClearElement("The_Best__Of___ The   Best+++ !!! (ахуенное кино) DVD quality ")]