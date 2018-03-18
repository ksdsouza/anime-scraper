from pymongo import MongoClient
import json
import logging
import LogUtils
comparisons = ["title", "numEps", "imgUrl", "release", "synopsis", "genres"]
def connect():
    logging.info("Attempting to connect to mongodb")
    client = MongoClient()
    logging.info("Connection success!")
    db = client.Anime
    logging.info("Working with the Anime collection")
    return db

def areEntriesSame(entry1, entry2):
    for comparison in comparisons:
        if entry1[comparison] != entry2[comparison]:
            return False
    return True

def addToDB(season, anime_list):
    db = connect()
    collection = db[season]

    for anime in anime_list:
        j = json.loads(anime.toJSONString())

        existing_doc = db[season].find_one({"title":anime.title})
        if existing_doc is None:
            logging.info("Inserting new document with title: " + str(anime.title.encode('ascii', 'ignore')))
            collection.insert_one(j)
        elif areEntriesSame(existing_doc, j):
            logging.info("Identical document with title: " + str(anime.title.encode('ascii', 'ignore')))
        else:
            logging.info("Document with title " + str(anime.title.encode('ascii', 'ignore')) + " needs to be updated")
            db[season].replace_one({"title":anime.title}, j)
    logging.info("Successfully imported given season into db")

