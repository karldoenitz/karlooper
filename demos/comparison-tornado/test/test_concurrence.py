# -*-coding:utf-8-*-

import time
import thread
import requests


def get_test_data(arg):
    print arg
    get_url = "http://127.0.0.1:9898/test"
    a = requests.get(url=get_url)
    print a.content


if __name__ == '__main__':
    thread.start_new_thread(get_test_data, (1,))
    thread.start_new_thread(get_test_data, (2,))
    thread.start_new_thread(get_test_data, (3,))
    time.sleep(2)
    # get_test_data(1)
