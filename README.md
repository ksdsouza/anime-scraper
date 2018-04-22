# What is this
A Python microservice designed to to scrape myanimelist.net for recent seasons of anime.<br>

## Dependencies:
* python3
* BeautifulSoup4
* pymongo

## Storage
*(Will soon be migrated to another microservice)*<br>
Scraped data is stored to MongoDB at localhost:27017 under database Anime. Each season will be stored in
the database in their own collection in the form "`SEASON YEAR`" (ex. `Winter 2018`). A season collection contains Anime objects.<br>
An Anime object is internally represented as:
```
{
    "title":"STRING",
    "numEps":"STRING",
    "imgURL":"STRING",
    "release":"String",
    "synopsis":"String",
    "genres":["String"]
}
``` 

## How to run
run the MALController.py file<br>
`python3 MALController.py`

