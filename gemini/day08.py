import requests
from requests.exceptions import JSONDecodeError
import json

def json_reshape(data,tab=0):
    for k,v in data.items():
        if isinstance(v,dict):
            print(' '*tab,k)
            json_reshape(v,tab+4)
        else:
            print(' '*tab,k,v)

# JSONを返すエンドポイントに変更
url = 'https://httpbin.org/get'
r = requests.get(url)

# レスポンスが成功したか確認
if r.status_code == 200:
    try:
        # JSONへの変換を試みる
        data = r.json()
        json_reshape(data)
        
    except JSONDecodeError:
        # JSONでなかった場合の処理
        print("レスポンスはJSON形式ではありませんでした。")
else:
    print(f"リクエストに失敗しました。ステータスコード: {r.status_code}")
url2 = 'https://httpbin.org/post'
# 送信するデータ（Pythonの辞書）
payload = {
        'user_id': 123,
        'name': 'Suzuki Ichiro',
        'is_active': True,
        'courses': ['Python', 'Data Science']
    }
# `json`パラメータに辞書を渡してPOSTリクエストを送信
res = requests.post(url2, json=payload, timeout=10)

# 4xx, 5xx系のエラーステータスコードの場合、例外を発生させる
res.raise_for_status()

# レスポンスをJSONとして取得
data2 = res.json()
print("--- サーバーからの応答 ---")
json_reshape(data2)

