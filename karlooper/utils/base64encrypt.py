# -*-coding:utf-8-*-
"""

security
~~~~~~~~

Use this model to encrypt string.

Usage
=====
>>> d = Encryption()
>>> d.input_key("123456789")
>>> s = "/static/hello.js"
>>> a = d.encode(s)
>>> print a
b14f1453ceddc91e492fbe883d552a2e
>>> b = d.decode(a)
>>> print b
/static/hello.js

"""

import base64


class Encryption(object):

    def __init__(self):
        self.__key = ""

    def input_key(self, key):
        """ set base key

        :param key: str type, the base key
        :return: None

        """
        self.__key = key

    def encode(self, s):
        """ encode a string

        :param s: the string will be encoded
        :return: encoded result

        """
        return base64.b64encode(s + self.__key)

    def decode(self, s):
        """ decode a string

        :param s: the string will be decoded
        :return: decoded result

        """
        missing_padding = 4 - len(s) % 4
        if missing_padding:
            s += b'=' * missing_padding
        decode_result = base64.b64decode(s)
        result = decode_result[:len(decode_result)-len(self.__key)]
        return result
