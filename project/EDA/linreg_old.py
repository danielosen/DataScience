from pymongo import MongoClient
from scipy.stats import linregress
import numpy as np
#import matplotlib.pyplot as plt
import requests
import pandas
import datetime
import time
import io
import sys


#### ACLED DATASET CLASS ###

def acled_get_match_aggdata_local(dataset,match_field,match_key,agg_field,dtype,lat_range = None,long_range = None):
	'''Returns two numpy arrays, one containing agg_field counts, the other of agg_field type dtype.
	These containing aggregate data from the acled database collection restricted to fields matching match_key,
	and summed over identical instances of agg_key. If no lat,long coords given, considers all of africa,
	otherwise everything inside the lat-long box specified by ranges.

	to-do: fix event_type grammatical bugs''' 

	if lat_range and long_range:
		pipeline = [{"$match": {match_field : match_key}}, 
					{"$match": {'latitude': {'$gte' : lat_range[0]}}},
					{"$match": {'longitude': {'$gte': long_range[0]}}},
					{"$match": {'latitude': {'$lte' : lat_range[1]}}},
					{"$match": {'longitude': {'$lte' : long_range[1]}}},
					{"$group": { "_id" : "${}".format(agg_field), "count" : {"$sum": 1}}}
					]
	else:
		pipeline = [{"$match": {match_field : match_key}}, 
					{"$group": { "_id" : "${}".format(agg_field), "count" : {"$sum": 1}}}
					]

	cursor = dataset.aggregate(pipeline)

	agg_column = []

	count_column = []

	for document in cursor:

		agg_column.append(document['_id'])

		count_column.append(document['count'])

	agg_column = np.asarray(agg_column,dtype=dtype)

	count_column = np.asarray(count_column,dtype=np.int64)

	sorted_indices = agg_column.argsort()

	return agg_column[sorted_indices],count_column[sorted_indices]


### WORLDBANK DATASET CLASS




worldbank_country_code_dict = { 'South Africa' : 'ZA', 'Africa' : 'AFR'}
worldbank_indicator_code_dict = {'GDP' : 'NY.GDP.MKTP.CD', 'Maternal Mortality' : 'MMR'}


def test_riot_vs_oda():
	#not correlated 2007-2014
	client = MongoClient()
	dataset = client['acled']['api']
	oda_SA_2007_2014 = np.array([807490000.0,1125180000.0,1074540000.0,1026680000.0,1395360000.0,1065940000.0,1295440000.0,	1070440000.0])
	year,no_events = get_acled_match_agg_local(dataset,'event_type','Riots/Protests','year',np.int64,[-40,-20],[15,35])
	slope,intercept,r_value,p_value,std_err = linregress(oda_SA_2007_2014,no_events[10:18])
	plt.plot(oda_SA_2007_2014,no_events[10:18],'+')
	print("slope = {}, p-value = {}".format(slope,p_value))
	plt.show()

def test_riot_vs_maternal():
	#not correlated 2007-2014
	client = MongoClient()
	dataset = client['acled']['api']
	maternal_SA_2007_2014 = np.array([126,138,148,154,154,152,145,140])
	year,no_events = get_acled_match_agg_local(dataset,'event_type','Riots/Protests','year',np.int64,[-40,-20],[15,35])
	slope,intercept,r_value,p_value,std_err = linregress(maternal_SA_2007_2014,no_events[10:18])
	plt.plot(maternal_SA_2007_2014,no_events[10:18],'+')
	print("slope = {}, p-value = {}".format(slope,p_value))
	plt.show()

if __name__ == '__main__':
	#test_riot_vs_oda()
	#test_riot_vs_maternal()
	worldbank_get_indicator_data('ZA',2,1997,2017)
