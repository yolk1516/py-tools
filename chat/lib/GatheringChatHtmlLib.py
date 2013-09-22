#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

# --- SETTING ---
UNNAMED_ENTRY_NAME = "未登録"

def form_init(_form, _rooms, _colors):
    dic = {}
    
    # --- 入力チェック ---

    # --- 部屋 ---
    _chat = _form.getfirst("chat", "0")
    if not _chat.isdigit():
        _chat = "0"
    else:
        if int(_chat) >= len(_rooms):
            _chat = "0"
    dic["chat"] = _chat
    
    # --- 動作 ---
    _mode = _form.getfirst("mode", "1")
    if not _mode.isdigit():
        _mode = "1"
    else:
        if int(_mode) >= 5:
            _mode = "1"
    dic["mode"] = _mode
    
    # --- 名前 ---
    dic["name"] = _form.getfirst("name", "")

    # --- 色 ---
    _color = _form.getfirst("color", "0")
    if not _color.isdigit():
        _color = "0"
    else:
        if int(_color) >= len(_colors):
            _color = "0"
    dic["color"] = _color

    # --- SPAM CHECK ---
    dic["spamchk"] = _form.getfirst("spamchk", "")
    if len(dic["name"]) > 0:
        dic["entry"] = dic["name"]
    else:
        dic["entry"] = UNNAMED_ENTRY_NAME

    # --- コメント ---
    _field = _form.getfirst("field", "")
    if len(_field) > 512:
        _field = ""
    dic["field"] = _field
    
    # --- リロード ---
    _refresh = _form.getfirst("r", "900")
    if not _refresh.isdigit():
        _refresh = "900"
    else:
        if int(_refresh) < 20:
            _refresh = "900"
    dic["refresh"] = _refresh
    
    # --- ログ表示行数 ---
    _limit = _form.getfirst("limit", "30")
    if not _refresh.isdigit():
        _limit = "30"
    dic["limit"] = _limit

    # --- ログ表示開始行 ---
    _offset = _form.getfirst("offset", None)
    if not _refresh.isdigit():
        _offset = None
    dic["offset"] = _offset
    
    # --- IPアドレス ---
    dic["remote_addr"] = os.environ.get("REMOTE_ADDR", "")
    return dic

def html_header(_title, _author, _charset, _myform, _sc):
    # --- HTML HEADER ---
    print "Content-type: text/html"
    print _sc.output()
    print """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<HTML LANG="ja">
<HEAD>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=%s">
<META NAME="Author" CONTENT="%s">
""" % (_charset, _author)

    if _myform["mode"] == "4":
        print '<META HTTP-EQUIV="REFRESH" CONTENT="%s;URL=./chat.cgi?chat=%s&amp;mode=%s&amp;r=%s&amp;name=%s">' % (_myform["refresh"], _myform["chat"], _myform["mode"], _myform["refresh"], _myform["entry"])
    print '<TITLE>%s</TITLE>' % _title
    print '</HEAD>'


def html_tag_body(_room=None):
    # --- TAG BODY ---
    _tag = '<BODY'
    if _room is not None:
        if len(_room.tag_background or '') > 0:
            _tag += ' background="' + _room.tag_background + '"'
        if len(_room.tag_bgcolor or '') > 0:
            _tag += ' bgcolor="' + _room.tag_bgcolor + '"'
        if len(_room.tag_text or '') > 0:
            _tag += ' text="' + _room.tag_text + '"'
        if len(_room.tag_link or '') > 0:
            _tag += ' link="' + _room.tag_link + '"'
        if len(_room.tag_alink or '') > 0:
            _tag += ' alink="' + _room.tag_alink + '"'
        if len(_room.tag_vlink or '') > 0:
            _tag += ' vlink="' + _room.tag_vlink + '"'
    _tag += '>'
    print _tag

def html_frame(_myform):
    print """
<FRAMESET ROWS="25%%,75%%">
<FRAME SRC="./chat.cgi?chat=%s&mode=3&r=%s" NAME="menu">
<FRAME SRC="./chat.cgi?chat=%s&mode=4&r=%s&name=%s" NAME="main">
<NOFRAMES>
""" % (_myform["chat"], _myform["refresh"], _myform["chat"], _myform["refresh"], _myform["entry"])
    html_tag_body()
    print '　あなたのブラウザでは-Gathering chat-フレーム版をご利用することはできません。<BR>'
    print '　<A HREF="./chat.cgi?chat=%s&mode=1">こちら</A>から通常版へお戻り下さい。' % _myform["chat"]
    print '</BODY>'
    print '</NOFRAMES>'
    print '</FRAMESET>'


def html_link(_chat, _mode):
    print '【<A HREF="http://www.lay-el.net/" TARGET="_top">トップページへ戻る</A>】'
    if _mode == "1":
        print '【<A HREF="./chat.cgi?chat=%s&amp;mode=2" TARGET="_top">フレーム版へ</A>】' % _chat
    elif _mode == "3":
        print '【<A HREF="./chat.cgi?chat=%s&amp;mode=1" TARGET="_top">通常版へ</A>】' % _chat
    print '<BR><BR>'


def html_form(_myform, _colors, _rooms, _spam_check_word):
    _mode = _myform["mode"]
    if _mode == "3":
        # フレーム版
        _mode = "2"

    print '<FORM ACTION="./chat.cgi" METHOD="POST" TARGET="_top">'
    print '<INPUT TYPE="hidden" NAME="mode" VALUE="%s">' % _mode
    html_link(_myform["chat"], _myform["mode"])

    print '名前<INPUT TYPE="text" NAME="name" SIZE="20" MAXLENGTH="64" VALUE="%s">' % _myform["name"] ,

    print '文字色<select name="color" size="1">'
    for c in _colors:
        if _myform["color"] == c.color_id:
            print '<option value="%s" selected>%s</option>' % (c.color_id, c.color_name)
        else:
            print '<option value="%s">%s</option>' % (c.color_id, c.color_name)
    print '</select>'
    
    if _myform["mode"] == "3":
        print '自動リロード<INPUT TYPE="text" NAME="r" VALUE="%s" SIZE="5">' % _myform["refresh"]

    print '部屋<select name="chat" size="1">'
    for r in _rooms:
        if _myform["chat"] == r.room_id:
            print '<option value="%s" selected>%s</option>' % (r.room_id, r.room_name)
        else:
            print '<option value="%s">%s</option>' % (r.room_id, r.room_name)
    print '</select>'

    print 'SPAM防止<INPUT TYPE="text" NAME="spamchk" SIZE="4" MAXLENGTH="10" VALUE="%s">' % _myform["spamchk"]
    print '<BR>'
    print '発言内容<INPUT TYPE="text" NAME="field" VALUE="" SIZE="80" MAXLENGTH="128"><BR>'
    print '<INPUT TYPE="SUBMIT" value="発言（空の発言でリロードになります）">',
    print '<SMALL>※必ずSPAM防止に『%s』と入力してください。</SMALL>' % _spam_check_word
    print '<BR><BR>'

def html_log(_logs):
    for l in _logs:
        if len(l.bot_reply or '') > 0:
            print l.bot_reply ,
        print '[%s]' % l.timestamp ,
        print '<font size="+1">　</font>',
        print '<FONT COLOR="%s"><B>%s</B><!--%s--></FONT>' % (l.color_value, l.entry_name, l.remote_addr) ,
        print '「%s」<BR>' % l.comment


def html_entries(_entries, _all_entries):
    print '(この部屋にいる人%s人/全部で%s人)' % (len(_entries), len(_all_entries))
    list = []
    for e in _entries:
        list.append(e.entry_name)
    print '☆'.join(list)
    print '<HR>'

def html_footer(_script_signature):
    # --- HTML FOOTER ---
    print """<HR>
<DIV ALIGN="right">
<FONT SIZE="2">%s</FONT>
</DIV>
</FORM>
</BODY>
</HTML>
""" % _script_signature

