# -*-encoding:utf-8-*-


class HttpIORoutinePool(object):
    """

    This class contains four methods.

    def __init__(self): initialize

    def add(self, file_no, coroutine): add co-routine

    def get(self, file_no): get co-routine

    def remove(self, file_no): remove co-routine

    """
    def __init__(self):
        self.pool = {}

    def add(self, file_no, coroutine):
        """add co-routine to pool

        :param file_no: number of file description
        :param coroutine: co-routine
        :return: None

        """
        self.pool[file_no] = coroutine

    def get(self, file_no):
        """ get co-routine from pool

        :param file_no: number of file description
        :return: co-routine

        """
        return self.pool.get(file_no, None)

    def remove(self, file_no):
        """remove co-routine from pool

        :param file_no: number of file description
        :return: None

        """
        if file_no in self.pool:
            del self.pool[file_no]
