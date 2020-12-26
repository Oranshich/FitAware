# import the necessary packages
from imutils.video import VideoStream
import argparse
import imutils
import time
from timeit import default_timer as timer
import cv2
import numpy as np
from modules.SpeakingQueue import SpeakingQueue


class PracticeBase():
    """
    Class responsible for the main algorithm of the practice, all the functionality of calculating repetitions happens
    in this class.It is inherited by the Bicep and PushUp classes - the only change between this class and them is the
    is_smaller function, in PushUp the function checks in reverse with respect to the Bicep.
    """

    def __init__(self):
        self.q = SpeakingQueue()
        self.firstFrame = None
        self.counter = 0
        self.isDown = False
        self.maxAvarage = 0
        self.t0 = timer()
        self.addition_down = 0
        self.addition_counter = 0

    def clear(self):
        """
        The function responsible for clear the variables before every run
        """
        self.firstFrame = None
        self.counter = 0
        self.isDown = False
        self.maxAvarage = 0
        self.t0 = timer()

    def speak(self, text):
        """
        The function is responsible for adding the text we want the computer to say into the SpeakingQueue queue.
        :param text: The text the voice needs to say
        :return: enter the the text to the queue of the speaking queue
        """
        self.q.push(text)

    def is_smaller(self, expected_smaller, expected_bigger):
        """
        The function checks if one variable is bigger then the second variable
        :param expected_smaller: the variable that should be smaller
        :param expected_bigger: the variable that should be smaller
        :return: true if smaller small then the bigger
        """
        return expected_smaller < expected_bigger

    def practice(self,vs, args, frame):
        """
        The central function, is responsible for all the logic that checks whether the trainee has performed the
        required movement and counts him accordingly the amount of repetitions he has performed. The function each time
        receives the current frame from the camera that captures the trainee performing the exercise,
        pre-processing the image and checking whether he has performed a full repetition of the exercise.
        :param frame: the current frame from the camera
        :return: retun the frame with text on him.
        """
        font = cv2.FONT_HERSHEY_SIMPLEX
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
            if self.is_smaller(cY, M_max_y):
                max_c = c
                M_max_x = cX
                M_max_y = cY

        if len(cnts) > 0:
            cv2.drawContours(frame, [max_c], -1, (0, 255, 0), 2)
            cv2.circle(frame, (M_max_x, M_max_y), 7, (255, 255, 255), -1)
            cv2.putText(frame, "center", (M_max_x - 20, M_max_y - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        cv2.putText(frame,
                    str(self.counter),
                    (50, 50),
                    font, 1,
                    (0, 255, 255),
                    2,
                    cv2.LINE_4)

        indices = np.where(thresh == [255])

        yCoordinatesAvarage = M_max_y
        # myCalc = np.sum(indices[1])/len(indices[1])

        if self.maxAvarage == 0:
            t1 = timer()

            if yCoordinatesAvarage > 0 and t1-self.t0 > 3:
                time.sleep(2)

                self.speak("3")
                self.speak("2 ")
                self.speak("1 ")
                self.speak("GO!")
                self.maxAvarage = M_max_y

        if self.is_smaller(yCoordinatesAvarage + self.addition_counter, self.maxAvarage) and self.isDown:

            self.counter += 1
            self.speak(str(self.counter))
            self.isDown = False

        if self.is_smaller(self.maxAvarage, yCoordinatesAvarage + self.addition_down) and self.maxAvarage != 0 and yCoordinatesAvarage != 0:
            self.isDown = True

        self.firstFrame = gray
        return frame
