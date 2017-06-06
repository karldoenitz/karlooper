# -*-coding:utf-8-*-

try:
    from base64encrypt import Encryption as StrEncryption
except ImportError:
    from des_encrypt import DES as StrEncryption
