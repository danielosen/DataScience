import panda_io
import numpy as np 
import matplotlib.pyplot as plt 


def get_fatality_class(fatality):
	'''given a number of fatalities, return the defined class membership'''
	if fatality < 1:	#no fatalities
		return 0
	elif fatality < 12: #if no values, report mentions, many, several, etc.
		return 1
	elif fatality < 100:#if no values, report mentions dozens
		return 2
	else:				#if no values, report mentions hundreds
		return 3

data = panda_io.csvreader('data_realtime.csv', column_list_of_names = ['YEAR','FATALITIES'])

x = [n in range(2001,2018)]
z = data['FATALITIES'].groupby(data['YEAR'])
plt.plot(x,z,'+')
plt.show()