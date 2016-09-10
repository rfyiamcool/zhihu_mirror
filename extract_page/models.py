# -*- coding: utf-8 -*-
from peewee import *
from playhouse.shortcuts import RetryOperationalError

from config import mysql_addr


""""
if not use MyRetryDB...
db = MySQLDatabase('zhihu_master',host='',user='',passwd='',threadlocals=True,charset='utf8mb4')
"""


class MyRetryDB(RetryOperationalError, MySQLDatabase):
    pass

db = MyRetryDB(host=mysql_addr['host'],
                                  port=mysql_addr['port'],
                                  user=mysql_addr['user'],
                                  passwd=mysql_addr['passwd'],
                                  database=mysql_addr['db'],
                                  charset='utf8mb4',
                                  threadlocals=True)


class User(Model):
    account = CharField(index=True,unique=True,max_length=100)                       #用户id
    pic = CharField(null=True)                                                       #头像
    name = CharField()                                                               #用户名
    weibo = CharField(null=True)                                                     #weibo 地址
    gender = CharField(null=True)                                                    #性别
    business = CharField(null=True)                                                  #所在行业
    bio = CharField(null=True)                                                       #句话介绍自己
    desc = CharField(null=True)                                                      #句话描述
    location = CharField(null=True)                                                  #居住地
    employment = CharField(null=True)                                                #职业
    position = CharField(null=True)                                                  #职位
    education = CharField(null=True)                                                 #学校
    education_extra = CharField(null=True)                                           #专业
    fans_num = IntegerField(null = True)                                             #粉丝数
    follow_num = IntegerField(null=True)                                             #关注数
    aggre = IntegerField(null = True)                                                #获得赞同
    thank = IntegerField(null = True)                                                #获得感谢
    ask_num = IntegerField(null = True,default=0)                                    #提问数
    answer_num = IntegerField(null = True,default=0)                                 #回答数
    post_num = IntegerField(null = True,default=0)                                   #文章数
    collect_num = IntegerField(null = True,default=0)                                #收藏数
    public_edit_num = IntegerField(null = True,default=0)                            #公共编辑数
    follow_topic_num = IntegerField(null = True,default=0)                           #关注话题数
    follow_column_num = IntegerField(null = True,default=0)                          #关注专栏数

    class Meta:
        database = db

class Topic(Model):
    tid = IntegerField(unique = True)                   #话题id,from zhihu
    name = CharField()                                  #话题的名字
    class Meta:
        database = db

class Question(Model):
    qid = IntegerField(unique=True)                     #from zhihu
    title = CharField(null=True)                        #问题标题
    content = TextField(null=True)                      #问题正文
    content_text = TextField(null=True)                 #问题正文    
    comment_num = IntegerField(null = True,default=0)   #问题评论数
    answer_num = IntegerField(null = True,default=0)    #问题回答数

    class Meta:
        database = db


class Answer(Model):
    qid = IntegerField()                                #问题idfrom知乎
    aid = IntegerField(unique=True)                     #答案idfrom zhihu
    user_url = CharField(null = True)                   #回答者
    content = TextField(null=True)                      #内容源码
    content_text = TextField(null=True)                 #内容文字
    vote = IntegerField(null=True,default=0)            #点赞数
    edit_date = DateField(null=True)                    #修改时间
    comment_num = IntegerField(null=True,default=0)     #评论数

    class Meta:
        database = db


class SpecialColumn(Model):
    user_name  = CharField(null=True)
    name = CharField()
    url = CharField()
    fans_num = IntegerField(null=True)
    desc = TextField(null=True)
    avatar = CharField(null = True)

    class Meta:
        database = db


class TopicQuestion(Model):
    """
    问题和话题关联关系
    """
    qid = IntegerField()
    tid = IntegerField()

    class Meta:
        database = db


if __name__ == '__main__':
    db.connect()
    for one in [TopicQuestion,Question,Topic,Answer,User,SpecialColumn]:
    #    one.drop_table(fail_silently=True)
        one.create_table()
