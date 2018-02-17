from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

class Anime:
    
    def __init__(self, title, numEps, imgUrl, release, synopsis, genres):
        self.title = title
        self.numEps = numEps
        self.imgUrl = imgUrl
        self.release = release
        self.synopsis = synopsis
        self.genres = genres
        self.synopsis_to_print = synopsis_to_print = self.synopsis[0:97] + "..." if(len(self.synopsis) > 97) else synopsis
            
 

    def __str__(self):
                return "{" + 'title:' + str(self.title) + "," +\
                'numEps:' +  self.numEps + "," +\
                'imgUrl:' + self.imgUrl + "," + \
                'release:' + self.release + "," +\
                'synopsis:' + self.synopsis_to_print + "," +\
                'genres:' + str(self.genres) + "}"


def scrape(url):
    client = urlopen(url)
    page_html = client.read()
    client.close()
    page_soup = soup(page_html, "html.parser")
    page_anime = page_soup.find_all("div", {"class":"seasonal-anime js-seasonal-anime"})
    list_anime = []
    for anime in page_anime:
        title = str(anime.find("a", {"class":"link-title"}).string)
        numEps = anime.find("div", {"class":"eps"}).find("span").string.split(' ')[0]
        image = anime.find("img")
        if image.has_attr('class'):
            image = image['data-src']
        else:
            image = image['src']

        release = str(anime.find("span", {"class":"remain-time"}).string).replace("  ","")
        synopsis = str(anime.find("span", {"class":"preline"}).string)
        genres = list(g.find("a").string for g in anime.find_all("span", {"class":"genre"}))

        list_anime.append(Anime(title, numEps, image, release, synopsis, genres))
    return list_anime
