#!python
# encoding=utf-8

# ===== ===== ===== ===== ===== ===== ===== ===== 
# クラス　チャットログ
# ===== ===== ===== ===== ===== ===== ===== ===== 
class ChatLog(object):
    #初期値
    def __init__(self):
        self._timestamp = ""
        self._room_id = ""
        self._entry_name = ""
        self._color_value = ""
        self._remote_host = ""
        self._remote_addr = ""
        self._comment = ""
        self._bot_reply = ""
    
    #プロパティ - タイムスタンプ
    def _get_timestamp(self):
        return self._timestamp
    
    def _set_timestamp(self, value):
        self._timestamp = value
    
    timestamp = property(_get_timestamp, _set_timestamp)
    
    #プロパティ - 部屋番号
    def _get_room_id(self):
        return self._room_id
    
    def _set_room_id(self, value):
        self._room_id = value
    
    room_id = property(_get_room_id, _set_room_id)
    
    #プロパティ - 名前
    def _get_entry_name(self):
        return self._entry_name
    
    def _set_entry_name(self, value):
        self._entry_name = value
    
    entry_name = property(_get_entry_name, _set_entry_name)
    
    #プロパティ - 文字色
    def _get_color_value(self):
        return self._color_value
    
    def _set_color_value(self, value):
        self._color_value = value
    
    color_value = property(_get_color_value, _set_color_value)
    
    #プロパティ - 接続元ホスト名
    def _get_remote_host(self):
        return self._remote_host
    
    def _set_remote_host(self, value):
        self._remote_host = value
    
    remote_host = property(_get_remote_host, _set_remote_host)

    #プロパティ - 接続元IPアドレス
    def _get_remote_addr(self):
        return self._remote_addr
    
    def _set_remote_addr(self, value):
        self._remote_addr = value
    
    remote_addr = property(_get_remote_addr, _set_remote_addr)
    
    #プロパティ - コメント
    def _get_comment(self):
        return self._comment
    
    def _set_comment(self, value):
        self._comment = value
    
    comment = property(_get_comment, _set_comment)
    
    #プロパティ - ボット返信
    def _get_bot_reply(self):
        return self._bot_reply
    
    def _set_bot_reply(self, value):
        self._bot_reply = value
    
    bot_reply = property(_get_bot_reply, _set_bot_reply)

# ===== ===== ===== ===== ===== ===== ===== ===== 
# クラス　エントリ
# ===== ===== ===== ===== ===== ===== ===== ===== 
class ChatEntry(object):
    #初期値
    def __init__(self):
        self._remote_addr = ""
        self._entry_name = ""
        self._room_id = ""
    
    #プロパティ - 接続元IPアドレス
    def _get_remote_addr(self):
        return self._remote_addr
    
    def _set_remote_addr(self, value):
        self._remote_addr = value
    
    remote_addr = property(_get_remote_addr, _set_remote_addr)
    
    #プロパティ - 名前
    def _get_entry_name(self):
        return self._entry_name
    
    def _set_entry_name(self, value):
        self._entry_name = value
    
    entry_name = property(_get_entry_name, _set_entry_name)
    
    #プロパティ - 部屋番号
    def _get_room_id(self):
        return self._room_id
    
    def _set_room_id(self, value):
        self._room_id = value
    
    room_id = property(_get_room_id, _set_room_id)

# ===== ===== ===== ===== ===== ===== ===== ===== 
# クラス　文字色
# ===== ===== ===== ===== ===== ===== ===== ===== 
class ChatColor(object):
    #初期値
    def __init__(self):
        self._color_id = ""
        self._color_name = ""
        self._color_value = ""
    
    #プロパティ - 文字色ID
    def _get_color_id(self):
        return self._color_id
    
    def _set_color_id(self, value):
        self._color_id = value
    
    color_id = property(_get_color_id, _set_color_id)
    
    #プロパティ - 文字色名
    def _get_color_name(self):
        return self._color_name
    
    def _set_color_name(self, value):
        self._color_name = value
    
    color_name = property(_get_color_name, _set_color_name)
    
    #プロパティ - 文字色
    def _get_color_value(self):
        return self._color_value
    
    def _set_color_value(self, value):
        self._color_value = value
    
    color_value = property(_get_color_value, _set_color_value)


# ===== ===== ===== ===== ===== ===== ===== ===== 
# クラス　部屋情報
# ===== ===== ===== ===== ===== ===== ===== ===== 
class ChatRoom(object):
    #初期値
    def __init__(self):
        self._room_id = ""
        self._room_name = ""
        self._tag_background = ""
        self._tag_bgcolor = ""
        self._tag_text = ""
        self._tag_link = ""
        self._tag_vlink = ""
        self._tag_alink = ""
        
    #プロパティ - 部屋番号
    def _get_room_id(self):
        return self._room_id
    
    def _set_room_id(self, value):
        self._room_id = value
    
    room_id = property(_get_room_id, _set_room_id)
    
    #プロパティ - 部屋名
    def _get_room_name(self):
        return self._room_name
    
    def _set_room_name(self, value):
        self._room_name = value
    
    room_name = property(_get_room_name, _set_room_name)


    #プロパティ - 背景画像
    def _get_tag_background(self):
        return self._tag_background
    
    def _set_tag_background(self, value):
        self._tag_background = value
    
    tag_background = property(_get_tag_background, _set_tag_background)


    #プロパティ - 背景色
    def _get_tag_bgcolor(self):
        return self._tag_bgcolor
    
    def _set_tag_bgcolor(self, value):
        self._tag_bgcolor = value
    
    tag_bgcolor = property(_get_tag_bgcolor, _set_tag_bgcolor)

    #プロパティ - 文字色
    def _get_tag_text(self):
        return self._tag_text
    
    def _set_tag_text(self, value):
        self._tag_text = value
    
    tag_text = property(_get_tag_text, _set_tag_text)

    #プロパティ - リンク文字色
    def _get_tag_link(self):
        return self._tag_link
    
    def _set_tag_link(self, value):
        self._tag_link = value
    
    tag_link = property(_get_tag_link, _set_tag_link)

    #プロパティ - リンク文字色(既に見たページ)
    def _get_tag_vlink(self):
        return self._tag_vlink
    
    def _set_tag_vlink(self, value):
        self._tag_vlink = value
    
    tag_vlink = property(_get_tag_vlink, _set_tag_vlink)

    #プロパティ - リンク文字色(選択中)
    def _get_tag_alink(self):
        return self._tag_alink
    
    def _set_tag_alink(self, value):
        self._tag_alink = value
    
    tag_alink = property(_get_tag_alink, _set_tag_alink)

