# -*-encoding:utf-8-*-


class HttpIORoutinePool(object):
    def __init__(self):
        self.pool = {}

    def add(self, file_no, coroutine):
        self.pool[file_no] = coroutine

    def get(self, file_no):
        return self.pool.get(file_no, None)

    def remove(self, file_no):
        if file_no in self.pool:
            del self.pool[file_no]
