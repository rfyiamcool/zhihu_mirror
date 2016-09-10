# -*- coding: utf-8 -*-

import re
import datetime

question_url_key = "question_url"

num_re = re.compile('\d+')

DATE_REGEX = (
    re.compile(u'(?P<year>\\d{4})-(?P<month>\\d{1,2})-(?P<day>\\d{1,2})', re.UNICODE),
    re.compile(u'(?P<text>今天|昨天)?\\s+?((?P<hours>\\d{1,2}):(?P<minutes>\\d{1,2}))?', re.UNICODE),
)


def to_legal_datetime(match):
    date_kwargs = {}
    text = ''
    for key, value in match.groupdict().items():
        if key == 'text':
            text = value
        else:
            if value:
                date_kwargs[key] = int(value)

    now = datetime.datetime.now()
    if text == u'今天' or text == None:
        result = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if len(date_kwargs):
            result += datetime.timedelta(**date_kwargs)
        return result

    elif text == u'昨天':
        result = now.replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=1)
        if len(date_kwargs):
            result += datetime.timedelta(**date_kwargs)
        return result
    try:
        result = datetime.datetime(**date_kwargs)
        if result > datetime.datetime.now():
            return None
    except ValueError:
        return None

    return result
