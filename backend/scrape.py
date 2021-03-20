from bs4 import BeautifulSoup as bs 
import requests, time 

BASE_URL = 'https://www.billboard.com/charts/hot-100/'
START = 3600 * 24 * 365 * 45 # ~2015
END = int(time.time())

SONG_CLASS = 'chart-element__information__song text--truncate color--primary'
ARTIST_CLASS = 'chart-element__information__artist text--truncate color--secondary'

songs = [] #List of 2-tuples
song_lookup = set()

#Get songs for each week
for t in range(START, END + 1, 3600 * 24 * 30):
    url_suff = time.strftime('%Y-%m-%d', time.localtime(t))
    url = BASE_URL + url_suff
    source = requests.get(url).text
    soup = bs(source, 'html.parser')
    titles = []
    artists = []
    for tag in soup.find_all(class_= SONG_CLASS):
        titles.append(tag.text)
    
    for tag in soup.find_all(class_= ARTIST_CLASS):
        artists.append(tag.text)
    
    for i in range(len(titles)):
        put = (artists[i], titles[i])
        if(not(put in song_lookup)):
            song_lookup.add(put)
            songs.append(put)
    
out_file = open('songs.out', 'w')
for elem in songs:
    out_file.write(elem[0] + ': ' + elem[1] + '\n')

out_file.close()