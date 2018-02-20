from MALReader import scrape
from MALReader import MALSeason
import time
import threading
ONE_HOUR = 3600
NUM_OF_PAST_SEASONS = 2
NUM_OF_FUTURE_SEASONS = 2
def main():
    current_season_url = "https://myanimelist.net/anime/season"
    try:
        while True:
            anime_list = scrape(current_season_url) # Will pass the anime list to another function 
                                                    # (as a background process) that will add the anime to a database

            season_date = MALSeason()  
            time.sleep(5)

            for i in range(NUM_OF_PAST_SEASONS):
                season_date.decrement()
                print("Scraping for season: " + str(season_date))
                anime_list = scrape(season_date.get_url_for_season())

            for i in range(NUM_OF_PAST_SEASONS):
                season_date.increment()

            for i in range(NUM_OF_FUTURE_SEASONS):
                season_date.increment()
                print("Scraping for season: " + str(season_date))
                anime_list = scrape(season_date.get_url_for_season())

            print("Scraping done. sleeping for " + str(ONE_HOUR) + " seconds")
            time.sleep(ONE_HOUR)
    except KeyboardInterrupt:
        print('Manual break by user')
        return

            
main()
