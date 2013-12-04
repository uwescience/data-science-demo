from time import sleep

class Fight(object):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def get_answer(self):
        sleep(.2)
        return {'first': self.first, 'second': self.second}
