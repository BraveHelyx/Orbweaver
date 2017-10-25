#!/usr/bin/python

# Keeps track of the surface area of a recon investigation.
class Surface:
	def __init__(self):
		self.reqDict = {} # reqDict[URL] = rqObj
		self.surface = [] # All Local URLs

	# Will also ignore duplicate adds
	def add_surface(self, url):
		self.surface.append(url)
		self.surface = list(sorted(set(self.surface)))

	def add_rq_response(self, rqObj, target):
		self.reqDict[target] = rqObj

	def get_surface(self):
		return self.surface

	def get_requests(self):
		return self.reqDict

	# Returns number of new nodes
	def assimilate_list(self, targets):
		oldLen = len(self.surface)
		for target in targets:
			self.add_surface(target)
		newLen = len(self.surface)
		return newLen - oldLen

	def get_pending(self):
		keys = self.reqDict.keys()
		pending = []
		for url in self.surface:
			if url not in keys:
				pending.append(url)
		return pending

def print_requests(surface):
	out = ''
	reqs = surface.get_requests()
	for key in reqs.keys():
		if key != reqs[key].url:
			out += '\t['
			out += str(reqs[key].status_code)
			out += '] - '
			out += key
			out += ' -> '
			out += reqs[key].url
		else:
			out += '\t['
			out += str(reqs[key].status_code)
			out += '] - '
			out += key
		out += '\n'
	print "Requests:\n%s" % out.rstrip('\n')

def print_pending(surface):
	out = ''
	i = 0
	for url in surface.get_pending():
		out += '[' + str(i) + ']\t'
		out += url
		out += '\n'
		i += 1
	print "%s" % out

# Old Functions
def append_rqobj(request, responses):
	responses.append(request)

def append_valid_rqobj(request, valid):
	if request.status_code == 200:
		valid.append(request)

def catalogue_response(request, res, valid):
	append_rqobj(request, res)
	append_valid_rqobj(request, valid)

