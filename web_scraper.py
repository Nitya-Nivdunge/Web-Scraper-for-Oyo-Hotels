# Web Scrapping using BeautifulSoup4 and requests

import requests
from bs4 import BeautifulSoup
import pandas
import argparse
import connection

parser = argparse.ArgumentParser()
parser.add_argument("--page_num_max", help='Enter the number of pages to parse : ', type = int)
parser.add_argument("--dbname", help = "Enter the name of db : ", type = str)
args = parser.parse_args()

web_url="https://www.oyorooms.com/hotels-in-banglore/?page="
page_num_Max = args.page_num_max
scraped_info_list = []
connection.connect(args.dbname)

for page_num in range(1,page_num_Max+1):
	url = web_url + str(page_num)
	print("\n GET REQUEST FOR URL : " + url)
	req = requests.get(url)
	content = req.content

	soup = BeautifulSoup(content,"html.parser")

	all_hotels = soup.find_all("div" , {"class":"hotelCardListing"})

	for hotel in all_hotels :
		hotel_dict = {}
		hotel_dict["name"] = hotel.find("h3" , {"class": "listingHotelDescription__hotelName"}).text
		hotel_dict["address"] = hotel.find("span" , {"itemprop": "streetAddress"}).text
		hotel_dict["price"] = hotel.find("span" , {"class": "listingPrice__finalPrice"}).text
		
		try:
			hotel_dict["rating"] = hotel.find("span" , {"class": "hotelRating__ratingSummary"}).text
		except AttributeError:
			hotel_dict["rating"] = None

		parent_amenities_elements = hotel.find("div" , {"class": "amenityWrapper"})
		amenities_list = []

		for amenity in parent_amenities_elements.find_all("div" , {"class": "amenityWrapper__amenity"}):
			amenities_list.append(amenity.find("span" , {"class": "d-body-sm"}).text.strip())

		hotel_dict["amenities"] = ', '.join(amenities_list[:-1])
		scraped_info_list.append(hotel_dict)
		connection.insert_into_table(args.dbname,tuple(hotel_dict.values()))
	

dataFrame = pandas.DataFrame(scraped_info_list)
print("\n Creating csv file ... \n")
dataFrame.to_csv("Oyo.csv")
connection.get_hotel_info(args.dbname)
