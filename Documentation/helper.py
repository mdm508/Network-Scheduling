###########################################
#			helper.py	
#  This file contains functions useful
# to the main function and the 
# simulate method in hw1.py
#
# It defines the constants
# used in this file,
# hw1.py and System.py
# 
# It imports useul library function
# used through the files afformentioned
###########################################

# Standard library imports
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from math import floor,ceil
from random import randint,gauss
from numpy import arange

'''
Constant Definitions
UNIT_NUM: A list that tells for each simulation
		  how many units a network should have 

MAX_CYCLES: cycles is the most number of cycles
            to do before aborting the simulation

MIN_CYCLES: min number of cycles before
  			ending simulation

STOPVAL:is the constant that tells simulation
		when to stop the simulation. It does so
		when the previous average and current 
		average differ by <= STOPVAL 

C:    is a value to help calculate the 
	  standard deviation when
	  generating random module requests
	  according to a normal distrib
'''
UNIT_NUM = [2,4,8,16,32,64]
MODULES = 2048 
MAX_CYCLES = 10**8
MIN_CYCLES = 100
STOP_VAL = .002
C  = 6

'''
M: number of slots 
choice: a string representing
		representing the userts choice
		of which random function to sue

The purpose of this function is to 
choose the random function that will be 
used during a simulation based on the 
users choice. The purpose of this function
is to moduralize so that 
two different simulations for the 
different distributions dont need to be
written. this function returns
a) function to be used
b) its arguments
'''
def choose_random_function(M:int, choice:str):
	if choice == 'G':
		# Use normal distribution to 
		# generate memory requests
		# guass(mu,sigma) returns random number
		# with mean mu and standar dev sigma
		# note that the mean is randomly chosen
		arg1 = randint(0, M-1)
		arg2 = ceil(M / C)
		return gauss,arg1,arg2
	if choice == 'U':
		# Use a uniform distribution
		# randint(a,b) returns random int in range
		# [a,b]
		arg1 = 0
		arg2 = M-1
		return randint,arg1,arg2
	else:
		raise ValueError

'''
num: a randomly generated number
	 from gauss or independent distrib

M: is the number of slots

This function transforms
a randomly generated number so that
the following conditions hold
a) num is positive
b) num is an integer
c) 0 <= num < M

Note that if num was generated
from a uniform distribution this
the transformatino has no effect
'''
def transform(num:float,M:int):
	#x = abs(floor(num))
	x = floor(num)
	if x >= M or x < 0: return x % M
	return x

'''
Returns true if it is time
to end the simulation

r:    is number of requests
old   the old average
cur   the current averag
'''
def end_sim(r:int,old:float,cur:float):
	return (r > MIN_CYCLES) and \
		   (abs(cur - old) <= STOP_VAL)
	
'''
Super imposes the plots of the 
averages for each each network
and generates a png file.

avg_list: a list of averages. avg_list[i]
		  is the average access time 
		  of the ith simulation

x_axis: is a list of values from 1..M
		where M=2048. x_axis is same
		regardles of how many units used
		thus we treat it like a constant

title: is the title of the plot
'''
def plot(avg_list,x_axis,title:str):
	for L in avg_list:
		plt.plot(x_axis,L[1:])
	plt.title(title)
	plt.xlabel("# of Memory Modules")
	plt.ylabel("Avg access time")
	plt.legend(title="# of units")
	plt.savefig(title + '.png')
	plt.show()