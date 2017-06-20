# -*-encoding:utf-8-*-

from base import BaseRestHandler, Status


class LoginRestHandler(BaseRestHandler):
    def process(self):
        user_name = self.get_parameter("user_name")
        password = self.get_parameter("password")
        if not self.redis_manager.get_user(username=user_name):
            return self.result(Status.USER_NOT_EXIST)
        if password != self.redis_manager.get_user(username=user_name):
            return self.result(Status.PSW_ERR)
        self.set_security_cookie("user_id", "1")
        return self.result(Status.SUCCESS, url="/main")


class RegisterRestHandler(BaseRestHandler):
    def process(self):
        user_name = self.get_parameter("user_name")
        password = self.get_parameter("password")
        if self.redis_manager.get_user(username=user_name):
            return self.result(Status.USER_EXIST)
        self.redis_manager.set_user(username=user_name, password=password)
        return self.result(Status.SUCCESS, url="/login")
