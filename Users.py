from Artist import Artist


class Users:
    # Playlists: [Alternative, Rock, House, Pop, Indie, Hip-Hop, Reggae, Blues, Jazz, Metal, Folk, Indie]
    def __init__(self):
        self.artists = {}
        self.no_genre = {}
        self.genres = {}
        self.genre_playlists = {"rock": [], "alt": [], "house": [], "pop": [], "hiphop": [], "reggae": [], "blues": [],
                          "jazz": [], "metal": [], "folk": [], "indie": [], "none": [], "rnb": []}
        self.find_cat = []
        self.playlists = {}

    def find_artist(self, key):
        return self.artists[key]

    def add_artist(self, artist):
        if artist.id not in self.artists:
            self.artists[artist.id] = artist
            if artist.genres == []:
                self.no_genre[artist.id] = artist

    def add_playlist(self, playlist):
        if playlist.id not in self.playlists:
            self.playlists[playlist.id] = playlist

    def has_genre(self, key):
        if key not in self.no_genre:
            return False
        else:
            return True

    def genre_exists(self, g):
        if g not in self.genres:
            return False
        else:
            return True

    def get_songs(self, key):
        artist = self.find_artist(key)
        return artist.get_songs()

    def add_song(self, song, key):
        artist = self.find_artist(key)
        artist.add_song(song)

    def add_genre(self, genre, key):
        if type(genre) is list:
            for g in genre:
                if self.genre_exists(g):
                    self.genres[g].append(key)
                else:
                    self.genres[g] = [key]
        else:
            if self.genre_exists(genre):
                self.genres[genre].append(key)
            else:
                self.genres[genre] = [key]
        artist = self.find_artist(key)
        if artist is None:
            return False
        artist.add_genre(genre)
        self.no_genre.pop(key)

    def print(self):
        for key, value in self.artists.items():
            value.print()

    def print_no_genres(self):
        print(len(self.no_genre))
        for key, value in self.no_genre.items():
            value.print()

    def get_artists(self):
        return self.artists

    def print_genres(self):
        print(len(self.genres))
        for key, value in self.genres.items():
            print(key)

    def print_num_songs(self):
        num = 0
        for key, value in self.artists.items():
            num += len(value.songs)
        print(num)

    def print_playlists(self):
        # print(len(self.find_cat))
        for key, value in self.genre_playlists.items():
            print(key)
            print(value)
            for v in value:
                v.print()
            print("------------------------------------------------------------------------\n")
        for g in self.find_cat:
            print(g)

    # Genres: [Alternative, Rock, House, Pop, Indie, Hip-Hop, Reggae, Blues, Jazz, Metal, Folk]
    def sort_genre(self):
        found = False
        for key, value in self.artists.items():
            for g in value.genres:
                if 'alternative' in g:
                    found = True
                    for k, song in value.songs.items():
                        self.genre_playlists["alt"].append(song)
                if 'rock' in g:
                    found = True
                    for k, song in value.songs.items():
                        self.genre_playlists["rock"].append(song)
                if 'house' in g or 'edm' in g or 'tech' in g or 'techno' in g or 'touch' in g or 'dnb' in g or 'drum and base' in g:
                    found = True
                    for k, song in value.songs.items():
                        self.genre_playlists["house"].append(song)
                if 'pop' in g:
                    found = True
                    for k, song in value.songs.items():
                        self.genre_playlists["pop"].append(song)
                if 'indie' in g:
                    found = True
                    for k, song in value.songs.items():
                        self.genre_playlists["indie"].append(song)
                if 'hip hop' in g:
                    found = True
                    for k, song in value.songs.items():
                        self.genre_playlists["hiphop"].append(song)
                if 'r&b' in g:
                    found = True
                    for k, song in value.songs.items():
                        self.genre_playlists["rnb"].append(song)
                if 'reggae' in g:
                    found = True
                    for k, song in value.songs.items():
                        self.genre_playlists["reggae"].append(song)
                if 'blues' in g:
                    found = True
                    for k, song in value.songs.items():
                        self.genre_playlists["blues"].append(song)
                if 'jazz' in g:
                    found = True
                    for k, song in value.songs.items():
                        self.genre_playlists["jazz"].append(song)
                if 'metal' in g:
                    found = True
                    for k, song in value.songs.items():
                        self.genre_playlists["metal"].append(song)
                if 'folk' in g:
                    found = True
                    for k, song in value.songs.items():
                        self.genre_playlists["folk"].append(song)
                if not found:
                    self.find_cat.append(g)
                    for k, song in value.songs.items():
                        self.genre_playlists["none"].append(song)
