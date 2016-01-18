import MySQLdb

class Config:

	def __init__(self):
		self.db = MySQLdb.connect('localhost', 'search_engine', 'search_engine_password', 'video_catalog')
		self.config = {}
		self.y = ['VideoClass', 'SubVideoClass', 'OtherClass', 'VideoCatalogSkip', 'FromElementDel']

	def Load(self, param):
		c = self.db.cursor()
		self.config[param] = []
		for n in range(0,2):
			query = "select alias_content from scaner_config where alias_name='%s' and alias_type='%s'" % (param, n)
			c.execute(query)
			x = []
			for i in c.fetchall():
				x.append(i[0])
			self.config[param].append(x)
		return self.config
	
	def LoadAll(self):
		for i in self.y:
			self.Load(i)
		return self.config
		
		