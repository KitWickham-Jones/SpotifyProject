import psycopg2
import os

USER = os.getenv('POSTGRES_USER')
PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB = os.getenv('POSTGRES_DB')



def insert_data(inputdata):
	try:		
		conn = psycopg2.connect(user=USER, password=PASSWORD,database=DB, host = "spottest-db-1", port=5432)
		cur = conn.cursor()
	except:
		raise psycopg2.errors.DatabaseError('Failed to connect to DB')
	
	insert_query = """INSERT INTO art_Songs (played_at, Artist_ID, Song_ID) VALUES (%s,%s,%s)"""
	print('here not in for loop')
	for i in range(0,len(inputdata['items'])):
		played_at = inputdata['items'][i]['played_at']
		artist = inputdata['items'][i]['track']['artists'][0]['name']
		song = inputdata['items'][i]['track']['name']
		try:
			cur.execute(insert_query, (played_at,artist,song))
			conn.commit()
		except (Exception, psycopg2.Error) as error:
			print("Failed to insert data" ,error )      
	if conn:
		cur.close()
		conn.close()

def fetch_data():
	try:		
		conn = psycopg2.connect(user=USER, password=PASSWORD,database=DB, host = "spottest-db-1", port=5432)
		cur = conn.cursor()
	except:
		raise psycopg2.errors.DatabaseError('Failed to connect to DB')		
	cur.execute('SELECT * FROM art_Songs')
	data = cur.fetchall()	
	if conn:
		cur.close()
		conn.close()

	return data








