from pymongo import MongoClient
import json

comparisons = ["title", "numEps", "imgUrl", "release", "synopsis", "genres"]
def connect():
    client = MongoClient()
    db = client.Anime
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
            print("Inserting new document with title: " + anime.title)
            collection.insert_one(j)
        elif areEntriesSame(existing_doc, j):
            print("Identical document with title: " + anime.title)
        else:
            print("Document with title " + anime.title + " needs to be updated")
            db[season].replace_one({"title":anime.title}, j)

