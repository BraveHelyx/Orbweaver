#!/usr/bin/python

from surface import *
from sectionedURL import *

from os import mkdir, makedirs, path

import re

# Structure
# blog.example.com/dir1/dir2/page.html
# ---------
# /orbweaver.py
# /saved/
# /saved/blog.example.com/unexplored
# /saved/blog.example.com/explored/index.html
# /saved/blog.example.com/explored/dir1/file1.html

# Writes surface.get_surface() to './saved/<HOSTNAME>/unexplored'
# Essentially writes the list out to a file.
def write_unexplored(saveDir, surface):
	fp = open(saveDir + '/unexplored', 'w+')

	targets = fp.readlines()

	# Write unexplored targets to file.
	unexplored = surface.get_surface()
	for url in unexplored:
		targets.append(url)

	targets = list(sorted(set(targets)))

	fp.seek(0)
	for target in targets:
		fp.write('%s\n' % target)

	fp.truncate()
	fp.close()

# Loads the list of unexplored targets
def load_unexplored(saveDir, surface):
	if path.isfile(saveDir + '/unexplored'):
		fp = open(saveDir + '/unexplored', 'r')

		targets = fp.readlines()

		print 'Loading %d records.' % len(targets)
		surface.assimilate_list(targets)

		fp.close()

# Relative to the saved directory
# sessDir = ./saved/<HOSTNAME>
def sess_exist(sUrl):
	sessDir = './saved/' + sUrl.hostname
	ret = False
	if path.isfile(sessDir + '/unexplored'):
		ret = True
	return ret

# Writes out the request objects to disk that we have explored
def write_explored(sUrl, surface):
	requests = surface.get_requests()
	# saveDir = './saved/' + sUrl.hostname + '/explored/'
	saveDir = './saved/' + sUrl.hostname + '/src/'

	# Let's iterate through the requests we made.
	for key in requests.keys():
		request = requests[key]

		if request.status_code == 200:
			filePath = request.url.lstrip(sUrl.scheme + '://') # Grab the URL of the file
			savePath = saveDir + filePath

			print 'Filepath: %s\nSavepath: %s' % (filePath, savePath)
			if savePath[len(savePath)-1] == '/':
				savePath = savePath + '/index.html'

			print 'Saving %s' % savePath

			if not path.exists(path.dirname(savePath)):
				try:
					makedirs(path.dirname(savePath))
				except OSError as exc:
					if exc.errno != errno.EEXIST:
						raise

			# Open and write all the src lines to the file.
			if path.isdir(savePath):
				savePath += '/index.html'

			fp = open(savePath, 'w+')

			fp.write(request.text) # Lines of source

			# Done, next!
			fp.close()

# High level API for saving the currence surface for the project specified in sUrl.
def save_session(sUrl, surface):
	saveDir = './saved/' + sUrl.hostname
	srcTree = saveDir + '/explored'

	# If the saved directory doesn't exist, make it.
	if not path.exists('./saved'):
		mkdir('./saved')

	# Make the directory for hostname
	if not path.exists(saveDir):
		mkdir(saveDir)

	if not path.exists(srcTree):
		mkdir(srcTree)

	# Writes the unexplored file.
	write_unexplored(saveDir, surface)
	write_explored(sUrl, surface)






