# from genre import *
import csv
import requests
import json
from Spotify import SpotifyClientCredentials
from Song import Song
from Artist import Artist
from Artists import Artists

clientSecret = "03796b826d064e059ac848e18695fe8b"
clientID = "53240351a0e44d5c98da6ca214fce4bd"
clientCreds = SpotifyClientCredentials(clientID, clientSecret)
token = clientCreds.get_access_token()
header = {'Authorization': 'Bearer {0}'.format(token)}
session = requests.Session()


csv_data = ['Spotify URI', 'Track Name', 'Artist Name', 'Album Name', 'Disc Number', 'Track Number',
            'Track Duration (ms)', 'Added By', 'Added At']
# ## Spotify Client ID: 53240351a0e44d5c98da6ca214fce4bd
# ## Spotify Client Secret: 03796b826d064e059ac848e18695fe8b
# creds = requests.post('https://accounts.spotify.com/api/token?grant_type=client_credentials?Authorization=%s:%s' % (spotifyID, spotifySecret))
# print(creds.content)

songList = []
all_artists = Artists()
lineCount = 0
with open('months/months.csv', 'rt', encoding='utf-8') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        # row = row.decode('utf-8')
        if lineCount == 0:
            lineCount += 1
        else:
            lineCount += 1
            uri = row[0]
            songList.append(uri[14:])
csvFile.close()


lotsOfTracks = []
for i in range(len(songList)):
    if (i != 0) and (i % 50 == 0):
        fiftySongs = ",".join(lotsOfTracks)
        fiftySongs = fiftySongs.strip()
        fiftySongs = fiftySongs.replace(" ", "")
        lotsOfTracks[:] = []
        response = session.get('https://api.spotify.com/v1/tracks?ids=%s' % fiftySongs, headers=header)
        currentSongs = response.json()
        for currentSong in currentSongs["tracks"]:
            artists = []
            albumJson = currentSong["album"]
            artistsJson = currentSong["artists"]
            album_release_date = albumJson["release_date"]
            album_name = albumJson["name"]
            song_name = currentSong["name"]
            song_id = currentSong["id"]
            for artist in artistsJson:
                artist_id = artist["id"]
                artist_name = artist["name"]
                new_artist = Artist(artist_id, artist_name)
                artists.append(new_artist)
                all_artists.add_artist(new_artist)
            new_song = Song(song_id, song_name, artists, album_name, album_release_date)
            for artist in artists:
                all_artists.add_song(new_song, artist.id)
    else:
        lotsOfTracks.append(songList[i])

lotsOfArtists = []
for i, key in enumerate(all_artists.get_artists()):
    if (i != 0) and (i % 50 == 0):
        fiftyArtists = ",".join(lotsOfArtists)
        fiftyArtists = fiftyArtists.strip()
        fiftyArtists = fiftyArtists.replace(" ", "")
        lotsOfArtists[:] = []
        response = session.get('https://api.spotify.com/v1/artists?ids=%s' % fiftyArtists, headers=header)
        currentArtists = response.json()
        for currentArtist in currentArtists["artists"]:
            genres = currentArtist["genres"]
            all_artists.add_genre(genres, currentArtist["id"])
    else:
        lotsOfArtists.append(key)

# response = requests.get("https://api.spotify.com/v1/search/")
# all_artists.print_genres()

# Playlists: [Alternative, Rock, House, Pop, Indie, Hip-Hop, Reggae]
# all_artists.sort_genre()
print(len(songList))
all_artists.print_num_songs()
# all_artists.print_playlists()