import pafy, glob
import pyrebase
from youtube_search import YoutubeSearch as yts
import match_peaks
import json
import os

from db_update import push

DB_CONFIG = {
    'apiKey': "AIzaSyDjfdc64v44B1fecsZSc_TBj4sJPzaCi-g",
    'authDomain': "goto-music-c98e1.firebaseapp.com",
    'databaseURL': "https://goto-music-c98e1-default-rtdb.firebaseio.com/",
    'projectId': "goto-music-c98e1",
    'storageBucket': "goto-music-c98e1.appspot.com",
    'messagingSenderId': "902734405248",
    'appId': "1:902734405248:web:8e815e60bd1694cb335065"
}

firebase = pyrebase.initialize_app(DB_CONFIG)
db = firebase.database()

in_file = open('songs.out', 'r')

def collect(query):
    res = json.loads(yts(query + ' audio', max_results=1).to_json())['videos'][0]
    dl = pafy.new(res['id'])
    stream = None
    if(len(dl.m4astreams) > 0):
        stream = dl.m4astreams[0]
    else:
        return       
    audio_file = 'audio_only.' + stream.extension

    remove = glob.glob('audio_only.*')
    for name in remove:
        os.remove(name)

    stream.download(filepath = audio_file)
    
    res = json.loads(yts(query + ' music video', max_results=1).to_json())['videos'][0]
    mv_id = res['id']
    dl = pafy.new(mv_id)
    stream = None
    if(len(dl.m4astreams) > 0):
        stream = dl.m4astreams[0]
    else:
        return   
    mv_file = 'music_video.' + stream.extension

    remove = glob.glob('music_video.*')
    for name in remove:
        os.remove(name)

    stream.download(filepath = mv_file)

    result = match_peaks.match(audio_file, mv_file)
    push(db, mv_id, result[0])


