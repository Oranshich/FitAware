from modules.PracticeBase import PracticeBase


class Bicep(PracticeBase):

    def __init__(self):
        super(Bicep, self).__init__()
        self.addition_down = 130
        self.addition_counter = 20

    def is_smaller(self, expected_bigger, expected_smaller):
        return expected_smaller < expected_bigger
