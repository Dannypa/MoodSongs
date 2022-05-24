from csv import DictReader
import sqlite3

with open("tcc_ceds_music.csv", encoding='utf-8', mode='r') as f:
    reader = DictReader(f, delimiter=',')
    con = sqlite3.connect("lyrics.db")
    cur = con.cursor()
    for i, line in enumerate(reader):
        artist = line["artist_name"].replace('\'', '').replace('"', '')
        name = line["track_name"].replace('\'', '').replace('"', '')
        text = line["lyrics"].replace('\'', '').replace('"', '')
        cmd = f"""INSERT INTO lyrics (artist, name, text)
                  VALUES ('{artist}', '{name}', '{text}')"""
        try:
            cur.execute(cmd)
        except sqlite3.OperationalError as e:
            print(str(e))
            exit(0)
    con.commit()
    con.close()
