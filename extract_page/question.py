# -*- coding: utf-8 -*-

import re

import redis
from furl import furl
from urlparse import urlparse ,parse_qs
from lxml.html import fromstring, tostring
from compress import decompress,base64decode

from config import rd
from log import logger
from task import send_task
from config import zhihu_url_key
from models import Question,Answer,User, Topic, TopicQuestion
from utils import DATE_REGEX,to_legal_datetime,question_url_key,num_re


comment_page_list = []


def extract_question(url,doc):
    """
    DESC:
        to extract zhihu'question field
    Args:
        url: url must contains page num  ,  #http://www.zhihu.com/question/20874376?sort=created&page=2
        doc: xpath's object

    Return:
        None
    """

    f = furl(url)
    page = f.args['page']
    question_id = f.pathstr.split('/')[-1]

    if page == "1":
        title = doc.xpath('.//*[@id="zh-question-title"]/h2/span/text()')[0].strip()
        content = doc.xpath('.//div[@class="zh-summary summary clearfix"]')[0]
        content_text = content.text_content().strip()
        content = tostring(content,encoding='utf-8')

        comment_num = answer_num = 0
        try:
            comment_num = doc.xpath('.//div[@id="zh-question-meta-wrap"]/div/a[@name="addcomment"]/text()')
            if len(comment_num_el):
                num_text = "".join(comment_num).strip()
                comment_num = num_re.search(num_text).group()[0]
        except:
            comment_num = 0

        answer_num_el = doc.xpath('.//h3[@id="zh-question-answer-num"]')
        if len(answer_num_el):
            answer_num_el =  answer_num_el[0]
            answer_num = answer_num_el.attrib['data-num']
        q,created = Question.get_or_create(qid = question_id)
        q.title = title.strip()
        q.content = content.strip()
        q.content_text = content_text.strip()
        q.comment_num = comment_num
        q.answer_num = answer_num
        q.save()

        topic_list = doc.xpath('.//a[@class="zm-item-tag"]')
        for topic_a  in topic_list:
            url = topic_a.attrib['href']
            name = topic_a.text.strip()
            t_id = url.split('/')[-1]
            try:
                t,created = Topic.get_or_create(name=name.strip(),tid = t_id)
                Tq,created = TopicQuestion.get_or_create(tid = t_id,qid = question_id)
            except:
                pass
        page_list = doc.xpath('.//div[@class="question-page-pager"]//span/text()')
        page_num_set = set()
        for one in page_list:
            try:
                page_num = int(one)
                page_num_set.add(page_num)
            except ValueError:
                continue

        if page_num_set:
            max_page = max(page_num_set)
            if max_page>100:
                max_page = 100# limit comment page to 50
            for one in range(2,max_page+1):
                f.args['page'] = one
                comment_page_list.append(f.url)
            if comment_page_list:
                for url in comment_page_list:
                    rd.sadd(zhihu_url_key,url)

    answer_list = doc.xpath('.//div[@id="zh-question-answer-wrap"]/div[contains(@class,"zm-item-answer")]')
    for one in answer_list:
        a_id = one.attrib['data-atoken']
        vote_num = one.xpath("./div/button/span[@class='count']/text()")
        if vote_num:
            vote_num = int(vote_num[0])
        else:
            vote_num = 0
        author_url = ''
        author = one.xpath('.//a[@class="author-link"]')
        if author: # false,anonymous user
            author_url = author[0].attrib['href']
        content = one.xpath(".//div[contains(@class,'zm-editable-content')]")[0]
        content_text = one.xpath(".//div[contains(@class,'zm-editable-content')]")[0]
        content_text = content_text.text_content()
        content = tostring(content,encoding='utf-8')

        comment_num = 0

        try:
            comment_num_el = one.xpath('.//div[@class="zm-meta-panel"]/a[@name="addcomment"]/text()')
            if len(comment_num_el):
                num_text = "".join(comment_num_el).strip()
                comment_num = num_re.search(num_text).group()
        except:
            pass

        date_element = one.xpath(".//div[@class='zm-meta-panel']/a[@itemprop='url']")[0]
        answer_url = date_element.attrib['href']
        date_text = date_element.text

        for regex in DATE_REGEX:
            date_result = regex.search(date_text)
            if date_result:
                break
        if date_result:
            date_edit = to_legal_datetime(date_result)
            date_re = re.search("\d*-\d*-\d*",str(date_edit))
            if date_re:
                date_edit = date_re.group()
        repetition_url = Answer.select().where(Answer.user_url == author_url)
        if repetition_url.count() == 0 :
            a,created = Answer.get_or_create(qid = question_id,aid=a_id)
            a.content = content.strip()
            a.edit_date = date_edit
            a.user_url = author_url or None
            a.vote = vote_num
            a.comment_num = comment_num
            a.content_text = content_text.strip()
            a.save()
            if author_url:
                rd.sadd(zhihu_url_key,author_url)
        else:
            logger.error("%s:url-repetition"%url)


def test():
    url = "https://www.zhihu.com/question/47076953?sort=created&page=1"
    user_agent = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
    r = requests.get(url,headers=user_agent,verify=False)
    doc = fromstring(r.text)
    extract_question(url,doc)


if __name__ == '__main__':
    test()

