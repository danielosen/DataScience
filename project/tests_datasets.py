"""
STK-INF4000 ML-project dataset tests module.
"""
import datasets

def test_mongodb_get_matching_aggdata_local():
	'''tests that correct count is obtained when using regular expressions in mongodb pipeline'''
	import re
	ds = datasets.ACLED()
	aggs, counts = ds.mongodb_get_matching_aggdata_local(column_name= 'event_type', column_key = "strAteGic deVelopment", agg_name = 'year')
	total_count = sum(counts)
	pipeline = [{ "$group" : { "_id" : "$event_type", "count" : {"$sum" : 1 } } } ]
	target = re.compile('strAteGic deVelopment',re.IGNORECASE)
	for document in ds.c.aggregate(pipeline):
		if target.match(document['_id']):
			total_count -= document['count']
	assert(total_count == 0)


if __name__ == '__main__':
	test_mongodb_get_matching_aggdata_local()