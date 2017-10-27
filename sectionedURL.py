#!/usr/bin/python

import re

# Written by Bruce Hely for funzies in 2017

class SectionedURL:
	def __init__(self):
		self.proto = '' 	# <PROTO>
		self.hostName = '' 	# <HOSTNAME>
		self.filePath = ''	# <FILEPATH>

		self.parentDir = '' # <PARENTDIR>
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

	def filepath(self):
		return self.filePath

	def parent_dir(self):
		return self.proto + "://" + self.hostName + self.parentDir

	def set_protocol(self, newProto):
		self.proto = newProto

	def set_hostname(self, newHostName):
		self.hostName = newHostName

	def set_filepath(self, newFilePath):
		self.filePath = newFilePath

	def set_parentdir(self, newParent):
		self.parentDir = newParent

	def print_values(self):
		print "[SectionedURL]\n\tProtocol: %s\n\tHostname: %s\n\tFile Path: %s\n\tParent Dir: %s\n" % (self.proto, self.hostName, self.filePath, self.parentDir)

	# Coupled Operators Below
	def equal_urls(self, sUrl):
		return self.url() == sUrl.url()

	def equal_protocols(self, sUrl):
		return self.protocol() == sUrl.protocol()

	def equal_hostnames(self, sUrl):
		return self.hostname == sUrl.hostname

	def equal_filepaths(self, sUrl):
		return self.filepath() == sUrl.filepath


# This is the function you call in order to initialise the sectioned url object.
# Assume that is just fills in the <PROTOCOL>, <HOSTNAME> and <FILEPATH> correctly.
# Give me a URL, like http://www.example.com/dir/file.jpg.
# ret->protocol = http
# ret->hostname = www.example.com
# ret->filepath = /dir/file.jpg
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
				# Set the file path in a disposable string
				fpString = '/' + '/'.join(urlSects).rstrip('\n')

				sUrl.set_filepath(fpString)
				sUrl.set_parentdir(re.sub('/[^/]+$', '', fpString))

	return sUrl
