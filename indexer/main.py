import video
import smb_client
import time
import os
import sys
import string
import cfg_file
import re
import locale
import database
import list_ws

locale.setlocale(locale.LC_ALL, 'ru')

debug_level = 1
def out(string, level):
	if debug_level >= level :
		sys.stdout.write(string)



class NetworkLister:
	def __init__(self, server):
		self.working_share = ''
		self.working_server = server
		self.working_path = ''
		self.total_files = 0
		self.total_dirs = 0
		self.recoursion_count = 0
		self.error_count = 0
		self.shares = 0
		self.start_time = time.time()
		self.video = video.VideoClass()
		self.good = 0
		self.speed_checked = 0

		self.run()

	def run(self):
		out("%s" % self.working_server, 2)
		shares = smb_client.GetSharesList(self.working_server)#Get list of server shares
		if shares:                                           #Server have shares
			self.shares = len(shares)
			out("\n", 2)
			self.do_shares(shares)                           #Process shares
		else:                                                #No shares or server inaccessable
			out("\t[no server]\n", 2)
			pass

	def do_shares(self, shares):
		global g
		for share in shares:
			self.working_share = share
			self.working_path = share
			if self.video.GetVideoClass(share.lower()):
				out("\t{%s}\n" % share, 2)
				self.VideoProcessor(share)
				#self.do_path(share)
	
	def ListClear(self, list, path):
		'sdf'
		#out("[%s]" % list, 2)
		full_path = "//" + self.working_server + "/" + path
		t = []
		for i in list:
			if self.video.GetVideoClass(i.lower()):
				if not os.path.isfile(full_path + "/" + i):
					t.append(i)
	
		if len(t) > 0:
			return t
		else:
			return list

	def check_speed(self, element, path):
		global speeds
		if self.speed_checked:
			return
		try:
			speeds[self.working_server] = 'hz'
			full_path = "//" + self.working_server + "/" + path + "/" + element
			el = smb_client.GetDirList(full_path)
			if el:
				element = full_path + "/" +  el[0]
			else:
				return
			test_file = open(element, 'rb')
			speed = 0
			done = 0
			while not done:
				t1 = time.time()
				test_file.read(1000000)
				t2 = time.time()
				dt = t2 - t1
				if dt:
					speed = speed + 1 / dt
					done = 1

			speed_a = speed

			if speed <= 0.3:
				index = 0
			elif speed > 0.3 and speed <= 1:
				index = 1
			else:
				index = 2
			
			if speed > 1:
				speed = "%1.1f Mb/s" % speed
			else:
				speed = "%d kb/s" % (speed * 1000)
			speeds[self.working_server] = [speed, index, speed_a]
			test_file.close()
			self.speed_checked = 1
		except:
			pass

	def GetAll(self):
		return self.good
	
	def add_film(self, element, path):
		global films
		work_name = self.video.ClearElement(element)
		if not films.has_key(work_name):
			films[work_name] = []
		films[work_name].append([self.working_server, path, element])
			
	def VideoProcessor(self, path):
		'kgkdflgkdf'
		pizda = 0
		full_path = "//" + self.working_server + "/" + path
		content_list = smb_client.GetDirList(full_path)
		#out("[%s]" % content_list, 2)
		#out("[%s]" % content_list, 2)
		
		if content_list:
			#tipa tipa opa		
			content_list = self.ListClear(content_list, path)
			for element in content_list:
				out("[%s]" % element, 4)
				
				#if pizda:
				#	break

				if os.path.isfile(full_path + "/" + element):
					out(" -> skipped (as file)\n", 4)
					pass

				elif self.video.GetVideoClass(element.lower()):
					#sdsd
					out(" -> video class\n", 4)
					self.VideoProcessor(path + "/" + element)
					#pizda = 1
				
				elif self.video.GetSubVideoClass(element.lower()):
					#sub video class
					out(" -> Sub video class\n", 4)
					self.VideoProcessor(path + "/" + element)
				
				elif self.video.GetOtherClass(element.lower()):
					#other class
					out(" -> other class\n", 4)
					pass
				
				elif self.video.GetVideoCatalogSkip(element.lower()):
					#asasddas
					out(" -> skipped\n", 4)
					pass
				
				#elif len(smb_client.GetDirList(full_path + "/" + element)) > 5:
				#	#content size lower than five
				#	out(" -> too many elements\n", 4)
				#	pass

				else:
					#ahuenna
					self.add_film(element, path)
					self.check_speed(element, path)
					self.good = self.good + 1
					out(" -> normal", 4)
					#out("%s\n" % element, 2)
					out("\t[%s]\n" % self.video.ClearElement(element), 2)
					#out("\t\t\t\t[%s]\n" % len(smb_client.GetDirList(full_path + "/" + element)), 2)



# ============= entry point

open('logging.txt', 'a+').write('Started at %s\n' % (time.asctime(time.localtime(time.time()))))
times = 0
start_up_time = time.time()
print "***********************************"
times = times + 1
good = 0
films = {}
speeds = {}
start_time = time.time()
#list_ws.make_list()
Config = cfg_file.Load()
#Config['servers'] = ['beetle']
print
print "Working network (%s)..." % times
print "\tservers: %s" % len(Config['servers'])
total_servers = len(Config['servers'])
done = 0
for i in Config['servers']:
	if i == 'absence-pc':
		continue
	lister = NetworkLister(i)
	done = done + 1
	percent = int((float(done) / total_servers) * 100)
	up_time = int(time.time() - start_up_time)
	log = open('log.txt', 'w')
	log.write("%s::%s::%s::%s::%s::%s" % (i, percent, good, total_servers, up_time, times))
	log.close()
	out("\tdone: %s [%s]              \r" % (done,i), 0)
	
	if lister.GetAll():
		good = good + 1
out("\tdone: all             \n", 0)
print "\ttime(sec): %s" % (int(time.time() - start_time))
print "\tvideo: %s" % good
print
database.database(films, speeds)
print "Sleeping..."
#time.sleep(300)
print

#drawing speed table
#for i in speeds.keys():
#	print i, speeds[i]



