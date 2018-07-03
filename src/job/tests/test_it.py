import os

from job.main import Job

def test_smoke():
    times = 1_000

    job = Job (cfg = dict (
        times     = times,
        processes = 2,
        threads   = 2,
        loglevel  = 'info',
        timeout   = None,
    ))

    assert job.calculations_submitted == times
    assert job.results_collected == times


def test_sigalrm():
    times = 10_000

    job = Job (cfg = dict (
        times     = times,
        processes = 1,
        threads   = 1,
        loglevel  = 'info',
        timeout   = 1,
    ))

    assert job.calculations_submitted < times
    assert job.results_collected < times
    assert job.results_collected < job.calculations_submitted


if __name__ == '__main__':
    test_smoke()
