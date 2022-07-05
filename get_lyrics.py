from csv import DictReader
import sqlite3
from bs4 import BeautifulSoup
import requests
import re
import logging

logging.basicConfig(filename='get_lyrics.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
lyrics = []  # array for data sample storage


def scrape_lyrics(artistname, songname):  # function to get lyrics from genius.com
    artistname2 = str(artistname.replace(' ', '-')) if ' ' in artistname else str(artistname)
    songname2 = str(songname.replace(' ', '-')) if ' ' in songname else str(songname)
    page = requests.get('https://genius.com/' + artistname2 + '-' + songname2 + '-' + 'lyrics')
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find("div", class_=re.compile("Lyrics"))
    try:
        return lyrics.get_text()
    except AttributeError:
        logging.error(f"No text for {artistname} - {songname}")
        return ""


def load_lyrics():  # function to load data
    with open("SongCSV.csv", encoding='utf-8', mode='r') as f:
        reader = DictReader(f, delimiter=',')
        con = sqlite3.connect("lyrics.db")
        cur = con.cursor()
        cur.execute("DELETE FROM lyrics WHERE TRUE")
        con.commit()
        for i, line in enumerate(reader):
            if i < 1000:
                continue
            if i == 2000:
                break
            artist = line["ArtistName"][1:-1].replace('\'', '').replace('"', '')
            name = line["Title"][1:-1].replace('\'', '').replace('"', '')
            if name.split()[-1][0] == '(' and name.split()[-1][-1] == ')':
                name = ' '.join(name.split()[:-1])
            text = scrape_lyrics(artist, name).replace('\'', '').replace('"', '')
            cmd = f"""INSERT INTO lyrics (artist, name, text)
                      VALUES ('{artist}', '{name}', '{text}')"""
            cur.execute(cmd)
            con.commit()
            lyrics.append((artist, name, text))
        con.close()


if __name__ == "__main__":
    load_lyrics()
