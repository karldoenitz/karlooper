# -*-encoding:utf-8-*-

from base import BaseRestHandler


class Login(BaseRestHandler):
    def process(self):
        user_name = self.get_parameter("user_name")
        password = self.get_parameter("password")
        
        
class Register(BaseRestHandler):
    def process(self):
        user_name = self.get_parameter("user_name")
        password = self.get_parameter("password")
