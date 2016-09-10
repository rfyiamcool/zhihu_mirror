import zlib
import base64
import hashlib
import time

def compress(source):
    return zlib.compress(source, 6) # use default level

def decompress(data):
    if not data.strip():
        return ""
    return zlib.decompress(data)  # default buffer size 16K

def base64encode(value):
    return base64.b64encode(value)

def base64decode(value):
    return base64.b64decode(value)
