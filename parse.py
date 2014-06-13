"""
parses all Idlebrain reviews to plot the review distribution and identify possible bias.
Builds a word corpus from the reviews. 
a) maps most used words in a histogram.
b) maps most used words for each popular actor/actress film.

"""
import urllib3
import bs4
from collections import Counter
import matplotlib.pyplot as plt
import numpy as  np
from operator import itemgetter
import nltk
import MySQLdb
import sys
import datetime
from dbconfig import db_config

class TeluguMovie():
	"""
	builds a TeluguMovie class with the following attributes:
	movie_id, movie_name, movie_url, movie_release_date, movie_rating
	"""
	def __init__(self):
		self.movie_id = 1
		self.movie_name = ""
		self.movie_url = ""
		self.movie_release_date = "30-04-1999"
		self.movie_rating = 3.0


def lookup_reviews_by_category(start_date, end_date):
	"""
	Input
	======
	date range

	Output
	=======
	number of reviews in each category [1-5 rating scale]
	"""
	cursor, db = db_config.db_config()
	query = "SELECT * FROM idlebrain_reviews WHERE movie_release_date>=%s AND movie_release_date<=%s"
	# year, month, date
	print int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2])
	print int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2])
	s_date = datetime.datetime( int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]) )
	e_date = datetime.datetime( int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]) )
	parameters = s_date, end_date
	print parameters
	try:
		cursor.execute(query, parameters)
		db.commit()
	except MySQLdb.Error, e:
		raise e
	rows = cursor.fetchall()
	cursor.close()
	for row in rows:
		print row

lookup_reviews_by_category('2010-01-15', '2005-01-14')


def read_data():
	"""
	Input
	======
	data.csv

	Output
	=======
	identifies the distribution of movie ratings from 0.5/5 to 5/5.
	ignores other kind of ratings "N/A" | "GBU series" etc.
	"""
	in_file = open("data.csv", "r")
	ratings = []
	val = 0.0
	for row in in_file:
		row = row.split(',')
		movie_rating = row[4].split('\n')[0]
		if movie_rating == 'Quarter':
			val = 0.25
			ratings.append(val)
		elif movie_rating == 'Half':
			val = 0.5
			ratings.append(val)
		elif movie_rating == 'One':
			val = 1.0
			ratings.append(val)
		elif movie_rating == 'One and half' or movie_rating == 'One nad half' or movie_rating == 'One and Half':
			val = 1.5
			ratings.append(val)
		elif movie_rating == 'two' or movie_rating == 'Two':
			val = 2.0
			ratings.append(val)
		elif movie_rating == 'Two and Quarter' or movie_rating == 'Two and quarter':
			val = 2.25
			ratings.append(val)
		elif movie_rating == 'Two and half' or movie_rating == 'Two and Half':
			val = 2.5
			ratings.append(val)
		elif movie_rating == 'Two and Three fourth' or movie_rating == 'Two and three fourth' or movie_rating == 'Two and Threefourth' or movie_rating == 'Two and three quarter':
			val = 2.75
			ratings.append(val)
		elif movie_rating == 'Three':
			val = 3.0
			ratings.append(val)
		elif movie_rating == 'Three and quarter' or movie_rating == 'Three and a quarter' or movie_rating == 'Three and Quarter':
			val = 3.25
			ratings.append(val)
		elif movie_rating == 'Three and half' or movie_rating == 'Three and Half':
			val = 3.5
			ratings.append(val)
		elif movie_rating == 'Three and three fourth' or movie_rating == 'Three and three quarter' :
			val = 3.75
			ratings.append(val)
		elif movie_rating == 'Four':
			val = 4.0
			ratings.append(val)
		elif movie_rating == 'Four and Half' or movie_rating == 'Four and half':
			val = 4.5
			ratings.append(val)
		elif movie_rating == 'Five':
			val = 5.0
			ratings.append(val)
		#ratings.append(movie_rating)
	data = dict( (i,ratings.count(i)) for i in set(ratings) )
	print sorted(data.iteritems(), key=itemgetter(1), reverse=True)


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
	# if below is uncommented, use python parse.py > data.html
	#print soup

	f = open("data.csv", "wb")
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
						row += movie_id + "," + movie_name + "," + movie_url + "," + movie_release_date + "," + str(val) + "\n"
						#else:
						#	print "WAT", movie_rating,inval
						val = 0.0
	f.write(row)
#parse_reviews()


def fetch_data_from_IB():
	"""
	fetches data for all movie reviews from respective URLs in data.csv
	"""
	in_file = open("data.csv", "r")
	http = urllib3.PoolManager()
	ctr = 0
	for row in in_file:
		ctr += 1
		row = row.split(',')
		url_parts = row[2].split('/')
		if len(url_parts) == 6:
			with open("data/"+url_parts[5], "w") as out_file:
				response = http.request('GET', row[2])
				soup = bs4.BeautifulSoup(response.data)
				out_file.write(str(soup))


def build_corpus():
	"""
	reads html file, tokenizes the text and spits the count for each token
	"""
	in_file = open("data/1nenokkadine.html", "r")
	url = "http://www.idlebrain.com/movie/archive/1nenokkadine.html"
	http = urllib3.PoolManager()
	scrape = http.request('GET', url)
	soup = bs4.BeautifulSoup(scrape.data).get_text()
	tokens = nltk.word_tokenize(soup)
	print Counter(tokens)

#build_corpus()


def insert_to_rdb():
	"""
	inserts all content from data.csv to MySQL database

	NO LONGER NEEDED.
	"""
	cursor = db_config.db_config()
	for row in file("data.csv"):
		row = row.split(',')
		query = "INSERT INTO idlebrain_reviews( \
			movie_id, movie_name, movie_url, movie_release_date, movie_rating) \
			VALUES (%s, %s, %s, %s, %s)"
		try:
			if row[3] != 'unreleased':
				release_date= int(row[3].split('-')[0])
				release_month = int(row[3].split('-')[1])
				release_year = int(row[3].split('-')[2])
				dt = datetime.datetime(release_year, release_month, release_date)
				movie_rating = float(row[4].split('\n')[0])
				#print int(row[0]), str(row[1]), str(row[2]), str(dt), movie_rating
				parameters = int(row[0]), str(row[1]), str(row[2]), dt, movie_rating
				cursor.execute(query, parameters)
				db.commit()
		except MySQLdb.Error, e:
			raise e
		except MySQLdb.IntegrityError, e:
			print "Integrity error"
		except MySQLdb.Warning, e:
			print "Warning: ", e
		except MySQLdb.ProgrammingError,e:
			print "Programming error", e
		except MySQLdb.OperationalError, e:
			print "Operational error"
