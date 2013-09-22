#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import BotWasuiSqliteLib

BOT_NAME = "わすぃ"
BOT_DB_PATH = "./log/botwasui.db"

# ===== ===== ===== ===== ===== ===== ===== ===== 
# ボットモジュール [ わすぃ ]
# ===== ===== ===== ===== ===== ===== ===== ===== 

# --- チャット内容と部屋番号からわすぃの出番かどうかを判定し、返信する ---
# 引数１: 名前
# 引数２: コメント
# 引数３: 部屋番号
# 引数４: 人数
# 戻り値: 返信
def send_message_to_bot(_name, _comment, _room, _entries):
    #「わすぃの和室」または「わすぃの居間」
    if _room == "1" or _room == "2":
        #「＞わすぃ」で終わるコメント
        if re.match(".*[>＞]" + BOT_NAME + "$", _comment) != None:
            m = re.match("^\(学習\)(.*)[>＞]" + BOT_NAME + "$", _comment)
            if m is not None:
                #(学習)ではじまるコメントの場合は学習
                return bot_learn_on_chat(m.group(1))
            m = re.match("^\(削除\)(.*)[>＞]" + BOT_NAME + "$", _comment)
            if m is not None:
                #(忘却)ではじまるコメントの場合は忘却
                return bot_forget_on_chat(m.group(1))
                
            return get_bot_reply(_name, _comment)
                
        #参加者が1人(ぼっち)の場合
        elif len(_entries) == 1:
            return get_bot_reply(_name, _comment)
    
    #「疲労者の休憩室」かつ「＞わすぃ」で終わるコメント
    if _room == "4" and re.match(".*[>＞]" + BOT_NAME + "$", _comment) != None:
        msg = '[<A HREF="./bot_t.cgi"><B><font color="#ff0000">' + BOT_NAME + '</font></B></A>]おつかれさまでふ＞' + _name + 'しゃん<BR>'
        return msg
    
    return ""


# --- 返信内容を取得する ---
# 引数１: 名前
# 引数２: チャット
# 戻り値: 返信
def get_bot_reply(_name, _comment):
    msg = '[<A HREF="./bot_t.cgi"><B><font color="#ff0000">' + BOT_NAME + '</font></B></A>]'
    
    botcon = BotWasuiSqliteLib.BotWasuiSqliteLib(BOT_DB_PATH)
    reply = botcon.db_select_keyword_dic(_comment)
    if len(reply or '') < 1 :
        reply = botcon.db_select_random_dic()
        if len(reply or '') < 1 :
            return ""
    msg += reply.replace("c_name", _name) + '<BR>'
    
    return msg

# --- (CHAT上で)学習させる ---
def bot_learn_on_chat(_msg):
    botcon = BotWasuiSqliteLib.BotWasuiSqliteLib(BOT_DB_PATH)
    if len(_msg or '') < 1:
        return ""

    if re.search(":", _msg) != None:
        keyvalue = _msg.split(':')
        
        if len(keyvalue[0] or '') < 1:
            return ""
        if len(keyvalue[1] or '') < 1:
            return ""
        botcon.db_update_keyword_dic(keyvalue[0], keyvalue[1])
    else:
        botcon.db_update_random_dic(_msg)
    botcon.commit()
    
    msg = '[<A HREF="./bot_t.cgi"><B><font color="#ff0000">' + BOT_NAME + '</font></B></A>]おぼえたでふ～♪<BR>'
    return msg

# --- (CHAT上で)忘れさせる ---
def bot_forget_on_chat(_msg):
    botcon = BotWasuiSqliteLib.BotWasuiSqliteLib(BOT_DB_PATH)
    if len(_msg or '') < 1:
        return ""

    if re.search(":", _msg) != None:
        keyvalue = _msg.split(':')
        
        if len(keyvalue[0] or '') < 1:
            return ""
        if len(keyvalue[1] or '') < 1:
            return ""
        botcon.db_delete_keyword_dic(keyvalue[0], keyvalue[1])
    else:
        botcon.db_delete_random_dic(_msg)
    botcon.commit()
    
    msg = '[<A HREF="./bot_t.cgi"><B><font color="#ff0000">' + BOT_NAME + '</font></B></A>]忘れたでふ～♪<BR>'
    return msg


# --- 学習させる ---
def bot_learn_keyword(_key, _msg):
    botcon = BotWasuiSqliteLib.BotWasuiSqliteLib(BOT_DB_PATH)
    if len(_msg or '') < 1 or len(_key or '') < 1:
        return ""

    botcon.db_update_keyword_dic(_key, _msg)
    botcon.commit()
    
    msg = '[<A HREF="./bot_t.cgi"><B><font color="#ff0000">' + BOT_NAME + '</font></B></A>]おぼえたでふ～♪<BR>'
    return msg

def bot_learn_random(_msg):
    botcon = BotWasuiSqliteLib.BotWasuiSqliteLib(BOT_DB_PATH)
    if len(_msg or '') < 1:
        return ""

    botcon.db_update_random_dic(_msg)
    botcon.commit()
    
    msg = '[<A HREF="./bot_t.cgi"><B><font color="#ff0000">' + BOT_NAME + '</font></B></A>]おぼえたでふ～♪<BR>'
    return msg


# --- 忘れさせる ---
def bot_forget_keyword(_key, _msg):
    botcon = BotWasuiSqliteLib.BotWasuiSqliteLib(BOT_DB_PATH)
    if len(_msg or '') < 1 or len(_key or '') < 1:
        return ""

    botcon.db_delete_keyword_dic(_key, _msg)
    botcon.commit()
    
    msg = '[<A HREF="./bot_t.cgi"><B><font color="#ff0000">' + BOT_NAME + '</font></B></A>]忘れたでふ～♪<BR>'
    return msg

def bot_learn_random(_msg):
    botcon = BotWasuiSqliteLib.BotWasuiSqliteLib(BOT_DB_PATH)
    if len(_msg or '') < 1:
        return ""

    botcon.db_delete_random_dic(_msg)
    botcon.commit()
    
    msg = '[<A HREF="./bot_t.cgi"><B><font color="#ff0000">' + BOT_NAME + '</font></B></A>]忘れたでふ～♪<BR>'
    return msg
