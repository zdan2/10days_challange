class Book:
    def __init__(self,title,author):
        self.title=title
        self.author=author
    
    def info(self):
        return f'『{self.title}』by {self.author}'

b1=Book('Hello World','DJ')
b2=Book('Pyhon','Conda')

print(b1.info())
print(b2.info())