from modules.PracticeBase import PracticeBase


class PushUp(PracticeBase):
    def __init__(self):
        super(PushUp, self).__init__()
        self.addition_down = -150
        self.addition_counter = -20