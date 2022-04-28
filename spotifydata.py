import json
import sqlite3
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#make a connection to the database
conn = sqlite3.connect('spotifydata.sqlite')
#acts like a file handle to the database
cur = conn.cursor()

#create tables
cur.execute('DROP TABLE IF EXISTS Playlists')
cur.execute('DROP TABLE IF EXISTS Tracks')
cur.executescript('''
    CREATE TABLE Playlists (
        id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name    TEXT UNIQUE,
        length  INTEGER
    );

    CREATE TABLE Tracks (
        id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        title   TEXT UNIQUE,
        artist  TEXT,
        album   TEXT
    )
''')

count = 0
artistcount = 0
trackcount = 0;
artisttracks = list()

#read json data
fhandle = open('Playlist1.json')
str_data = fhandle.read()
json_data = json.loads(str_data)

selectedartist = input("Choose an Artist (case sensitive): ")

#each entry = 1 playlist (should be 109 playlists)
for entry in json_data["playlists"]:
    count = count+1
    print('Playlist Name: ', entry["name"]) #playlist name
    name = entry["name"]

    print(len(entry["items"])) #number of tracks per playlist
    length = len(entry["items"])

    try:
        index = 0
        while index < length:
            title = entry["items"][index]["track"]["trackName"]
            artist = entry["items"][index]["track"]["artistName"]
            album = entry["items"][index]["track"]["albumName"]

            cur.execute('''INSERT OR IGNORE INTO Tracks (title, artist, album) VALUES ( ?, ?, ?)''', (title, artist, album))
            cur.execute('SELECT id FROM Tracks WHERE title = ? AND artist = ? AND album = ?', (title, artist, album))

            if artist.startswith(selectedartist):
                artistcount = artistcount + 1
                artisttracks.append(title)

            index = index+1
            trackcount = trackcount+1
    except:
        title = "none"
        artist = "none"
        album = "none"

    cur.execute('''INSERT OR IGNORE INTO Playlists (name, length) VALUES ( ?, ? )''', (name , length) )
    cur.execute('SELECT id FROM Playlists WHERE name = ? AND length = ?' , (name, length ))

    conn.commit()

    print('-------------')

print('Artist Selected:', selectedartist)
print('Total Playlists:', count)
print('Total ' + selectedartist + ' Tracks:', artistcount)
print('Percent of Tracks that are by ' + selectedartist + ':', str(np.round(artistcount/trackcount*100, 2)) + '%')
print('Total Tracks:', trackcount)

#plt.hist(artisttracks[:25])
#plt.show()
