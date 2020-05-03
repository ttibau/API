import sys

from settings import Config as config

from utils.cdn_clients.s3 import S3
from utils.cdn_clients.b2 import B2


class Cdn:
    def __init__(self, obj):
        """ Wrapper for aiobotocore & aiob2. """

        if config.cdn["b2"]["enabled"]:
            obj.cdn = B2(obj=obj)
        elif config.cdn["s3"]["enabled"]:
            obj.cdn = S3()
        else:
            sys.exit("Must give s3 or b2.")
