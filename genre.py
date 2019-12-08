# from genre import *
import csv
import requests
import json
from Spotify import SpotifyClientCredentials
from Spotify import *
from Song import Song
from Artist import Artist
from Users import Users
from Playlist import Playlist

clientSecret = "03796b826d064e059ac848e18695fe8b"
clientID = "53240351a0e44d5c98da6ca214fce4bd"
clientCreds = SpotifyClientCredentials(clientID, clientSecret)
token = clientCreds.get_access_token()
header = {'Authorization': 'Bearer {0}'.format(token)}
session = requests.Session()
user_id = "iabouhashish"

csv_data = ['Spotify URI', 'Track Name', 'Artist Name', 'Album Name', 'Disc Number', 'Track Number',
            'Track Duration (ms)', 'Added By', 'Added At']


# ## Spotify Client ID: 53240351a0e44d5c98da6ca214fce4bd
# ## Spotify Client Secret: 03796b826d064e059ac848e18695fe8b
# creds = requests.post('https://accounts.spotify.com/api/token?grant_type=client_credentials?Authorization=%s:%s' % (spotifyID, spotifySecret))
# print(creds.content)
token = prompt_for_user_token(user_id, client_id=clientID, client_secret=clientSecret, redirect_uri='http://localhost/')


def make_playlists():
    for key, value in user.genre_playlists.items():
        exists = False
        play_id = ""
        for k, v in user.playlists.items():
            if key == v.name:
                exists = True
                play_id = v.id
            else:
                exists = False

        if exists:
            # Playlist already exists
            play_id = 0
            add_songs_to_spotify(play_id, value)
        else:
            # Create playlist
            desc = "New playlist for %s created by Spotify Genre Generator" % value
            body = {"name": key, "description": desc}
            create_response = session.post("https://api.spotify.com/v1/users/%s/playlists" % user_id, json=body,
                                    headers=header)
            new_p = create_response.json()
            print(new_p)
            play_id = new_p["id"]
            add_songs_to_spotify(play_id, value)


def add_songs_to_spotify(play_id, songs):
    list_songs = ""
    for v in songs:
        list_songs += "spotify:%s," % v.id
    list_songs = list_songs[:-1]
    playlist_response = session.post("https://api.spotify.com/v1/playlists/%s/tracks?uris=%s" % (play_id, list_songs),
                            headers=header)
    print(playlist_response.json())


songList = []
user = Users()
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
test_art_id = 0
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
                user.add_artist(new_artist)
                test_art_id = new_artist.id
            new_song = Song(song_id, song_name, artists, album_name, album_release_date)
            for artist in artists:
                user.add_song(new_song, artist.id)
    else:
        lotsOfTracks.append(songList[i])

lotsOfArtists = []
for i, key in enumerate(user.get_artists()):
    if (i != 0) and (i % 50 == 0):
        fiftyArtists = ",".join(lotsOfArtists)
        fiftyArtists = fiftyArtists.strip()
        fiftyArtists = fiftyArtists.replace(" ", "")
        lotsOfArtists[:] = []
        response = session.get('https://api.spotify.com/v1/artists?ids=%s' % fiftyArtists, headers=header)
        currentArtists = response.json()
        for currentArtist in currentArtists["artists"]:
            genres = currentArtist["genres"]
            user.add_genre(genres, currentArtist["id"])
    else:
        lotsOfArtists.append(key)

listOfPlaylists = []
offset = 0
response = session.get('https://api.spotify.com/v1/users/%s/playlists?offset=%d&limit=50' % (user_id, offset),
                       headers=header)
currentPlaylists = response.json()
while len(currentPlaylists["items"]) > 0:
    offset += 50
    for playlist in currentPlaylists["items"]:
        playlistName = playlist["name"]
        playlistId = playlist["id"]
        new_playlist = Playlist(playlistId, playlistName)
        user.add_playlist(new_playlist)
    response = session.get('https://api.spotify.com/v1/users/%s/playlists?offset=%d&limit=50' % (user_id, offset),
                           headers=header)
    currentPlaylists = response.json()

print(len(user.playlists))

# Playlists: [Alternative, Rock, House, Pop, Indie, Hip-Hop, Reggae]
user.sort_genre()
make_playlists()
# user.print_playlists()
