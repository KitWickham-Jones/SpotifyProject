import psycopg2
import os

USER = os.getenv('POSTGRES_USER')
PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB = os.getenv('POSTGRES_DB')



def insert_data(inputdata):
    conn = psycopg2.connect(user=USER, password=PASSWORD,database=DB, host = "spottest-db-1", port=5432)
    cur = conn.cursor()
    
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
    conn = psycopg2.connect(user=USER, password=PASSWORD,database=DB, host = "spottest-db-1", port=5432)
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM art_Songs')
        data = cur.fetchall()
    except:
        print('failed to fetch data')
    
    if conn:
        cur.close()
        conn.close()

    return data








