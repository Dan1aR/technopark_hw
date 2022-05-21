'''
    Counter cache - using to find
    most popular tokens in list of tokens
'''
from itertools import islice

class CCache:
    '''
        CCache implimentation
    '''
    def __init__(self, elems: list=None, top_k=10, ignore_tags='./ignore_tags.txt'):
        self.data = {}
        self.top_k = top_k
        if ignore_tags:
            with open(ignore_tags, 'r', encoding='utf-8') as fin:
                self.tags = {line.strip() for line in fin.readlines()}
        if elems:
            for elem in elems:
                self.add(elem)

    def add(self, elem):
        '''
            Add one token to data
        '''
        if not elem in self.tags:
            if elem in self.data:
                self.data[elem] += 1
            else:
                self.data[elem] = 1

    def extend(self, elems: list):
        '''
            Add tokens to data
        '''
        for elem in elems:
            self.add(elem)

    def clear(self):
        '''
            Reset data
        '''
        self.data = {}

    def get_top_k(self):
        '''
            Getting most popular tokens
        '''
        res = dict(sorted(self.data.items(), key=lambda item: item[1], reverse=True))
        res = dict(islice(res.items(), self.top_k))
        return res
