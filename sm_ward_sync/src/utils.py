import os
import re
import datetime


def getenv(key):
    return os.getenv(key)

def now():
    return datetime.datetime.now()