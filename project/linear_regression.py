from pymongo import MongoClient
from scipy.stats import linregress
import numpy as np
import matplotlib.pyplot as plt

world_bank_url = 'databank.worldbank.org/data/reports.aspx?source=2&series=DT.ODA.ALLD.CD&country='

def get_acled_match_agg(dataset,match_field,match_key,agg_field,dtype):
	'''Returns two numpy arrays, one containing agg_field counts, the other of agg_field type dtype.
	These containing aggregate data from a MongoDB database collection restricted to fields matching match_key,
	and summed over identical instances of agg_key.''' 

	pipeline = [ {"$match": {match_field : match_key}}, 
				{"$group": { "_id" : "${}".format(agg_field), "count" : {"$sum": 1}}}
				]

	cursor = dataset.aggregate(pipeline)

	agg_column = []

	count_column = []

	for document in cursor:

		agg_column.append(document['_id'])

		count_column.append(document['count'])

	agg_column = np.asarray(agg_column,dtype=dtype)

	sorted_indices = agg_column.argsort()

	count_column = np.asarray(count_column,dtype=np.int64)

	return agg_column[sorted_indices],count_column[sorted_indices]

def test_riot_vs_time():
	client = MongoClient()
	dataset = client['acled']['api']
	year,no_events = get_acled_match_agg(dataset,'event_type','Riots/Protests','year',np.int64)
	slope,intercept,r_value,p_value,std_err = linregress(year[0:-1],no_events[0:-1])
	plt.plot(year[0:-1],no_events[0:-1])
	print("slope = {}, p-value = {}".format(slope,p_value))
	plt.show()

if __name__ == '__main__':
	test_riot_vs_time()
