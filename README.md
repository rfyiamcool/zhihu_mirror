#抓知乎的那些事

`其实这个呼声在我刚来的时候就有了，终于有开动的样子...
其实不是说不能抓，产品模型的不确定对开发带来的痛苦是非常严重的。这就好比数据结构，一个错误的是数据结构对程序开发的造成困难几乎是不可修复的。`

####知乎网站分析

对于知乎这样一个ugc（User Generated Content）网站而言，用户是核心，所有的内容都是用户产生的。

1.  问题，用户发表问题

2.  回答，用户回答问题

3.  评论，对于答案还有评论(不抓)

4.  投票，用户对支持的答案投票，就是点赞吧

5.  专栏，用户还可以写专栏

6.  收藏，收藏(colletion)，用户创建，类似豆瓣书单之类，

7.  话题，就是给问题打得标签，问题一般都会从属于话题，就是给问题打得标签


以上大部分都是非登录可见的，

==================================

最开始的地方

topic列表

专栏api

以这个 [http://zhuanlan.zhihu.com/biochem](看的懂的生物学)为例：

* http://zhuanlan.zhihu.com/api/columns/biochem 获取该专栏的详细信息
* http://zhuanlan.zhihu.com/api/columns/biochem/posts 获取所有发布得文章信息

* http://zhuanlan.zhihu.com/api/columns/biochem/followers 获取专栏的粉丝
* http://zhuanlan.zhihu.com/api/columns/biochem/followers?limit=20&offset=20 分页粉丝


####频率限制

知乎在2016-5月份之后开始做了单ip的限制频率.


####目前的方案

知乎的[跟话题](https://www.zhihu.com/topic/19776749/questions),我们认为通过这个页面可以找到知乎所有的问题，假装是吧。

由问题页可以得到user，通过user可以获取专栏，通过专栏的粉丝接口可以获取更多user，如此反复，无穷匮也


##下面是抓取知乎全站的方法

####抽象出来一共是三个入口.  
1.  把任务扔到大爬虫里面.  `extract_page/task.py`
2.  从大爬虫的结果集里面取任务,并且扔到redis队列里 `extract_page/spider_sample.py`
3.  从redis取结果，解析 `extrac_page/main.py`

#####生成任务的思路:

A.  根据经验根话题生成5w个page页面.

B. 暂时, 用户的信息抓取, 需要手动来生成url任务。  File: `get_user_url.py`  ,它把库中的question的user_url字段提取出来，拼装url. [https://www.zhihu.com/people/magicying](https://www.zhihu.com/people/magicying)。



#####抓取解析的思路:

A.  首先找到他的根话题的页面，[https://www.zhihu.com/topic/19776749/newest](https://www.zhihu.com/topic/19776749/newest) , 知乎的根话题页是含有所有的问题页的。

B.  调用`topic.py` 抽取question_link | href 属性，组装url再塞入大爬虫里。 url加了时间排序的参数后判断是否含有分页特征。  

C.  具体的问答页面如果有答案的`分页`，那么我们是可以拿到最小，最大分页数。 (有些热门问答，答案贼多)，样例: [https://www.zhihu.com/question/35233031?sort=created](https://www.zhihu.com/question/35233031?sort=created)。 那么，xpath分析页面后，可以把具体的问答页拆分成一个个含有分页的url，再次推送给大爬虫。 url样例: [https://www.zhihu.com/question/35233031?sort=created&page=2](https://www.zhihu.com/question/35233031?sort=created&page=2) 


    注意:  到此为止，问题，答案，topic信息都已经抓取.


#####注:
1. 暂时没做更新的机制.
