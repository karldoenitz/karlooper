# -*-coding:utf-8-*-

import json
import requests

base_url = "http://127.0.0.1:9988/test"


def test_post():
    headers = {
        "content-type": "application/json"
    }
    post_data = {
        "post1": "test-post"
    }
    post_data = json.dumps(post_data, ensure_ascii=False)
    response = requests.post(base_url, post_data, headers=headers)
    content = response.content
    result = json.loads(content)
    test_result = {
        "key": "value",
        "test": 7758521,
        "post1": "test-post"
    }
    if result != test_result:
        assert "post test failed!"
    cookie = response.cookies.get("what")
    if cookie != "happened":
        assert "get cookie failed"


def test_put():
    test_result = {"msg": "cookie cleared"}
    response = requests.put(base_url)
    result = response.content
    result = json.loads(result)
    if test_result != result:
        assert "put test failed"
    cookies = response.cookies
    if cookies._cookies:
        assert "clear cookie failed"


def test():
    test_post()
    test_put()


if __name__ == '__main__':
    test()
