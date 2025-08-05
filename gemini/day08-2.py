import requests
url='https://jsonplaceholder.typicode.com/posts/1'

res=requests.get(url)
data=res.json()
print('title:',data['title'])
print('body:',data['body'])