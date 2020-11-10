import cv2
import numpy as np
import time
import imutils
import argparse

from voiceRecognitiation import takeCommand

cap = cv2.VideoCapture(0)

ret, frame1 = cap.read()
ret, frame2 = cap.read()
counter = 0
isDown = False
maxAvarage = 100
firstFrame = None
# diff = cv2.absdiff(frame1, frame2)
# gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
# (thresh, blackAndWhiteFrame) = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
# indices = np.where(blackAndWhiteFrame == [255])
# maxAvarage = indices[1].mean()

while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if firstFrame is None:
        firstFrame = gray
        continue

    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cv2.imshow("feed", frameDelta)
    # loop over the contours
    # for c in cnts:
    #     # if the contour is too small, ignore it
    #     if cv2.contourArea(c) < args["min_area"]:
    #         continue
    #     # compute the bounding box for the contour, draw it on the frame,
    #     # and update the text
    #     (x, y, w, h) = cv2.boundingRect(c)
    #     cv2.rectangle(diff, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #     text = "Occupied"
    # gray = cv2.(gray)
    # (thresh, blackAndWhiteFrame) = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)

    # indices = np.where(blackAndWhiteFrame == [255])
    # print(indices)
    # yCoordinatesAvarage = indices[1].mean()

    # if yCoordinatesAvarage >= maxAvarage and isDown:
    #     maxAvarage = yCoordinatesAvarage
    #     counter += 1
    #     isDown = False
    #
    # if yCoordinatesAvarage < maxAvarage:
    #     isDown = True

    # print("avarage", yCoordinatesAvarage)

    # query = takeCommand()
    #
    # maxAvarage = yCoordinatesAvarage
    # if query == 'go':
    #     print("going!!!")
    #     indices = np.where(blackAndWhiteFrame == [255])
    #     print(indices)
    #     yCoordinatesAvarage = indices[1].mean()
    #     print("avarage", yCoordinatesAvarage)
    #
    #
    #     if yCoordinatesAvarage < maxAvarage:
    #         isDown = True
    print("you did ", counter)
    # print("Avarage ", yCoordinatesAvarage)
    # print("Max Aavrage", maxAvarage)
    # cv2.imshow('video bw', blackAndWhiteFrame)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("you did ", counter)
cap.release()
cv2.destroyAllWindows()

# import cv2
# import numpy as np
#
# cap = cv2.VideoCapture(0)
# frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#
# frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))
#
# fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
#
# out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1280,720))
#
# ret, frame1 = cap.read()
# ret, frame2 = cap.read()
# # print(frame1.shape)
# while cap.isOpened():
#     diff = cv2.absdiff(frame1, frame2)
#     gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(gray, (5,5), 0)
#     _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
#     dilated = cv2.dilate(thresh, None, iterations=3)
#     contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#
#     for contour in contours:
#         (x, y, w, h) = cv2.boundingRect(contour)
#
#         if cv2.contourArea(contour) < 900:
#             continue
#         cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
#         cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
#                     1, (0, 0, 255), 3)
#     #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
#
#     image = cv2.resize(frame1, (1280,720))
#     out.write(image)
#     cv2.imshow("feed", frame1)
#     frame1 = frame2
#     ret, frame2 = cap.read()
#
#     if cv2.waitKey(40) == 27:
#         break
#
# cv2.destroyAllWindows()
# cap.release()
# out.release()