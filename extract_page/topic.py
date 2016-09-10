# -*- coding: utf-8 -*-

import requests
from lxml.html import fromstring, tostring

from models import Topic
from log import logger
from task import send_task
from config import zhihu_url_key,rd
from question import comment_page_list


def extract_topic(url,doc):
    """
    DESC:
        extrace zhihu topic (话题)
    ARGV:
        url:
            topic url
        doc:
            xpath object

    RETURN:
        None
    """
    a_el = doc.xpath('.//a[@class="question_link"]')
    url_list = []
    for one in a_el:
        url = one.attrib['href']
        url = "http://www.zhihu.com"+url+"?sort=created&page=1"
        url_list.append(url)
    for url in url_list:
        rd.sadd(zhihu_url_key, url)


if __name__ == "__main__":
    url = "http://www.zhihu.com/topic/19551627/questions?page=1"
    req = requests.get(url)
    doc = fromstring(req.content)
    extract_topic(url,doc)
