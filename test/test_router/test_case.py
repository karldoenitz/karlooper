# -*-encoding:utf-8-*-

from karlooper.router.router import Router, PathParam


class Test(object):
    pass


handlers = {
    "/test": Test,
    "/path/{test}": Test
}


def test():
    router = Router(handles=handlers, url="/test")
    handler = router.get_handler()
    if Test != handler[0] and (not isinstance(handler[1], PathParam)):
        print(Test)
        print(handler)
        assert "Router get handler error"
    router = Router(handles=handlers, url="/path/test-param")
    path_param = router.get_path_param("/path/{test}")
    if path_param.value.get("test") != "test-param":
        print(router.get_path_param("/path/{test}"))
        assert "Router get path param error"


if __name__ == '__main__':
    test()
