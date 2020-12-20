from modules.PracticeBase import PracticeBase


class Bicep(PracticeBase):
    """
    The class of the Bicep exercise, inherit from PracticeBase, override the is_smaller function to adapt to the
     bicep exercise.
    """

    def __init__(self):
        super(Bicep, self).__init__()
        self.addition_down = 130
        self.addition_counter = 20

    def is_smaller(self, expected_bigger, expected_smaller):
        """
        Override the is_smaller function form PracticeBase, the only difference is the opposite sign
        :return: true if the the smaller variable small then the bigger variable.
        """
        return expected_smaller < expected_bigger
