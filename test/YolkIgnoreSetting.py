#!python
# encoding=utf-8

import re

IGNORE_TAGS = [u"パチスロ",u"R-18",u"例のアレ", u"歌ってみた", u"朗読", u"レスリングシリーズ"]

IGNORE_KEYWORDS = [u"ボイス集", u"してみた"]


def match_tag(tag):
    for s in IGNORE_TAGS:
        if s == tag:
#            print "[IGNORE-TAG] %s" % s
            return True
    return False

def match_keyword(title):
    for s in IGNORE_KEYWORDS:
        if re.search(s, title) != None:
#            print "[IGNORE-KEYWORD] %s" % s
            return True
    return False

