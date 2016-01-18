import win32net
import win32netcon
import string



def make_list():
	(dict, total, handle) = win32net.NetServerEnum(None, 100 , win32netcon.SV_TYPE_ALL , None , 0)
	f = open('ws.txt', 'wb')
	for i in dict:
		f.write(i['name'].lower()+ "\n")
	f.close()
	return