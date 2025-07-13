def heap_sort(arr,p=None):
    if p==None:
        p=(len(arr)-2)//2
    if p==0:
        return arr
    if p*2+1<len(arr):
        if arr[p]>arr[p*2+1]:
            arr[p],arr[p*2+1]=arr[(p*2+1)//2],arr[p]
            return heap_sort(arr,p*2)
    if p*2+2<len(arr):
        if arr[p]>arr[p*2+2]:
            arr[p],arr[p*2+2]=arr[p*2+2],arr[p]
            return heap_sort(arr,(p*2+2)//2)

print(heap_sort([1,5,6,8,9,-1,0,4]))