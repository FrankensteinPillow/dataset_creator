class DataNotFound(Exception):
    def __init__(self, msg):
        self.msg = msg
