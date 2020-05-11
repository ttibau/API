import sys

from settings import Config

from utils.cdn.s3 import S3
from utils.cdn.b2 import B2


class Cdn:
    def __init__(self, obj):
        """ Wrapper for aiobotocore & aiob2. """

        self.obj = obj

    def load(self):
        if Config.cdn["b2"]["enabled"]:
            return B2(obj=self.obj)
        elif Config.cdn["s3"]["enabled"]:
            return S3()
        else:
            sys.exit("Must give s3 or b2.")
