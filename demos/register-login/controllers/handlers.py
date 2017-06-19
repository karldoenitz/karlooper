# -*-encoding:utf-8-*-

from base import is_login
from karlooper.web.request import Request


class Login(Request):
    def get(self):
        return self.render("/register-login.html", button="login", title="LOGIN")


class Register(Request):
    def get(self):
        return self.render("/register-login.html", button="sign up", title="REGISTER")


class MainPage(Request):
    @is_login
    def get(self):
        return self.http_response(
            "<html>"
            "<head>"
            "<title>Main Page</title>"
            "</head>"
            "<body><h1>Login Successfully!</h1></body>"
            "</html>"
        )
