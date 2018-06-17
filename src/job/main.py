import random
import numpy

from fask.main import Fask

def randoms ():
    return lambda: numpy.mean ([ random.randint(1, 1_000) for _ in range (1_000) ])

class Job (Fask):
    def __init__ (self, **kwa):
        self.times = kwa.get ('times')
        super().__init__ (debug = kwa.get ('debug'))


    def calculations (self):
        return [randoms() for _ in range (self.times)]


if __name__ == '__main__':
    job = Job (
        debug = False,
        times = 10,
    )
