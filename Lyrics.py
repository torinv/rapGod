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
	for i in range(0, 1048):
		print("Dave's Raps: Track " + str(i + 1) + "/1048")
		daves_results = sp.user_playlist_tracks(username, daves_playlist_id, fields="items(track(name,artists))", offset=i, limit=1) # Spotipy playlist query, incrementing by 1 offset each time

		artist_name = daves_results["items"][0]["track"]["artists"][0]["name"] # Artist name index from JSON file
		track_name = daves_results["items"][0]["track"]["name"] # Track name index from JSON file
		track = genius.search_song(track_name, artist=artist_name) # Using genius API to pull song lyrics

		print(track.lyrics, file=lyrics)
	
	# Same for other playlist
	for i in range(0, 1523):
		print("Pass Me the Aux: Track " + str(i + 1) + "/1523")
		aux_results = sp.user_playlist_tracks(username, aux_playlist_id, fields="items(track(name,artists))", offset=i, limit=1)

		artist_name = aux_results["items"][0]["track"]["artists"][0]["name"]
		track_name = aux_results["items"][0]["track"]["name"]
		track = genius.search_song(track_name, artist=artist_name)

		print(track.lyrics, file=lyrics)

getTracksFromPlaylists()

# Get lyrics and save to a txt file
# artist = genius.search_artist("XXXTENTACION", max_songs=1)

# song = genius.search_song("", artist.name)
# print(song.lyrics, file=out)
# artist.add_song(song)

