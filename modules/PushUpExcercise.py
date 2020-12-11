# import the necessary packages
from imutils.video import VideoStream
import argparse
import imutils
import time
from timeit import default_timer as timer
import cv2
import numpy as np
from modules.SpeakingQueue import SpeakingQueue
q = SpeakingQueue()


class PushUp():
    def __init__(self):
        self.q = SpeakingQueue()
        self.firstFrame = None
        self.counter = 0
        self.isDown = False
        self.maxAvarage = 0
        self.t0 = timer()

    def clear(self):
        self.firstFrame = None
        self.counter = 0
        self.isDown = False
        self.maxAvarage = 0
        self.t0 = timer()

    def speak(self, text):
        self.q.push(text)

    def practice(self,vs, args, frame):

        frame = frame if args.get("video", None) is None else frame[1]
        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if frame is None:
            return frame
        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        # if the first frame is None, initialize it

        if self.firstFrame is None:
            self.firstFrame = gray
        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(self.firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)


        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        max_c = cnts[0] if len(cnts) > 0 else 0
        index = 0
        M_max_y = 0
        M_max_x = 0
        for c in cnts:
            # compute the center of the contour
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            M_max = cv2.moments(max_c)
            M_max_x = int(M_max["m10"] / M_max["m00"])
            M_max_y = int(M_max["m01"] / M_max["m00"])
            if cY < M_max_y:
                max_c = c

        if len(cnts) > 0:
            cv2.drawContours(frame, [max_c], -1, (0, 255, 0), 2)
            cv2.circle(frame, (M_max_x, M_max_y), 7, (255, 255, 255), -1)
            cv2.putText(frame, "center", (M_max_x - 20, M_max_y - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        print("cnetroid yyyyy:   ", M_max_y)
        indices = np.where(thresh == [255])

        yCoordinatesAvarage = M_max_y
        # myCalc = np.sum(indices[1])/len(indices[1])

        if self.maxAvarage == 0:
            print("inside")
            t1 = timer()

            if yCoordinatesAvarage > 0 and t1-self.t0 > 3:
                time.sleep(2)

                self.speak("3")
                self.speak("2 ")
                self.speak("1 ")
                self.speak("GO!")
                self.maxAvarage = M_max_y

        if yCoordinatesAvarage -20 <= self.maxAvarage and self.isDown:
            self.counter += 1
            self.speak(str(self.counter))
            self.isDown = False

        if yCoordinatesAvarage - 110 > self.maxAvarage != 0:
            self.isDown = True

        print("you did ", self.counter)
        print("Avarage ", yCoordinatesAvarage)
        print("Max Aavrage", self.maxAvarage)
        self.firstFrame = gray
        return frame
