from collections import Counter
import timeit


class NumberStats():
    '''
    This class is used to calculate the statistics of a list of numbers.
    It has the following methods:
    - get_size()
    - get_mean()
    - get_median()
    - get_mode()
    - get_variance()
    - get_standard_deviation()
    - __repr__()
    - __str__()
    '''

    def __init__(self,*args):
        if len(args)==0:
            raise ValueError("No numbers provided")
        else:
            self.numbers=list(args)
        
        self.stats=self.numbers.sort()
    
    def get_size(self):
        return len(self.numbers)
    
    def get_mean(self):
        return sum(self.numbers)/len(self.numbers)
    
    def get_median(self):
        self.numbers.sort()
        if len(self.numbers)%2==0:
            return (self.numbers[len(self.numbers)//2]+self.numbers[len(self.numbers)//2-1])/2
        else:
            return self.numbers[len(self.numbers)//2]
    
    def get_mode(self):
        return Counter(self.numbers).most_common()
    
    def get_variance(self):
        mean=self.get_mean()
        return sum([(x-mean)**2 for x in self.numbers])/len(self.numbers)
    
    def __repr__(self):
        return f"Size: {self.get_size()}\nMean: {self.get_mean()}\nMedian: {self.get_median()}\nMode: {self.get_mode()}\nVariance: {self.get_variance()}"
    
    def __str__(self):
        return f"Size: {self.get_size()}\nMean: {self.get_mean()}\nMedian: {self.get_median()}\nMode: {self.get_mode()}\nVariance: {self.get_variance()}"
    
s=NumberStats(1,2,3,4,5,6,7,8,9,10,1,1,1,1,10,10,10,10,10,10)
print(s)
print(timeit.timeit('s',number=1000000,globals=globals()))