# -*-encoding:utf-8-*-


def get_http_content_type(http_content):
    if http_content and ";" in http_content:
        return http_content.split(";")[0]
    else:
        return http_content
