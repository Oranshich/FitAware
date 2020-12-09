from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from modules.SpeakingQueue import SpeakingQueue

class WelcomeScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class FitAwareSM(ScreenManager):


    def __init__(self, **kwargs):
        super(FitAwareSM, self).__init__(**kwargs)
        self.wlcm = WelcomeScreen()
        self.mainScrn = MainScreen()

    def move_to_page(self, page_name_to_go):
        self.current = '_main_screen_' if page_name_to_go == "main" else '_wlcm_screen_'


class CamApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.sm = FitAwareSM()
        # self.q = SpeakingQueue()
        return self.sm



if __name__ == '__main__':
    CamApp().run()
