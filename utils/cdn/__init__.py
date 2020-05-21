import sys

from settings import Config

from .s3 import S3
from .b2 import B2


class Cdn:
    def load(self):
        if Config.cdn["b2"]["enabled"]:
            return B2()
        elif Config.cdn["s3"]["enabled"]:
            return S3()
        else:
            sys.exit("Must give s3 or b2.")
