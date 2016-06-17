# -*-coding:utf-8-*-

from jinja2 import Template
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

__author__ = 'karlvorndoenitz@gmail.com'


def render(template_path, **kwargs):
    template_file = open(template_path)
    template_data = template_file.read()
    template = Template(template_data)
    data = template.render(kwargs)
    template_file.close()
    return data


def render_string(template_string, **kwargs):
    template = Template(template_string)
    return template.render(kwargs)
