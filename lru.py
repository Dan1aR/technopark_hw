''' LRUcache implementation'''


class LRUCache:
    ''' LRUcache class'''
    def __init__(self, limit=42):
        self.cache = {}
        self.keys = []
        self.full = False
        self.limit = limit

    def get(self, key):
        ''' LRUcache get method'''
        if key in self.cache:
            self.keys.remove(key)
            self.keys.insert(0, key)
            return self.cache[key]
        return None

    def __getitem__(self, key):
        ''' getitem wrapper'''
        return self.get(key)

    def set(self, key, value):
        ''' LRUcache set method'''
        if key in self.cache:
            self.keys.remove(key)
        else:
            if self.full:
                last_key = self.keys[-1]
                self.cache.pop(last_key)

        self.cache[key] = value
        self.keys.insert(0, key)
        self.full = len(self.cache) == self.limit

    def __setitem__(self, key, value):
        ''' setitem wrapper '''
        self.set(key, value)

    def pop(self, key):
        ''' LRUcache pop method'''
        if key in self.cache:
            self.keys.remove(key)
        self.full = len(self.keys) == self.limit
        return self.cache.pop(key, None)

    def __len__(self):
        return len(self.cache)

