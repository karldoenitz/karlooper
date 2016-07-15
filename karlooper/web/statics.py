# -*-coding:utf-8-*-
"""

statics
~~~~~~~

introduction
a simple static http handler

Warning: this model just support debug model, we do not recommend developer use this models,
we recommend developer to use nginx as a static server.


"""

import os
import hashlib
from karlooper.web.request import Request
from karlooper.config import get_cli_data
from karlooper.config.config import content_type, HttpStatus, HttpStatusMsg


class StaticHandler(Request):
    """

    Two methods:

    def get(self): http get method

    def get_file_etag(self, file_path): get file's etag

    """
    def get(self):
        """

        :return: http response data, status, status message

        """
        global_config_data = get_cli_data()
        static_root = global_config_data.get("static", ".")
        request_expire_days = self.get_header("expires")
        now_time = self.get_now_time()
        if request_expire_days and now_time <= request_expire_days:
            return "", HttpStatus.RESOURCE_NOT_MODIFIED, HttpStatusMsg.RESOURCE_NOT_MODIFIED
        request_etag = self.get_header("if-none-match")
        file_path = self.get_request_url()
        file_absolute_path = static_root+file_path
        if not os.path.exists(file_absolute_path):
            return "404", HttpStatus.NOT_FOUND, HttpStatusMsg.NOT_FOUND
        file_etag, file_data = self.get_file_etag(file_absolute_path)
        if request_etag and request_etag == file_etag:
            return "", HttpStatus.RESOURCE_NOT_MODIFIED, HttpStatusMsg.RESOURCE_NOT_MODIFIED
        expires = self.generate_expire_date(expires_days=7)
        file_extension = file_path.split(".")[-1]
        self.set_header({
            "ETag": file_etag,
            "Expires": expires,
            "Content-Type": content_type.get(file_extension)
        })
        return file_data, HttpStatus.SUCCESS, HttpStatusMsg.SUCCESS

    def get_file_etag(self, file_path):
        """get file's etag

        :param file_path: static file's path
        :return: file's etag

        """
        f = open(file_path)
        file_data = f.read()
        f.close()
        etag = hashlib.md5(file_data).hexdigest()
        self.logger.info("%s's etag is %s" % (file_path, etag))
        return etag, file_data
