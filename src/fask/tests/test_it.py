import math

from fask.main import Fask


def simple_sqrt (x):
    return lambda: math.sqrt(x)


class Jimmy (Fask):
    def __init__ (self, **kwa):
        self.times = kwa.get ('times')
        super().__init__ (debug = kwa.get ('debug'))


    def calculations (self):
        return [simple_sqrt (x) for x in range (self.times)]


def test_fask():
    times = 10

    tf = Jimmy (
        debug = False,
        times = times,
    )

    assert tf.count_calculations == 10
    assert tf.count_results == 10
    assert (
        sorted ([ r.get ('result') for r in tf.results ])
        ==
        sorted ([ simple_sqrt (x)() for x in range (times) ])
    )
