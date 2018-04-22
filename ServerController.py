from pymongo import MongoClient
import json
import logging
import requests
import LogUtils
comparisons = ["title", "numEps", "imgUrl", "release", "synopsis", "genres"]

def 

def sendToDBService(season_date, anime_list):
    animeL = []
    for anime in anime_list:
        animeL.append(json.loads(anime.toJSONString()))
    payload = json.dumps({"anime":animeL, "season":season_date.get_season(), "year":season_date.get_year()})
    logging.info("Sending data to Tohru...")
    logging.info("Using payload: " + payload)
    r = requests.put("http://localhost:8085/services/tohru/insert", payload)
    logging.info("Tohru returned with status code: " + r.status_code)

