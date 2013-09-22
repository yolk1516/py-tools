#!python
# encoding=utf-8

userid="mail@address"
passwd="********"
import sys, re, cgi, urllib, urllib2, cookielib, xml.dom.minidom, time
import json

def getToken(userid, passwd):
    html = urllib2.urlopen("http://www.nicovideo.jp/my/mylist").read()
    for line in html.splitlines():
        mo = re.match(r'^\s*NicoAPI\.token = "(?P<token>[\d\w-]+)";\s*',line)
        if mo:
            token = mo.group('token')
            break
    assert token
    return token

def mylist_create(token, name):
    cmdurl = "http://www.nicovideo.jp/api/mylistgroup/add"
    q = {}
    q['name'] = name.encode("utf8")
    q['description'] = ""
    q['public'] = 0
    q['default_sort'] = 0
    q['icon_id'] = 0
    q['token'] = token
    cmdurl += "?" + urllib.urlencode(q)
    j = json.load( urllib2.urlopen(cmdurl), encoding='utf8')
    return j['id']

def addvideo_tomylist(token, mid,smids):
    for smid in smids:
        cmdurl = "http://www.nicovideo.jp/api/mylist/add"
        q = {}
        q['group_id'] = mid
        q['item_type'] = 0
        q['item_id'] = smid
        q['description'] = u""
        q['token'] = token
        cmdurl += "?" + urllib.urlencode(q)
        # print smid
        # print cmdurl
        j = json.load( urllib2.urlopen(cmdurl), encoding='utf8')
        # print j
        time.sleep(0.5)

def mylist_list(token, mid):
    cmdurl = "http://www.nicovideo.jp/api/mylist/list"
    q = {}
    q['group_id'] = mid
    q['token'] = token
    cmdurl += "?" + urllib.urlencode(q)
    j = json.load( urllib2.urlopen(cmdurl), encoding='utf8')
    ret = []
        
    # 動画番号の抽出
    for e in j['mylistitem']:
        # print e['item_data']['video_id']
        # print e['item_data']['first_retrieve']
        ret.append(e['item_data']['first_retrieve']) 
    return ret

def delvideo_tomylist(token, mid,frs):
    id_list = ""
    for fr in frs:
        id_list += "&id_list[0][]=%s" % fr
    
    cmdurl = "http://www.nicovideo.jp/api/mylist/delete"
    q = {}
    q['group_id'] = mid
    q['token'] = token
    cmdurl += "?" + urllib.urlencode(q) + id_list
    # print cmdurl
    j = json.load( urllib2.urlopen(cmdurl), encoding='utf8')
    # print j
    time.sleep(0.5)


##ログイン
#opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
#urllib2.install_opener(opener)
#urllib2.urlopen("https://secure.nicovideo.jp/secure/login",
#                 urllib.urlencode( {"mail":userid, "password":passwd}) )
##トークン取得
#token = getToken(userid, passwd)

#vids = mylist_list(token,"31618721")
#delvideo_tomylist(token,"31618721",vids)

##マイリストの作成と動画の登録
#mid = mylist_create(token, u"テストリスト")
#addvideo_tomylist(token, mid, ["sm9","sm1097445", "sm1715919"  ] )

