from itertools import islice

class CCash:
    def __init__(self, elems: list=[], top_k=10, ignore_tags='./ignore_tags.txt') -> None:
        self.data = {}
        self.top_k = top_k
        if ignore_tags:
            with open(ignore_tags, 'r') as fin:
                self.tags = set([line.strip() for line in fin.readlines()])
        for el in elems:
            self.add(el)

    def add(self, el) -> None:
        if not el in self.tags:
            if el in self.data:
                self.data[el] += 1
            else:
                self.data[el] = 1

    def get_top_k(self):
        res = dict(sorted(self.data.items(), key=lambda item: item[1], reverse=True))
        res = dict(islice(res.items(), self.top_k))
        return res
