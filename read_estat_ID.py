# -*- coding=utf-8 -*-
from pandas import Series, DataFrame
import pandas as pd
import json
from urllib.request import urlopen
from urllib.parse import quote_plus
from pandas.io.json import json_normalize
from ast import literal_eval

# 政府統計の総合窓口(e-Stat)
# 統計表IDを取得

# 統計表IDを取得するための統計調査名等のキーワードを指定する。
field_code = 'うなぎのかば焼き'
# keywordをURLエンコーディングする。
# python2ではurllib.quote
field_code = quote_plus(field_code, encoding="utf-8")

#e-statにアクセスするためのIDをセットする。
with open('data/app_id.txt', encoding='utf-8') as a_file:
    for a_line in a_file:
        app_id = a_line

# 統計表情報取得       
request = 'http://api.e-stat.go.jp/rest/2.0/app/json/getStatsList?'
search_word ='&searchWord=' + field_code

request_set = request + app_id + search_word

# urlopen(...).read()はByte型を返すので、decode('utf-8')でstr型に変換している。
resp = urlopen(request_set).read().decode('utf-8')

resp = json.loads(resp)

print('======================================================================')
print(resp['GET_STATS_LIST']['PARAMETER'])
print('======================================================================')
print(resp['GET_STATS_LIST']['RESULT'])
print('======================================================================')
print(resp['GET_STATS_LIST']['DATALIST_INF']['RESULT_INF'])
print('======================================================================')
print(resp['GET_STATS_LIST']['DATALIST_INF']['NUMBER'])

resp_list = resp['GET_STATS_LIST']['DATALIST_INF']['TABLE_INF']
# “Normalize” semi-structured JSON data into a flat table
result = json_normalize(resp_list)
result.to_excel('data/Stat_ID.xlsx', sheet_name='Stat')