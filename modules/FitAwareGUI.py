import argparse
import cv2
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.toolbar import MDToolbar
from modules.BicepExcercise import Bicep
from modules.PushUpExcercise import PushUp

"""
This is the Main Py file of the FitAware,
it is starting the GUI and the Algorithm app
"""

class WelcomeScreen(Screen):
    """
    This class is representing the welcome window in the KV file
    """
    pass


class MainScreen(Screen):
    """
    This class is representing the Main window of the app,
    is has a child widget of the KivyCamera which is runs the camera for
    capturing the video
    """
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
        """
        This function is creating the toolbar of the Main screen to be similar as the Welcome screen
        """
        self.toolbar.title = "Fit Aware"
        self.toolbar.type = "top"
        self.toolbar.anchor_title = 'center'
        self.toolbar.left_action_items = [["keyboard-backspace", lambda x: self.parent.move_to_page("else")]]
        self.toolbar.elevation = 10

    def create_camera(self):
        """
        This function is creating the OpenCV camera
        with the video capturing and creates the
        KivyCamera child of the Main Screen
        """
        self.vs = cv2.VideoCapture(0)
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video", help="path to the video file")
        ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")

        args = vars(ap.parse_args())
        if self.cam in self.grid.children:
            self.grid.remove_widget(self.cam)
        self.cam = KivyCamera(capture=self.vs, fps=1000000, args=args, pr_type=self.practice_type,
                              prnt=self)
        self.grid.add_widget(self.cam)
        # self.cam.started = True


class KivyCamera(Image):
    """
    This class is representing the KivyCamera widget
    it is inheriting from the Image widget of Kivy
    in-order to show the captured video
    """
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

    def update(self):
        """
        This function is the update function
        is it being called every 1 / fps
        and it updates the Image in the widget
        so it look like it is a video
        """
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
    """
    This class is representing the Screen Manager
    of the App, this manager is managing the two screens of the app
    the <i>Welcome Screen</i> \n
    and the <i>Main Screen</i>
    """

    def __init__(self, prnt, **kwargs):
        super(FitAwareSM, self).__init__(**kwargs)
        self.prnt = prnt
        self.dialog = None
        self.wlcm = WelcomeScreen()
        self.mainScrn = MainScreen(scrn_mngr=self)
        self.mainScrn.name = '_main_screen_'
        # self.t = testBox()
        self.add_widget(self.wlcm)
        self.add_widget(self.mainScrn)
        self.practice_type = Bicep()
        # self.call_practice()
        self.started = False

    def move_to_page(self, page_name_to_go):
        """
        This function is getting the name of the next screen
        and change the screen of the app
        :param page_name_to_go: the name of the next screen to go to
        """
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
        """
        This function is cleaning the Welcome Screen before changing back to it,
        it needs to be cleaned from the input data of the user
        """
        chooser = self.wlcm.ids.chooser
        for chip in chooser.children:
            chip.color = chip.theme_cls.primary_color
        self.wlcm.ids.rep_num.text = ""

    def show_alert_dialog(self, text):
        """
        This function is getting a text message
        and popups a modal windows with message
        :param text: the text to show to the user
        """
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
        """
        This function is closing the opened dialog
        """
        self.dialog.dismiss(force=True)

    def validate_inputs(self):
        """
        This function is validating the inputs of the user
        """
        try:
            if self.mainScrn.practice_type is None or int(self.wlcm.ids.rep_num.text) <= 0:
                return False
            else:
                self.mainScrn.create_camera()
                return True
        except Exception:
            return False

    def success(self,msg, speakingQ):
        """
        This function is  getting a message and a Queue of speaking Queue
        and reading the given message to the user
        :param msg: the message to be read to the user
        :param speakingQ: the Queue of the messages
        """
        self.change_screen_to_welcome()
        speakingQ.push(msg)
        self.show_alert_dialog("Well Done!")


    def change_screen_to_welcome(self):
        """
        This function is changing the screen specifically to the Welcome screen
        :return:
        """
        self.clear_welcome_screen()
        self.current = '_wlcm_screen_'
        self.mainScrn.vs.release()
        self.mainScrn.cam.started = False


class CamApp(MDApp):

    def build(self):
        self.sm = FitAwareSM(prnt=self)
        self.theme_cls.primary_palette = "Teal"
        self.title = "Fit Aware"

        return self.sm

    def select_practice(self,instance, value):
        self.sm.mainScrn.practice_type = Bicep() if str(value).lower() in "bicep" else PushUp()


if __name__ == '__main__':
    cam_app = CamApp()
    cam_app.run()
    cam_app.sm.mainScrn.practice_type.q.stop()

