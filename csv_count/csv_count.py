#!/usr/local/bin/python 
# -*- coding: utf-8 -*-
# なんでサクラエディタで開こうとするときにutf-8にならんのo(｀ω´*)oﾌﾟﾝｽｶﾌﾟﾝｽｶ!!
import cgi
import cgitb; cgitb.enable()
import os
import sys
import codecs

# --- UPLOAD FORM ---
print '''Content-Type: text/html

<html>
<head>
  <meta http-equiv="Content-Type" content="text/html" charset="UTF-8" />
  <title>CSVファイルの各行の項目数をカウントする</title>
</head>
<body>
<h1>CSVファイルの各行の項目数をカウントする</h1>
'''



result = ''
rowidx = 1
form = cgi.FieldStorage()
if form.has_key('file'):
    item = form['file']
    if item.file:
        lines = item.file.read()
        if '\0' in lines:
            print '<p>Uploaded file is binary</p>'
        else:
            print '<table border>'
            print '<tr><td>行番号</td><td>項目数</td><td>内容</td></tr>'
            for line in lines.decode('cp932').encode('utf-8').replace("\r\n", "\n").split("\n"):
                print '<tr>' ,
                print '<td>' ,
                print rowidx , 
                print '</td>' ,
                print '<td>' ,
                print line.count(',') + 1 ,
                print '</td>' ,
                print '<td>' ,
                if len(line) > 100:
                    print line[0:99],'...'
                else:
                    print line ,
                print '</td>' ,
                print '</tr>'
                rowidx = rowidx + 1
            print '</table>'

print '''
<form action="csv_count.py" method="post" enctype="multipart/form-data">
  <input type="file" name="file" />
  <input type="submit" />
</form>
</body>
</html>
'''