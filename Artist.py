from Song import Song


class Artist:
    def __init__(self, id, name, genres=None):
        self.id = id
        self.name = name
        if genres is None:
            self.genres = []
        else:
            self.genres = genres
        self.songs = []

    def add_song(self, song):
        self.songs.append(song)

    def get_songs(self):
        return self.songs

    def add_genre(self, genre):
        if type(genre) is list:
            for g in genre:
                self.genres.append(g)
        else:
            self.genres.append(genre)

    def print(self):
        print("Artist is %s, id: %s" % (self.name, self.id))
        for song in self.songs:
            song.print()