"""
$ python3 datasets_example.py
Database 'acled' does not exist or is empty.
Grab it from ACLED server (Y/N)? y
Warning! Query ACLED server for all data newer than date 1995-01-01 could cause heavy load on the server.
Continue (Y/N)? y
2017-03-03 13:41:29.898922 Query API ............................................................................................................................................................................................................................................................................................................................
2017-03-03 14:00:27.018707 312 pages retrieved from ACLED API.
2017-03-03 14:00:27.018821 Make DataFrame...
2017-03-03 14:00:28.082986 Apply str->datetime on event_date...
155990 records inserted, 158446 lines in csv. (Why a diffrence?)
2017-03-03 14:00:41.150627 Done.
Newest event_date in mongodb is 2017-02-25 00:00:00
    event_date   location  fatalities                     event_type
654 2017-02-08     Owachi          98  Battle-No change of territory
522 2017-02-10      Dikwa          37  Battle-No change of territory
794 2017-02-04     Ombasi          32  Battle-No change of territory
536 2017-02-10  Tshimbulu          30  Battle-No change of territory
581 2017-02-09  Tshimbulu          30  Battle-No change of territory
...
"""

import pandas
import datetime
import numpy

# Adding relative directory (to be updated again once 'datasets' module is moved)
import sys
sys.path.insert(0, '../')
import modules.datasets as datasets


acled = datasets.ACLED()
acled.mongodb_update_database()   # will update the database if needed

print("Newest event_date in mongodb is",acled.mongodb_get_newest_event_date())

df = acled.mongodb_get_entire_database()
starttime = datetime.datetime(2017, 2, 1)
endtime = datetime.datetime(2017, 2, 17)
ndf = df[df['event_date'] >= starttime][df['event_date'] <= endtime]
print(ndf[['event_date','location','fatalities','event_type']].sort_values(['fatalities'],ascending=False)[:5])
