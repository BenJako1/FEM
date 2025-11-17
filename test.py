import numpy as np

arr = np.array([1,2,3,4,5])

def modArr(array):
    array[0] += 1

modArr(arr)

print(arr)