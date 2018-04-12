# Вдохновитель: https://www.youtube.com/watch?v=zlWiw99bBUk

import requests
from bs4 import BeautifulSoup
import csv

#План
#	1. выяснить количество страниц
#	2. сформировать список урлов
#	3. Собрать данные


def get_html(url):
	r = requests.get(url)
	return r.text
# функция должна возвращать количество страниц, но так как нет кнопки последняя на странице внизу, то НАДО РАбираться!!1
def get_total_pages(html):
		soup = BeautifulSoup(html, 'lxml')
		
		pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
		total_pages = pages.split('=')[1].split('&')[0]
		#На данные момент возвращает только количество первых 10 стараниц
		return int(total_pages)

def write_csv(data):
	with open('avito.csv', 'a') as f:
		writer = csv.writer(f)
		
		writer.writerow( (data['title'],
						  data['price'],
						  data['city'],
						  data['date_publication'],
						  data['url']) )
	
	
def get_page_date(html):
	soup = BeautifulSoup(html, 'lxml')
	
	ads = soup.find('div', class_ = 'catalog-list').find_all('div', class_ = 'item_table')
	
	for ad in ads:
		#title, price, city, url, date
		name = ad.find('div', class_ = 'description').find('h3').text.strip().lower()
		
		if 'htc' in name:
		
			try:
				title = ad.find('div', class_ = 'description').find('h3').text.strip()
			except:
				title = ''
			try:
				url = 'https://www.avito.ru' + ad.find('div', class_ = 'description').find('h3').find('a').get('href')
			except:
				url = ''
			try:
				price = ad.find('div', class_ = 'about').text.strip()
			except:
				price = ''
			#try:
			#	metro = ad.find('div', class_ = 'data').find_all('p')[-1]
			#except:
			#	metro = ''
				
			try:
				city = ad.find('div', class_ = 'data').find('p').text.strip()
			except:
				city = ''
			try:
				date_publication = ad.find('div', class_ = 'c-2').text.strip()
			except: 
				date_publication = ''
				
			data = {'title': title,
					'price': price,
					'city' : city,
					'date_publication' : date_publication,
					'url' : url}
					
			write_csv(data)
		else:
			continue
		
			
def main():
	url = 'https://www.avito.ru/rossiya/telefony?p=1&q=htc'
	base_url = 'https://www.avito.ru/rossiya/telefony?'
	page_part = 'p='
	query_part = '&q=htc'
	
	total_pages = get_total_pages(get_html(url))
	
	for i in range(1, 3): # вместо 3-ки, так как долго парсится будт total_pages + 1):
		url_gen = base_url + page_part + str(i) + query_part
		#print(url_gen)
		html = get_html(url_gen)
		get_page_date(html)




if __name__ == '__main__':
	main()
	
