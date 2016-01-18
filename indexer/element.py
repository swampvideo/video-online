import string

class Element:
	def __init__(self):
		pass

	def DivideInWords(self, element):
		"Divide element in words (FuckOff4 -> fuck off 4)"
		# (i) recerved for future use
		pass
	
	def Normalize(self, element):
		#Normalize element (Final Fantasy -> final fantasy)
		#divide in words is more powerful but..
		norm_element = element.lower()
		return norm_element