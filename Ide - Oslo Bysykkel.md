# # Business proposal - Oslo city bike statistics

## Background (from webpage)
"The city bike system in Oslo is a collaboration between the Municipality of Oslo and Clear Channel Norway AS, where the municipality makes public advertising space available and gets a city bike service in return. Urban Infrastructure Partner AS owns and operates the city bikes in Oslo"

## Optimizing the service

### Popularity
Ensuring the popularity of the city bikes by delivering a good service is important to:

* Growing popularity of service 
  * Maintain agreement between Oslo Municipality
  * Membership income 


Ensuring that the users of the city bikes are happy increases the likelyhood that Clear Channel will be allowed to continue their contract. Further, extensive usage of the city bikes also makes the advertising space on the bikes more attractive to companies.


### Circulation of commercials
For companies considering to buy advertising space on the city bikes, the pattern of usage of the bikes is also relevant.

In particular, a bike ride outside the city centre is likely to have less audience (for the adds), arguably resulting in a lower return of investment than if the bike ride was in the middle of the city.

Documenting "statistical circulation" of bikes could therefore add extra value.

**Alternatively**, customers buying adds could be segmented and adds on bikes in less rural areas could be cheaper... (this would require smarter redistribution of bikes, as some would leak from "Ring 1 to Ring 3)


### Logistics
What is the main question of an end user of the city bike system?

  **Is there an available bike nearby and free parking where I am heading?**
  
For Urban Infrastructure Partner AS, this means that the main challenge is to continuously work towards a "Yes" on both questions above...

... while at the same time not investing in unessesary infrastructure (e.g., too many employees at work or cars to move bikes).


### Delingsøkonomi: "Bike movers" as a service
* A weird, but not impossible scheme would be to give users incentives to use the bike from areas with high bike influx, distributing the bikes... :P
* Think "delingsøkonomi": people without a paid membership (but with ID) can use bikes to help restribution...

### Possible service improvements (not part of this project) 
* Voluntary fields in users profile:
  * Preferred seat height: The bike selected for you based on setting of the previous user

## Development ideas:

### Data base:

Write functions to:

* Get "Oslo Bysykkel" JSON raw data (uploaded per month)
* Import and preprocess
* Add other data sources (different collections, see below):
    * Station location
      * Adding in altitude from google
    * Weather data

Save the above to MongoDB database

### Calculations/statistics
* Net flow of bicicles (function of time and stop)
* Average ride (velocity and length)
  * Length: Integrate google maps path planning API for distance?
* Height trends
  * How much do users prefer a downhill ride?

* Given bike taken from station X, where is it most likely to go?

### Visualization
* A lot of visual things could be done...
  * Inspiration: http://hubwaydatachallenge.org/
  * As long as we credit the authors, I believe it is legit to take inspiration from these...


### Data gathering:
* Use live Oslo Bysykkel API:
  * Predictions on when rack will be empty
    * Usings models from above that we create using historic data (from MongoDB)
  * "Simulate" planning instructions sent to trucks


### Integrate information from other data sources:
* Get elevation of stop from google
  * E.g.: http://stackoverflow.com/questions/21104592/json-to-pandas-dataframe
* Integrate map
* Add environmental data layer
  * Does the below impact usage?
  * Weather data (yr.no or other)
  * Polution/air quality data
  
### Testing packages
* Test module for all functions (as lectured)
* Several interesting tests:
  * APIs (google, bysykkel)
    * Verification of communication with APIs
    * Verification of function

  
