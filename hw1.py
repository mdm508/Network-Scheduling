# Author: Matthew McLaughlin
# email:  matthedm@uci.edu
# id:	  34026707

###########################################
#			hw1.py	
# this file contains the main function
# as well as the simulate function
###########################################
'''
NOTES TO THE GRADER
*I will provide information about 
functions, classes, constants, etc
in comments above the actual implementation
above the implementation of said objects.
I prefer this format for documenting my code.

*If this code doesn't make sense I reccomend
reading through System.py 
'''
# User defined Modules
# these statements import
# everything both libraries
from helper import *
from system import *

'''
N: Number of units to use
M: Number of slots to use
Returns the avg access time for
a network with N units and M slots 

'choose_random_function' will store in f
a function that generates random numbers
according to either a guassian or uniform
distribution depending on the value of
the string 'choice'. I did this so that
I didnt need to write the simulate function
twice. 

transform ensures that the randomly chosen
index is within the indices of the
module list
'''
def simulate(N,M,choice:str):
	f,arg1,arg2 = choose_random_function(M,choice)
	Net = Network(N,M)
	old_avg = float('-inf')
	cur_avg = float('inf') 
	for counter in range(MAX_CYCLES):
		# Generate requests for each unit in network
		for unit in Net.UnitList:
			# CASE1: Unit was waiting
			if unit.is_waiting():
				i = unit.module_index
				# if memory slot is free
				if Net.Module.is_free(i):
					unit.reset_wait_time()
					unit.free_unit()
					Net.Module.occupy(i)
				else: # memory slot wasnt free
					unit.increment_wait_time()
					Net.increment_total_wait()
			# CASE2: Unit was not waiting
			else:
				# randomly map a unit to a slot 
				i = transform(f(arg1,arg2), M)
				if Net.Module.is_free(i):
					Net.Module.occupy(i)
				else:
					unit.bind_unit(i)
					unit.increment_wait_time()
					Net.increment_total_wait()
		#END OF CYCLE UPDATES
		Net.update_total_requests()
		Net.UnitList.update_priority()
		Net.Module.free_slots()		
		## Decide if it is time to end
		## the simulation
		old_avg = cur_avg
		cur_avg = Net.average_access_time()
		if end_sim(Net.total_requests,old_avg,cur_avg):
			return cur_avg
	#### Program only reaches here, if maxcycles reached
	return cur_avg

'''
Runs the simulation, gathers the averages,
then plots them. Note that two simulations
are performed, for varying sizes
of proccessors and memory modules.

Two simulations are performed. To map
units to slots, two different distributions
are used
'U' uniform distribution
'G' guassian distribution
'''
def main():
	uni = list() 
	gau	= list() 
	# run simulations with networks
	# varying the number of units
	# and the number of modules
	for num in UNIT_NUM:
		uni_avgs = [num] 
		gau_avgs = [num] 
		for i in range(1,MODULES + 1):
			uni_avgs.append(simulate(num, i, 'U'))
			gau_avgs.append(simulate(num, i, 'G'))
		uni.append(uni_avgs)
		gau.append(gau_avgs)
	# Plot the results of the simulations
	x_axis = [i for i in range(1,MODULES+1)]
	plot(uni,x_axis,'Uniform Distribution')
	plot(gau,x_axis, 'Gauss Distribution')

main()
