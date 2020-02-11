import requests
import json
import urllib.request
from bs4 import BeautifulSoup
import csv
import os
import time




# Get few band names from wikipedia
def get_prog_metal_bands():

	bands_l = []
	url = 'https://en.wikipedia.org/wiki/List_of_progressive_metal_artists'
	source = urllib.request.urlopen(url)
	html = source.read()
	source.close()
	soup = BeautifulSoup(html, 'lxml')
	soup1 = soup.body.find_all('div')
	soup1 = soup1[2].find_all('div')[7]
	soup1 = soup1.find_all('ul')
	for i in range(1, len(soup1)-2):
		soup2 = soup1[i].find_all('li')
		for j in range(0, len(soup2)):
			try:
				soup3 = soup2[j].a.text
				bands_l.append(soup3)
			except:
				print('error')

	print(bands_l)
	print(len(bands_l))	
	
# Get few band names from wikipedia
def get_post_rock_bands():
		
	bands_l = []
	url = 'https://en.wikipedia.org/wiki/List_of_post-rock_bands'
	source = urllib.request.urlopen(url)
	html = source.read()
	source.close()
	soup = BeautifulSoup(html, 'lxml')
	soup1 = soup.body.find_all('div')
	soup1 = soup1[2].find_all('div')[7]
	print(soup1)


# Get names of metal, progressive and alernative bands and save it
def get_bands_shop():
	data = {'prog':34, 'metal':126, 'alternative':89}
	bands_l = []
	for dat in data:
		for page in range(1, data[dat]):
			url = f'https://www.recordshopx.com/{dat}/cd/?p={page}&o=a'
			source = urllib.request.urlopen(url)
			html = source.read()
			source.close()
			soup = BeautifulSoup(html, 'lxml')
			soup1 = soup.body.find_all('div', id="content")
			soup1 = soup1[0].find_all('div', class_='col-xs-12 col-md-8')
			soup1 = soup1[0].find_all('ul', class_='list-unstyled list-products')[0].find_all('li')
			for i in range(0, len(soup1) - 1):
				try:
					soup2 = soup1[i].find_all('div', class_='col-xs-8 col-sm-10 details')[0]
				except:
					print(page, i)
				try:
					soup2 = soup2.h3.text.split('\n')[2]
					try:
						band = soup2.split(',')
						band = band[0] + ' ' + band[1]
						bands_l.append(band)
					except:
						bands_l.append(band[0])
				except:
					print('skipping')
			print('sleeping 5 sec')
			time.sleep(5)

	bands_l = list(set(bands_l))
	with open('bands.csv', 'w') as f:
		for i in bands_l:
			try:
				f.write(f'{i}\n')
			except:
				print('cannot write')


# Get albums covers from deezer API 
def get_covers():

	with open('bands.csv', 'r') as f:
		reader = csv.reader(f)
		
		for i in reader:

			try:
				response2 = requests.get(f'https://api.deezer.com/search/album?q=artist:"{i[0]}"/album')
				r2 = response2.json()
	
				for j in r2['data']:

					title = j['title']
					pic = j['cover_big']
					if not os.path.exists(f'albums/{i}_{title}.jpg'):
						urllib.request.urlretrieve(str(pic), f'albums/{i[0]}_{title}.jpg')
			except:
				print(f'Error getting {i}')
			print('sleeping')
			time.sleep(5)
				
get_covers()





