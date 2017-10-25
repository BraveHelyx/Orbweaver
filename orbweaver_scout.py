#!/usr/bin/python

# Written by Bruce Hely for funzies in 2017

from urlreqs import make_request
from filters import filter_tags, categorise_tags, filter_local_links
from render import render_output

# Import classes
from sectionedURL import *
from surface import *

def expand_target(sUrl, surface):
	rqObj = make_request(sUrl.url(), surface)
	if rqObj.status_code == 200:
		srcLines = rqObj.text

		# Obtain the tags from the source code
		tags = filter_tags(srcLines)

		# Output is a tuple of lists: (links, scripts, images, forms)
		links, scripts, images, forms = categorise_tags(tags)

		# Gather the next level of outgoing local links within the
		locLinks = filter_local_links(sUrl, links)
		numNew = surface.assimilate_list(locLinks)

		render_output(surface)
		# print_requests(surface)
		# print '\n>> EXPLORATION <<'
		# print 'Discovered: %d\tNew: %d' % (len(surface.get_surface()), numNew)
		# print_pending(surface)
	return rqObj

def scout_mode(surface):
	while(1):
		if surface.get_num_pending() > 0:
			print '\nOrbweaver Scout: "Where 2 next?"'
			user_target_selection(surface)
		else:
			print '\nOrbweaver Scout: "Outta targets to shoot."'
			exit()

def user_target_selection(surface):
	targets = surface.get_pending() # Get unexplored targets
	nTargets = len(targets)


	selection = raw_input()

	target = ''

	try:
		uIndex = int(selection) # Can throw exception

		# Length check
		if uIndex < nTargets and uIndex >= 0:
			target = targets[uIndex] # Grab the next target
		else:
			print "That's a dodgy 'i' m8. R u blind?!"
	except:
		if selection == 'q': # Escape Condition
			print "l8tr buddi."
			exit()
		pass

	if target != '':
		print 'Expanding Target(%s). Loading...' % target
		expand_target(section_url(target), surface)

