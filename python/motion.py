#!/usr/bin/python

from utils.getopts import getopts
import sys
from firebase import Firebase

args = getopts(sys.argv)
path = args['-path']
#print("---------------------")
#print("path: %s" % path)
filename = path.split("/")[4]
#print("---------------------")
#print("filename: %s" % filename)

fb = Firebase()
fb.uploadNewPic(path, filename)

