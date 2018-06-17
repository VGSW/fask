from job.main import Job

def test_smoke():
    times = 1_000

    job = Job (debug = False, times = times)
    assert job.count_calculations == times
    assert job.count_results == times


if __name__ == '__main__':
    test_smoke()
