import requests
from requests import get
from bs4 import BeautifulSoup as btfs
import pandas as pd
import numpy as np
import re
from time import sleep
from random import randint

titles = []
years = []
time = []
imdb_ratings = []
metascores = []
votes = []
us_gross=[]

pages = np.arange(1, 951, 50)

for page in pages:
	page = requests.get(
		'https://www.imdb.com/search/title/?title_type=feature&release_date=1990-01-01,&user_rating=7.0,7.9&languages=en&start=' + str(page) + '&ref_=adv_nxt')

	soup = btfs(page.text, 'html.parser')
	# print(soup.prettify())

	movie_div = soup.find_all('div', class_='lister-item mode-advanced')

	sleep(randint(2, 10))

	# SCRAPPING ELEMENTS
	for i in movie_div:

		nv = i.find_all('span', {'name': 'nv'})

		try:
			vote = nv[0].text
		except:
			vote='0'
		if int(vote.replace(',', '')) < 10000: continue  # Filter all unpopular movies
		votes.append(vote)

		gross = nv[1].text if len(nv) > 1 else '-'
		us_gross.append(gross)

		name = i.h3.a.text
		titles.append(name)

		age = i.h3.find('span', class_='lister-item-year').text
		years.append(age)

		length = i.p.find('span', class_='runtime').text if i.p.find('span', class_='runtime') else '-'
		time.append(length)

		imdb = float(i.strong.text)
		imdb_ratings.append(imdb)

		meta = i.find('span', class_='metascore').text if i.find('span', class_='metascore') else '-'
		if len(meta)<1: continue
		metascores.append(meta)

#CREATE PANDAS DATAFRAME
movies = pd.DataFrame({
'Movie': titles,
'Year': years,
'Runtime': time,
'IMDB': imdb_ratings,
'Metascore': metascores,
'Votes': votes,
'US gross Millions': us_gross,
})
pd.set_option('max_columns', 7)

#CLEANING DATA
movies['Metascore'] = movies['Metascore'].str.extract('(\d+)')
movies['Metascore'] = pd.to_numeric(movies['Metascore'], errors='coerce')
movies['Year'] = movies['Year'].str.extract('(\d+)').astype(int)
movies['Runtime'] = movies['Runtime'].str.extract('(\d+)').astype(int)
movies['Votes'] = movies['Votes'].str.replace(',', '').astype(int)
movies['US gross Millions'] = movies['US gross Millions'].map(lambda x: x.lstrip('$').rstrip('M'))
movies['US gross Millions'] = pd.to_numeric(movies['US gross Millions'], errors='coerce')

print(movies)
movies.to_csv('movies.csv')