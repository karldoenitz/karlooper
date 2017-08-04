# -*-encoding:utf-8-*-

from karlooper.coroutine.coroutine_pool import *


class TT(object):
    def __init__(self, num):
        self.sum = num

    def print_sum(self):
        print self.sum, 'a'


class Test(TT):

    @koroutine
    def test(self):
        for i in xrange(3):
            self.sum += 1
            yield i, self
        yield self.sum, self


class Parser(object):
    def parser(self):
        t = Test(6)
        result = t.test()
        if not isinstance(result, type):
            result[-1].print_sum()
            return result[0]
        return None


if __name__ == '__main__':
    p = Parser()
    for j in xrange(5):
        print p.parser()
    # t = test()
    # for j in xrange(10):
    #     print t
