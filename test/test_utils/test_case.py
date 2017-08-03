# -*-encoding:utf-8-*-

from karlooper.utils.encrypt import StrEncryption


def test():
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


if __name__ == '__main__':
    test()
