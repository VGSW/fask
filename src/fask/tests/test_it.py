import math

from fask.main import Fask


def simple_sqrt (x):
    return lambda: math.sqrt(x)


class Jimmy (Fask):
    def __init__ (self, **kwa):
        cfg = kwa.get ('cfg')

        self.times = cfg.get ('times')
        super().__init__ (cfg = kwa.get ('cfg'))


    def calculations (self):
        return [simple_sqrt (x) for x in range (self.times)]


def test_fask():
    times = 10

    tf = Jimmy (cfg = dict (
        times     = times,
        processes = 2,
        threads   = 2,
        debug     = False,
    ))

    assert tf.count_calculations == 10
    assert tf.count_results == 10
    assert (
        sorted ([ r.get ('result') for r in tf.results ])
        ==
        sorted ([ simple_sqrt (x)() for x in range (times) ])
    )
