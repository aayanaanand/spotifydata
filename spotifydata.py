import json
import sqlite3

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

#read json data
fhandle = open('Playlist1.json')
str_data = fhandle.read()
json_data = json.loads(str_data)

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

            index = index+1
    except:
        title = "none"
        artist = "none"
        album = "none"

    cur.execute('''INSERT OR IGNORE INTO Playlists (name, length) VALUES ( ?, ? )''', (name , length) )
    cur.execute('SELECT id FROM Playlists WHERE name = ? AND length = ?' , (name, length ))

    conn.commit()

    print('-------------')

print('Total Playlists: ', count)
