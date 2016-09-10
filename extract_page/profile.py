# -*- coding: utf-8 -*-
import sys

import re
import traceback

import requests
from lxml.html import fromstring, tostring

from config import mysql_addr,rd,migrate_id_set
from models import Question,Answer,User,Topic,SpecialColumn
from utils import DATE_REGEX,to_legal_datetime


def extract_profile(url,doc):
    """
    Args:
        url: url must contains page num, example url https://www.zhihu.com/people/rainman-73
        doc: xpath's object

    Return:
        None
    """
    account = url.split('/')[-1]
    name = bio = location = weibo = gender = business = employment = education = desc = bio = position = education_extra = pic = u""
    aggre = thank = follow_num = fans_num = ask_num = answer_num = post_num = collect_num = public_edit_num = follow_column_num = follow_topic_num = 0
    bio_doc = doc.xpath('.//div[@class="bio"]/text()')
    if bio_doc:
        bio = bio_doc[0]

    desc_doc = doc.xpath('.//div[@class="zm-profile-header-description editable-group "]//textarea') 
    if desc_doc:
        desc = desc_doc[0].text_content()

    pic = doc.xpath(".//div[@class='body clearfix']/img/@src")
    if pic:
        pic = pic[0]

    name_el = doc.xpath('.//div[@class="top"]/div[2]/span[@class="name"]/text()')
    if name_el:
        name = name_el[0]

    weibo_el = doc.xpath('.//a[@class="zm-profile-header-user-weibo"]')
    if weibo_el:
        weibo = weibo_el[0].attrib['href']

    location_el =doc.xpath('.//div[@data-name="location"]/span[@class="info-wrap"]/span[contains(@class,"location")]')
    if location_el:
        location = location_el[0].text_content().strip()

    business_el =doc.xpath('.//div[@data-name="location"]/span[@class="info-wrap"]/span[contains(@class,"business")]')
    if business_el:
        try:
            business  = business_el_el[0].text_content().strip()
        except:
            pass

    gender_el = doc.xpath('.//div[@data-name="location"]/span[@class="info-wrap"]/span[contains(@class,"gender")]/i')
    if gender_el:
        class_info  = gender_el[0].attrib['class']
        gender = 'f' if 'female' in class_info else 'm'

    employment_el = doc.xpath('.//div[@data-name="employment"]/span[@class="info-wrap"]/span[contains(@class,"employment")]')
    if employment_el:
        employment = employment_el[0].text_content().strip()

    position_el = doc.xpath('.//div[@data-name="employment"]/span[@class="info-wrap"]/span[contains(@class,"position")]')
    if position_el:
        position = position_el[0].text_content().strip()
        
    education_el = doc.xpath('.//div[@data-name="education"]/span[@class="info-wrap"]/span[contains(@class,"education")]')
    if education_el:
        education = education_el[0].text_content().strip()

    education_extra_el = doc.xpath('.//div[@data-name="education"]/span[@class="info-wrap"]/span[contains(@class,"education-extra")]')
    if education_extra_el:
        education_extra = education_extra_el[0].text_content().strip()
        
    aggre_el = doc.xpath('.//span[@class="zm-profile-header-user-agree"]/strong/text()')
    if aggre_el:
        aggre = aggre_el[0]

    thank_el = doc.xpath('.//span[@class="zm-profile-header-user-thanks"]/strong/text()')
    if thank_el:
        thank = thank_el[0]

    follow_fan = doc.xpath('.//div[contains(@class,"zm-profile-side-following")]/a[@class="item"]/strong/text()')
    if follow_fan:
        follow_num,fans_num = follow_fan

    misc_num = doc.xpath('.//div[contains(@class,"profile-navbar")]/a/span[@class="num"]/text()')
    if len(misc_num) == 5:
        ask_num, answer_num,post_num,collect_num,public_edit_num = misc_num

    fav_el = doc.xpath('.//div[@class="zm-profile-side-section-title"]/a/strong/text()')
    for one_text in fav_el:
        if one_text.endswith(u'话题'):
            follow_topic_num = one_text.split(" ")[0]
        if one_text.endswith(u'专栏'):
            follow_topic_num = one_text.split(" ")[0]
            
    user = User.select().where(User.account == account)
    if not user:
        user = User.create(account=account,name = name)
    else:
        user = user[0]
    user.weibo = weibo
    user.desc = desc
    user.bio = bio
    user.pic = pic
    user.gender = gender
    user.business = business
    user.location = location
    user.employment = employment
    user.position = position
    user.education = education
    user.education_extra = education_extra
    user.follow_num = follow_num
    user.fans_num = fans_num
    user.aggre= aggre
    user.thank = thank
    user.ask_num = ask_num
    user.answer_num = answer_num
    user.post_num = post_num
    user.collect_num = collect_num
    user.public_edit_num = public_edit_num
    xx = Answer.select().where(Answer.user_url == '/people/'+account)
    if xx.count() == 1:
        yy = xx[0].id
        rd.sadd(migrate_id_set,yy)
    user.save()

    topic_url_list = doc.xpath('.//div[@id="zh-profile-following-topic"]/a')
    topic_name_list = doc.xpath('.//div[@id="zh-profile-following-topic"]/a/img')
    tid_list = [];tname_list = []
    for topic_a  in topic_url_list:
        url = topic_a.attrib['href']
        t_id = url.split('/')[-1]
        tid_list.append(t_id)
    for name_img in topic_name_list:
        t_name = name_img.attrib['alt']
        tname_list.append(t_name)

    for i,n in zip(tid_list,tname_list):
        try:
            t,created = Topic.get_or_create(name=n.strip(),tid = i)
        except Exception:
            pass

    column_url_list = doc.xpath('.//div[@class="zm-profile-side-columns"]/a')
    column_name_list = doc.xpath('.//div[@class="zm-profile-side-columns"]/a/img')
    curl_list =[];cname_list=[]
    for column_url in column_url_list:
        url = column_url.attrib['href']
        curl_list.append(url)

    for column_name in column_name_list:
        name = column_name.attrib['alt']
        cname_list.append(name)

    for curl,cname in zip(curl_list,cname_list):
        sc, created = SpecialColumn.get_or_create(name = cname ,url= curl)


def test():
    import requests
    from lxml.html import fromstring
    url = "http://www.zhihu.com/people/rainman-73"
    user_agent = {'User-agent': 'Mozilla/5.1'}
    r = requests.get(url,headers=user_agent)
    doc = fromstring(r.text.decode('utf8'))
    extract_profile(url,doc)


if __name__ == '__main__':
    test()

