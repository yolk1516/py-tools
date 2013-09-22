#!python
# encoding=utf-8

import xmlrpclib
import datetime

# ===== ===== ===== ===== ===== ===== ===== ===== 
# MovableTypeの操作モジュール
# ===== ===== ===== ===== ===== ===== ===== ===== 

# ニコニコ動画の投稿
def blog_entry_post(id_list, mylist_id):
    rpc_url = 'http://192.168.1.89/wp/xmlrpc.php'
    blog_id = '1'

    parts   = u"""
<script type="text/javascript" src="http://ext.nicovideo.jp/thumb_watch/%s?w=490&h=307"></script>
<noscript><a href="http://www.nicovideo.jp/watch/%s">【ニコニコ動画】%s</a></noscript>
<br><br>
"""

    msg = ""
    for ent in id_list:
        msg = msg + parts % (ent["id"], ent["id"], ent["title"]) + "\n"
    
    msg += u"""<A HREF="http://www.nicovideo.jp/mylist/%s">本日の動画リスト(ニコニコ動画のマイリスト)</A>\n""" % mylist_id

    user    = "admin"
    passwd  = "1234asdf"
    post    = {'title'        : "作業用BGM新着 [%s]" % datetime.datetime.now().strftime(u'%Y/%m/%d'),
               'description'  : msg,
               'mt_keywords'  : '作業用BGM',
               'mt_text_more' : ''}
    publish = True
    api = xmlrpclib.ServerProxy(rpc_url)
    api.metaWeblog.newPost(blog_id, user, passwd, post, publish)
    


