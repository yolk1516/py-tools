#!python
# encoding=utf-8

import os
import sys
import re
import urllib
import urllib2
import cookielib
import httplib
import cgi
import time
import datetime
import YolkMovableType
import YolkSqliteForNico
import YolkIgnoreSetting
import YolkNicoMylist
from xml.etree import ElementTree
from optparse import OptionParser

# Constants for niconico
TAG_SEARCH_URL = "http://www.nicovideo.jp/tag/"
PAGE_STR = "?page="
RSS_STR = "&rss=atom"
GETTHUMBINFO_URL = "http://ext.nicovideo.jp/api/getthumbinfo/"
LOGIN_URL = "https://secure.nicovideo.jp/secure/login"

YOUBI_MYLIST_ID = ["31620747","31620757","31620760","31620762","31620777","31620785","31620800"]

### タグ検索結果XMLの固有設定
# 名前空間
XMLNS = "{http://www.w3.org/2005/Atom}"
# ID取得に使う正規表現
VIDEO_ID_RE = re.compile(r'/watch/([sn][mo]\d+)')

SEARCH_END_PAGE = 5

COOKIE_FILE = "nico-cookie.txt"

class LoginError(Exception):
    pass

# ログイン処理
def login(mail, password):
    for i in range(2):
        if mail is None: mail = raw_input("mail: ")
        if password is None: password = raw_input("pass: ")
        query = {"mail":mail, "password":password}
        query = urllib.urlencode(query)
        try:
            response = urllib2.urlopen(LOGIN_URL, query)
            if response.headers["x-niconico-authflag"] == "1":
                return True
            else:
                mail = password = None
        except urllib2.URLError:
            pass
    return False

# タグ検索結果XMLの取得
def get_xml_search(tag, page):
    try:
        seturl = TAG_SEARCH_URL + urllib.quote_plus(tag.encode('utf-8')) + PAGE_STR + page + RSS_STR
#        print "[SEARCH_URL] " + seturl
        f = ElementTree.fromstring(urllib2.urlopen(seturl).read())
        for e in f.findall('.//' + XMLNS +  'entry'):
#            print "[TITLE] " + e.find(XMLNS + 'title').text
#            print "[ID] " + e.find(XMLNS +'id').text
            search = VIDEO_ID_RE.search(e.find(XMLNS +'id').text)
            video_id = search.group(1)
#            print "[VIDEO_ID] " + video_id
            time.sleep(3)
            if not con.db_exists_video_id(video_id) :
                get_xml_video_info(video_id)
            
            if len(id_list) >= 10:
                return
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

# 動画の詳細情報XMLの取得
def get_xml_video_info(video_id):
    try:
        i = ElementTree.fromstring(urllib2.urlopen(GETTHUMBINFO_URL + video_id).read())
#        print video_id + "[GETTHUMBINFO_RESPONSE_STATUS] " + i.get('status')
        if i.get('status') == 'ok':

            # 値の取得
            upd_id = i.find('./thumb/video_id').text
            upd_title = i.find('./thumb/title').text
            upd_view = i.find('./thumb/view_counter').text
            upd_comment = i.find('./thumb/comment_num').text
            upd_mylist = i.find('./thumb/mylist_counter').text
            upd_tags = []
            
#            print u"%s[再生数] %s" % (upd_id, upd_view)
#            print u"%s[コメ数] %s" % (upd_id, upd_comment)
#            print u"%s[マイリス数] %s" % (upd_id, upd_mylist)

            # 無視判定
            if YolkIgnoreSetting.match_keyword(upd_title):
                return
            
            for e in i.findall("./thumb/tags[@domain='jp']/tag"):
#                print "%s[TAG] %s " % (upd_id, e.text)
                # 無視判定
                if YolkIgnoreSetting.match_tag(e.text):
                    return
                upd_tags.append(e.text)

            # DB更新処理
            con.db_update_id(upd_id, upd_title)
            con.db_update_info(upd_id, upd_title, upd_view, upd_comment, upd_mylist)
            for tag in upd_tags:
                con.db_update_tag(upd_id, tag)

            #ブログ掲載対象に追加
            id_list.append({"id": upd_id, "title": upd_title})
    except:
#        print "Unexpected error:", sys.exc_info()[0]
        raise

# Create the command line options parser and parse command line
usage = "usage: %prog [options] {TAG}"
parser = OptionParser(usage)
parser.add_option("-m", dest="mail",
                  help="specify the email address")
parser.add_option("-p", dest="password",
                  metavar="PASS",
                  help="specify the password")
parser.add_option("-c", dest="cookie_file",
                  metavar="FILE",
                  help="load cookies from FILE of the Mozilla/Netscape 'cookie.txt' format"),
parser.add_option("-n", dest="no_title",
                  action="store_true",
                  help="save the file under the name {ID}.flv (default {title}.flv)")

(options, args) = parser.parse_args()

# Check arguments
if not args:
    parser.print_help()
    sys.exit(1)

# メイン処理
tag = args[0]

# Configure urllib2 to use cookies
cj = cookielib.MozillaCookieJar()
try:
    cj.load(options.cookie_file or COOKIE_FILE)
except:
    pass
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

con = YolkSqliteForNico.YolkSqliteForNico()

id_list = []

try:

    # ===== ログイン不要な処理 =====
    # 動画検索
    for i in range(5):
        if len(id_list) < 10 and i + 1 < 5:
            get_xml_search(u'作業用BGM', str(i + 1))

    # 動画リストをブログに投稿
    if len(id_list) > 0:
        # ===== ログインが必要な処理 =====
        if login(options.mail, options.password):
            cj.save(COOKIE_FILE)
            get_xml_search(u'作業用BGM', "1")
        else:
            sys.exit("Error: unable to login")
       
        # マイリストIDの設定
        day = datetime.datetime.now()
        mylist_id = YOUBI_MYLIST_ID[day.weekday()]
        
        # トークン取得
        token = YolkNicoMylist.getToken(options.mail, options.password)
        
        # マイリストから動画削除
        vids = YolkNicoMylist.mylist_list(token, mylist_id)
        if len(vids) > 0:
            YolkNicoMylist.delvideo_tomylist(token, mylist_id , vids)
        
        # マイリストに動画登録
        smids = []
        # VIDEO_IDのみ抽出
        for id in id_list:
            smids.append(id['id'])
        YolkNicoMylist.addvideo_tomylist(token, mylist_id , smids)

        # ブログへ投稿
        YolkMovableType.blog_entry_post(id_list, mylist_id)
    con.commit()
#    con.rollback()
except:
#    print "Unexpected error:", sys.exc_info()[0]
    con.rollback()
    raise


