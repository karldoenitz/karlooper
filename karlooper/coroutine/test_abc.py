# -*-encoding:utf-8-*-

from coroutine_pool import *


# class Future(object):
#     pass
#
#
# def test():
#     yield 1
#     yield 2
#     yield 3
#     yield 4
#     yield 5
#
#
# a = test()
# print next(a, Future)
# print next(a, Future)
# print next(a, Future)
# print next(a, Future)
# print next(a, Future)
# print next(a, Future)


class Test(object):
    @koroutine
    def test(self):
        for i in xrange(3):
            yield i


class Parser(object):
    def parser(self):
        t = Test()
        return t.test()


if __name__ == '__main__':
    p = Parser()
    for j in xrange(5):
        print p.parser()
    # t = test()
    # for j in xrange(10):
    #     print t
