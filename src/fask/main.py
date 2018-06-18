from dask.distributed import Client, LocalCluster, as_completed


class Fask:
    def __init__ (self, **kwa):
        """ kwa.debug ... print some debug output
        """

        cfg = kwa.get ('cfg')

        self.debug = cfg.get ('debug')
        self.reset()

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

        if self.debug:
            print ("started")

        self.run()


    # def __del__ (self):
    #     # self.client.cancel()
    #     self.cluster.close()


    def reset (self):
        self.count_calculations = 0
        self.count_results      = 0
        self.results            = []


    def run (self):
        self.reset()
        cs = self.calculations()

        if not len (cs):
            raise (LookupError, 'no calculations available')

        futures = []
        for ci, c in enumerate (cs):
            # futures.append (self.client.submit (c))
            futures.append (self.client.submit (c, pure = False))
            self.count_calculations += 1

        for xi, future in enumerate (as_completed (futures)):
            self.count_results += 1
            result = future.result()
            future.cancel()

            if self.debug:
                print ('task {xi} result: {result}'.format (
                    xi = xi,
                    result = result,
                ))

            self.results.append (dict (
                index = xi,
                result = result,
            ))

        print ('ran {ci} calculations; collected {xi} results'.format (
            ci = self.count_calculations,
            xi = self.count_results,
        ))


    def calculations (self):
        """ overwrite this virtual method
            this is where your actual code goes

            OUT: a list of functions to run
        """

        raise (NotImplementedError, 'virtual method run() not implemented')


if __name__ == '__main__':
    raise (NotImplementedError, 'Fask can not be run directly')
