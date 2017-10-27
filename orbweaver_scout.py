#!/usr/bin/python

# Written by Bruce Hely for funzies in 2017

from urlreqs import make_request
from filters import filter_tags, categorise_tags, filter_local_links
from render import render_output

# Import classes
from sectionedURL import *
from surface import *
from recon import *

def expand_target(sUrl, surface):
	rqObj = make_request(sUrl.url(), surface)

	# Create initialisable recon object
	pr = PageRecon(sUrl)

	numNew = 0
	# Only initialise if we get something.
	if rqObj.status_code == 200:

		pr.initialise(rqObj) # Now we can initialise the recon obj.

		# srcLines = rqObj.text
		#
		# # Obtain the tags from the source code
		# tags = filter_tags(srcLines)
		#
		# # Output is a tuple of lists: (links, scripts, images, forms)
		# links, scripts, images, forms = categorise_tags(tags)
		#
		# # Testing
		# for tag in tags:
		# 	assert(tag in pr.tags)
		#
		# for link in links:
		# 	assert(link in pr.hyperlinks)
		#
		# for script in scripts:
		# 	assert(script in pr.scripts)

		# locLinks = filter_local_hyperlinks(sUrl, links)
		numNew = surface.assimilate_list(pr.locals())

	# Render the Discovery / Request output to the user
	render_output(surface, numNew)

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

