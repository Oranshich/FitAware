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
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.toolbar import MDToolbar

from modules.BicepExcercise import Bicep
from modules.PushUpExcercise import PushUp


class WelcomeScreen(Screen):
    pass

class MainScreen(Screen):
    def __init__(self, scrn_mngr, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.grid = MDGridLayout()
        self.grid.cols = 1
        # self.manager.transition.direction = 'right'
        scrn_mngr.transition.direction = 'right'

        self.toolbar = MDToolbar()
        self.set_tool_bar_params()
        self.grid.add_widget(self.toolbar)

        ''' Create the camera view'''
        self.cam = None
        self.create_camera()

        # ''' Set the back button'''
        # self.set_back_btn()

        self.add_widget(self.grid)

    # def set_back_btn(self):
    #     # box = MDBoxLayout()
    #     btn = MDRoundFlatButton()
    #     btn.text = "Back"
    #
    #     # box.add_widget(btn)
    #     # box.orientation = 'vertical'
    #     # box.center_x = 0.5
    #     # box.center_y = 0.5
    #     # box.height = 25
    #     self.grid.add_widget(btn)

    def set_tool_bar_params(self):
        self.toolbar.title = "Fit Aware"
        self.toolbar.type = "top"
        self.toolbar.anchor_title = 'center'
        self.toolbar.left_action_items = [["keyboard-backspace", lambda x: self.parent.move_to_page("else")]]
        self.toolbar.elevation = 10

    def create_camera(self):
        vs = cv2.VideoCapture(0)
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video", help="path to the video file")
        ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")

        args = vars(ap.parse_args())
        self.cam = KivyCamera(capture=vs, fps=100, args=args)
        # self.cam.started = True
        self.grid.add_widget(self.cam)


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
        self.mainScrn = MainScreen(scrn_mngr=self)
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
            self.mainScrn.cam.practice_type.clear()
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
