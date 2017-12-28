import pyrebase
import json
import time

configPath = "../.keys/config.json"
configJSON = json.load(open(configPath))

print configJSON[]

config = {
    "apiKey": configJSON['apiKey'],
    "authDomain": "crittercatcher-61af4.firebaseapp.com",
    "databaseURL": "https://crittercatcher-61af4.firebaseio.com",
    "projectId": "crittercatcher-61af4",
    "storageBucket": "crittercatcher-61af4.appspot.com",
    "messagingSenderId": "745850059470",
    "serviceAccount": "../.keys/crittercatcher-61af4-firebase-adminsdk-7kdr7-db73c72f78.json"
}

firebase = pyrebase.initialize_app(config)

userJSON = "../.keys/user.json"
userData = json.load(open(userJSON))

uuid = userData["uuid"]

print "-------------"
print "uuid: %s" % uuid

# Get a reference to the auth service
auth = firebase.auth()

token = auth.create_custom_token(uuid)

print "-------------"
print "token: %s" % token

user = auth.sign_in_with_custom_token(token)

userInfo = auth.get_account_info(user['idToken'])

print "-------------"
print "userInfo: %s" % userInfo

db = firebase.database()

#all_users = db.child("people").get()
#for user in all_users.each():
#    print(user.key())
#    print(user.val())

key = db.child("posts").push('')[u'name']

print "-------------"
print 'key: %s' % key

storage = firebase.storage()

picPath = uuid + '/full/' + key + '/foobar.jpg'

print "-------------"
print 'picPath: %s' % picPath

# as admin
image = storage.child(picPath).put("/home/pi/var/camera/photos/dark.jpg", user['idToken'])

print "-------------"
print 'image: %s' % image

url = storage.child(picPath).get_url(image['downloadTokens'])

print "-------------"
print "url: %s" % url

data = {}
postPath = "/posts/" + key
data[postPath] = {
    "full_url": url,
    "thumb_url": url,
    "text": "motion captured picture",
    "timestamp": int(round(time.time() * 1000)),
    "full_storage_uri": picPath,
    "thumb_storage_uri": picPath,
    "author": {
        "uid": uuid,
        "full_name": userInfo['users'][0]['displayName'],
        "profile_picture": userInfo['users'][0]['photoUrl']
    }
}

#associate post to person
peoplePath = "/people/" + uuid + "/posts/" + key
print "-------------"
print "peoplePath: %s" % peoplePath
data[peoplePath] = "true"

#update the feed
feedPath = "/feed/" + uuid + "/" + key
print "-------------"
print "feedPath: %s" % feedPath
data[feedPath] = "true"

db.update(data)
