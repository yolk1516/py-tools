#!/usr/bin/python
# -*- coding: utf-8 -*-
# なんでサクラエディタで開こうとするときにutf-8にならんのo(｀ω´*)oﾌﾟﾝｽｶﾌﾟﾝｽｶ!!


# text/xml
# POST
# sjis

import sys
import cgi
import codecs

#sys.stdin  = codecs.getreader('shift_jis')(sys.stdin)
#sys.stdout = codecs.getwriter('shift_jis')(sys.stdout)

# とりあえず200のステータスコードを返す
print "Content-Type: text/xml"
print
print "Hello!"
print "Hello!"
#for line in iter(sys.stdin.readline, ""):
#	print line,
#sys.stdin.close()


