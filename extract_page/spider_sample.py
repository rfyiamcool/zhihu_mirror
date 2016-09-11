# -*- coding: utf-8 -*-
import time

import json
import requests
import redis

from config import rd as r
from config import user
from config import  base_url
from config import  token
from config import zhihu_task_key
from log import get_logger

logger = get_logger("/home/operation/zhihu/log/transfer.log",'transfer')
logger_err = get_logger("/home/operation/zhihu/log/transfer.err",'transfer')

"""

get the spider result by given api ,and store into redis

http://code.admaster.co/social-base/quantum_docs/blob/master/SuperSpider/UserManual.md

"""

def get_task():
    get_dict = {
        "user":user,
        "token":token,
        "size":100
    }
    res = requests.get(base_url+"/getStreamResults",params = get_dict)
    if res.status_code == 200:
        if res.headers['Result-Queue-Length'] == '0':
            time.sleep(0.5)
        source_list = json.loads(res.text)
        for one in source_list:
            r.rpush(zhihu_task_key,json.dumps(one))
    else:
        logger.error(r.text)


def receive_task():
    while 1:
        get_task()


if __name__ == "__main__":
    receive_task()
