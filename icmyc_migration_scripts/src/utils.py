import os
import re
import datetime


def getenv(key):
    return os.getenv(key)

def now():
    return datetime.datetime.now()

def validate_mobile_number(mobile_number):
    return re.match(r'[6789]\d{9}$', mobile_number)