# -*-encoding:utf-8-*-

from karlooper.escape import utf8
from karlooper.template import render, render_string


class Obj(object):
    def __init__(self):
        self.h1 = "This is h1"


def test():
    with open("./example_result.html", "r") as f:
        example_result = f.read()
    title = "test case"
    obj = Obj()
    numbers = [1, 2, 3, 4, 5, 6]
    dictionary = {"dict": "Tis is dict"}
    render_result = render("./example.html", title=title, obj=obj, numbers=numbers, dict=dictionary)
    render_result = render_result.replace(" ", "").replace("\t", "").replace("  ", "").replace("\n", "")
    render_result = utf8(render_result)
    example_result = example_result.replace(" ", "").replace("\t", "").replace("  ", "").replace("\n", "")
    if render_result != example_result:
        print type(example_result), type(render_result)
        print example_result
        print render_result
        assert "render error"
    with open("./example.html", "r") as f:
        example_html = f.read()
    render_result = render_string(example_html, title=title, obj=obj, numbers=numbers, dict=dictionary)
    render_result = render_result.replace(" ", "").replace("\t", "").replace("  ", "").replace("\n", "")
    render_result = utf8(render_result)
    example_result = example_result.replace(" ", "").replace("\t", "").replace("  ", "").replace("\n", "")
    if render_result != example_result:
        print type(example_result), type(render_result)
        print example_result
        print render_result
        assert "render_string error"


if __name__ == '__main__':
    test()
