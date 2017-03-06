from pymongo import MongoClient
from scipy.stats import linregress
import numpy as np
import matplotlib.pyplot as plt

world_bank_url = 'databank.worldbank.org/data/reports.aspx?source=2&series=DT.ODA.ALLD.CD&country='

oda_SA_2007_2014 = np.array([807490000.0,1125180000.0,1074540000.0,1026680000.0,1395360000.0,1065940000.0,1295440000.0,	1070440000.0])

def get_acled_match_agg_local(dataset,match_field,match_key,agg_field,dtype,lat_range = None,long_range = None):
	'''Returns two numpy arrays, one containing agg_field counts, the other of agg_field type dtype.
	These containing aggregate data from the acled database collection restricted to fields matching match_key,
	and summed over identical instances of agg_key. If no lat,long coords given, considers all of africa

	to-do: fix event_type grammatical bugs''' 

	if lat_range and long_range:
		pipeline = [{"$match": {match_field : match_key}}, 
					{"$group": { "_id" : "${}".format(agg_field), "count" : {"$sum": 1}}},
					{"$match": {'latitude': $gte : lat_range[0]}},
					{"$match": {'latitude': $lte : lat_range[1]}},
					{"$match": {'longitude': $gte : long_range[0]}},
					{"$match": {'longitude': $lte : long_range[1]}},
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

def test_riot_vs_time():
	client = MongoClient()
	dataset = client['acled']['api']
	year,no_events = get_acled_match_agg_local(dataset,'event_type','Riots/Protests','year',np.int64)
	slope,intercept,r_value,p_value,std_err = linregress(year[0:-1],no_events[0:-1])
	plt.plot(year[0:-1],no_events[0:-1])
	print("slope = {}, p-value = {}".format(slope,p_value))
	assert(p_value <= 0.05)
	plt.show()

if __name__ == '__main__':
	test_riot_vs_time()
