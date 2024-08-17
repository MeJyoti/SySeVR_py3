import re
import time
import pickle
import bisect

def linear_search(arr, x):

	for i in range(len(arr)):
	
		if arr[i] == x:
			return i
			
	return -1
	
def binary_search(arr, x):
	low = 0
	high = len(arr) - 1
	mid = 0
	
	while low <= high:
		mid = (high + low) // 2
		
		if arr[mid] < x:
			low = mid + 1
		elif arr[mid] > x:
			high = mid - 1
		else:
			return mid
			
	return -1
	
def binary_search_bisect(arr, x):
	i = bisect.bisect_left(arr, x)
	if i != len(arr) and arr[i] == x:
		return i
	else:
		return -1
	
if __name__ == '__main__':

	file = open('./sensitive_func.pkl', 'rb')
	sensitive_func_list = pickle.load(file)
	file.close()
	
	fin = open("sensitive_func.pkl", 'rb')
	list_sensitive_funcname = pickle.load(fin)
	fin.close()
	
	list_sensitive_funcname.sort()
	
	f = open("sensitive_func_sorted.pkl", 'wb')
	pickle.dump(list_sensitive_funcname, f, True)
	f.close()
	
	fin = open("sensitive_func_sorted.pkl", 'rb')
	list_sensitive_funcname = pickle.load(fin)
	fin.close()
	
	print(list_sensitive_funcname)
	
	begin = time.time()
	sensitive_func_list.sort()
	end = time.time()
	print(f"Total runtime for sorting list: {end - begin}")
	
	ele = 'main'
	
	begin = time.time()
	index = linear_search(sensitive_func_list, ele)
	end = time.time()
	print(f"Total runtime for linear search: {end - begin} \n Index: {index}")
	'''
	begin = time.time()
	index = re.search(ele, sensitive_func_list)
	end = time.time()
	print(f"Total runtime for linear search using re: {end - begin} \n Index: {index}")
	'''
	begin = time.time()
	index = ele in sensitive_func_list
	end = time.time()
	print(f"Total runtime for ele in list: {end - begin} \n Index: {index}")
	'''
	begin = time.time()
	index = sensitive_func_list.find(ele)
	end = time.time()
	print(f"Total runtime for find ele in list: {end - begin} \n Index: {index}")
	'''
	begin = time.time()
	index = binary_search(sensitive_func_list, ele)
	end = time.time()
	print(f"Total runtime for binary search: {end - begin} \n Index: {index}")
	
	begin = time.time()
	index = binary_search_bisect(sensitive_func_list, ele)
	end = time.time()
	print(f"Total runtime for binary search bisect: {end - begin} \n Index: {index}")
