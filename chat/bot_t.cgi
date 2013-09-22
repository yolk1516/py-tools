#!/usr/bin/python
# -*- coding: utf-8 -*-
# なんでサクラエディタで開こうとするときにutf-8にならんのo(｀ω´*)oﾌﾟﾝｽｶﾌﾟﾝｽｶ!!
import cgi
import cgitb; cgitb.enable()
import os
import sys
#import codecs
sys.path.append('./lib')
import BotWasuiLib

# --- ENCODE ---
#sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

# --- SETTING ---
AUTHOR = "WASHI"
BOT_NAME = "わすぃ"
SCRIPT_SIGNATURE = "-Gathering Chat Ver,3.00- Script written by " + AUTHOR + "."
TITLE = "居間の前"
CHARSET = "UTF-8"
SPAM_CHECK_WORD = "和室"

# --- Get Arguments ---
form = cgi.FieldStorage()

bot_reply = ""

keyword = form.getfirst("keyword","")
reply = form.getfirst("reply","")
spamchk = form.getfirst("spamchk","")
# --- DB LOG UPDATE ---
if len(keyword) > 0 and len(reply) > 0 and spamchk == SPAM_CHECK_WORD:
    bot_reply = BotWasuiLib.bot_learn_keyword(keyword, reply)

# --- HTML ---
print "Content-type: text/html"
print """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<HTML LANG="ja">
<HEAD>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=%(charset)s">
<META NAME="Author" CONTENT="%(author)s">

<STYLE>
/* Line Style */
HR      {color : olive;}

/* Font Class Style */
.outside { font-size: 9pt; color: 004040; font-family: "Times New Roman"; }
.main    { font-size:11pt; color: 008080; font-family: "ＭＳ Ｐゴシック"; }
.title   { font-weight: bold; font-size: 14pt; color: 408080; 
           font-family: "Times New Roman","ＭＳ Ｐ明朝";}
/* Link Fonts Style */
/* Default */
A       { text-decoration:none;}
A:VISITED   { color: #CA95FF; }
A:HOVER     { text-decoration:underline; color:#FF00FF;}
A:ACTIVE    { color: #7800F0; }
.form { border: 1; 
    border-color: "#008080"; 
    border-style: solid;
    border-width : 1px;
    background : #FCFCFC;
    font-family : 'ダサ字';
}
</STYLE>
<TITLE>%(title)s</TITLE>
</HEAD>
<BODY>
<FONT CLASS="outside">Living room</FONT>

<FONT CLASS="main">
<BLOCKQUOTE>
<FONT CLASS="title">%(bot_name)sに言葉を教えて！</FONT>　
<A HREF="http://www.lay-el.net/" CLASS="menu">
<FONT CLASS="outside">【Home】</FONT></A>　
<A HREF="./chat.cgi?chat=2&mode=1" CLASS="menu">
<FONT CLASS="outside">【Chat】</FONT></A>
<form method="post" action="bot_t.cgi">
辞書は定期的に%(author)sがチェックしているかもしれません。<BR>
その時、この%(bot_name)sに相応しくない返事は<BR>
勝手に変更・削除する場合があります。<P>

キーワード（例：まったり）<BR>
<FONT COLOR="#008000">%(bot_name)sが返事をする為のキーワードです。<BR>
発言した時このキーワードが入ってると下で<BR>
書いた返事が返ってきます。</FONT>
<br><input type=text name="keyword" size="20" class="form"><br>
<br>
返事（例：お茶が美味いでふ・・・(しみじみ ））<br>
<FONT COLOR="#008000">『c_name』と入力するとその部分に名前が入ります。<BR>
あと、%(bot_name)sは『でふまふ調』が基本の口調ですので<BR>
入力時は協力してくださると助かります。<BR>
<input type=text name="reply" size="50" class="form"><BR>
<BR>
※必ずSPAM防止に『%(spamword)s』と入力してください。 <BR>
<input type=text name="spamchk" size="20" class="form"><BR>
<BR>
</FONT>
<input type=submit value="登録" class="form"></form>

%(reply)s

</FONT>
</BLOCKQUOTE>
</body>
</html>
""" % {"charset": CHARSET, "author": AUTHOR, "title": TITLE, "bot_name": BOT_NAME, "reply": bot_reply, "spamword": SPAM_CHECK_WORD}

