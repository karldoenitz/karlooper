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
        return len(self.cid_list)


__coroutine_pool = CoroutinePool()


def koroutine(method):

    @functools.wraps(method)
    def _deco(*args, **kwargs):
        global __coroutine_pool
        future = Future()
        if not hasattr(method, "coroutine_id"):
            cid = __coroutine_pool.cid_list[-1] + 1
            setattr(method, "coroutine_id", cid)
            __coroutine_pool.cid_list.append(cid)
            coroutine_obj = Coroutine()
            generator = method(*args, **kwargs)
            coroutine_obj.coroutine = generator
            coroutine_obj.context = next(generator)
            __coroutine_pool.pool[cid] = coroutine_obj
            return future
        cid = getattr(method, "coroutine_id")
        coroutine_obj = __coroutine_pool.pool.get(cid, None)
        if not coroutine_obj:
            ce = CoroutineException()
            ce.message = "Coroutine Error"
            raise ce
        coroutine = getattr(coroutine_obj, "coroutine")
        result = next(coroutine, future)
        if not isinstance(result, Future):
            setattr(coroutine_obj, "context", result)
            return future
        result = getattr(coroutine_obj, "context")
        del method.coroutine_id
        __coroutine_pool.cid_list.remove(cid)
        del __coroutine_pool.pool[cid]
        return result

    return _deco

