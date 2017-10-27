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

# Writes out the request objects to disk that we have explored
def write_explored(sUrl, surface):
	requests = surface.get_requests()
	# saveDir = './saved/' + sUrl.hostname() + '/explored/'
	saveDir = './saved/src/'

	# Let's iterate through the requests we made.
	for key in requests.keys():
		request = requests[key]

		filePath = request.url.lstrip(sUrl.protocol() + '://') # Grab the URL of the file
		savePath = saveDir + filePath
		# print 'Filepath: %s\nSavepath: %s' % (filePath, savePath)
		if savePath[len(savePath)-1] == '/':
			savePath = savePath + 'index'

		print 'Saving %s' % savePath

		if not path.exists(path.dirname(savePath)):
			try:
				makedirs(path.dirname(savePath))
			except OSError as exc:
				if exc.errno != errno.EEXIST:
					pass

		# Open and write all the src lines to the file.
		fp = open(savePath, 'w+')
		fp.write(request.text) # Lines of source

		# Done, next!
		fp.close()

# Creates and writes the lines of srcList to the file in pathName.
# Hard Overwrites with truncate.
# Useful for writing HTML files, or images.
# def write_file(sUrl, srcList):
# 	fp = open('./saved/' + sUrl.hostname() + '/' + sUrl.filepath() , 'w+')
# 	for line in srcList:
# 		fp.write('%s\n' % line)
# 	fp.truncate()
# 	fp.close()

# High level API for saving the currence surface for the project specified in sUrl.
def save_session(sUrl, surface):
	saveDir = './saved/' + sUrl.hostname()
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






