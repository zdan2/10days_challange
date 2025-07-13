import os
file_name='web2.py'
path='d:/Python/web_scraping'
try:
    file_path=path+'/'+file_name
    print(file_path)
    print(list(os.listdir(path)))
    print(os.getcwd())
    if file_name not in os.listdir(path):
        raise FileNotFoundError
    with open(file_path) as f:
        lines=f.readlines()
    
    for line in lines:
        print(line)
except FileNotFoundError:
    print('ファイルがありません')
    

try:
    n=float(input())
    print(100/n)
except ValueError:
    print('数値以外が入力されました')
except ZeroDivisionError:
    print('0では割れません')
    
    