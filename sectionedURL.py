#!/usr/bin/python

import re

class SectionedURL:
	def __init__(self):
		self.proto = ''
		self.hostName = ''
		self.filePath = ''

	# <PROTO>://<HOSTNAME><FILEPATH>
	# http://www.example.com/file/1.jpg
	def url(self):
		return self.proto + '://' + self.hostName + self.filePath

	# <PROTO>
	# http
	def protocol(self):
		return self.proto

	# <HOSTNAME>
	# www.example.com
	def hostname(self):
		return self.hostName

	# <PROTO>://<HOSTNAME>
	# http://www.example.com
	def server(self):
		# outStr = self.proto + "://" + self.hostName
		return self.proto + "://" + self.hostName

	def set_protocol(self, newProto):
		self.proto = newProto

	def set_hostname(self, newHostName):
		self.hostName = newHostName

	def set_filepath(self, newFilePath):
		self.filePath = newFilePath

	def filepath(self):
		return self.filePath

	def print_values(self):
		print "[SectionedURL]\n\tProtocol: %s\n\tHostname: %s\n\tFile Path: %s\n" % (self.proto, self.hostName, self.filePath)

def section_url(url):
	sUrl = SectionedURL()

	# Let's capture the protocol first
	protoPattern = "^(.*)://"
	rePattern = re.compile(protoPattern)
	res = rePattern.search(url)

	# Set the protocol if we found it
	if res is not None:
		sUrl.set_protocol(res.group(1))

	urlPattern = '^' + sUrl.protocol() + '://(.*)'
	rePattern = re.compile(urlPattern)
	res = rePattern.search(url)

	# Then, let's set up the hostname and filepath if we have it
	if res is not None:
		url = res.group(1)
		urlSects = url.split('/')
		nUrlSects = len(urlSects)

		if nUrlSects > 0:
			sUrl.set_hostname(urlSects[0]) # Set the host name

			if nUrlSects > 1:
				urlSects.pop(0)
				# Set the file path
				sUrl.set_filepath('/' + '/'.join(urlSects).rstrip('\n'))
	return sUrl
