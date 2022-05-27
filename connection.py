# databases : organised collection of data , generally stored and accesed electronically
# sql : structured query language
# pip install db--sqlite

import sqlite3

def connect(dbname):
	conn = sqlite3.connect(dbname)

	conn.execute("CREATE TABLE IF NOT EXISTS OYO_HOTELS (NAME TEXT, ADDRESS TEXT , PRICE INT , AMENITIES TEXT, RATING TEXT)")
	print("\n Table created successfully !!")
	conn.close()

def insert_into_table(dbname,val):
	conn = sqlite3.connect(dbname)
	print("Inserted into table : " + str(val))
	conn.execute("INSERT INTO OYO_HOTELS (NAME , ADDRESS , PRICE , AMENITIES , RATING) VALUES ( ? , ? , ? , ? , ?)",val)
	conn.commit()
	conn.close()

def get_hotel_info(dbname):
	conn = sqlite3.connect(dbname)
	cur = conn.cursor()
	cur.execute("SELECT * FROM OYO_HOTELS")
	table_data = cur.fetchall()

	for record in table_data:
		print(record)

	conn.close()