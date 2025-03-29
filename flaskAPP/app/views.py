from app import app
import os
import urllib
from flask import redirect, request, session
import requests
from .database import insert_data, fetch_data


# load_dotenv("/Users/kitwj/Documents/Personal/Projects/spotTest/.env", override=True)
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
app.secret_key = os.getenv('FLASK_SECRET')

@app.route('/')
def hello_world():
	return "<a href= 'http://127.0.0.1:5000/login'>Login here     <a/>" +  "<a href= 'http://127.0.0.1:5000/databaseData'> whats in teh database? <a/>"

@app.route('/login')
def login():
	#generate url
	url = 'https://accounts.spotify.com/authorize?'
	params = {
		'response_type' :'code',
		'client_id' : CLIENT_ID,
		'redirect_uri' : 'http://127.0.0.1:5000/callback',
		'scope' : 'user-read-recently-played'
	}
	return redirect(url + urllib.parse.urlencode(params))

@app.route('/callback')
def callback():
	if 'code' in request.args:
		url = 'https://accounts.spotify.com/api/token' 
		form = {
			'code' : request.args['code'],
			'redirect_uri' : 'http://127.0.0.1:5000/callback',
			'grant_type' : 'authorization_code',
			'client_id' : CLIENT_ID,
			'client_secret': CLIENT_SECRET
		}
		
		response = requests.post(url=url, data = form)
		
		response_data = response.json()
		session['access_token'] = response_data['access_token']		
		return redirect('http://127.0.0.1:5000/recentlyPlayed')
	
@app.route('/recentlyPlayed')
def recentlyPlayed():
	url = 'https://api.spotify.com/v1/me/player/recently-played?limit=50&after=1742428800'
	headers = {
		'Authorization' : 'Bearer ' + session['access_token'],       
	}
	response = requests.get(url=url, headers=headers)
	response = response.json()
	try:
		insert_data(response)
	except:
		return 'failed'
	finally:
		return f"Successfully inputted {len(response)} items :) " + "<a href= 'http://127.0.0.1:5000'>Return home<a/>"
	
@app.route('/databaseData')
def get_data():
	try :
		out =fetch_data()
	except:
		return 'failed'
	return out

	

