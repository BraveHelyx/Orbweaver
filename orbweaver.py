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

		# Make sure "http://" is prepended
		if not re.match('^http[s]?://', domain):
			domain = 'http://' + domain

		if domain[len(domain)-1] == '/':
			domain = domain.rstrip('/')
		#done
		sfc = Surface()
		run_scan(domain, sfc)

# Should only be run for valid targets
def run_scan(target, surface):
	# Request Responses
	res = []
	validRes = []


	print 'Received valid target(%s). Scanning...' % target

	# Create the sectioned URL for the target
 	sUrl = section_url(target)
	sUrl.print_values()

	# Get the sections once for easability
	proto = sUrl.protocol()
	hostName = sUrl.hostname()
	filePath = sUrl.filepath()

	# Do the request and register results to surface object
	rqObj = expand_target(sUrl, surface)

	if rqObj.status_code == 200:

		# Never returns
		scout_mode(sUrl, surface)

		print 'Something strange surfaced...'
	else:
		print 'Done.'

# Call Main
main()