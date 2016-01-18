import string

def Load():
	cfg = {}
	cfg['servers'] = map(lambda x: string.replace(string.strip(x).lower(), "\\", ""), open("ws.txt", "r").readlines())
	cfg['threads'] = 5
	return cfg