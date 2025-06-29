def selection_sort(arr):
    for i in range(len(arr)):
        min_idx=i
        for j in range(i+1,len(arr)):
            if arr[min_idx]>arr[j]:
                min_idx=j
                arr[i],arr[min_idx]=arr[min_idx],arr[i]
    return arr

def quick_sort(arr):
    if len(arr)<=1:
        return arr
    pivot=arr[0]
    left=[x for x in arr[1:] if x<=pivot]
    right=[x for x in arr[1:] if x>pivot]
    return quick_sort(left)+[pivot]+quick_sort(right)

'''
>>> selection_sort([3, 1, 4])
[1, 3, 4]
>>> quick_sort([3, 1, 4])
[1, 3, 4]
>>> quick_sort([3,5,6,7,8,1,2,9])
[1, 2, 3, 5, 6, 7, 8, 9]
'''
print(selection_sort([3,1,4]))           
print(quick_sort([3,1,4]))          