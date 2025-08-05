# 必要なライブラリをインポート
import requests
from requests.exceptions import RequestException

def main():
    """
    APIから投稿データを取得し、タイトルと本文を表示する。
    """
    # データを取得したいAPIのURLを定義
    # JSONPlaceholderは、開発やテスト用のダミーAPIを提供してくれるサービス
    # /posts/1 は、IDが1の投稿データを指す
    url = 'https://jsonplaceholder.typicode.com/posts/1'

    try:
        # 指定したURLにGETリクエストを送信し、サーバーからの応答（レスポンス）を取得
        # timeoutを設定することで、応答がない場合に無限に待ち続けるのを防ぐ
        res = requests.get(url, timeout=10)

        # ステータスコードが4xx（クライアントエラー）や5xx（サーバーエラー）の場合、例外を発生させる
        res.raise_for_status()

        # レスポンスのボディをJSON形式からPythonの辞書（dict）に変換
        data = res.json()

        # 辞書から'title'キーと'body'キーの値を取り出して表示
        # .get()メソッドを使うと、キーが存在しなくてもエラーにならず、Noneを返すのでより安全
        title = data.get('title', '（タイトルなし）')
        body = data.get('body', '（本文なし）')
        
        print('title:', title)
        print('body:', body)

    except RequestException as e:
        # ネットワーク接続エラー、タイムアウト、HTTPエラーなど、リクエストに関する問題をまとめて捕捉
        print(f"データの取得中にエラーが発生しました: {e}")
    except Exception as e:
        # その他の予期せぬエラーを捕捉
        print(f"予期せぬエラーが発生しました: {e}")

if __name__ == "__main__":
    main()