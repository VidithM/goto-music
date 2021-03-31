import pafy, glob
from youtube_search import YoutubeSearch as yts
import match_peaks
import json
import os


in_file = open('songs.out', 'r')

for query in in_file:
    print(query)
    res = json.loads(yts(query + ' audio', max_results=1).to_json())['videos'][0]
    dl = pafy.new(res['id'])
    stream = None
    if(len(dl.m4astreams) > 0):
        stream = dl.m4astreams[0]
    else:
        continue        
    audio_file = 'audio_only.' + stream.extension

    remove = glob.glob('audio_only.*')
    for name in remove:
        os.remove(name)

    stream.download(filepath = audio_file)
    
    res = json.loads(yts(query + ' music video', max_results=1).to_json())['videos'][0]
    dl = pafy.new(res['id'])
    stream = None
    if(len(dl.m4astreams) > 0):
        stream = dl.m4astreams[0]
    else:
        continue     
    mv_file = 'music_video.' + stream.extension

    remove = glob.glob('music_video.*')
    for name in remove:
        os.remove(name)

    stream.download(filepath = mv_file)

    result = match_peaks.match(audio_file, mv_file)
    print(query + ':', result[0], result[1])


