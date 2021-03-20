import pafy
from youtube_search import YoutubeSearch as yts
import json


in_file = open('songs.out', 'r')

for query in in_file:
    res = json.loads(yts(query + ' audio', max_results=1).to_json())['videos'][0]
    dl = pafy.new(res['id'])
    stream = dl.getbestaudio()
    out_file = 'audio_only.' + stream.extension
    stream.download(filepath = out_file)
    
    res = json.loads(yts(query + ' music video', max_results=1).to_json())['videos'][0]
    dl = pafy.new(res['id'])
    stream = dl.getbestaudio()
    out_file = 'music_video.' + stream.extension
    stream.download(filepath = out_file)
    break


