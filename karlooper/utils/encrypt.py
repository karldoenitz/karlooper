# -*-coding:utf-8-*-
"""

"""
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
            return encrypt_str(s, self.__key)

        def decode(self, s):
            """ decode string

            :param s: the string will be decoded
            :return: the string be decoded

            """
            return decrypt_str(s, self.__key)

except ImportError:
    try:
        from base64encrypt import Encryption as StrEncryption
    except ImportError:
        from des_encrypt import DES as StrEncryption
