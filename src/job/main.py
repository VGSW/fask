import os
import random
import numpy

from fask.main import Fask

def randoms (times):
    return lambda: numpy.mean ([ random.randint(1, times) for _ in range (times) ])

class Job (Fask):
    def __init__ (self, **kwa):
        self.cfg = kwa.get ('cfg')
        super().__init__ (cfg = self.cfg)


    def calculations (self):
        times = self.cfg.get ('times')
        return [randoms(times) for _ in range (times)]
