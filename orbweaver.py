#!/usr/bin/python

# Written by Bruce Hely for funzies in 2017
# Peripheral scan of a domain.
import sys, requests, re

# Method imports
from urlreqs import *
from filters import *

# System Import
from orbweaver_scout import *

# Class Imports
from sectionedURL import *
from surface import *

recursiveFlag = True

def main():
	# Check for incorrect usage
	if (len(sys.argv) < 2) :
		print 'Usage: ./%s <TARGET>' % sys.argv[0]
	else:

		# Passed in flags
		if (len(sys.argv) > 2):
			# Iterate through each argument
			for argument in sys.argv:
				print '%s' % argument
				if argument[0] is '-':
					# Isolate recursive flag.
					if argument[1] is 'r':
						recursiveFlag = True
		# For Valid Input
		domain = sys.argv[1]

		# Make sure "http://" is prepended. Change me later. Works for now.
		if not re.match('^http[s]?://', domain):
			domain = 'http://' + domain

		if domain[len(domain)-1] == '/':
			domain = domain + 'index.html'

		# Create the sectioned URL for the target
	 	sUrl = section_url(domain)
		# sUrl.print_values()

		# Create the session surface object
		sfc = Surface()

		# Check if session exists and offer to load it.
		if sess_exist(sUrl):
			print 'Session exists. Load it? (y/n)'
			selection = ''
			selection = raw_input()
			if len(selection) >= 1:
				if selection[0] == 'y' or selection[0] == 'Y':
					load_unexplored('./saved/' + sUrl.hostname(), sfc)


		# Begin the scan with the loaded/unloaded surface object
		run_scan(sUrl, sfc)

# Should only be run for valid targets
def run_scan(sUrl, surface):
	# Request Responses
	res = []
	validRes = []

	print 'Received valid target(%s). Scanning...' % sUrl.url()

	# Get the sections once for easability
	proto = sUrl.protocol()
	hostName = sUrl.hostname()
	filePath = sUrl.filepath()

	# Never returns
	scout_mode(sUrl, surface)

	print 'Something strange surfaced...'

# Call Main
main()