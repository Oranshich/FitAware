# import the necessary packages
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import numpy as np
from modules.SpeakingQueue import SpeakingQueue
q = SpeakingQueue()

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

def speak(text):
    q.push(text)


def practice():

    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="path to the video file")
    ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")

    args = vars(ap.parse_args())
    # if the video argument is None, then we are reading from webcam
    if args.get("video", None) is None:
        vs = VideoStream(src=0).start()
        time.sleep(2.0)
    # otherwise, we are reading from a video file
    else:
        vs = cv2.VideoCapture(args["video"])
    # initialize the first frame in the video stream
    firstFrame = None
    counter = 0
    isDown = False
    maxAvarage = 0

    # loop over the frames of the video
    while True:

        # grab the current frame and initialize the occupied/unoccupied
        # text
        frame = vs.read()
        frame = frame if args.get("video", None) is None else frame[1]
        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if frame is None:
            break
        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)

        indices = np.where(thresh == [255])
        yCoordinatesAvarage = np.median(indices[1], axis=0)

        if maxAvarage == 0:
            print("inside")

            if yCoordinatesAvarage > 0:

                speak("3")
                speak("2 ")
                speak("1 ")
                speak("GO!")
                maxAvarage = 250


        # yCoordinatesAvarage, frame = get_current_avg(vs, firstFrame, args)
        if yCoordinatesAvarage >= maxAvarage and isDown:
            if yCoordinatesAvarage > maxAvarage:
                maxAvarage = yCoordinatesAvarage - 20
            counter += 1
            speak(str(counter))
            isDown = False

        if yCoordinatesAvarage < maxAvarage:
            isDown = True

        print("you did ", counter)
        print("Avarage ", yCoordinatesAvarage)
        print("Max Aavrage", maxAvarage)
        # show the frame and record if the user presses a key
        # cv2.imshow("Security Feed", frame)
        cv2.imshow("Thresh", frame)
        # cv2.imshow("Frame Delta", frameDelta)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break
    # cleanup the camera and close any open windows
    vs.stop() if args.get("video", None) is None else vs.release()
    cv2.destroyAllWindows()
