# -*-encoding:utf-8-*-

import functools


class Future(object):
    pass


class CoroutineException(Exception):
    message = None


class Coroutine(object):
    coroutine = None
    context = None


class CoroutinePool(object):
    cid_list = [0]
    pool = {}

    @property
    def size(self):
        """ get coroutine pool's size

        :return: size

        """
        return len(self.cid_list)

    def add(self, cid, coroutine_obj):
        """ add a coroutine object to coroutine pool

        :param cid: coroutine id
        :param coroutine_obj: coroutine object
        :return: None

        """
        self.cid_list.append(cid)
        self.pool[cid] = coroutine_obj

    def remove(self, cid):
        """ remove the coroutine object by id

        :param cid: coroutine's id
        :return: None

        """
        self.cid_list.remove(cid)
        del self.pool[cid]


__coroutine_pool = CoroutinePool()


def koroutine(method):

    @functools.wraps(method)
    def _deco(*args, **kwargs):
        global __coroutine_pool
        if not hasattr(method, "coroutine_id"):
            cid = __coroutine_pool.cid_list[-1] + 1
            setattr(method, "coroutine_id", cid)
            coroutine_obj = Coroutine()
            generator = method(*args, **kwargs)
            coroutine_obj.coroutine = generator
            coroutine_obj.context = next(generator)
            __coroutine_pool.add(cid, coroutine_obj)
            return Future
        cid = getattr(method, "coroutine_id")
        coroutine_obj = __coroutine_pool.pool.get(cid, None)
        if not coroutine_obj:
            ce = CoroutineException()
            ce.message = "Coroutine Error"
            raise ce
        coroutine = getattr(coroutine_obj, "coroutine")
        result = next(coroutine, Future)
        if not isinstance(result, type):
            setattr(coroutine_obj, "context", result)
            return Future
        result = getattr(coroutine_obj, "context")
        del method.coroutine_id
        __coroutine_pool.remove(cid)
        return result

    return _deco
