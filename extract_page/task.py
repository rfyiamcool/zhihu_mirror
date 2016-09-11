# -*- coding: utf-8 -*-

import os
import json

import requests

from log import logger
from config import user, token, base_url


task_item_dict = {
    "user": user,
    "interval": 86400,
    "timeout": 30,
    "priority": 1,
    "index": 0,
    "depth": 0,
    "force": 1,
    "extra":""
}


##url_list 上限100
def send_task_list(url_list, kwargs=None):
    task_list = []
    for one in url_list:
        task_item_dict['url']=one
        if kwargs:
            for k,v in kwargs.items():
                task_item_dict[k] = v
        task_list.append(task_item_dict.copy())
    task_list_dict = {
        "user":user,
        "token":token,
        "tasks":task_list
    }
    res = requests.post(base_url+"/putTaskBatch",data = json.dumps(task_list_dict))
    return res

def send_task(list_url, **kwargs):
    urls = []
    err = 201
    for u in list_url:
        urls.append(u)
        if len(urls) >= 50:
            res = send_task_list(urls, kwargs)
            if res.status_code != 201:
                err = res.status_code
                logger.error("%s ,task send error.Info:%s scode:%s" % (kwargs,res.reason, res.status_code))
            urls = []

    if len(urls)>0:
        res = send_task_list(urls, kwargs)

        if res.status_code != 201:
            err = res.status_code
            logger.error("%s ,task send error.Info:%s scode:%s" % (kwargs,res.reason, res.status_code))

    return err


if __name__ == '__main__':
    url_list = []
    # url_format = "http://www.zhihu.com/topic/19551627/questions?page={0}"
    # for one in range(1,100):
    #     url = url_format.format(one)
    #     url_list.append(url)
    with open("user_list.txt") as f :
        for one in f:
            url_list.append(one.strip())
    send_task(url_list)
