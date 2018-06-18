import os
import yaml

from job.main import Job

configfile = '%s/job.yml' % os.path.dirname (os.path.realpath (__file__))

with open (configfile, 'r') as config:
    job = Job (cfg = yaml.load (config))
