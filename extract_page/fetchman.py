#coding:utf-8

import json
import time
import traceback

import redis
import requests

from config import rd, zhihu_url_key
from log import logger


def push_url(url):
    pass


def fetch_data(url):
    pass


if __name__ == '__main__':
    limiter = 3
    url_list = []
    while 1:
        try:
            url = rd.spop(zhihu_url_key)
            if not url:
                time.sleep(1)
                continue

            fetch_data(url)
        except Exception , e:
            logger.info(traceback.format_exc())

