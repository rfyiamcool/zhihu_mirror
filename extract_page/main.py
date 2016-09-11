# -*- coding: utf-8 -*-
import sys
#reload(sys)
#sys.setdefaultencoding("utf-8")
import os
import re
import time
import json
import traceback

import requests
from lxml.html import fromstring, tostring

from compress import decompress,base64decode
from question import  extract_question
from profile import extract_profile
from topic import extract_topic
from log import logger
from config import rd
from config import zhihu_task_key


"""
    zhihu url regex
"""
profile_re = re.compile('www\.zhihu\.com/people\/(?!.*\/).*$')
question_re = re.compile('www\.zhihu\.com/question/\d+\?sort=created&page=\d+$')
topic_re = re.compile('www\.zhihu\.com/topic/\d+/questions\?page=\d+$')


def main():
    while 1:
        task = rd.lpop(zhihu_task_key)
        if not task:
            time.sleep(3)
            continue
        try:
            task_info = json.loads(task)
            task_url = task_info['url']
            logger.info("handle url %s",task_url)
            if task_info['status_code'] != 200:
                logger.info("spider error http_code : %s"%task_info['status_code'])
                continue
            task_content = decompress(base64decode(task_info['content']))
            doc = fromstring(task_content.decode('utf-8', errors='ignore'))
            if topic_re.search(task_url):
                extract_topic(task_url,doc)
            elif question_re.search(task_url):
                extract_question(task_url,doc)
            elif profile_re.search(task_url):
                extract_profile(task_url,doc)
            else:
                logger.info(" url %s did not match any schema",task_url)
        except Exception , e:
            print traceback.format_exc()


if __name__ == '__main__':
    main()
