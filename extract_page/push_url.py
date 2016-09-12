#coding:utf-8

import json
import time
import traceback

import redis
import requests

from config import rd, zhihu_url_key
from task import send_task
from log import logger


def push_url(url):
    status_code = send_task(url)
    if status_code != 201:
        logger.error("url:%s ,task not send. errcode:%s." % (url, status_code))
    logger.info("push url %s" % (url))


if __name__ == '__main__':
    limiter = 3
    url_list = []
    while 1:
        try:
            url = rd.spop(zhihu_url_key)
            if not url:
                time.sleep(1)
                continue

            url_list.append(url)
            if len(url_list) > limiter:
                push_url(url_list)
                time.sleep(0.05)
                url_list = []
        except Exception , e:
            logger.info(traceback.format_exc())

