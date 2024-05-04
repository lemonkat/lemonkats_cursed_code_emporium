"""
A while back, someone at my school put out a mini-contest
to find the worst possible way to solve the following problem:

you are given a number, an integer between 1 and 8 inclusive.
If the number is over 4, return 1, otherwise, return 0.

Many of the solutions apply extra hard-to-read code just for fun.
"""

import sys
import inspect
import random
import os
import time

# set the recursion limit to 6 + what it currently is.
# then, call a recursive function num times.
# if the thing hits the recursion limit, return -1, else, return 1.

def over4_v1(num):
	old_reclim = sys.getrecursionlimit()
	current_depth = 6 + len(inspect.stack(0))
	def over4_v4_helper(num):
		x = 0 if num == 0 else over4_v4_helper(num - 1)
	sys.setrecursionlimit(current_depth)
	try:
		over4_v4_helper(num)
		sys.setrecursionlimit(old_reclim)
		return -1
	except:
		sys.setrecursionlimit(old_reclim)
		return 1

# dump num into a list of things, bogo sort the list, and determine where the thing is
def over4_v2(num):
	lst = "1a,2a,3a,4a,5a,6a,7a,8a".split(",")
	lst.append(str(num))
	check = True
	while check: #bogo sort
		random.shuffle(lst)
		[(check := check and lst[i] < lst[i + 1]) for i in range(len(lst) - 1)]
	return -1 if lst[0] == str(num) or lst[1] == str(num) or lst[2] == str(num) or lst[3] == str(num) else 1

# big pile of eval and .join turns the thing into a horrible mess
def over4_v3(num):
	return eval("'".join(['eval(" ".join([', '-1', ', ', 'if', ', ', 'str(num)', ', ', 'in', ', ', '["1",', ', ', '"2",', ', ', '"3",', ', ', '"4"]', ', ', 'else', ', ', '1', ']))']))

# write to a1.py through a4.py, then try to import for a{num}.py
def over4_v4(num):
	for i in range(1, 5):
		os.system(f"echo x=5 > a{i}.py")
	try:
		exec("from a" + str(num) + " import *")
		return -1
	except:
		return 1

# generate random numbers between 1 and 8, check how many fall above or below
def over4_v5(num):
	lows = 0
	highs = 0
	for i in range(100000):
		x = (highs := highs + 1) if  1 + (random.random() * 7) > num else (lows := lows + 1)
	return 1 if lows > highs else -1

# wait num seconds. wait 4.5 seconds. determine which took longer.
def over4_v6(num):
	t0 = time.time()
	time.sleep(num)
	t1 = time.time()
	time.sleep(4.5)
	t2 = time.time()
	return [-1, 1][t1 - t0 < t2 - t1]