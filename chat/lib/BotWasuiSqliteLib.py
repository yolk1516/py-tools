#!python
# encoding=utf-8

import sqlite3

# ===== ===== ===== ===== ===== ===== ===== ===== 
# SQLite3の操作クラス
# ===== ===== ===== ===== ===== ===== ===== ===== 
class BotWasuiSqliteLib:

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
        self.db_table_create("BOT_KEYWORD_DIC")
        self.db_table_create("BOT_RANDOM_DIC")

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
        if _tablename == "BOT_KEYWORD_DIC":
            rtn = """
CREATE TABLE BOT_KEYWORD_DIC (
    keyword         TEXT,
    reply           TEXT,
    primary key(keyword,reply)
)
"""
        elif _tablename == "BOT_RANDOM_DIC":
            rtn = """
CREATE TABLE BOT_RANDOM_DIC (
    reply   TEXT,
    primary key(reply)
)
"""
        else:
            rtn = ""
        
        return rtn

    # コミット
    def commit(self):
        self.con.commit()
        
    # ロールバック
    def rollback(self):
        self.con.rollback()

    # キーワード辞書更新
    # 引数１: キーワード
    # 引数２: 返信
    def db_update_keyword_dic(self, _keyword, _reply):
        sql = u"""
INSERT OR REPLACE INTO
BOT_KEYWORD_DIC (keyword,reply)
VALUES (?, ?)
"""
        cur = self.con.execute(sql, (_keyword,_reply))
        
    # キーワード辞書削除
    # 引数１: キーワード
    # 引数２: 返信
    def db_delete_keyword_dic(self, _keyword, _reply):
        sql = "DELETE FROM BOT_KEYWORD_DIC WHERE keyword = '%s' and reply = '%s'"
        cur = self.con.execute(sql, (_keyword,_reply))

    # ランダム辞書更新
    # 引数１: 返信
    def db_update_random_dic(self, _reply):
        sql = u"""
INSERT OR REPLACE INTO
BOT_RANDOM_DIC (reply)
VALUES (?)
"""
        cur = self.con.execute(sql , [_reply])

    # ランダム辞書削除
    # 引数１: 返信
    def db_delete_random_dic(self, _reply):
        sql = "DELETE FROM BOT_RANDOM_DIC WHERE reply = '%s'"
        cur = self.con.execute(sql % _reply)

    # キーワード辞書から取得
    def db_select_keyword_dic(self, _key):
        sql = "SELECT reply FROM BOT_KEYWORD_DIC WHERE '%s' LIKE '%%' || keyword || '%%' ORDER BY RANDOM() LIMIT 1"
        cur = self.con.execute(sql % _key)
        
        rtn = []
        row = cur.fetchone()
        if row is None:
            return ""
        else:
            return row[0]

    # ランダム辞書から取得
    def db_select_random_dic(self):
        sql = "SELECT reply FROM BOT_RANDOM_DIC ORDER BY RANDOM() LIMIT 1"
        cur = self.con.execute(sql)
        
        rtn = []
        row = cur.fetchone()
        if row is None:
            return ""
        else:
            return row[0]
        