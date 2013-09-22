#!/usr/bin/python
# -*- coding: utf-8 -*-
# なんでサクラエディタで開こうとするときにutf-8にならんのo(｀ω´*)oﾌﾟﾝｽｶﾌﾟﾝｽｶ!!
import cgi
import cgitb; cgitb.enable()
import os
import sys
import Cookie
import datetime
#import codecs
sys.path.append('./lib')
import GatheringChatHtmlLib
import GatheringChatEntity
import GatheringChatSqliteLib
import BotWasuiLib

# --- ENCODE ---
#sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

# +++ TEST CODE +++
debug = ""
debug += "[os.environ['REQUEST_METHOD']]" + os.environ['REQUEST_METHOD'] + "\n"

# --- SETTING ---
DB_PATH = 'log/gatheringchat.db'
AUTHOR = "WASHI"
SCRIPT_SIGNATURE = "-Gathering chat Ver,3.00- Script written by " + AUTHOR + "."
TITLE = "チャット"
CHARSET = "UTF-8"
SPAM_CHECK_WORD = "和室"

# --- Get Arguments ---
form = cgi.FieldStorage()

# --- DB CONNECT ---
con = GatheringChatSqliteLib.GatheringChatSqliteLib(DB_PATH)

# --- DB READ ROOMS ---
rooms = con.db_select_room_all()

# --- DB READ COLORS ---
colors = con.db_select_color()

# --- INPUT CHECK ---
myform = GatheringChatHtmlLib.form_init(form, rooms, colors)

try:
    # --- DB ENTRY UPDATE ---
    entry = GatheringChatEntity.ChatEntry()
    entry.remote_addr = myform["remote_addr"]
    entry.entry_name = myform["entry"]
    entry.room_id = myform["chat"]
    con.db_update_entry(entry)
    con.db_clear_entry()

    # --- DB READ ENTRYS ---
    entries = con.db_select_entry(myform["chat"])
    all_entries = con.db_select_entry_all()

    # --- DB LOG UPDATE ---
    if len(myform["field"]) > 0 and len(myform["name"]) and myform["spamchk"] == SPAM_CHECK_WORD:
        log = GatheringChatEntity.ChatLog()
        log.room_id = myform["chat"]
        log.entry_name = myform["name"]
        for color in colors:
            if color.color_id == myform["color"]:
                log.color_value = color.color_value
                break
        log.remote_addr = myform["remote_addr"]
        log.comment = myform["field"]
        log.bot_reply = BotWasuiLib.send_message_to_bot(myform["name"], myform["field"], myform["chat"], entries)
        con.db_insert_log(log)

    con.commit()
except:
    con.rollback()
    raise

# --- DB READ MY ROOMS ---
myroom = con.db_select_room(myform["chat"])

# --- READ LOGS ---
logs = con.db_select_log(myform["chat"], myform["limit"], myform["offset"])

# --- READ COOKIE ---
sc = Cookie.SimpleCookie(os.environ.get('HTTP_COOKIE', ''))
if len(myform["name"]) == 0 and 'entry_name' in sc:
    myform["name"] = sc.get('entry_name').value
    myform["color"] = sc.get('color_id').value
    myform["spamchk"] = sc.get('spam_chk').value

# --- SET COOKIE ---
if os.environ['REQUEST_METHOD'] == "POST":
    sc["entry_name"] = myform["name"]
    sc["color_id"] = myform["color"]
    sc["spam_chk"] = myform["spamchk"]
    # POSTのときのみクッキーセット
    if len(form.getfirst("name","")) == 0:
        # 名前を空欄にしてきたらクッキーを削除する
        expires = datetime.datetime.now()+datetime.timedelta(days=-1)
        #sc["entry_name"]["path"] = "/"
        sc["entry_name"]["expires"] = expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
        #sc["color_id"]["path"] = "/"
        sc["color_id"]["expires"] = expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
        #sc["spam_chk"]["path"] = "/"
        sc["spam_chk"]["expires"] = expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
        # +++ TEST CODE +++
        debug += "[COOKIE削除に入ったよ]\n"
    else:
        # 有効期限は7日間とする
        expires = datetime.datetime.now()+datetime.timedelta(days=7)
        sc["entry_name"]["expires"] = expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
        sc["color_id"]["expires"] = expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
        sc["spam_chk"]["expires"] = expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
        # +++ TEST CODE +++
        debug += "[COOKIEを設定しましたよ]\n"

if myform["mode"] == "2":
	# フレームモード
    # --- HTML HEADER ---
    GatheringChatHtmlLib.html_header(TITLE, AUTHOR, CHARSET, myform, sc)
    GatheringChatHtmlLib.html_frame(myform)
    
elif myform["mode"] == "3":
	# フレームモードのフォーム側
    # --- HTML HEADER ---
    GatheringChatHtmlLib.html_header(TITLE, AUTHOR, CHARSET, myform, sc)
    GatheringChatHtmlLib.html_tag_body(myroom)
    
    # --- HTML FORM ---
    GatheringChatHtmlLib.html_form(myform, colors, rooms, SPAM_CHECK_WORD)
    
    # --- HTML FOOTER ---
    GatheringChatHtmlLib.html_footer(SCRIPT_SIGNATURE)
    
elif myform["mode"] == "4":
	# フレームモードのログ側
    # --- HTML HEADER ---
    GatheringChatHtmlLib.html_header(TITLE, AUTHOR, CHARSET, myform, sc)
    GatheringChatHtmlLib.html_tag_body(myroom)

    # --- HTML ENTRIES ---
    GatheringChatHtmlLib.html_entries(entries, all_entries)

    # --- HTML LOGS ---
    GatheringChatHtmlLib.html_log(logs)

    # --- HTML FOOTER ---
    GatheringChatHtmlLib.html_footer(SCRIPT_SIGNATURE)

else:
	# 通常モード
    # --- HTML HEADER ---
    GatheringChatHtmlLib.html_header(TITLE, AUTHOR, CHARSET, myform, sc)
    GatheringChatHtmlLib.html_tag_body(myroom)
    
    
    # --- HTML FORM ---
    GatheringChatHtmlLib.html_form(myform, colors, rooms, SPAM_CHECK_WORD)

    # --- HTML ENTRIES ---
    GatheringChatHtmlLib.html_entries(entries, all_entries)

    # --- HTML LOGS ---
    GatheringChatHtmlLib.html_log(logs)

    # --- HTML FOOTER ---
    GatheringChatHtmlLib.html_footer(SCRIPT_SIGNATURE)



def test_code():
    # +++ TEST CODE +++
    print "<pre>"
    for key in form.keys():
        print '[FIELD:%s] %s' % (key, form.getfirst(key, ""))
    print debug
    print "</pre>"
