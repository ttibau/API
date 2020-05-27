import sys

from settings import CONFIG

from .s3 import S3
from .b2 import B2


class Cdn:
    def load(self):
        if CONFIG.cdn["b2"]["enabled"]:
            return B2()
        elif CONFIG.cdn["s3"]["enabled"]:
            return S3()
        else:
            sys.exit("Must give s3 or b2.")
