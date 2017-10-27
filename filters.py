#!/usr/bin/python

# Written by Bruce Hely for funzies in 2017

import re
import sectionedURL

# Strip the raw tags out of the HTML
def filter_tags(pageSource):
	tags = []
	values = []

	# Find First Tag
	i = 0;
	for c in pageSource:
		if c == '<':
			break
		else:
			i += 1
	startIndex = i

	inTag = True

	tmpStr = ''
	for c in pageSource[startIndex:len(pageSource)]:
		if inTag is True:
			if c == '>': # Append to Tag if terminating
				tags.append('<' + tmpStr + '>')
				tmpStr = ''

				# Toggle inTag
				inTag = False
			else: # Add character to tag string if not.
				tmpStr = tmpStr + c
		else:
			if c == '<':
				values.append(tmpStr)
				tmpStr = ''

				# Tpgg;e inTag
				inTag = True
			else:
				tmpStr = tmpStr + c
	return tags

# Output is a tuple of lists: (links, scripts, images, forms)
def categorise_tags(tags):
	links = []
	scripts = []
	images = []
	forms = []
	localUrls = []

	for tag in tags:
		linkPattern = '<[ ]*a'
		scriptPattern = '<[ ]*script'
		imgPattern = '<[ ]*img'
		formPattern = '<[ ]*form'

		rePattern = re.compile(linkPattern)

		res = rePattern.search(tag)
		if res is not None:
			links.append(tag)
		else:
			rePattern = re.compile(imgPattern)

			res = rePattern.search(tag)
			if res is not None:
				images.append(tag)
			else:
				rePattern = re.compile(scriptPattern)

				res = rePattern.search(tag)
				if res is not None:
					scripts.append(tag)
				else:
					rePattern = re.compile(formPattern)

					res = rePattern.search(tag)
					if res is not None:
						forms.append(tag)

	return (links, scripts, images, forms)

# From a list of link tags, filter out the href value from each.
# Works on '/', './' and 'sUrl.server()' values.
def filter_local_links(sUrl, links):
	localLinks = []
	links = list(sorted(set(links)))

	for link in links:
		rePattern = re.compile(' href="(.+)"')

		hostPattern = re.compile('^' + sUrl.server() + '/(.+)')
		rootPattern = re.compile('^' + '/(.+)')
		localPattern = re.compile('^' + './(.+)')

		res = rePattern.search(link)
		if res is not None:
			url = res.group(1)

			rMatch = rootPattern.search(url)
			hMatch = hostPattern.search(url)
			lMatch = localPattern.search(url)

			if rMatch is not None:
				localLinks.append(sUrl.server() + '/' + rMatch.group(1))
			elif lMatch is not None:

				localLinks.append(sUrl.parent_dir() + '/' + lMatch.group(1))
			elif hMatch is not None:
				localLinks.append(sUrl.server() + '/' + hMatch.group(1))

	return localLinks
