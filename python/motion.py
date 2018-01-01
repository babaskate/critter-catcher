from datetime import datetime as dt
from utils.getopts import getopts
import sys
import firebase

args = getopts(sys.argv)
path = args['-path']
print("---------------------")
print("path: %s" % path)
print("---------------------")

#now=dt.now().strftime("%m-%d-%y-%H-%M")
#filename = "capture_" + now + ".jpg"
#fb = FirebaseWrapper()
#fb.uploadNewPic(path)

