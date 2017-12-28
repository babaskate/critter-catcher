from picamera import PiCamera
from time import sleep
from fractions import Fraction
from datetime import datetime as dt
from firebase import Firebase

class Camera:

    def __init__(self):
        # Force sensor mode 3 (the long exposure mode), set
        # the framerate to 1/6fps, the shutter speed to 6s,
        # and ISO to 800 (for maximum gain)
        self.__camera = PiCamera(
            resolution=(1280, 720),
            framerate=Fraction(1, 6),
            sensor_mode=3)
        self.__camera.rotation=180
        self.__camera.meter_mode='average'
        self.__camera.shutter_speed = 6000000
        self.__camera.iso = 800
        # Give the camera a good long time to set gains and
        # measure AWB (you may wish to use fixed AWB instead)
        #sleep(2)
        self.__camera.exposure_mode = 'off'
        # Finally, capture an image with a 6s exposure. Due
        # to mode switching on the still port, this will take
        # longer than 6 seconds

    def capture(self):
        now=dt.now().strftime("%m-%d-%y-%H-%M")
        filename = "capture_" + now + ".jpg"
        path='/home/pi/var/camera/photos/%s' % (filename)
        self.__camera.capture(path)
        self.__camera.close()
        fb = Firebase()
        fb.uploadNewPic(filename)

camera = Camera()
camera.capture()
