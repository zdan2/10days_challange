import sys
from dataclasses import dataclass, field
from collections import defaultdict
import json

# ID生成はシンプルにクラス変数で管理する方法もあります
class BlogSystem:
    def __init__(self):
        # --- ステップ1: 記事コンテナを辞書に変更 ---
        # {id: BlogPost_object} という形式で記事を保存
        self._posts = {}
        
        # --- ステップ1: 逆引きインデックスの値をsetに変更 ---
        # {tag_name: {id1, id2, ...}} という形式
        self._tag_index = defaultdict(set)
        
        # 次に割り振るID
        self._next_id = 1

    def post(self, title, content, tags):
        """新しい記事を投稿する"""
        post_id = self._next_id
        
        # tagsは文字列のセットとして扱う
        tags_set = set(tags)
        
        new_post = BlogPost(id=post_id, title=title, content=content, tags=tags_set)
        
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
            print(f"ID: {post.id: <3} | Title: {post.title}")
        print("----------------\n")

    def view(self, post_id):
        """IDで指定した記事を表示する"""
        # --- ステップ1: 辞書なのでO(1)で高速にアクセス ---
        post = self._posts.get(post_id)
        if post:
            print(f"\n---記事詳細 (ID: {post.id})---")
            print(f"Title: {post.title}")
            print(f"Content: {post.content}")
            # setをカンマ区切りの文字列に変換して表示
            print(f"Tags: {', '.join(post.tags)}")
            print("--------------------------\n")
        else:
            print(f"エラー: ID {post_id} の記事は見つかりませんでした。")

    def search_by_tag(self, tag):
        """タグで記事を検索する（高速な逆引きインデックスを使用）"""
        print(f"\n--- タグ '{tag}' の検索結果 ---")
        
        # --- ステップ1: 建設した高速道路を走る！ ---
        post_ids = self._tag_index.get(tag)
        
        if not post_ids:
            print("このタグを持つ記事はありません。")
            return
        
        for post_id in post_ids:
            post = self._posts[post_id] # IDが分かっているので、ここも高速
            print(f"ID: {post.id: <3} | Title: {post.title}")
        print("---------------------------\n")
        
# from dataclasses import asdict # こちらを使うと、より簡潔になります

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
        """ファイルから記事を読み込む"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)

            # 辞書をBlogPostオブジェクトに変換
            self._posts = {post['id']: BlogPost(**post) for post in data['posts']}
            self._next_id = data['next_id']
            self._tag_index = defaultdict(set, data['tag_index'])

            print(f"記事を {filename} から読み込みました。")
        except FileNotFoundError:
            print(f"エラー: {filename} が見つかりません。")
        except json.JSONDecodeError:
            print(f"エラー: {filename} のフォーマットが正しくありません。")


# dataclassはクラスの外で定義するのが一般的です
@dataclass(frozen=True) # frozen=Trueにすると、作成後に内容を変更できなくなり、より安全になります
class BlogPost:
    id: int
    title: str
    content: str
    tags: set[str]

def main():
    """メインの実行ループ"""
    system = BlogSystem()
    print("ミニブログへようこそ！ (コマンド: post, list, view <ID>, search <tag>, save, load, quit)")
    
    while True:
        try:
            raw_input = input("> ").strip().split(maxsplit=1)
            if not raw_input:
                continue

            command = raw_input[0].lower()
            args = raw_input[1] if len(raw_input) > 1 else ""

            if command == "post":
                title = input("   title: ")
                content = input(" content: ")
                tags_str = input("    tags (カンマ区切り): ")
                tags = [tag.strip() for tag in tags_str.split(',')]
                system.post(title, content, tags)
            
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
                # ここでファイルに保存する処理を実装します
                system.save("blog_data.json")
                pass
            
            elif command == "load":
                # ここでファイルから読み込む処理を実装します
                system.load("blog_data.json")
                pass

            elif command == "quit":
                print("プログラムを終了します。")
                break
            
            else:
                print(f"エラー: '{command}' は不明なコマンドです。")
        
        except (ValueError, IndexError) as e:
            print(f"入力エラーが発生しました: {e}")
        except KeyboardInterrupt:
            # Ctrl+Cが押されたときに綺麗に終了する
            print("\nプログラムを終了します。")
            sys.exit()

if __name__ == '__main__':
    main()