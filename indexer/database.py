import MySQLdb
import re
import string

class database:
	"store finded data to database"

	def __init__(self, data, speeds):
		self.db = MySQLdb.connect('127.0.0.1', 'radm', 'vfqjytP', 'video_catalog')
		self.cursor = self.db.cursor()
		self.speeds = speeds
		self.data = data
		self.new_elements = 0
		self.old_elements  = 0
		self.added_elements = 0
		self.deleted_elements = 0
		self.Store()

	def present_in_catalog(self, film):
		self.cursor.execute("select film_id from video_catalog where film_id = '%s'" % film)
		film_id = self.cursor.fetchone()
		if film_id:
			return 1
		else:
			return 0

	
	def get_film_id(self, element):
		self.cursor.execute("select film_id from films_aliases where alias = '%s'" % element)
		film_id = self.cursor.fetchone()
		if film_id:
			return film_id[0]
		else:
			return 0

	def Store(self):
		print "Database working ..."
		self.cursor.execute('LOCK TABLES films_aliases WRITE, films_locations WRITE, new_elements WRITE')
		#self.clear_catalog()
		self.cursor.execute("delete from films_locations")
		self.cursor.execute("delete from new_elements")


		query_1 = "insert into films_locations (film_id, workstation, path, element, speed, speed_index, speed_a) values\n"
		query_2 = "insert into new_elements (element_name, element_locations) values\n"
		f_1 = f_2 = 0

		for element in self.data.keys():
			film_id = self.get_film_id(element)
			if film_id:
				self.added_elements = self.added_elements + 1
				#alias found, insert element to catalog
				#todo:
				#	check ctalog, pc dont scan - pass this element, else kill'em
				#	drop locations for dropped catalog elements
				#if not self.present_in_catalog(film_id):
				#	#dot't present -> add
				#	self.cursor.execute("insert into video_catalog (film_id) values('%s')" % film_id)
				#self.cursor.execute("delete from films_locations where film_id = '%s'" % film_id)
				for location in self.data[element]:

					if f_1:
						query_1 = query_1 + ","
					#self.cursor.execute("insert into films_locations (film_id, workstation, path, element) values('%s', '%s', '%s', '%s')" % (film_id, location[0], location[1], re.escape(location[2])))
					query_1 = query_1 + "('%s', '%s', '%s', '%s', '0', '0', '0')\n" % (film_id, re.escape(location[0]), re.escape(location[1]), re.escape(location[2]))
					f_1 = 1

			else:
				#alias not found - copy element(only) into 'new' table
				loc = ""
				for i in self.data[element]:
					loc = loc + i[0] + " "
				if f_2:
					query_2 = query_2 + ","
				query_2 = query_2 + "('%s', '%s')\n" % (re.escape(element), re.escape(loc.lower()))
				f_2 = 2
				#self.cursor.execute("insert into new_elements (element_name, element_locations) values('%s', '%s')" % (element, re.escape(loc.lower())))
				self.new_elements = self.new_elements + 1
				#print "insert into new_elements (element_name) values('%s')" % (element)
				#insert_id()
				#for location in self.data[element]:
				#	print ("insert into films_locations (film_id, workstation, path, element) values('%s', '%s', '%s', '%s')" % (film_id, location[0], location[1], location[2]))

		query_1 = query_1 + ";"
		query_2 = query_2 + ";"
		print query_1
		print "========"
		print query_2
		#self.cursor.execute(query_1)
		#self.cursor.execute(query_2)
		#open('asdadasd.txt', 'w').write(query)
		
		#done
		self.cursor.execute('UNLOCK TABLES')
		print "\taliased: %s\n\told: %s\n\tunaliased: %s\n\tdel: %s" % (self.added_elements, self.old_elements, self.new_elements, self.deleted_elements)

	def film_location_pcs(self, film):
		wc = []
		self.cursor.execute("select * from films_locations where film_id = '%s'" % (film))
		for loc in self.cursor.fetchall():
			wc.append(loc[2])
		return wc


	def film_location_pcs_new(self):
		wc = []
		for element in self.data.keys():
			for paths in self.data[element]:
				wc.append(paths[0])
		return wc

	def scanned(self, film):
		for scanned_pc in self.film_location_pcs_new():
			for film_pc in self.film_location_pcs(film):
				if scanned_pc == film_pc:
					#delete location for this pc from locations table
					#but one computr not scanned leave element in catalog
					return 1
		return 0

	def clear_catalog(self):
		a = 0
		self.cursor.execute("delete from new_elements") #delete unknowns (cash)
		self.cursor.execute("select * from video_catalog")
		for el in self.cursor.fetchall():
			for element in self.data.keys():
				a = 0
				if el[1] == self.get_film_id(element):
					#catalog element in new found list -> pass (don't drop) catalog element
					#only edit locations
					#self.cursor.execute("delete from films_locations where film_id = '%s'" % el[1])
					#print "delete from films_locations where film_id = '%s'" % el[1]
					#print "film %s present in the catalog, leave'em" % element
					self.old_elements = self.old_elements + 1
					self.cursor.execute("delete from films_locations where film_id = '%s'" % el[1])
					a = 1 #found
					break

			if not a:
				#catalog element not found in the new list
				if self.scanned(el[1]):
					#and if pc scanned seccess -> film is dead, drop it
					#else don't drop
					self.cursor.execute("delete from video_catalog where film_id = '%s'" % el[1])
					self.cursor.execute("delete from films_locations where film_id = '%s'" % el[1])
					#print "film %s not found again, and pc is scanned, drop'em" % el[1]
					self.deleted_elements = self.deleted_elements + 1
					pass
