# -*- coding: utf-8 -*-

import json

import requests
from lxml.html import fromstring, tostring

from utils import DATE_REGEX,to_legal_datetime
from models import Question,Answer,User,Topic,SpecialColumn


special_about = "http://zhuanlan.zhihu.com/api/columns/{special_name}"
special_fans_api = "http://zhuanlan.zhihu.com/api/columns/{special_name}/followers?limit={limit}&offset={offset}"


def get_special_fans(special_name):
    limit = 20
    get_page = True
    page = 1
    while get_page :
        offset = (page-1)*limit
        fans_url = special_fans_api.format(special_name = special_name,limit =limit,offset=offset)
        r = requests.get(fans_url)
        user_list = json.loads(r.text)
        for one in user_list:
            print one['profileUrl']
        if len(user_list)<20:
            page = 0
        else:
            page = page +1

if __name__ == '__main__':
    name = "jszxs"
    get_special_fans(name)
