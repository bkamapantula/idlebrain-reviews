"""
parses all Idlebrain reviews to plot the review distribution and identify possible bias.
Builds a word corpus from the reviews.
a) maps most used words in a histogram.
b) maps most used words for each popular actor/actress film.

"""
import urllib3
import bs4
from collections import Counter
import sqlite3


def parse_reviews():
    """
    fetch movie review information from Idlebrain review archive page
    Step 1: identify all categories of movie Ratings in strings. frame if
     elif conditions based on that. Uncomment movie_ratings code to check.
    """
    url = "http://www.idlebrain.com/movie/archive/index.html"
    http = urllib3.PoolManager()
    scrape = http.request('GET', url)
    soup = bs4.BeautifulSoup(scrape.data)

    db = sqlite3.connect("reviews.db")
    c = db.cursor()
    row = ""
    counter = -5
    movie_id = ""
    movie_name = ""
    movie_rating = ""
    movie_release_date = ""
    #movie_ratings = []
    val = 0.0
    inval = 1

    for table in soup.findAll('table', attrs={'cellpadding': 3}):
        for tr in table.findAll('tr'):
            for td in tr.findAll('td'):
                counter += 1
                if counter > 0:
                    if counter%4 == 1:
                        movie_id = td.text
                    elif counter%4 == 2:
                        # split splits string by space. join groups list items separated by a space.
                        # this takes of extra space in between a string of format "a      b"
                        movie_name = td.text.split()
                        movie_name = ' '.join(movie_name)
                        for a in td.findAll('a'):
                            movie_url = "http://www.idlebrain.com/movie/archive/"+a['href']
                    elif counter%4 == 3:
                        movie_release_date = td.text
                    elif counter%4 == 0:
                        movie_rating = td.text.split()
                        movie_rating = ' '.join(movie_rating)
                        #movie_ratings.append(movie_rating)
                        #movie_rating = row[4].split('\n')[0]
                        if movie_rating == 'Quarter':
                            val = 0.25
                        elif movie_rating == 'Half':
                            val = 0.5
                        elif movie_rating == 'One':
                            val = 1.0
                        elif movie_rating == 'One and half' or movie_rating == 'One nad half' or movie_rating == 'One and Half':
                            val = 1.5
                        elif movie_rating == 'Two' or movie_rating == 'two':
                            val = 2.0
                        elif movie_rating == 'Two and Quarter' or movie_rating == 'Two and quarter':
                            val = 2.25
                        elif movie_rating == 'Two and half' or movie_rating == 'Two and Half':
                            val = 2.5
                        elif movie_rating == 'Two and Three fourth' or movie_rating == 'Two and three fourth' or movie_rating == 'Two and Threefourth' or movie_rating == 'Two and three quarter':
                            val = 2.75
                        elif movie_rating == 'Three':
                            val = 3.0
                        elif movie_rating == 'Three and quarter' or movie_rating == 'Three and a quarter' or movie_rating == 'Three and Quarter':
                            val = 3.25
                        elif movie_rating == 'Three and half' or movie_rating == 'Three and Half':
                            val = 3.5
                        elif movie_rating == 'Three and three fourth' or movie_rating == 'Three and three quarter' :
                            val = 3.75
                        elif movie_rating == 'Four':
                            val = 4.0
                        elif movie_rating == 'Four and Half' or movie_rating == 'Four and half':
                            val = 4.5
                        elif movie_rating == 'Five':
                            val = 5.0
                        elif movie_rating == 'NA' or \
                            movie_rating == 'GBU series' or\
                            movie_rating == 'Not Rated' or\
                            movie_rating == 'reviewed by MLN' or\
                            movie_rating == '-' or\
                            movie_rating == 'N/A analysis' or\
                            movie_rating == 'NA (devotional film)':
                            continue
                        # row += movie_id + "," + movie_name + "," + movie_url + "," + movie_release_date + "," + str(val) + "\n"
                        q = "SELECT * FROM movies WHERE id={}".format(movie_id)
                        c.execute(q)
                        if(not c.fetchone()):
                            q = 'INSERT INTO movies VALUES("{id}", "{name}", "{url}", "{dt}", "{rating}")'.format(id=movie_id, name=movie_name, url=movie_url, dt=movie_release_date, rating=str(val))
                            c.execute(q)
                            db.commit()
                        #else:
                        #	print("WAT", movie_rating,inval)
                        val = 0.0
    db.close()
# parse_reviews()


def fetch_data_from_IB():
    """
    fetches data for all movie reviews from respective URLs in data.csv
    """
    db = sqlite3.connect("reviews.db")
    c = db.cursor()
    q = "SELECT * FROM movies"
    c.execute(q)

    http = urllib3.PoolManager()
    ctr = 0
    for row in c.fetchall():
        print(row[0], row[1], row[2], row[3], row[4])
        ctr += 1
        url_parts = row[2].split('/')
        if len(url_parts) == 6:
            with open("data/"+url_parts[5], "w") as out_file:
                response = http.request('GET', row[2])
                soup = bs4.BeautifulSoup(response.data)
                out_file.write(str(soup))
# fetch_data_from_IB()


def build_corpus():
    """
    reads html file, tokenizes the text and spits the count for each token.
    `BeautifulSoup` doesn't support xpath-based DOM selection, using `lxml` instead.
    """
    from lxml import html, etree
    review_selector = "body > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(10) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1)"
    page = open("data/1nenokkadine.html")
    xpath_cast = "/html/body/table/tbody/tr[6]"
    xpath_review = "/html/body/table/tbody/tr[10]/td/table/tbody/tr/td[1]/table[1]"
    tree = html.fromstring(page.read())
    for el in tree.xpath(xpath_review):
        print(etree.tostring(el, pretty_print=True))

    for el in tree.xpath(xpath_cast):
        print(etree.tostring(el, pretty_print=True))
    # print(Counter(tokens))

build_corpus()
