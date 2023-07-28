import pafy, glob
from youtube_search import YoutubeSearch as yts
import match_peaks
import json
import os

from db_update import push

in_file = open('songs.out', 'r')

def collect(query):
    print(query)
    try:
        res = json.loads(yts(query + ' audio', max_results=1).to_json())['videos'][0]
    except(Exception) as e:
        print('Exception during audio download:', e)
        return
    
    dl = pafy.new(res['id'])
    stream = None
    print(dl)
    if(len(dl.m4astreams) > 0):
        stream = dl.m4astreams[0]
    else:
        return       

    audio_file = 'audio_only.' + stream.extension
    remove = glob.glob('audio_only.*')
    for name in remove:
        os.remove(name)

    stream.download(filepath = audio_file)
    
    try:
        res = json.loads(yts(query + ' music video', max_results=1).to_json())['videos'][0]
    except(Exception) as e:
        print('Exception during video download:', e)
        return

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
    push(mv_id, result[0])


