# -*-encoding:utf-8-*-


class HttpIORoutinePool(object):
    def __init__(self):
        self.pool = {}

    def add(self, file_no, coroutine):
        self.pool[file_no] = coroutine

    def get(self, file_no):
        return self.pool[file_no]

    def remove(self, file_no):
        del self.pool[file_no]
