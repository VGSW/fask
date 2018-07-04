import pytest
import math
import time
import random


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
        loglevel  = 'debug',
    ))

    assert tf.calculations_submitted == 10
    assert tf.results_collected == 10
    assert (
        sorted ([ r.get ('result') for r in tf.results ])
        ==
        sorted ([ simple_sqrt (x)() for x in range (times) ])
    )


class Hendrix (Fask):
    def __init__ (self, **kwa):
        cfg = kwa.get ('cfg')

        self.times = cfg.get ('times')
        super().__init__ (cfg = kwa.get ('cfg'))


def test_fask_hendrix():
    times = 10

    with pytest.raises (NotImplementedError):
        tf = Hendrix (cfg = dict (
            times     = times,
            processes = 2,
            threads   = 2,
            loglevel  = 'error',
        ))

class Sid (Fask):
    def __init__ (self, **kwa):
        cfg = kwa.get ('cfg')

        self.times = cfg.get ('times')
        super().__init__ (cfg = kwa.get ('cfg'))


    def calculations (self):
        return [simple_sqrt (x) for x in range (self.times)]

    def stop_condition (self):
        return random.randint (1, 10) % 2 == 0 and True or False


def test_fask_sid():
    # XXX this test will in most cases succeed, but it might not
    # more deterministic stop_condition will fix this
    times = 1000

    tf = Sid (cfg = dict (
        times     = times,
        processes = 2,
        threads   = 2,
        loglevel  = 'error',
    ))

    assert tf.calculations_submitted < times
    assert tf.results_collected < times
