import lyricsgenius as lg
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import json
import APIkeys
import spotipy

# Spotipy for track name finding
def getTracksFromPlaylists():

	# Initialize genius API and flag for skipping non-songs
	genius = lg.Genius(APIkeys.geniusClientToken())
	genius.skip_non_songs = True
	genius.remove_section_headers = True

	# Setup the Spotipy credentials manager for Oauth and feed it my keys
	client_credentials_manager = SpotifyClientCredentials(client_id=APIkeys.spotifyClientID(), client_secret=APIkeys.spotifyClientSecret())
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

	# This sets the playlist IDs, using two playlists here, "daves" and "aux" for short
	daves_uri = 'spotify:10dwebb:spotifycharts:playlist:5e8vFdHvnMjnk7fP9x41oQ'
	aux_uri = 'spotify:jdawg2000:spotifycharts:playlist:3YjUPovYVgaUHPTw2QUpMg'
	username = daves_uri.split(':')[2]
	daves_playlist_id = daves_uri.split(':')[4]
	aux_playlist_id = aux_uri.split(':')[4]

	# Open an output file
	lyrics = open("lyrics.txt", "a")
	# Get the JSON for the playlist and search each track/artist in Genius, then print to file
	for i in range(0, 1000, 100):
		daves_results = sp.user_playlist_tracks(username, daves_playlist_id, fields="items(track(name,artists))", offset=i) # Spotipy playlist query, incrementing by 1 offset each time

		for j in range(0, 100):
			try:
				print("Dave's Raps: Track " + str(i + j + 1) + "/1048")
				artist_name = daves_results["items"][j]["track"]["artists"][0]["name"] # Artist name index from JSON file
				track_name = daves_results["items"][j]["track"]["name"] # Track name index from JSON file
				track = genius.search_song(track_name, artist=artist_name) # Using genius API to pull song lyrics
				print(track.lyrics, file=lyrics)
			except:
				continue

	# Spotipy playlist query, incrementing by 1 offset each time
	daves_results = sp.user_playlist_tracks(
	username, daves_playlist_id, fields="items(track(name,artists))", offset=1000)

	for j in range(0, 48):
		try:
			print("Dave's Raps: Track " + str(j + 1001) + "/1048")
			# Artist name index from JSON file
			artist_name = daves_results["items"][j]["track"]["artists"][0]["name"]
			# Track name index from JSON file
			track_name = daves_results["items"][j]["track"]["name"]
			# Using genius API to pull song lyrics
			track = genius.search_song(track_name, artist=artist_name)
			print(track.lyrics, file=lyrics)
		except:
			continue


	for i in range(0, 1500, 100):
		# Spotipy playlist query, incrementing by 1 offset each time
		aux_results = sp.user_playlist_tracks(username, aux_playlist_id, fields="items(track(name,artists))", offset=i)

		for j in range(0, 100):
			try:
				print("Aux: Track " + str(i + j + 1) + "/1523")
				# Artist name index from JSON file
				artist_name = aux_results["items"][j]["track"]["artists"][0]["name"]
				# Track name index from JSON file
				track_name = aux_results["items"][j]["track"]["name"]
				# Using genius API to pull song lyrics
				track = genius.search_song(track_name, artist=artist_name)
				print(track.lyrics, file=lyrics)
			except:
				continue

	# Spotipy playlist query, incrementing by 1 offset each time
	aux_results = sp.user_playlist_tracks(username, aux_playlist_id, fields="items(track(name,artists))", offset=1500)

	for j in range(0, 23):
		try:
			print("Dave's Raps: Track " + str(j + 1501) + "/1523")
			# Artist name index from JSON file
			artist_name = aux_results["items"][j]["track"]["artists"][0]["name"]
			# Track name index from JSON file
			track_name = aux_results["items"][j]["track"]["name"]
			# Using genius API to pull song lyrics
			track = genius.search_song(track_name, artist=artist_name)
			print(track.lyrics, file=lyrics)
		except:
			continue

getTracksFromPlaylists()
