class Song:
    def __init__(self, id, name, artists, album, release_date=None):
        self.id = id
        self.name = name
        self.artists = artists
        self.album = album
        self.release_date = release_date

    def add_release_date(self, release_date):
        self.release_date = release_date

    def print(self):
        if len(self.artists) == 1:
            print("%s, by %s from %s, released in %s\n" % (
                self.name, self.artists[0].name, self.album, self.release_date))
        else:
            print("%s" % self.name)
            # for artist in self.artists:
            #     print("%s " % artist.name)
            # print("from %s, released in %s \n" % (self.album, self.release_date))
