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

def expand_target(sUrl, surface):
	rqObj = make_request(sUrl.url(), surface)

	# Create initialisable recon object
	pr = PageRecon(sUrl)

	# numNew = 0
	# Only initialise if we get something.
	if rqObj.status_code == 200:

		pr.initialise(rqObj) # Now we can initialise the recon obj.
		# numNew = surface.assimilate_list(pr.locals())

	# # Render the Discovery / Request output to the user
	# render_output(surface, numNew)

	return pr

def scout_mode(sUrl, surface):
	newSurface = []
	if surface.get_num_scouted() == 0:
		recon = expand_target(sUrl, surface)
		newSurface.append(surface.assimilate_list(recon.locals()))

	render_output(surface, newSurface)
	# Primary Loop
	while(1):
		surface.print_surface()
		if surface.get_num_scouted() > 0:
			print '\nOrbweaver Scout: "Where 2 next?"'
			user_target_selection(sUrl, surface)
		else:
			print '\nOrbweaver Scout: "Outta targets to shoot."'
			exit()

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
		recon = expand_target(section_url(target), surface)
		newSurface = surface.assimilate_list(recon.locals())
		render_output(surface, newSurface)


