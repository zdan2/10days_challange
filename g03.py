from dataclasses import dataclass, field
from itertools import count
from threading import Lock
from collections import defaultdict

_counter = count(1)
_lock = Lock()

def _auto_id():
    with _lock:
        return next(_counter)
@dataclass
class BlogPost:
    title: str
    content: str
    tags: set[str]
    id: int = field(default_factory=_auto_id)
        
Blogs=[]
tags=defaultdict(list)
def blog_post_input():
    title=input("title:")
    content=input("content:")
    tags=input("tags:")
    tags=set(tags.split())
    blog_post = BlogPost(title, content, tags)
    Blogs.append(blog_post)
    for tag in tags:
        tags[tag].append(blog_post.id)

def search():
    print("1:title 2:content 3:tag" )
    command=input("command:")
    if command=="1":
        title=input("title:")
        for blog_post in Blogs:
            if blog_post.title==title:
                print(blog_post)
    elif command=="2":
        content=input("content:")
        for blog_post in Blogs:
            if blog_post.content==content:
                print(blog_post)
    elif command=="3":
        tag=input("tag:")
        for blog_post in Blogs:
            if tag in blog_post.tags:
                print(blog_post)
                
def main():
    print("1:input 2:search 3:exit")
    while True:
        command=input("command:")
        if command=="1":
            blog_post_input()
        elif command=="2":
            search()
        elif command=="3":
            break
if __name__ == '__main__':
    main()