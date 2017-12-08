# -*-coding:utf-8-*-

from jinja2 import Template
from karlooper.utils import PY3
import sys

if not PY3:
    reload(sys)
    sys.setdefaultencoding('utf-8')

__author__ = 'karlvorndoenitz@gmail.com'


def render(template_path, **kwargs):
    """read template from file and compile to html content

    :param template_path: template file's path
    :param kwargs: parameters
    :return: html content

    """
    with open(template_path) as template_file:
        template_data = template_file.read()
    template = Template(template_data)
    data = template.render(kwargs)
    return data


def render_string(template_string, **kwargs):
    """compile template string to html content

    :param template_string: template string
    :param kwargs: parameters
    :return: html content

    """
    template = Template(template_string)
    return template.render(kwargs)
