#!python
# encoding=utf-8

# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# 『みんなで決めるゲーム音楽ベスト100』用 投票集計スクリプト
# 
# [対応フォーマット]
# 順位｜曲名｜ゲームタイトル｜機種名｜コメント 
# 
# [実装済]
# HTMLをダウンロード
# HTMLを解析→レスごとに分ける→ヘッダと明細に分ける
# イレギュラーなレスかどうか判断
# イレギュラーなレスをファイル出力
# 整形してファイル出力(全投票に情報を追加して出力)
#     スレ情報/レス番/HOST
# [TODO]
# レスが登録済みかどうかの判断
# レスごとに被りがどのぐらいあるか判定できると良いなぁ～(ﾉ∀`)ﾀﾊｰ
#     1レスごとに全レスを検査
#     ここまでやるにはDB化する必要ある
# 
# ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

import sys
import codecs
import urllib2
import re
import csv
import unicodecsv

# 変動しそうな値

#1レスあたりの最大投票数
VOTE_COUNT_MAX = 25  

#投票フォーマット
VOTE_PATTERN = u"([0-9]*[0-9])[｜|](.*)[｜|](.*)[｜|](.*)[｜|](.*)$"

# 投稿データの定義
class VoteData:
	def __init__(self):
		self.seq = ""
		self.musicname = ""
		self.gamename = ""
		self.platform = ""
		self.note = ""

# レスデータの定義
class ResponseData:
	def __init__(self):
		self.no = ""
		self.name = ""
		self.mail = ""
		self.date = ""
		self.honbun = ""
		self.title = ""
		self.id = ""
		self.vote = []
		self.comment = ""
		self.errmsg = ""

# HTTP GETする
def get_http_text(sURL) :
	ret = ""
	info = ""

	# スレのURLからDAT形式のデータを得るURLを取得
	# ※したらばの仕様
	# http://jbbs.livedoor.jp/bbs/rawmode.cgi/[カテゴリ]/[掲示板番号]/[スレッド番号]/
	# http://jbbs.livedoor.jp/bbs/read.cgi/music/25545/1344425052/
	match = re.match(u"http://jbbs.livedoor.jp/bbs/read.cgi(.*)$", sURL)
	if match is not None:
		info = match.group(1).strip()
		sURL = 'http://jbbs.livedoor.jp/bbs/rawmode.cgi' + info

	# サイトに接続
	site = urllib2.urlopen(sURL)

	ret = site.read()
	site.close()
	return ret, info

# スレを解析
def threadAnalyze(ret, threadinfo) :
	
	# レスごとに処理を行う
	for line in ret.split('\n') :
		# レスを分解
		# [レス番号]<>[名前]<>[メール]<>[日付]<>[本文]<>[スレッドタイトル]<>[ID]
		resData = line.decode('euc_jp', 'ignore').split('<>')

		# テストコード
		# print(resData)
		if len(resData) == 7:
			
			#スレッドタイトルが被っているとダメなのでスレURLに置き換え
			resData[5] = threadinfo
			
			#レス解析
			irregular,data = responseAnalyze(resData)
			
			#ファイル出力
			outputFile(irregular, data)
			

# ファイル出力
def outputFile(irregular, data):
	if irregular == False:
		# 正常ファイル出力(csv形式)
		# スレッドタイトル,レス番号,名前,メール,日付,ID,全体コメントの有無,SEQ,曲目,ゲーム名,機種,コメント

		csvList = []
		
		#タイトル行
		#csvRow = ["スレタイ","レス番","名前","メール","日付","ID","全体コメントの有無","順位","曲名","ゲーム名","機種","コメント"]
		#csvList.append(csvRow)
		#for res in data:
		
		res = data
		if res.vote is not None:
			for tmpvote in res.vote:
				csvRow = [res.title, res.no, res.name, res.mail, res.date, res.id]
				
				if len(res.comment.strip()) == 0:
					csvRow.append(u"無")
				else:
					csvRow.append(u"有")
				
				csvRow.append(tmpvote.seq)
				csvRow.append(tmpvote.musicname)
				csvRow.append(tmpvote.gamename)
				csvRow.append(tmpvote.platform)
				csvRow.append(tmpvote.note)
				
				csvList.append(csvRow)
		else:
			#投票データがない場合
			csvRow = [res.title, res.no, res.name, res.mail, res.date, res.id]
			if len(res.comment.strip()) == 0:
				csvRow.append(u"無")
			else:
				csvRow.append(u"有")
			csvRow.append(u"投票データがありません")
			csvRow.append()
			csvRow.append()
			csvRow.append()
			csvRow.append()
		
		# 書き込み
		writer = open('OK.csv', 'a')
		writer = unicodecsv.UnicodeWriter(writer)
		writer.writerows(csvList)
		
	else:
		# イレギュラーファイル出力
		# テキスト形式
		# *****
		# スレッドタイトル
		# レス番号
		# 名前 : メール : 日付 : ID
		# 本文
		
		fo = open('NG.txt', 'a')
		fo = codecs.lookup('utf_8')[-1](fo)
		#for res in data:
		res = data
		fo.write("***** ***** ***** ***** ***** ***** ***** ***** *****\n")
		fo.write(u"[スレッド名]" + res.title + "\n")
		fo.write(u"[レス番号　] " + res.no + "\n")
		fo.write(res.name + ":" + res.mail + ":" + res.date + ":" + res.id + "\n")
		fo.write(u"[本文　　　]\n" + res.honbun + "\n")
		if len(res.comment.strip()) > 0:
			fo.write(u"【コメント】\n" + res.comment + "\n")
		fo.write("\n")
		if len(res.errmsg.strip()) > 0:
			fo.write(u"[エラー　　]\n" + res.errmsg + "\n")
		fo.write("\n")
		
		
# レスを解析
def responseAnalyze(resData) :

	res = ResponseData()
	
	# 初期化＆デコード
	res.no = resData[0].strip()
	res.name = resData[1].strip()
	res.mail = resData[2].strip()
	res.date = resData[3].strip()
	res.honbun = resData[4].strip()
	res.title = resData[5].strip()
	res.id = resData[6].strip()
	res.vote = []
	res.comment = ""

	# コメントを抽出する
	match = re.search(u"【コメント】(.*)$", res.honbun)
	if match is not None:
		res.comment = match.group(1).replace('<br>', '\n')

		# コメントにフォーマット書く阿呆がいるので削っとく
		res.honbun = res.honbun.replace(match.group(1), '')
		res.honbun = res.honbun.replace(u"【コメント】", '')

	# 改行タグを改行にしとく
	res.honbun = res.honbun.replace('<br>', '\n')

	# フォーマットに沿わない行が見つかったら、全てイレギュラーファイル行き
	rtn, errmsg = check_format(res.honbun)
	if rtn == False:
		res.errmsg += u"【フォーマットエラー】" + errmsg + "\n"
		return True, res

	# フォーマットに沿ったものを抽出して処理
	voteList = []
	for match in re.finditer(VOTE_PATTERN, res.honbun, re.MULTILINE):
		print(u"投稿:" + match.group(1))
		
		# 投票を取得
		vote = VoteData()
		vote.seq = match.group(1).strip()
		vote.musicname = match.group(2).strip()
		vote.gamename = match.group(3).strip()
		vote.platform = match.group(4).strip()
		vote.note = match.group(5).strip()
		
		# 内容がない場合は次にいく
		if len(vote.musicname) == 0:
			continue
		
		# 投票内容をチェック、異常があったら全てイレギュラーファイル行き
		rtn, errmsg = check_vote(voteList, vote)
		if rtn == False:
			res.errmsg += u"【投票内容エラー】" + errmsg + "\n"
			return True, res
		
		# 投票に追加
		voteList.append(vote)

	res.vote = voteList
	return False, res


# フォーマットに沿わないレスが見つかったら、全てイレギュラーファイル行き
# ※訂正依頼／なんか主張してるコメ／フォーマットをミスってるコメ／投票が多すぎ
# 　ここは手作業で対応するしかなさげ
def check_format(honbun) :
	voteCount = 0		# 投票カウンタ
	
	for line in honbun.split('\n'):
		#改行のみの場合はOK
		if len(line.strip()) == 0:
			continue
		
		#タイトル行は許せ
		ret = re.search(u"順位｜曲名｜ゲームタイトル｜機種名｜コメント", line)
		if ret is not None:
			continue
		
		#フォーマットに合っていない場合はNG
		ret = re.search(VOTE_PATTERN, line.strip())
		if ret is None:
			return False, u'行フォーマットが不正' + '\n' + line + '\n'
		else:
			voteCount += 1
			
			#投票数を超えた場合はNG
			if voteCount > VOTE_COUNT_MAX:
				return False, u'投票数が多すぎ'
	
	# 投票がない場合はNG
	if voteCount == 0:
		return False, u'投票がない'
	 
	return True, ''


# 投票内容を細かく見てチェックする
# 　　同じ投票内で曲名が被っているもの
# 　　同じ投票内で順位が被っているもの
def check_vote(voteList, vote) :
	for tmp in voteList:
		# 順位が被っている
		if vote.seq == tmp.seq:
			return False, u'順位が被っている[' + vote.seq + ', ' + tmp.seq + ']'
		
		# 曲名が被っている
		if vote.musicname + vote.gamename == tmp.musicname + tmp.gamename:
			return False, u'曲名が被っている[' + vote.musicname + ']'
			
	return True, ''




# メイン処理 
if __name__ == '__main__' :
	
	for url in open('urllist.txt', 'r'):
	
		if len(url.strip()) == 0:
			continue
		
		ret, threadinfo = get_http_text(url)

		#スレ解析
		threadAnalyze(ret, threadinfo)


