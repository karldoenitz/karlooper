# -*-encoding:utf-8-*-

from karlooper.utils.encrypt import StrEncryption
from karlooper.utils.base64encrypt import Encryption
from karlooper.utils.des_encrypt import DES


def test_encrypt():
    str_encryption = StrEncryption()
    str_encryption.input_key("test")
    _str = "make a test"
    encode_str = str_encryption.encode(_str)
    decode_str = str_encryption.decode(encode_str)
    if _str != decode_str:
        print encode_str
        print decode_str
        print _str
        assert "encode string error"


def test_base64encrypt():
    str_encryption = Encryption()
    str_encryption.input_key("test")
    _str = "make a test"
    encode_str = str_encryption.encode(_str)
    decode_str = str_encryption.decode(encode_str)
    if _str != decode_str:
        print encode_str
        print decode_str
        print _str
        assert "base64 encode string error"


def test_des_encrypt():
    str_encryption = DES()
    str_encryption.input_key("test123456")
    _str = "make a test"
    encode_str = str_encryption.encode(_str)
    decode_str = str_encryption.decode(encode_str)
    if _str != decode_str:
        print encode_str
        print decode_str
        print _str
        assert "des encode string error"


def test():
    test_encrypt()
    test_base64encrypt()
    test_des_encrypt()


if __name__ == '__main__':
    test()
