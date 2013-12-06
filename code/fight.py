from time import sleep

class Fight(object):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def get_answer(self):
        sleep(.2)
        return [{'label': self.first, 'value': 10},
                {'label': self.second, 'value': 5}]
