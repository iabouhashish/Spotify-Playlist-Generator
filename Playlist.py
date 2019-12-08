

class Playlist:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.songs = []

    def add_song(self, song):
        if song not in self.songs:
            self.songs.append(song)
