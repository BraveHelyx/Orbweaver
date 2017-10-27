#!/usr/bin/python

import requests
from surface import *

# My Imports
import sectionedURL

# Request and add robots.txt to surface
# @return			HTTP Request Status Code
def request_robots(sUrl):
	robots = sUrl.server() + "/robots.txt"
	rqObj = requests.get(robots)
	print '[%d] - %s' % (rqObj.status_code, robots)
	return rqObj

def request_git(sUrl):
	git = sUrl.server() + "/.git"
	rqObj = requests.get(git)

	print '[%d] - %s' % (rqObj.status_code, git)
	return rqObj

def request_source(target):
	rqObj = requests.get(target)

	print '[%d] %s -> %s' % (rqObj.status_code, target, rqObj.url)
	return rqObj

# Request and add target to surface
# @return			HTTP Request Objec
def make_request(target, surface):
	rqObj = requests.get(target)
	surface.add_surface(target)
	surface.add_rq_response(rqObj, target)
	return rqObj

