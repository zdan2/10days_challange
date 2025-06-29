import sys
from dataclasses import dataclass, field, asdict
from collections import defaultdict
import json

# --- クラス定義 ---
# dataclassはクラスの外で定義するのが一般的です

@dataclass
class BlogPost:
    """
    基底クラス。ここではデフォルト値を持たない共通フィールドのみを定義するのが安全。
    """
    id: int
    title: str
    content_type: str
    # tagsはここから削除し、各子クラスで定義する

@dataclass
class Article(BlogPost):
    """「記事」クラス"""
    # 最初に、このクラス固有の「デフォルト値なし」フィールドを定義
    content: str
    
    # 次に、「デフォルト値あり」のフィールドを定義
    tags: set[str] = field(default_factory=set)
    
    def display(self):
        """記事の内容を整形して表示"""
        print(f"\n--- 記事詳細 (ID: {self.id}) ---")
        print(f"Title: {self.title}")
        print(f"Content: {self.content}")
        print(f"Tags: {', '.join(self.tags) if self.tags else 'なし'}")
        print("--------------------------\n")

@dataclass
class Memo(BlogPost):
    """「メモ」クラス"""
    # 最初に、このクラス固有の「デフォルト値なし」フィールドを定義
    memo_body: str
    
    # 次に、「デフォルト値あり」のフィールドを定義
    tags: set[str] = field(default_factory=set)
    
    def display(self):
        """メモの内容を整形して表示"""
        print(f"\n--- メモ詳細 (ID: {self.id}) ---")
        print(f"Title: {self.title}")
        print(f"Memo: {self.memo_body}")
        print(f"Tags: {', '.join(self.tags) if self.tags else 'なし'}")
        print("--------------------------\n")

class BlogSystem:
    def __init__(self):
        # {id: BlogPost_object} という形式で記事を保存
        self._posts = {}
        # {tag_name: {id1, id2, ...}} という形式
        self._tag_index = defaultdict(set)
        # 次に割り振るID
        self._next_id = 1

    def post(self, title, body, tags, content_type):
        """新しい記事またはメモを投稿する"""
        post_id = self._next_id
        tags_set = set(tags)
        
        new_post = None
        # content_typeに応じて、適切なクラスのインスタンスを生成
        if content_type == "article":
            new_post = Article(id=post_id, title=title, content=body, tags=tags_set, content_type=content_type)
        elif content_type == "memo":
            new_post = Memo(id=post_id, title=title, memo_body=body, tags=tags_set, content_type=content_type)
        else:
            print(f"エラー: 不明なコンテンツタイプ '{content_type}' です。")
            return None

        self._posts[post_id] = new_post
        
        # 逆引きインデックスを更新
        for tag in tags_set:
            self._tag_index[tag].add(post_id)
            
        self._next_id += 1
        print(f"記事ID: {post_id} として投稿しました。")
        return new_post

    def list_all(self):
        """全ての記事のIDとタイトルを一覧表示する"""
        if not self._posts:
            print("まだ記事がありません。")
            return
        
        print("\n--- 記事一覧 ---")
        for post in self._posts.values():
            print(f"ID: {post.id: <3} | Type: {post.content_type: <7} | Title: {post.title}")
        print("----------------\n")

    def view(self, post_id):
        """IDで指定した記事/メモの詳細を表示する"""
        post = self._posts.get(post_id)
        if post:
            # 各オブジェクトが持つdisplayメソッドを呼び出す（ポリモーフィズム）
            post.display()
        else:
            print(f"エラー: ID {post_id} の記事は見つかりませんでした。")

    def search_by_tag(self, tag):
        """タグで記事を検索する"""
        print(f"\n--- タグ '{tag}' の検索結果 ---")
        post_ids = self._tag_index.get(tag)
        
        if not post_ids:
            print("このタグを持つ記事はありません。")
            return
        
        for post_id in sorted(list(post_ids)): # ID順で表示されるようにソート
            post = self._posts[post_id]
            print(f"ID: {post.id: <3} | Type: {post.content_type: <7} | Title: {post.title}")
        print("---------------------------\n")

    def save(self, filename):
        """記事をファイルに保存する（修正版）"""

        # 1. posts の中の BlogPost オブジェクトを、JSON互換の辞書に変換する
        posts_data = []
        for post in self._posts.values():
            # post.__dict__ は便利ですが、dataclassなら asdict(post) がより確実です
            post_dict = post.__dict__.copy()  # 安全のためコピーを操作します
            # ここで、辞書の中の set を list に変換します！
            post_dict['tags'] = list(post.tags) 
            posts_data.append(post_dict)

        # 2. tag_index の中の set を list に変換する
        #    辞書の構造はそのまま維持します
        tag_index_data = {tag: list(ids) for tag, ids in self._tag_index.items()}

        # 3. すべてのデータを一つの辞書にまとめる
        data_to_save = {
            "posts": posts_data,
            "next_id": self._next_id,
            "tag_index": tag_index_data
        }
    
        # 4. ファイルに書き出す
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)
    
        print(f"データを {filename} に保存しました。")
    
    def load(self, filename):
        """ファイルからデータを読み込む"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self._posts.clear() # 現在のデータをクリア

            # 読み込んだ辞書から、正しい型のオブジェクトを復元する
            for post_data in data['posts']:
                content_type = post_data.get('content_type')
                # JSONから読み込んだtags(list)をsetに変換
                post_data['tags'] = set(post_data.get('tags', []))

                post_obj = None
                if content_type == 'article':
                    post_obj = Article(**post_data)
                elif content_type == 'memo':
                    post_obj = Memo(**post_data)
                
                if post_obj:
                    self._posts[post_obj.id] = post_obj

            self._next_id = data['next_id']
            
            # JSONから読み込んだtag_indexのvalue(list)をsetに変換して復元
            self._tag_index.clear()
            loaded_tag_index = data.get('tag_index', {})
            for tag, ids in loaded_tag_index.items():
                self._tag_index[tag] = set(ids)

            print(f"データを {filename} から読み込みました。")

        except FileNotFoundError:
            print(f"情報: セーブファイル {filename} が見つかりませんでした。新しいファイルを作成します。")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"エラー: {filename} のフォーマットが正しくないか、必要なデータがありません。 ({e})")

def main():
    """メインの実行ループ"""
    system = BlogSystem()
    system.load("blog_data.json") # 起動時に自動ロード
    
    print("\nミニブログへようこそ！")
    print("コマンド: post_article, post_memo, list, view <ID>, search <tag>, save, load, quit")
    
    while True:
        try:
            # Python 2のraw_inputはPython 3ではinput
            user_input = input("> ").strip().split(maxsplit=1)
            if not user_input:
                continue

            command = user_input[0].lower()
            args = user_input[1] if len(user_input) > 1 else ""

            if command == "post_article":
                title = input("   title: ")
                content = input(" content: ")
                tags_str = input("    tags (カンマ区切り): ")
                tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
                system.post(title, content, tags, "article")

            elif command == "post_memo":
                title = input("   title: ")
                memo_body = input("    memo: ")
                tags_str = input("    tags (カンマ区切り): ")
                tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
                system.post(title, memo_body, tags, "memo")
            
            elif command == "list":
                system.list_all()
                
            elif command == "view":
                if not args:
                    print("エラー: 表示する記事のIDを指定してください。(例: view 1)")
                    continue
                system.view(int(args))

            elif command == "search":
                if not args:
                    print("エラー: 検索するタグを指定してください。(例: search Python)")
                    continue
                system.search_by_tag(args)
                
            elif command == "save":
                system.save("blog_data.json")
            
            elif command == "load":
                system.load("blog_data.json")

            elif command == "quit":
                print("変更を保存しますか？ (yes/no)")
                if input("> ").lower().strip() == 'yes':
                    system.save("blog_data.json")
                print("プログラムを終了します。")
                break
            
            else:
                print(f"エラー: '{command}' は不明なコマンドです。")
        
        except ValueError:
            print("エラー: IDには数値を入力してください。")
        except KeyboardInterrupt:
            print("\nプログラムを終了します。")
            sys.exit()

if __name__ == '__main__':
    main()