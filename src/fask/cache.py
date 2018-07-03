import hashlib

class Cache ():

    def __init__ (self, **kwa):
        self.logger = kwa.get ('logger')
        self._cache = dict()

    @classmethod
    def genkey (cls, fn, params):
        key = str (id (fn))
        for p in [params]:
            key += str (id (p))

        return hashlib.sha256 (key.encode ('utf8')).hexdigest()

    def has (self, **kwa):
        fn     = kwa.get ('fn')
        params = kwa.get ('params')
        key    = self.genkey (fn, params)

        if self._cache.get (key):
            self.logger.error ('[cache] known key: <{key}>'.format (key = key))
            return True
        else:
            self.logger.error ('[cache] new key: <{key}>'.format (key = key))
            return False

    def add (self, **kwa):
        fn     = kwa.get ('fn')
        params = kwa.get ('params')
        key    = self.genkey (fn, params)

        self._cache[key] = True

    def delete (self):
        fn     = kwa.get ('fn')
        params = kwa.get ('params')
        key    = self.genkey (fn, params)

        del self._cache[key]

