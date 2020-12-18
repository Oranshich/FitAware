# import the necessary packages
from imutils.video import VideoStream
import argparse
import imutils
import time
from timeit import default_timer as timer
import cv2
import numpy as np

from modules.PracticeBase import PracticeBase
from modules.SpeakingQueue import SpeakingQueue



class Bicep(PracticeBase):

    def __init__(self):
        super(Bicep, self).__init__()
        self.addition_down = 130
        self.addition_counter = 20

    def is_smaller(self, expected_bigger, expected_smaller):
        return expected_smaller < expected_bigger