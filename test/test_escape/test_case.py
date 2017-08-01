# -*-encoding:utf-8-*-

from karlooper.escape import *


def test():
    if not isinstance(to_unicode("test"), unicode):
        assert "to_unicode error"
    if to_basestring("test").__class__.__name__ != "basestring":
        assert "to_basestring error"
    if not isinstance(utf8("test"), (bytes, type(None))):
        assert "utf8 error"
    html = "<html><head><title>test</title></head><body><h1>hello world!</h1></body></html>"
    html_escape = xhtml_escape(html)
    if html != xhtml_unescape(html_escape):
        print html
        print html_escape
        assert "html escape or unescape error"
    url = "http://www.test.com/test?param=参数"
    url_escaped = url_escape(url)
    if url != url_unescape(url_escaped):
        print url
        print url_escaped
        assert "url escape or unescape error"


if __name__ == '__main__':
    test()
