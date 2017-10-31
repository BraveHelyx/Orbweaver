#!/usr/bin/python

# Written by Bruce Hely for funzies in 2017
from urlreqs import make_request
from filters import filter_tags, categorise_tags, filter_local_links
from render import render_output
from session import *
# Import classes
from sectionedURL import *
from surface import *
from recon import *

# Primary function for making a request to a url.
# Returns a PageRecon object from recon.py
def expand_target(sUrl, surface):
	sUrl.print_values()
	rqObj = make_request(sUrl.url_full(), surface)

	# Create initialisable recon object
	pr = PageRecon(sUrl)

	# numNew = 0
	# Only initialise if we get something.
	if rqObj.status_code == 200:

		pr.initialise(rqObj) # Now we can initialise the recon obj.

	return pr

# Primary driving loop for scout mode.
def scout_mode(sUrl, surface):
	newSurface = []
	if surface.get_num_scouted() == 0:
		recon = expand_target(sUrl, surface)
		newSurface.append(surface.assimilate_list(recon.locals()))

	render_output(surface, newSurface)
	# Primary Loop
	while(1):
		# surface.print_surface()
		if surface.get_num_scouted() > 0:
			print '\nOrbweaver Scout: "Where 2 next?"'
			user_target_selection(sUrl, surface)
		else:
			print '\nOrbweaver Scout: "Outta targets to shoot."'
			exit()

# Asks the user to select a target.
# Expands before asking again
def user_target_selection(sUrl, surface):
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
			print "Save The Session?"
			choice = raw_input()

			if choice == 'y' or choice == 'Y':
				save_session(sUrl, surface) # SAVE THE SESSION!

			print "l8tr buddy."
			exit()
		pass

	# If we got a valid target
	if target != '':
		print 'Expanding Target(%s). Loading...' % target
		recon = expand_target(SectionedURL(target), surface)
		newSurface = surface.assimilate_list(recon.locals())
		render_output(surface, newSurface)


