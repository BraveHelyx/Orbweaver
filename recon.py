#!/usr/bin/python

import requests
from filters import *
from sectionedURL import *

# Instanciation dependant on sectionedURL module.
class PageRecon:
	def __init__(self, sUrl):
		self.sUrl = sUrl
		self.status = 0
		self.srclines = []
		self.tags = []
		self.hyperlinks = []
		self.images = []
		self.forms = []
		self.scripts = []
		self.localUrls = []

	def initialise(self, rqObj):
		if rqObj is not None:
			# Result dependant programming.
			# Caches result and initialises other values on those results.
			self.status = rqObj.status_code

			self.srclines = rqObj.text # Set Page Source

			self.tags = filter_tags(self.srclines) # Filter all tags

			# Using the tags, categorise them.
			self.hyperlinks, self.scripts, self.images, self.forms = categorise_tags(self.tags)

			# Create list of urls from the tags/source
			self.localUrls = filter_local_links(self.sUrl, self.hyperlinks)

	def source(self):
		return self.srclines

	def tags(self):
		return self.tags

	def hyperlinks(self):
		return self.hyperlinks

	def images(self):
		return self.images

	def locals(self):
		return self.localUrls

