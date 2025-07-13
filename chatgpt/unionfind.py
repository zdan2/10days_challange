class Unionfind:
    def __init__(self,n):
        self.parents=[i for i in range(n)]
    
    
    def merge(self,a,b):
        if self.parents[a]!=self.parents[b]:
            r=self.find(self.parents[a])
            l=self.find(self.parents[b])
            self.parents[l]=r
            
        
        
    def find(self,a):
        if self.parents[a]==a:
            return a
        self.parents[a]=self.find(self.parents[a])
        return self.parents[a]
    
      
uf=Unionfind(6)
uf.merge(1,2)
uf.merge(3,4)
print(uf.find(1),uf.find(2),uf.find(3),uf.find(4))