#!/usr/bin/python
# -*- coding: utf-8 -*-
import cgi
import os
import sys
sys.path.append('./lib')
import GatheringChatHtmlLib

# --- SETTING ---
DB_PATH = 'log/gatheringchat.db'
SCRIPT_SIGNATURE = "-Gathering chat Ver,1.60- Script written by WASHI."
TITLE = "チャット"
AUTHOR = "WASHI"
CHARSET = "UTF-8"

# --- Get Arguments ---
form = cgi.FieldStorage()

# --- HTML HEADER ---
GatheringChatHtmlLib.html_header(TITLE, AUTHOR, CHARSET, form)


# +++ TEST CODE +++
print "<pre>"
for key in os.environ.keys():
	print '[%s] %s' % (key, os.environ[key])
print "</pre>"

# +++ TEST CODE +++
print "<pre>"
for key in form.keys():
	print '[FIELD:%s] %s' % (key, form[key].value)
print "</pre>"

# --- HTML FOOTER ---
GatheringChatHtmlLib.html_footer(SCRIPT_SIGNATURE)




