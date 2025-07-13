three_x=[i for i in range(1,101) if i%3==0]
print(three_x)

names = ["佐藤", "鈴木", "高橋"]
ages = [25, 32, 41]

for name,age in zip(names,ages):
    print(f'{name}さんの年齢は{age}歳です')