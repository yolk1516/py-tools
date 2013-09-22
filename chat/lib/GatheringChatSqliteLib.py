#!python
# encoding=utf-8

import sqlite3
import GatheringChatEntity

# ===== ===== ===== ===== ===== ===== ===== ===== 
# SQLite3の操作クラス
# ===== ===== ===== ===== ===== ===== ===== ===== 
class GatheringChatSqliteLib:

    # コンストラクタ
    def __init__(self, _path):
        self.con = sqlite3.connect(_path)
        self.con.text_factory = str 
        self.con.row_factory = sqlite3.Row
        self.db_table_init()
        
    # デストラクタ
    def __del__(self):
        if self.con:
            self.con.close()

    # テーブル初期化
    def db_table_init(self):
        self.db_table_create("GATHERINGCHAT_LOG")
        self.db_table_create("GATHERINGCHAT_ENTRY")
        self.db_table_create("GATHERINGCHAT_ROOM")
        self.db_table_create("GATHERINGCHAT_COLOR")

    # テーブル作成
    # 引数: テーブル名
    def db_table_create(self, _tablename):
        checksql = self.db_get_check_sql()
        cur = self.con.execute(checksql % _tablename)
        if cur.fetchone() == None:
            self.con.execute(self.db_get_create_sql(_tablename))
            self.con.commit()

    # テーブルが存在するかチェックするSQL
    # 戻り値: SQL
    def db_get_check_sql(self):
        checksql = u"""
SELECT
    * 
FROM
    sqlite_master
WHERE
    type='table' 
AND name='%s'
"""
        return checksql

    # テーブルを作成するSQLを取得
    # 引数: テーブル名
    def db_get_create_sql(self, _tablename):
        rtn = ""
        if _tablename == "GATHERINGCHAT_LOG":
            rtn = """
CREATE TABLE GATHERINGCHAT_LOG (
    ins_timestamp    TEXT,
    room_id          TEXT,
    entry_name       TEXT,
    color_value      TEXT,
    remote_host      TEXT,
    remote_addr      TEXT,
    comment          TEXT,
    bot_reply        TEXT
)
"""
        elif _tablename == "GATHERINGCHAT_ENTRY":
            rtn = """
CREATE TABLE GATHERINGCHAT_ENTRY (
    remote_addr      TEXT,
    timestamp        TEXT,
    entry_name       TEXT,
    room_id          TEXT,
    primary key(remote_addr)
)
"""
        elif _tablename == "GATHERINGCHAT_ROOM":
            rtn = """
CREATE TABLE GATHERINGCHAT_ROOM (
    room_id         TEXT,
    room_name       TEXT,
    tag_background  TEXT,
    tag_bgcolor     TEXT,
    tag_text        TEXT,
    tag_link        TEXT,
    tag_vlink       TEXT,
    tag_alink       TEXT,
    primary key(room_id)
)
"""
        elif _tablename == "GATHERINGCHAT_COLOR":
            rtn = """
CREATE TABLE GATHERINGCHAT_COLOR (
    color_id        TEXT,
    color_name      TEXT,
    color_value     TEXT,
    primary key(color_id)
)
"""
        else:
            rtn = ""
        
        return rtn

    # エントリー更新
    # 引数１: エントリクラス
    def db_update_entry(self, _chat_entry):
        sql = u"""
INSERT OR REPLACE INTO
GATHERINGCHAT_ENTRY (remote_addr,timestamp,entry_name,room_id)
VALUES (?, datetime('now', 'localtime'), ?, ?)
"""
        cur = self.con.execute(sql, (_chat_entry.remote_addr,_chat_entry.entry_name,_chat_entry.room_id))

    # ログ追加
    # 引数１: チャットログクラス
    def db_insert_log(self, _chat_log):
        sql = u"""
INSERT INTO
GATHERINGCHAT_LOG(ins_timestamp,room_id,entry_name,color_value,remote_host,remote_addr,comment,bot_reply)
VALUES(datetime('now', 'localtime'), ?, ?, ?, ?, ?, ?, ?)
"""
        cur = self.con.execute(sql, (_chat_log.room_id,_chat_log.entry_name,_chat_log.color_value,_chat_log.remote_host,_chat_log.remote_addr,_chat_log.comment,_chat_log.bot_reply))

    # ルーム更新
    # 引数１: 部屋情報クラス
    def db_update_room(self,_chat_room):
        sql = u"""
INSERT OR REPLACE INTO
GATHERINGCHAT_ROOM(room_id,room_name,tag_background,tag_bgcolor,tag_text,tag_link,tag_vlink,tag_alink)
VALUES(?, ?, ?, ?, ?, ?, ?, ?)
"""
        cur = self.con.execute(sql, (_chat_room.room_id, _chat_room.room_name, _chat_room.tag_background, _chat_room.tag_bgcolor, _chat_room.tag_text, _chat_room.link, _chat_room.vlink, _chat_room.alink))

    # カラー更新
    # 引数１: カラークラス
    def db_update_room(self,_chat_color):
        sql = u"""
INSERT OR REPLACE INTO
GATHERINGCHAT_COLOR(color_id,color_name,color_value)
VALUES(?, ?, ?)
"""
        cur = self.con.execute(sql, (_chat_color.color_id, _chat_color.color_name, _chat_color.value))

    # ログ削除
    def db_delete_log(self, _chat_logs):
        sql = u"""
DELETE FROM GATHERINGCHAT_LOG
WHERE ins_timestamp = ?
"""
        for _chat_log in _chat_logs:
            cur = self.con.execute(sql, _chat_log.timestamp)


    # エントリ削除
    def db_delete_entry(self, _chat_entries):
        sql = u"""
DELETE FROM GATHERINGCHAT_ENTRY
WHERE remote_addr = ?
"""
        for _chat_entry in _chat_entries:
            cur = self.con.execute(sql, _chat_entry.remote_addr)

    # エントリ削除(5分経過したものは削除)
    def db_clear_entry(self):
        sql = u"""
DELETE FROM GATHERINGCHAT_ENTRY
WHERE datetime(timestamp) < datetime('now', 'localtime', '-5 minutes')
"""
        cur = self.con.execute(sql)

    # ルーム削除
    def db_delete_room(self, _chat_rooms):
        sql = u"""
DELETE FROM GATHERINGCHAT_ROOM
WHERE room_id = ?
"""
        for _chat_room in _chat_rooms:
            cur = self.con.execute(sql, _chat_room.room_id)

    # カラー削除
    def db_delete_color(self, _chat_colors):
        sql = u"""
DELETE FROM GATHERINGCHAT_COLOR
WHERE color_id = ?
"""
        for _chat_color in _chat_colors:
            cur = self.con.execute(sql, _chat_color.color_id)


    # コミット
    def commit(self):
        self.con.commit()
        
    # ロールバック
    def rollback(self):
        self.con.rollback()
        
    # チャットログ取得
    # 引数１: 部屋番号
    # 引数２: 取得件数 ※省略可
    # 引数３: 開始行   ※省略可
    def db_select_log(self, _room_id, _limit="30", _offset=None):
        sql = "SELECT * FROM GATHERINGCHAT_LOG WHERE room_id ='%s'"
        sql += " ORDER BY ins_timestamp desc"
        if _limit != None:
            sql += " LIMIT " + _limit
        if _offset != None:
            sql += " OFFSET " + _offset
        cur = self.con.execute(sql % _room_id)
        
        rtn = []
        for row in cur:
            chatlog = GatheringChatEntity.ChatLog()
            # yyyy-mm-dd -> yyyy/mm/ddに置換
            chatlog.timestamp = row["ins_timestamp"].replace('-', '/')
            chatlog.room_id = row["room_id"]
            chatlog.entry_name = row["entry_name"]
            chatlog.color_value = row["color_value"]
            chatlog.remote_host = row["remote_host"]
            chatlog.remote_addr = row["remote_host"]
            chatlog.comment = row["comment"]
            chatlog.bot_reply = row["bot_reply"]
            rtn.append(chatlog)
        return rtn


    # エントリ取得
    # 引数１: 部屋番号
    def db_select_entry(self, _room_id):
        sql = "SELECT * FROM GATHERINGCHAT_ENTRY WHERE room_id ='%s'"
        cur = self.con.execute(sql % _room_id)
        
        rtn = []
        for row in cur:
            chatentry = GatheringChatEntity.ChatEntry()
            chatentry.room_id = row["room_id"]
            chatentry.entry_name = row["entry_name"]
            chatentry.remote_addr = row["remote_addr"]
            rtn.append(chatentry)
        return rtn
        
    # 全エントリ取得
    def db_select_entry_all(self):
        sql = "SELECT * FROM GATHERINGCHAT_ENTRY"
        cur = self.con.execute(sql)
        
        rtn = []
        for row in cur:
            chatentry = GatheringChatEntity.ChatEntry()
            chatentry.room_id = row["room_id"]
            chatentry.entry_name = row["entry_name"]
            chatentry.remote_addr = row["remote_addr"]
            rtn.append(chatentry)
        return rtn


    # カラー取得
    def db_select_color(self):
        sql = "SELECT * FROM GATHERINGCHAT_COLOR"
        cur = self.con.execute(sql)
        
        rtn = []
        for row in cur:
            ent = GatheringChatEntity.ChatColor()
            ent.color_id = row["color_id"]
            ent.color_name = row["color_name"]
            ent.color_value = row["color_value"]
            rtn.append(ent)
        return rtn
        
    # ルーム取得
    def db_select_room_all(self):
        sql = "SELECT * FROM GATHERINGCHAT_ROOM"
        cur = self.con.execute(sql)
        
        rtn = []
        for row in cur:
            ent = GatheringChatEntity.ChatRoom()
            ent.room_id = row["room_id"]
            ent.room_name = row["room_name"]
            ent.tag_background = row["tag_background"]
            ent.tag_bgcolor = row["tag_bgcolor"]
            ent.tag_text = row["tag_text"]
            ent.tag_link = row["tag_link"]
            ent.tag_vlink = row["tag_vlink"]
            ent.tag_alink = row["tag_alink"]
            rtn.append(ent)
        return rtn
            
    # ルーム取得
    # 引数１: 部屋番号
    def db_select_room(self, _room_id):
        sql = "SELECT * FROM GATHERINGCHAT_ROOM WHERE room_id = '%s'"
        cur = self.con.execute(sql % _room_id)
        
        for row in cur:
            ent = GatheringChatEntity.ChatRoom()
            ent.room_id = row["room_id"]
            ent.room_name = row["room_name"]
            ent.tag_background = row["tag_background"]
            ent.tag_bgcolor = row["tag_bgcolor"]
            ent.tag_text = row["tag_text"]
            ent.tag_link = row["tag_link"]
            ent.tag_vlink = row["tag_vlink"]
            ent.tag_alink = row["tag_alink"]
            return ent
        return None
