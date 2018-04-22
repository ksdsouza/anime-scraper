from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import LogUtils
import logging

this_season = 0


class Anime:
    def __init__(self, title, numEps, imgUrl, release, synopsis, genres):
        self.title = title
        self.numEps = numEps
        self.imgUrl = imgUrl
        self.release = release.strip('\n').strip('\r')
        self.synopsis = synopsis
        self.genres = genres
        self.synopsis_to_print = self.synopsis[0:97] + "..." if (len(self.synopsis) > 97) else synopsis

    def __str__(self):
        return "{" + '"title":"' + str(self.title) + '",' + \
               '"numEps":"' + self.numEps + '",' + \
               '"imgUrl":"' + self.imgUrl + '",' + \
               '"release":"' + self.release + '",' + \
               '"synopsis":"' + self.synopsis_to_print + '",' + \
               '"genres":' + str(self.genres).replace('\'', '"') + "}"

    def toJSONString(self):
        return "{" + '"title":"' + str(self.title) + '",' + \
               '"numEps":"' + self.numEps + '",' + \
               '"imgUrl":"' + self.imgUrl + '",' + \
               '"release":"' + self.release + '",' + \
               '"synopsis":"' + self.synopsis + '",' + \
               '"genres":' + str(self.genres).replace('\'', '"') + "}"


class MALSeason:
    @staticmethod
    def __current_season():
        page_soup = loadSoup("https://myanimelist.net/anime/season")
        season = page_soup.find("a", {"class": "on"}).string
        return str(season).replace("  ", "").replace("\n", "")

    @staticmethod
    def __map_to_string(season_num):
        options = {0: "winter", 1: "spring", 2: "summer", 3: "fall"}
        return options[season_num]

    def __init__(self, season=""):
        if (season == "" and this_season == 0):
            season = MALSeason.__current_season().split(" ")
        elif (season == ""):
            season = this_season
        month = season[0]
        if ("Winter" in month):
            self.season = 0
        elif ("Spring" in month):
            self.season = 1
        elif ("Summer" in month):
            self.season = 2
        else:
            self.season = 3
        self.year = int(season[1])

    def increment(self):
        if (self.season == 3):
            self.season = 0
            self.year += 1
        else:
            self.season = self.season + 1
        return self

    def decrement(self):
        if (self.season == 0):
            self.season = 3
            self.year -= 1
        else:
            self.season = self.season - 1
        return self

    def get_year(self):
        return self.year

    def get_season(self):
        return MALSeason.__map_to_string(self.season)

    def get_url_for_season(self):
        return "https://myanimelist.net/anime/season/" + str(self.year) + "/" + MALSeason.__map_to_string(self.season)

    def __str__(self):
        return MALSeason.__map_to_string(self.season) + " " + str(self.year)


def loadSoup(url):
    client = urlopen(url)
    page_html = client.read()
    client.close()
    page_soup = soup(page_html, "html.parser")
    return page_soup


def clean_str(item):
    item = item.replace('"', '&quot;')
    item = item.replace('\n', '\\n')
    mpa = dict.fromkeys(range(32))
    item = item.translate(mpa)
    return item


def scrape(url):
    logging.info("Beginning to scrape page with url: " + url)
    page_soup = loadSoup(url)
    logging.info("Loaded " + url + " into BS")
    this_season = str(page_soup.find("a", {"class": "on"}).string).replace("  ", "").replace("\n", "")

    page_anime = page_soup.find_all("div", {"class": "seasonal-anime js-seasonal-anime"})
    logging.info("Found anime section of page")
    logging.info("Scraping all anime...")
    list_anime = []
    for anime in page_anime:
        title = clean_str(str(anime.find("a", {"class": "link-title"}).string))

        numEps = anime.find("div", {"class": "eps"}).find("span").string.split(' ')[0]

        image = anime.find("img")

        if image.has_attr('class'):
            image = image['data-src']
        else:
            image = image['src']

        release = str(anime.find("span", {"class": "remain-time"}).string).replace("  ", "")

        synopsis = clean_str(str(anime.find("span", {"class": "preline"}).string))

        genres = list(g.find("a").string for g in anime.find_all("span", {"class": "genre"}))

        list_anime.append(Anime(title, numEps, image, release, synopsis, genres))

    logging.info("Scraping complete!")

    logging.info("Scraped " + str(len(list_anime)) + " anime from season " + str(this_season))
    return list_anime
