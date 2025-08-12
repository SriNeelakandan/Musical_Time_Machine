# Musical Time Machine Project

import requests
from bs4 import BeautifulSoup

import spotipy as sp
from spotipy.oauth2 import SpotifyOAuth

import os
from dotenv import load_dotenv

load_dotenv()
Client_Id= os.getenv("SPOTIPY_CLIENT_ID")
Client_Secret = os.getenv("SPOTIPY_CLIENT_SECRET")
USER_ID = os.getenv("SPOTIFY_USER_ID")
date_travel = input("Which year you want to travel to ? Type the date in YYYY-MM-DD format: ")
print(date_travel)

# Add Custom Headers on requesting the website
custom_header = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"}

# Create Custom Website
website = "https://www.billboard.com/charts/hot-100/"+date_travel
print(website)

# Get response 
response = requests.get(website,headers=custom_header)
web_contents = response.text

# Create a soup object to perform web scraping
soup = BeautifulSoup(web_contents,'html.parser')

# Get the content present inside li -> ul -> li -> h3"
song_titles_headings = soup.select(selector='li ul li h3')
print(song_titles_headings)

escape_c= "\n\t\r\b\f\v"
song_titles_list = [x.getText().translate(str.maketrans('',"",escape_c)) for x in song_titles_headings]
print(song_titles_list)

###############

spot = sp.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com",
        client_id=Client_Id,
        client_secret=Client_Secret,
        show_dialog=True,
        cache_path="token.txt",
    )
)


# user_id = spot.current_user()["id"]
song_uris = []
year = date_travel.split("-")[0]
for song in song_titles_list:
    result = spot.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Create a private playlist
playlist_name = date_travel+" Billboard 100"
private_playlist = spot.user_playlist_create(user=USER_ID,name=playlist_name,public=False)
print(f"Private List id {private_playlist}")

# Add songs to the playlist
spot.playlist_add_items(playlist_id=private_playlist["id"],items=song_uris)
"""
Authenticating with Spotify is quite complicated, especially when you want to access a user's account. So instead, we're going to use one of the most popular Python Spotify modules - Spotipy to make things easier.

- Spotipy is a lightweight Python library for the Spotify Web API. With Spotipy you get full access to all of the music data provided by the Spotify platform.
"""








"""
--------------------------------------------------------------------------------------------------------
"""
# Custom Headers are Passed to  the request statement

# Need of Custom Headers: 
#1.Pretend to be a normal browser
#   - Many websites block requests that look like bots (e.g., the default python-requests header).

#   - By sending headers like User-Agent, you mimic a real browser (Chrome, Firefox, etc.) so the server thinks you’re a regular visitor.

# 2. Avoid getting blocked or served different content

# 3. Access restricted or dynamic content

# 4. Control the request behavior