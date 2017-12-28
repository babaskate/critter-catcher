import pyrebase
import json
import time

class Firebase:

    __configPath = "../.keys/config.json"
    __configJSON = {}
    __configData = {}
    __userPath = "../.keys/user.json"
    __userData = {}
    __firebase = {}
    __uuid = ""

    def __init__(self):
        
        self.__configJSON = json.load(open(self.__configPath))

        self.__configData = {
            "apiKey": self.__configJSON['apiKey'],
            "authDomain": "crittercatcher-61af4.firebaseapp.com",
            "databaseURL": "https://crittercatcher-61af4.firebaseio.com",
            "projectId": "crittercatcher-61af4",
            "storageBucket": "crittercatcher-61af4.appspot.com",
            "messagingSenderId": "745850059470",
            "serviceAccount": "../.keys/crittercatcher-61af4-firebase-adminsdk-7kdr7-db73c72f78.json"
        }

        self.__firebase = pyrebase.initialize_app(self.__configData)

        self.__userData = json.load(open(self.__userPath))

        self.__uuid = self.__userData["uuid"]

    def getUser(self):

        # Get a reference to the auth service
        auth = self.__firebase.auth()

        token = auth.create_custom_token(self.__uuid)

        user = auth.sign_in_with_custom_token(token)

        return user

    def getUserInfo(self):

        # Get a reference to the auth service
        auth = self.__firebase.auth()

        userInfo = auth.get_account_info(self.getUser()['idToken'])

        return userInfo

    def uploadNewPic(self):

        db = self.__firebase.database()

        key = db.child("posts").push('')['name']

        print "-------------"
        print 'key: %s' % key

        storage = self.__firebase.storage()

        picPath = self.__uuid + '/full/' + key + '/foobar.jpg'

        print "-------------"
        print 'picPath: %s' % picPath

        # as admin
        image = storage.child(picPath).put("/home/pi/var/camera/photos/dark.jpg", self.getUser()['idToken'])

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
                "uid": self.__uuid,
                "full_name": self.getUserInfo()['users'][0]['displayName'],
                "profile_picture": self.getUserInfo()['users'][0]['photoUrl']
            }
        }

        #associate post to person
        peoplePath = "/people/" + self.__uuid + "/posts/" + key
        print "-------------"
        print "peoplePath: %s" % peoplePath
        data[peoplePath] = "true"

        #update the feed
        feedPath = "/feed/" + self.__uuid + "/" + key
        print "-------------"
        print "feedPath: %s" % feedPath
        data[feedPath] = "true"

        db.update(data)

fb = Firebase()
fb.uploadNewPic()
