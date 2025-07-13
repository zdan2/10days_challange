def calc(arr):
    def sum_arr(arr,i=0):
        if i==len(arr):
            return 0
        return arr[i]+sum_arr(arr,i+1)
    def ave_arr(arr):
        return sum_arr(arr)/len(arr)
    def max_arr(arr,i=0,m=-float('inf')):
        if i==len(arr):
            return m
        return max_arr(arr,i+1,max(m,arr[i]))
    return sum_arr(arr),ave_arr(arr),max_arr(arr)

print(calc([1,2,3,4,5,4,3,2]))
            
def sum_all(*args):
    return sum(args)

print(sum_all(1,2,3,4,5))