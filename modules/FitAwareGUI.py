import argparse
import time

import cv2
from imutils.video import VideoStream
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRoundFlatButton

from modules.BicepExcercise import Bicep

class WelcomeScreen(Screen):
    pass

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.box = BoxLayout()
        self.cam = None

        self.create_camera()
        self.btn = MDRoundFlatButton()
        self.btn.text = "Back"
        self.box.add_widget(self.btn)
        self.add_widget(self.box)

    def create_camera(self):
        vs = cv2.VideoCapture(0)
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video", help="path to the video file")
        ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")

        args = vars(ap.parse_args())
        self.cam = KivyCamera(capture=vs, fps=60, args=args)
        # self.cam.started = True
        self.box.add_widget(self.cam)


class KivyCamera(Image):
    def __init__(self, capture, fps,args, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        self.args = args
        self.started = False
        self.allow_stretch = True
        self.practice_type = Bicep()
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        if self.started:
            ret, frame = self.capture.read()
            if ret:
                # convert it to texture
                frame = self.practice_type.practice(vs=self.capture, args=self.args, frame=frame)
                buf1 = cv2.flip(frame, 0)
                buf = buf1.tostring()
                image_texture = Texture.create(
                    size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                # display image from the texture
                self.texture = image_texture


class FitAwareSM(ScreenManager):


    def __init__(self, **kwargs):
        super(FitAwareSM, self).__init__(**kwargs)
        self.wlcm = WelcomeScreen()
        self.mainScrn = MainScreen()
        self.mainScrn.name = '_main_screen_'
        # self.t = testBox()
        self.add_widget(self.mainScrn)
        self.practice_type = Bicep()
        # self.call_practice()
        self.started = False


    def move_to_page(self, page_name_to_go):
        if page_name_to_go == "main":
            self.current = '_main_screen_'
            self.mainScrn.cam.started = True
        else:
            self.current = '_wlcm_screen_'
            self.mainScrn.cam.started = False


    # def call_practice(self):
    #     ap = argparse.ArgumentParser()
    #     ap.add_argument("-v", "--video", help="path to the video file")
    #     ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
    #
    #     # args = vars(ap.parse_args())
    #     # if the video argument is None, then we are reading from webcam
    #     # if args.get("video", None) is None:
    #     #     vs = VideoStream(src=0).start()
    #     #     time.sleep(2.0)
    #     # # otherwise, we are reading from a video file
    #     # else:
    #     #     vs = cv2.VideoCapture(args["video"])
    #     # Clock.schedule_interval(self.practice_type.practice(vs, args), 1.0 / 60)


class testBox(Screen):

    def __init__(self, **kwargs):
        super(testBox, self).__init__(**kwargs)
        vs = cv2.VideoCapture(0)
        self.cam = KivyCamera(capture=vs, fps=60)
        self.cam.started = True
        self.box = BoxLayout()
        self.box.add_widget(self.cam)
        self.add_widget(self.box)


class CamApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.sm = FitAwareSM()
        # self.sm = testBox()
        # self.q = SpeakingQueue()
        # vs = cv2.VideoCapture(0)
        # self.sm = KivyCamera(capture=vs,fps=60)
        # self.sm.started = True
        return self.sm



if __name__ == '__main__':
    CamApp().run()
