 #!/usr/bin/python

import re
 # scheme:[//[user[:password]@]host[:port]][/path][?query][#fragment]

class SectionedURL:
 	def __init__(self, uriString):
		self.scheme = ''
		self.hostname = ''
		self.filepath = ''
		self.parentpath = ''
		self.query = ''
		self.fragment = ''

		# Let's capture the protocol first
		protoPattern = "^(.*)://"
		rePattern = re.compile(protoPattern)
		res = rePattern.search(uriString)
		if res is not None:
			self.scheme = res.group(1)

		# Now we have the scheme
		# Next we want the hostname.
		urlPattern = '^' + self.scheme + '://(.*)'
		rePattern = re.compile(urlPattern)
		res = rePattern.search(uriString)
		if res is not None:
			url = res.group(1)
			urlSects = url.split('/') # Split the sections by '/' char
			nUrlSects = len(urlSects)

			if nUrlSects > 0: # If we got one or more sections,
				self.hostname = urlSects[0] # Set the host name

				# Now, we have the hostname. Let's work with the file path.
				if nUrlSects > 1:
					urlSects.pop(0) # Ditch the hostname.

					# Set the file path in a disposable string
					fpString = '/' + '/'.join(urlSects).rstrip('\n')

					# Next we discern if a query is available.
					argSections = fpString.split('?')
					if len(argSections) == 2:
						self.query = '?' + argSections[1]
					self.filepath = argSections[0]

					# Set the parent directory
					self.parentpath = re.sub('/[^/]+$', '', argSections[0])

					# Now we got the filepath and query.
					fragSection = fpString.split('#')
					if len(fragSection) == 2:
						self.fragment = '#' + fragSection[1]
						self.query = self.query.rstrip(self.fragment)
					# Now we got the fragment.

	def print_values(self):
		print "[SectionedURL]\n\tScheme:\t%s\n\tHostname:\t%s\n\tFile Path:\t%s\n\tQuery:\t\t%s\n\tParent Dir:\t%s\n\tFragment:\t%s\n" % (self.scheme, self.hostname, self.filepath, self.query, self.parentpath, self.fragment)

	def url_full(self):
		ret = self.scheme + '://' + self.hostname + self.filepath + self.query + self.fragment
		if ret == '://':
			ret = ''
		return ret

	def url_filepath(self):
		return self.scheme + '://' + self.hostname + self.filepath

	def url_server(self):
		return self.scheme + '://' + self.hostname

	def equals(self, sUrl):
		equals = True

		if self.scheme != sUrl.scheme:
			equals = False

		if self.hostname != sUrl.hostname:
			equals = False

		if self.filepath != sUrl.filepath:
			equals = False

		if self.query != sUrl.query:
			equals = False

		if self.fragment != sUrl.fragment:
			equals = False

		return equals

def test_surl():
	urlString = 'http://blog.systemd.rip/dir1/dir2/script?arg1=uArg1&arg2=uArg2#fragment'
	sUrl = SectionedURL(urlString)
	sUrl.print_values()

	assert(sUrl.scheme =='http')
	assert(sUrl.hostname == 'blog.systemd.rip')
	assert(sUrl.filepath == '/dir1/dir2/script')
	assert(sUrl.query == '?arg1=uArg1&arg2=uArg2')
	assert(sUrl.fragment == '#fragment')

	print sUrl.url_full()
	print sUrl.url_filepath()
	print sUrl.url_server()
	assert(sUrl.url_full() == urlString)

	sUrl1 = SectionedURL(urlString)
	assert(sUrl.equals(sUrl1))
	print 'Tests for SectionedURL passed.'

test_surl()


