# -*-coding:utf-8-*-
"""

security
~~~~~~~~

Use this model to encrypt string.

Usage
=====
>>> d = StrEncryption()
>>> d.input_key("123456789")
>>> s = "/static/hello.js"
>>> a = d.encode(s)
>>> print a
L3N0YXRpYy9oZWxsby5qczEyMzQ1Njc4OQ==
>>> b = d.decode(a)
>>> print b
/static/hello.js

"""

__author__ = 'karlvorndoenitz@gmail.com'


try:
    from encryption import encrypt_str, decrypt_str


    class StrEncryption(object):
        def __init__(self):
            self.__key = ""

        def input_key(self, key):
            """ set input key

            :param key: input key
            :return: None

            """
            self.__key = key

        def encode(self, s):
            """ encode string

            :param s: the string will be encoded
            :return: the string be encoded

            """
            return encrypt_str(s + self.__key)

        def decode(self, s):
            """ decode string

            :param s: the string will be decoded
            :return: the string be decoded

            """
            decode_result = decrypt_str(s)
            return decode_result[:len(decode_result)-len(self.__key)]

except ImportError:
    try:
        from base64encrypt import Encryption as StrEncryption
    except ImportError:
        from des_encrypt import DES as StrEncryption
