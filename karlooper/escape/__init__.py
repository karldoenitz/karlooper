# -*-coding:utf-8-*-

import re
import urllib
import htmlentitydefs

_XHTML_ESCAPE_RE = re.compile('[&<>"\']')
_XHTML_ESCAPE_DICT = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', '\'': '&#39;'}
_BASESTRING_TYPES = (basestring, type(None))
_TO_UNICODE_TYPES = (type(u''), type(None))
_unicode_type = type(u'')


def to_unicode(value):
    """Converts a string argument to a unicode string.

    :param value: value to unicode
    :return: unicode value

    """
    if isinstance(value, _TO_UNICODE_TYPES):
        return value
    if not isinstance(value, bytes):
        raise TypeError(
            "Expected bytes, unicode, or None; got %r" % type(value)
        )
    return value.decode("utf-8")


def to_basestring(value):
    """Converts a string argument to a subclass of basestring.

    :param value: the value will to be basestring
    :return: basestring value

    """
    if isinstance(value, _BASESTRING_TYPES):
        return value
    if not isinstance(value, bytes):
        raise TypeError(
            "Expected bytes, unicode, or None; got %r" % type(value)
        )
    return value.decode("utf-8")


def utf8(value):
    """Converts a string argument to a byte string.

    :param value: value will encode to utf-8
    :return: utf-8 value

    """
    if isinstance(value, (bytes, type(None))):
        return value
    if not isinstance(value, _TO_UNICODE_TYPES):
        raise TypeError(
            "Expected bytes, unicode, or None; got %r" % type(value)
        )
    return value.encode("utf-8")


def _build_unicode_map():
    unicode_map = {}
    for name, value in htmlentitydefs.name2codepoint.items():
        unicode_map[name] = unichr(value)
    return unicode_map


def _convert_entity(m):
    if m.group(1) == "#":
        try:
            if m.group(2)[:1].lower() == 'x':
                return unichr(int(m.group(2)[1:], 16))
            else:
                return unichr(int(m.group(2)))
        except ValueError:
            return "&#%s;" % m.group(2)
    try:
        return _build_unicode_map()[m.group(2)]
    except KeyError:
        return "&%s;" % m.group(2)


def xhtml_escape(value):
    """Escapes a string so it is valid within HTML or XML.

    :param value: the value will be escaped
    :return: escaped value

    """
    return _XHTML_ESCAPE_RE.sub(
        lambda match: _XHTML_ESCAPE_DICT[match.group(0)],
        to_basestring(value)
    )


def xhtml_unescape(value):
    """Un-escapes an XML-escaped string.

    :param value: value will be escaped
    :return: unescaped value

    """
    return re.sub(r"&(#?)(\w+?);", _convert_entity, to_unicode(value))


def url_escape(value, plus=True):
    """Returns a URL-encoded version of the given value.

    :param value: url will be escaped
    :param plus: default True, whether need plus
    :return: the escaped value

    """
    quote = urllib.quote_plus if plus else urllib.quote
    return quote(utf8(value))


def url_unescape(value, encoding='utf-8', plus=True):
    """Decodes the given value from a URL.

    :param value: value will be unescaped
    :param encoding: the encoding default is utf-8
    :param plus: whether need plus default True
    :return: the unescaped url

    """
    unquote = (urllib.unquote_plus if plus else urllib.unquote)
    if encoding is None:
        return unquote(utf8(value))
    else:
        return _unicode_type(unquote(utf8(value)), encoding)
