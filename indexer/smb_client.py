import smb, nmb
import thread
import os
import time

class nb:
	def __init__(self, host, user, passwd, timeout):
		self.host = host
		self.user = user
		self.passwd = passwd
		self.timeout = timeout
		self.check = 0.1
		self.done = 0
		self.shares = []
		self.error = 0
		thread.start_new_thread(self.thr, ())
	
	def thr(self):
		try:
			conn = smb.SMB(self.host, self.host, my_name = '172.16.128.100', host_type = nmb.TYPE_SERVER, sess_port = nmb.NETBIOS_SESSION_PORT)
			conn.login(self.user, self.passwd, '', timeout = 1)
			s_list = conn.list_shared()
			for s in s_list:
				if s.get_type() == 0:
					self.shares.append(s.get_name())
			self.done = 1
		except:
			self.error = 1

	def get_share(self):
		for i in range(0, self.timeout/self.check):
			if self.done:
				return self.shares
			elif self.error:
				return 0
			else:
				time.sleep(self.check)
		return 0 #ping timeout

def GetSharesList(server):
	shar = []
	o = nb(server, 'guest', '', 30)
	shares = o.get_share()
	del o
	return shares



def GetDirList(path):
	try:
		return os.listdir(path)
	except:
		return 0

