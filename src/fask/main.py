import logging
import os
import sys
import signal

from dask.distributed import Client, LocalCluster, as_completed


class Fask:
    def __init__ (self, **kwa):
        cfg = kwa.get ('cfg')

        loglevel = dict (
            debug = logging.DEBUG,
            info  = logging.INFO,
            warn  = logging.WARN,
            error = logging.ERROR,
        ).get (
            cfg.get ('loglevel'),
            logging.INFO,
        )

        self.reset()

        handler = logging.FileHandler ('%s/../log/fask.log' % os.path.dirname (os.path.realpath (__file__)))
        handler.setFormatter (logging.Formatter (fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger = logging.getLogger ('fask')
        self.logger.addHandler (handler)
        self.logger.setLevel (loglevel)

        self.cluster = LocalCluster (
            n_workers           = cfg.get ('processes'),
            processes           = True,
            threads_per_worker  = cfg.get ('threads'),

            # make bokeh available outside of a docker container too
            # see: https://github.com/dask/distributed/issues/1875
            # well, that was a fun two hours (for moderate values of "fun" ;-)
            ip                  = '',
        )

        self.client = Client (self.cluster)
        self.setup_signals (timeout = cfg.get ('timeout'))

        self.logger.info ('ready')

        # signalling fask to stop (SIGINT, SIGALRM) will raise SystemExit
        #
        try:
            self.run()
        except SystemExit:
            self.logger.info ('done')


    ###
    ### sysprog


    def log_status (self, caller='xxx'):
        self.logger.info ('[status at {caller}] F {futures} | dF {done_futures} | cF {cancelled_future}| !cdF {not_cancelled_and_done} | CS {cs} | RC {rc}'.format (
            caller = caller,
            futures = len (self.futures),
            done_futures = len (list (filter (lambda f: f.done() == True, self.futures))),
            cancelled_future = len (list (filter (lambda f: f.cancelled() == True, self.futures))),
            not_cancelled_and_done = len (list (filter (lambda f: f.cancelled() == False and f.done() == True, self.futures))),
            cs = self.calculations_submitted,
            rc = self.results_collected,
        ))


    def cleanup (self):
        self.logger.info ('cleaning up')
        self.log_status('cleanup')

        self.collect_results (all = False)

        # Client.cancel()
        # This stops future tasks from being scheduled if they have not yet
        # run and deletes them if they have already run. After calling, this
        # result and all dependent results will no longer be accessible

        self.logger.info ('cancel all futures')

        # XXX
        # cancelling a future also markes it done
        self.client.cancel (self.futures)


    def setup_signals (self, **kwa):
        signal.signal (signal.SIGINT, self.handler_sigint)

        if kwa.get ('timeout'):
            signal.signal (signal.SIGALRM, self.handler_sigalrm)
            signal.alarm (kwa.get ('timeout'))


    def handler_sigint (self, signum, frame):
        self.logger.warning ('exit because of SIGINT')
        self.cleanup()
        self.bailout()


    def handler_sigalrm (self, signum, frame):
        self.logger.warning ('exit because of SIGALRM')
        self.cleanup()
        self.bailout()


    def bailout (self):
        self.logger.warning ('bailing out')
        self.log_status('bailout')
        sys.exit (0)


    def reset (self):
        self.calculations_submitted = 0
        self.results_collected      = 0
        self.results            = []
        self.futures            = []


    ###
    ### worker

    def run (self):
        """ submit all given calculations
        """
        self.reset()

        if not len (self.calculations()):
            raise (LookupError, 'no calculations available')

        for ci, c in enumerate (self.calculations()):
            future = self.client.submit (c, pure = False)

            self.logger.debug ('[{ci}] future {key} submitted'.format (ci = ci, key = future.key))
            self.futures.append (future)
            self.calculations_submitted += 1

        self.log_status('run')
        self.collect_results (all = True)


    def collect_results (self, **kwa):
        """ collect (and log) results as they become available
            (this will block)
        """

        if kwa.get ('all'):
            self.logger.info ('collect all results')
            futures = as_completed (self.futures)
        else:
            self.logger.info ('collect already done results only')
            futures = filter (lambda f: f.done() == True, self.futures)

        # for xi, future in enumerate (as_completed (self.futures)):
        for xi, future in enumerate (futures):
            self.results_collected += 1
            result = future.result()
            key = future.key
            # future.cancel()

            self.logger.debug ('[{xi}] future {key} yielded {result}'.format (xi = xi, key = key, result = result))

            self.results.append (dict (
                index = xi,
                result = result,
            ))

        self.log_status ('collect_results')


    def calculations (self):
        """ overwrite this virtual method
            this is where your actual code goes

            OUT: a list of functions to run
        """

        raise NotImplementedError ('virtual method run() not implemented')


if __name__ == '__main__':
    raise (NotImplementedError, 'Fask can not be run directly')
