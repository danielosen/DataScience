#python .csv reader
import pandas as pd 
import numpy as np 

def csvreader(filename, delimiter=',', column_list_of_names = None):
	return pd.read_csv(filename, delimiter=delimiter, header='infer', usecols=column_list_of_names)



