Melding til gruppa: 

1. Sorry hvis dette skulle vært lagret på en annen måte i denne mappa, og jeg ødelegger noe:
jeg er fullstendig noob og jeg vil ikke ringe og forstyrre Torgeir på utdrikningslaget hans :p

2. Deler av dette er bare en kjapp-kjapp oversettelse av Daniel's ide1.md fra Feb6th

----------------------------------------------------------------------------------------------------------------------------------------
DRAFT FOR EMAIL BASE:

**Group members:**
* Børge S. Andreassen
* Daniel Osen
* Øivind ???!!!
* Marie Lilleborge

**What:**
Applying data science techniques and algorithms to extract useful information from the ACLED (Armed Conflict Location and Event Data Project) dataset. The ACLED dataset contains approximately 150.000 instances of political violence and protests in Africa. Note that the dataset also contains instances in other countries, however we only use the data from Africa. 

We will also enhance the ACLED dataset with other datasources for our models.

utilize data from other sources together with the ACLED data and both ... and visualize the results.

Use time/place with type of violence, group, type of conflict with the probability that a given group will initialize a protest/violence based on other data.

**Customer:**
Companies involved in aid, trade in developing countries, government decision making. May be revised as the project matures.

**Data sets:**
* Armed Conflict Location and Event Data project [http://www.acleddata.com/data/conflict-by-type-and-actor/] (weekly loaded realtime data 2017)
* Datasets from: www.gapminder.org/data
* GIS data: http://www.naturalearthdata.com/


Packages/data structures/database applied:
* MongoDB 
  * Database containing collections of all data sources 
  * Functionality to upload live data
  
-loads weekly updates from acled webpage
* Bokeh - have started visualization tasks
* Linear regression model: Total number of events (of type X) regressed on year, amount of charity funds received, number of child births per woman, education level, etc


----------------------------------------------------------------------------------------------------------------
PLANS/IDEAS etc:
* Simple ToDos:

* Ongoing work:

* Long term ideas not initialized:

  * SVM classifier ?
  
  * Clustering ?

