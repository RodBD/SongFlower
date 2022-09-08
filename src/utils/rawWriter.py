from src.data.playlist_parser import PlaylistParser
import csv
import os

class rawWriter:

    PLAYLIST_RAW_OUT_PATH = r"C:\Users\Usuario\PycharmProjects\SongFlower\songflower-engine\data\raw\playlists"

    def __init__(self, origen):
        self.origen = origen
        self.playlist = PlaylistParser(origen).playlist

    def playlist_write(self):

        os.chdir(rawWriter.PLAYLIST_RAW_OUT_PATH)
        self.playlist.to_csv(self.origen + ".csv", sep =',')


tst = rawWriter('6ZWdA2cosw0MzqSdY9EHqP').playlist_write()


