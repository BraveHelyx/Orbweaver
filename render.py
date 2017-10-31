#!/usr/bin/python
# Written by Bruce Hely for funzies in 2017
# from termcolor import colored

def format_targets(targets, newSurface):
	formattedTargets = []
	i = 0
	for target in targets:
		if target in newSurface:
			formattedTargets.append("%-8s%-56s" % (i, target + ' [*]'))
		else:
			formattedTargets.append("%-8s%-56s" % (i, target))
		i += 1
	return formattedTargets

def format_responses(responses):
	formattedResponses = []
	for (status, urlRes) in responses:
		formattedResponses.append("%-8s%s" % (status, urlRes))
	return formattedResponses

# Primary function for rendering output.
# Helper functions are above.
def render_output(surface, newSurface):
	targets = format_targets(surface.get_pending(), newSurface)
	responses = []
	fmtRes = []
	rqs = surface.get_requests()

	# Format the response list right
	for key in rqs.keys():
		rqObj = rqs[key]
		resString = ''
		if key.rstrip('/') != rqObj.url.rstrip('/'):
			resString = key + ' -> ' + rqObj.url
		else:
			resString = key
		fmtRes.append((str(rqObj.status_code), resString))

	responses = format_responses(fmtRes)

	numTargets = len(targets)
	numResponses = len(responses)

	# Padd the lists
	rows = max(numTargets, numResponses)
	while (len(targets) < rows):
		targets.append("%-8s%-56s" % ("", ""))

	while (len(responses) < rows):
		responses.append("%-8s%s" % ("", ""))

	output = []
	# print "Discovered: %d" % newSurface
	print "%-64s | %s" % (">> SCOUTED << [%d NEW]" % len(newSurface), ">> EXPLORED <<")
	print "%-8s%-56s | %-8s%s" % ("ID", "URL", "STATUS", "URL")
	for i in range(0, rows):
		output.append("%s | %s" % (targets[i], responses[i]))
		print "%s | %s" % (targets[i], responses[i])

# targetList = ["http://abc.com", "http://abc.com/a", "http://abc.com/b"]
# resList = [("200", "http://abc.com/home"), ("404", "http://abc.com/biz")]
#
# print_output(format_targets(targetList), format_responses(resList))
