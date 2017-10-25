#!/usr/bin/python
# Written by Bruce Hely for funzies in 2017


def format_targets(targets):
	formattedTargets = []
	i = 0
	for target in targets:
		formattedTargets.append("%-8s%-48s" % (i, target))
		i += 1
	return formattedTargets

def format_responses(responses):
	formattedResponses = []
	for (status, urlRes) in responses:
		formattedResponses.append("%-8s%s" % (status, urlRes))
	return formattedResponses

# Primary function for rendering output.
# Helper functions are above.
def render_output(surface):
	targets = format_targets(surface.get_pending())
	responses = []
	fmtRes = []
	rqs = surface.get_requests()

	# Format the response list right
	for key in rqs.keys():
		rqObj = rqs[key]
		resString = key + ' -> ' + rqObj.url
		fmtRes.append((str(rqObj.status_code), resString))

	responses = format_responses(fmtRes)

	numTargets = len(targets)
	numResponses = len(responses)

	# Padd the lists
	rows = max(numTargets, numResponses)
	while (len(targets) < rows):
		targets.append("%-8s%-48s" % ("", ""))

	while (len(responses) < rows):
		responses.append("%-8s%s" % ("", ""))

	output = []
	print "%-56s | %s" % (">> SCOUTED <<", ">> EXPLORED <<")
	print "%-8s%-48s | %-8s%s" % ("ID", "URL", "STATUS", "URL")
	for i in range(0, rows):
		output.append("%s | %s" % (targets[i], responses[i]))
		print "%s | %s" % (targets[i], responses[i])

# targetList = ["http://abc.com", "http://abc.com/a", "http://abc.com/b"]
# resList = [("200", "http://abc.com/home"), ("404", "http://abc.com/biz")]
#
# print_output(format_targets(targetList), format_responses(resList))
