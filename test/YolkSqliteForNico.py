#!python
# encoding=utf-8

import sqlite3

# ===== ===== ===== ===== ===== ===== ===== ===== 
# SQLite3の操作クラス
# ===== ===== ===== ===== ===== ===== ===== ===== 
class YolkSqliteForNico:

    # コンストラクタ
    def __init__(self):
        self.con = sqlite3.connect("data.db")
        self.db_table_init()
        
    # デストラクタ
    def __del__(self):
        if self.con:
            self.con.close()

    # テーブル初期化
    def db_table_init(self):
        self.db_table_create("NICOVIDEO_ID")
        self.db_table_create("NICOVIDEO_TAG")
        self.db_table_create("NICOVIDEO_INFO")

    # テーブル作成
    # 引数: テーブル名
    def db_table_create(self, tablename):
        checksql = self.db_get_check_sql()
        cur = self.con.execute(checksql % tablename)
        if cur.fetchone() == None:
            self.con.execute(self.db_get_create_sql(tablename))
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
    def db_get_create_sql(self, tablename):
        rtn = ""
        if tablename == "NICOVIDEO_ID":
            rtn = u"""
CREATE TABLE NICOVIDEO_ID (
    id      TEXT,
    title   TEXT,
    primary key(id)
)
"""
        elif tablename == "NICOVIDEO_TAG":
            rtn = u"""
CREATE TABLE NICOVIDEO_TAG (
    id      TEXT,
    tag     TEXT,
    primary key(id,tag)
)
"""
        elif tablename == "NICOVIDEO_INFO":
            rtn = u"""
CREATE TABLE NICOVIDEO_INFO (
    id               TEXT,
    ins_timestamp    TEXT,
    title            TEXT,
    view_counter     INTEGER,
    comment_num      INTEGER,
    mylist_counter   INTEGER,
    primary key(id,ins_timestamp)
)
"""
        else:
            rtn = ""
        
        return rtn

    # 更新
    # 引数１: ID
    # 引数２: タイトル
    def db_update_id(self, id,title):
        sql = u"""
INSERT OR REPLACE INTO
NICOVIDEO_ID (id,title)
VALUES (?, ?)
"""
        cur = self.con.execute(sql, (id,title))

    # 更新
    # 引数１: ID
    # 引数２: タグ
    def db_update_tag(self, id,tag):
        sql = u"""
INSERT OR REPLACE INTO
NICOVIDEO_TAG(id,tag)
VALUES(?, ?)
"""
        cur = self.con.execute(sql, (id,tag))

    # 更新
    # 引数１: ID
    # 引数２: タイトル
    # 引数３: 再生数
    # 引数４: コメント数
    # 引数５: マイリスト数
    def db_update_info(self,id,title,view_counter,comment_num,mylist_counter):
        sql = u"""
INSERT OR REPLACE INTO
NICOVIDEO_INFO(id,ins_timestamp,title,view_counter,comment_num,mylist_counter)
VALUES(?, datetime('now', 'localtime'), ?, ?, ?, ?)
"""
        cur = self.con.execute(sql, (id,title,view_counter,comment_num,mylist_counter))

    # コミット
    def commit(self):
        self.con.commit()
        
    # ロールバック
    def rollback(self):
        self.con.rollback()
        
    # video_idが存在するかどうかチェックする
    # 引数: ID
    def db_exists_video_id(self, id):
        checksql = "SELECT * FROM NICOVIDEO_ID WHERE id ='%s'"
        cur = self.con.execute(checksql % id)
        if cur.fetchone() == None:
            return False
        else:
            return True
