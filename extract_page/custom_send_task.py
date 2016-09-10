#coding:utf-8

import time

from task import send_task


if __name__ == '__main__':
    while 1:
        url_format = "http://www.zhihu.com/topic/19776749/questions?page={0}"#约20w

        max = 200000
        url_list = []
        for one in xrange(1, max):
            print one
            url = url_format.format(one)
            url_list.append(url)
            if len(url_list) > 5:
                send_task(url_list)
                time.sleep(10)
                url_list = []
        time.sleep(60 * 60 * 1)

    """
        cost time counter:
            (200000*0.4)/60/6022.22222222222222
    """
