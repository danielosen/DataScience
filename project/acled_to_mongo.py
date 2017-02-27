# This program will query the entire ACLED dataset from API
# and insert it into MongoDB collection 'acled.api' 

# Example:
# $ python3 acled_to_mongo.py 
# 2017-02-26 21:03:08.227662 Query API ............................................................................................................................................................................................................................................................................................................................
# 2017-02-26 21:14:25.329391 312 pages retrieved from ACLED API.
# 2017-02-26 21:14:25.401224 Make DataFrame...
# 2017-02-26 21:14:26.340036 Apply datetime...
# 2017-02-26 21:14:27.345876 2017-02-18 00:00:00 <class 'pandas.tslib.Timestamp'>
# 2017-02-26 21:14:27.349225 Done.


import requests
import pandas
import numpy
import datetime
import time
import io
import sys
from pymongo import MongoClient


acled_column_dtypes = {
    'data_id'           : numpy.int64,
    'gwno'              : numpy.int64,
    'event_id_cnty'     : str,
    'event_id_no_cnty'  : str,
    'event_date'        : str,              # datetime.datetime
    'year'              : numpy.int64,
    'time_precision'    : numpy.int64,
    'event_type'        : str,
    'actor1'            : str,
    'ally_actor_1'      : str,
    'inter1'            : numpy.int64,
    'actor2'            : str,
    'ally_actor_2'      : str,
    'inter2'            : numpy.int64,
    'interaction'       : numpy.int64,
    'country'           : str,
    'admin1'            : str,
    'admin2'            : str,
    'admin3'            : str,
    'location'          : str,
    'latitude'          : numpy.float64,
    'longitude'         : numpy.float64,
    'geo_precision'     : numpy.int64,
    'source'            : str,
    'notes'             : str,
    'fatalities'        : numpy.int64,
}


URL_ACLED_READ = 'http://acleddata.com/api/acled/read.csv'


def acled_api_request(query):
    """
    Query the ACLED API server by a HTTP GET request.
    """
    r = requests.get(URL_ACLED_READ + query)
    assert (r.status_code == 200)
    return r.text


def acled_api_page_flipper(query):
    """
    The ACLED server prefers returning data in pages, each page with about
    500 lines. This function will iteratively request all the pages for the
    quven query, collating a singular response.
    """

    page = 1
    data = None

    # ACLED API returns 'No data has been found' at end of data
    while True:
        time.sleep(1)           # don't DoS ACLED server
        print('.',end='')
        sys.stdout.flush()
        result = acled_api_request(query + '&page=%i' % page)
        if result.startswith('No data'): break
        if page == 1:
            data = result
        else:
            data += result.split("\n",1)[1]     # remove csv header
        page += 1

    print(datetime.datetime.now(), "%i pages retrieved from ACLED API." % (page-1))
    return data 


def get_acled_data_newer_than_date(date):
    """
    Will ask the ACLED API for data newer than given date.
    Date format (str): YYYY-MM-DD
    """
    query = '?event_date=%s&event_date_where=>' % date
    return acled_api_page_flipper(query)       


def ymd(datestr):
    return datetime.datetime.strptime(datestr,"%Y-%m-%d")


def dump_entire_acled_db_api():
    dump_to_csv = "acled.entire.csv"

    print(datetime.datetime.now(),"Query API ...", end='')
    csvblob = get_acled_data_newer_than_date("1995-01-01")
    open(dump_to_csv,"w").write(csvblob)

    print(datetime.datetime.now(), "Make DataFrame...")
    f = io.StringIO(csvblob)
    df = pandas.read_csv(f, dtype=acled_column_dtypes, engine='c', keep_default_na=False)
    f.close()

    print(datetime.datetime.now(), "Apply datetime...")
    df['event_date'] = df['event_date'].apply(ymd)

    print(datetime.datetime.now(),df['event_date'][0],type(df['event_date'][0]))

    c = MongoClient().acled.api
    c.insert_many(df.to_dict('records'))    

    print(c.count(),"records imported.")    

    #db.testimport.find( { 'year' : 2016 } )


dump_entire_acled_db_api()

print(datetime.datetime.now(), "Done.")
