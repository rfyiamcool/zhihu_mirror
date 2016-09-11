# -*- coding: utf-8 -*-

import redis
import time

from task import send_task
from models import Answer


site = "http://www.zhihu.com"


def get_user_url():
    global offset
    url_list = []
    for one in Answer.select(Answer.id,Answer.user_url).where(~(Answer.user_url >> None),Answer.id > offset).limit(500):
        url = site + one.user_url
        url_list.append(url)
        if one.id == offset:
            raise("ok")
        if one.id > offset:
            offset = one.id
    return url_list

def transfer_url_redis():
    with open("user_url_list.txt") as f:
        for line in f:
            r.rpush(user_url_key,line.strip())


if __name__ == '__main__':
    offset = 0
    tmp = []
    while 1:
        url_list = get_user_url()
        for url in url_list:
            tmp.append(url)
            if len(tmp) > 50:
                send_task(tmp)
                tmp = []
                time.sleep(1.5)
        time.sleep(1)

