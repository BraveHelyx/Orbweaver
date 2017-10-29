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
		sUrl.print_values()

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
		# else:
		# 	# Do the request and register results to surface object
		# 	rqObj = expand_target(sUrl, sfc)
		#
		# 	if rqObj.status_code == 404:
		# 		print "Couldn't gain initial surface."
		# 		exit()
		# Begin the scan with the loaded/unloaded surface object
		run_scan(sUrl, sfc)

# Should only be run for valid targets
def run_scan(sUrl, surface):
	# Request Responses
	res = []
	validRes = []


	print 'Received valid target(%s). Scanning...' % sUrl.url()

	# # Create the sectioned URL for the target
 # 	sUrl = section_url(target)
	# sUrl.print_values()


	# Get the sections once for easability
	proto = sUrl.protocol()
	hostName = sUrl.hostname()
	filePath = sUrl.filepath()

	# # Check if session exists and offer to load it.
	# if sess_exist(sUrl):
	# 	print 'Session exists. Load it? (y/n)'
	# 	selection = ''
	# 	selection = raw_input()
	# 	if len(selection) >= 1:
	# 		if selection[0] == 'y' or selection[0] == 'Y':
	# 			load_unexplored('./saved/' + sUrl.hostname(), surface)
	# else:
	# 	# # Do the request and register results to surface object
	# 	rqObj = expand_target(sUrl, surface)
	#
	# 	if rqObj.status_code == 404:
	# 		print "Couldn't gain initial surface."
	# 		exit()

	# Never returns
	# print 'Orbweaver Scout: "...YesSsSs?"'
	scout_mode(sUrl, surface)

	print 'Something strange surfaced...'
	# else:
	# 	print 'Done.'

# Call Main
main()