from MALReader import scrape
from MALReader import MALSeason
from ServerController import sendToDBService
from etc import environment

import LogUtils

import logging
import time

SLEEP_TIME = environment.WAIT_TIME
NUM_OF_PAST_SEASONS = environment.NUM_OF_PAST_SEASONS
NUM_OF_FUTURE_SEASONS = environment.NUM_OF_FUTURE_SEASONS


def main():
    current_season_url = "https://myanimelist.net/anime/season"

    logging.info("Beginning script")
    try:
        while True:
            LogUtils.updateLogFile()
            logging.info("Scraping current season")
            anime_list = scrape(current_season_url)  # Will pass the anime list to another function
            # (as a background process) that will add the anime to a database

            season_date = MALSeason()
            logging.info("Current season is: " + str(season_date))
            logging.info("Adding season to database")
            sendToDBService(season_date, anime_list)
            logging.info("Season added successfully")

            for i in range(NUM_OF_PAST_SEASONS):
                season_date.decrement()
                logging.info("Scraping for season: " + str(season_date))
                logging.info(season_date.get_url_for_season())
                anime_list = scrape(season_date.get_url_for_season())
                logging.info("Season scraped successfully")
                logging.info("Adding season to database")
                sendToDBService(season_date, anime_list)
                logging.info("Season added successfully")

            for i in range(NUM_OF_PAST_SEASONS):
                season_date.increment()

            for i in range(NUM_OF_FUTURE_SEASONS):
                season_date.increment()

                logging.info("Scraping for season: " + str(season_date))
                logging.info(season_date.get_url_for_season())
                anime_list = scrape(season_date.get_url_for_season())

                logging.info("Season scraped successfully")
                logging.info("Adding season to database")
                sendToDBService(season_date, anime_list)
                logging.info("Season added successfully")

            logging.info("Scraping done. sleeping for " + str(SLEEP_TIME) + " seconds")
            time.sleep(SLEEP_TIME)
            logging.info("About to begin scraping")
    except KeyboardInterrupt:
        logging.error('Manual break by user - stopping process')
        return


main()
