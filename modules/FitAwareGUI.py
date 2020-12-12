import argparse
import time

import cv2
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivymd.uix.button import MDRoundFlatButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.chip import MDChip
from modules.BicepExcercise import Bicep
from modules.PushUpExcercise import PushUP

class WelcomeScreen(Screen):
    pass

class MainScreen(Screen):
    def __init__(self, scrn_mngr, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.grid = MDGridLayout()
        self.grid.cols = 1
        self.practice_type = None
        self.vs = None
        self.rep_num = 0
        # self.manager.transition.direction = 'right'
        self.scrn_mngr = scrn_mngr
        self.scrn_mngr.transition.direction = 'right'

        self.toolbar = MDToolbar()
        self.set_tool_bar_params()
        self.grid.add_widget(self.toolbar)

        # ''' Create the camera view'''
        self.cam = None
        # self.grid.add_widget(self.cam)

        # self.create_camera()

        # ''' Set the back button'''
        # self.set_back_btn()

        self.add_widget(self.grid)



    def set_tool_bar_params(self):
        self.toolbar.title = "Fit Aware"
        self.toolbar.type = "top"
        self.toolbar.anchor_title = 'center'
        self.toolbar.left_action_items = [["keyboard-backspace", lambda x: self.parent.move_to_page("else")]]
        self.toolbar.elevation = 10

    def create_camera(self):
        self.vs = cv2.VideoCapture(0)
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video", help="path to the video file")
        ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")

        args = vars(ap.parse_args())
        if self.cam in self.grid.children:
            self.grid.remove_widget(self.cam)
        self.cam = KivyCamera(capture=self.vs, fps=60, args=args, pr_type=self.practice_type,
                              prnt=self)
        self.grid.add_widget(self.cam)
        # self.cam.started = True


class KivyCamera(Image):
    def __init__(self, capture, fps,args, pr_type, prnt, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        self.args = args
        self.prnt = prnt
        self.rep_num = 0
        self.started = False
        self.allow_stretch = True
        self.practice_type = pr_type
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        if self.started:
            ret, frame = self.capture.read()
            if ret:
                # convert it to texture
                frame = self.practice_type.practice(vs=self.capture, args=self.args, frame=frame)
                if self.practice_type.counter >= self.rep_num:
                    # self.practice_type.q.push("Success")
                    self.started = False
                    Clock.unschedule(self.update)
                    self.prnt.scrn_mngr.success("success", self.practice_type.q)
                buf1 = cv2.flip(frame, 0)
                buf = buf1.tostring()
                image_texture = Texture.create(
                    size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                # display image from the texture
                self.texture = image_texture


class FitAwareSM(ScreenManager):


    def __init__(self, prnt, **kwargs):
        super(FitAwareSM, self).__init__(**kwargs)
        self.prnt = prnt
        #self.dialog = None
        self.wlcm = WelcomeScreen()
        #self.mainScrn = MainScreen(scrn_mngr=self)
        #self.mainScrn.name = '_main_screen_'
        # self.t = testBox()
        self.add_widget(self.wlcm)
        #self.add_widget(self.mainScrn)
        self.practice_type = None
        # self.call_practice()
        self.started = False

    def move_to_page(self, page_name_to_go):
        if page_name_to_go == "main":
            if self.validate_inputs():
                self.current = '_main_screen_'
                self.mainScrn.cam.started = True
                self.mainScrn.cam.practice_type.clear()
                self.mainScrn.cam.rep_num = int(self.wlcm.ids.rep_num.text)
            else:
                self.show_alert_dialog("Please choose practice type and Fill the number of repetitions")
        else:
            self.change_screen_to_welcome()

    def clear_welcome_screen(self):
        chooser = self.wlcm.ids.chooser
        for chip in chooser.children:
            chip.color = chip.theme_cls.primary_color
        self.wlcm.ids.rep_num.text = ""

    def show_alert_dialog(self, text):
        if not self.dialog:
            self.dialog = MDDialog(
                text="",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        text_color=self.prnt.theme_cls.primary_color
                    )
                ],
            )
            self.dialog.buttons[0].bind(on_press=self.close_dialog)
        self.dialog.text = text
        self.dialog.open()

    def close_dialog(self, instance):
        self.dialog.dismiss(force=True)

    def validate_inputs(self):
        if self.mainScrn.practice_type is None or len(self.wlcm.ids.rep_num.text) == 0:
            return False
        else:
            self.mainScrn.create_camera()
            return True

    def success(self,msg, speakingQ):
        self.change_screen_to_welcome()
        speakingQ.push(msg)
        self.show_alert_dialog("Well Done!")


    def change_screen_to_welcome(self):
        self.clear_welcome_screen()
        self.current = '_wlcm_screen_'
        self.mainScrn.vs.release()
        self.mainScrn.cam.started = False


class CamApp(App):

    def build(self):
        self.sm = FitAwareSM(prnt=self)
        #self.theme_cls.primary_palette = "Teal"
        self.title = "Fit Aware"

        return self.sm

    def select_practice(self,instance, value):
        self.sm.mainScrn.practice_type = Bicep() if str(value).lower() in "bicep" else PushUP()


if __name__ == '__main__':
    CamApp().run()
