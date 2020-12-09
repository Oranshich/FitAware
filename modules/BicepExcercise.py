# import the necessary packages
from imutils.video import VideoStream
import argparse
import imutils
import time
from timeit import default_timer as timer
import cv2
import numpy as np
from modules.SpeakingQueue import SpeakingQueue

# def get_current_avg(vs, firstFrame, args):
#     frame = vs.read()
#     frame = frame if args.get("video", None) is None else frame[1]
#     frame = imutils.resize(frame, width=500)
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     gray = cv2.GaussianBlur(gray, (21, 21), 0)
#     if firstFrame is None:
#         firstFrame = gray
#     frameDelta = cv2.absdiff(firstFrame, gray)
#     thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
#     thresh = cv2.dilate(thresh, None, iterations=2)
#
#     indices = np.where(thresh == [255])
#     yCoordinatesAvarage = np.median(indices[1], axis=0)
#
#     return yCoordinatesAvarage, frame

class Bicep():

    def __init__(self):
        self.q = SpeakingQueue()
        self.firstFrame = None
        self.counter = 0
        self.isDown = False
        self.maxAvarage = 0
        self.t0 = timer()

    def speak(self,text):
        self.q.push(text)


    def practice(self,vs, args, frame):


        # initialize the first frame in the video stream


        index = 0
        # loop over the frames of the video

        # while True:
        # grab the current frame and initialize the occupied/unoccupied
        # text
        # frame = vs.read()
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
            if cY > M_max_y:
                max_c = c
            #     # draw the contour and center of the shape on the image
            #     cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
            #     cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
            #     cv2.putText(frame, "center", (cX - 20, cY - 20),
            #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            #
            # else:
        if len(cnts) > 0:
            cv2.drawContours(frame, [max_c], -1, (0, 255, 0), 2)
            cv2.circle(frame, (M_max_x, M_max_y), 7, (255, 255, 255), -1)
            cv2.putText(frame, "center", (M_max_x - 20, M_max_y - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            # print("cnetroid yyyyy:   ", M_max_y)
            # show the image
        # cv2.imshow("Image", frame)


        print("cnetroid yyyyy:   ", M_max_y)
        indices = np.where(thresh == [255])
        # yCoordinatesAvarage = np.average(indices[1], axis=0)
        yCoordinatesAvarage = M_max_y
        myCalc = np.sum(indices[1])/len(indices[1])
        # print("my avarage ", myCalc)
        if self.maxAvarage == 0:
            print("inside")
            t1 = timer()
            # print('t1 time', t1)
            if yCoordinatesAvarage > 0 and t1-self.t0 > 3:

                self.speak("3")
                self.speak("2 ")
                self.speak("1 ")
                self.speak("GO!")
                self.maxAvarage = M_max_y

        # yCoordinatesAvarage = np.average(indices[1], axis=0)

        # yCoordinatesAvarage, frame = get_current_avg(vs, firstFrame, args)
        if yCoordinatesAvarage >= self.maxAvarage and self.isDown:
            # if yCoordinatesAvarage < maxAvarage:
                # maxAvarage = M_max_y
            self.counter += 1
            self.speak(str(self.counter))
            isDown = False
            time_between_repitition = timer()

        time_to_check = timer()

        if self.counter > 0 and ((time_to_check - time_between_repitition) > 5):
            print("time to check - time between = ", (time_to_check - time_between_repitition))
            print("time between: ", time_between_repitition)
            print("time to check: ", time_between_repitition)
            self.speak("You take too much time between iterations")
            time_between_repitition = timer()
        if yCoordinatesAvarage + 110 < self.maxAvarage:
            isDown = True

        print("you did ", self.counter)
        print("Avarage ", yCoordinatesAvarage)
        print("Max Aavrage", self.maxAvarage)
        # show the frame and record if the user presses a key
        # cv2.imshow("Security Feed", frame)
        # cv2.imshow("Threshold", thresh)
        # cv2.imshow("Orginal", frame)
        # cv2.imshow("Frame Delta", frameDelta)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key is pressed, break from the lop
        # if key == ord("q"):
        #     return
        # cleanup the camera and close any open windows
        # vs.stop() if args.get("video", None) is None else vs.release()
        # cv2.destroyAllWindows()
        return frame
