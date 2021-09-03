import lyricsgenius as lg
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import json
import APIkeys
import spotipy

# Spotipy for track name finding
# USAGE: uri is Spotify playlist ID, n is playlist length, filename is output file
def getLyrics(uri, n, filename, writeMode):

	# Initialize genius API and flag for skipping non-songs
	genius = lg.Genius(APIkeys.geniusClientToken())
	genius.skip_non_songs = True
	genius.remove_section_headers = True

	# Setup the Spotipy credentials manager for Oauth and feed it my keys
	client_credentials_manager = SpotifyClientCredentials(client_id=APIkeys.spotifyClientID(), client_secret=APIkeys.spotifyClientSecret())
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

	# Open an output file and incrementer
	lyrics = open(filename, writeMode)
	json = open("spoty-results.json", "w")
	inc = 0
	list_id = uri.split(':')[4]
	username = uri.split(':')[2]

	# Get the JSON for the playlist and search each track/artist in Genius, then print to file
	for i in range(0, n, 100):
		spoty_results = sp.user_playlist_tracks(username, list_id, fields="items(track(name,artists))", offset=i) # Spotipy playlist query, incrementing by 1 offset each time

		for j in range(0, len(spoty_results["items"])):
			try:
				print("Track " + str(j + inc) + " / " + str(n))
				artist_name = spoty_results["items"][j]["track"]["artists"][0]["name"] # Artist name index from JSON file
				track_name = spoty_results["items"][j]["track"]["name"] # Track name index from JSON file
				track = genius.search_song(track_name, artist=artist_name) # Using genius API to pull song lyrics
				print(track.lyrics, file=lyrics)
			except:
				print("Error: No results returned or API call failure")
				continue
		
		inc += 100

