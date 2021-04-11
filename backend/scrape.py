from bs4 import BeautifulSoup as bs 
import requests, time 

BASE_URL = 'https://www.billboard.com/charts/year-end/'
START = 2015
END = 2020

SONG_CLASS = 'ye-chart-item__title'
ARTIST_CLASS = 'ye-chart-item__artist'

songs = [] #List of 2-tuples
song_lookup = set()

#Get songs for each week
for t in range(START, END + 1):
    url = BASE_URL + str(t) + '/hot-100-songs'
    source = requests.get(url).text
    soup = bs(source, 'html.parser')
    titles = []
    artists = []
    for tag in soup.find_all(class_= SONG_CLASS):
        titles.append(tag.text.strip())
    
    for tag in soup.find_all(class_= ARTIST_CLASS):
        artists.append(tag.text.strip())
    
    for i in range(len(titles)):
        put = (artists[i], titles[i])
        if(not(put in song_lookup)):
            song_lookup.add(put)
            songs.append(put)
    
out_file = open('songs.out', 'w')

for elem in songs:
    out_file.write(elem[0] + ': ' + elem[1] + '\n')

out_file.close()