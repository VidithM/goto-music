import pyaudio
import math, random
import numpy as np 
import find_peaks as fp
from search_tree import SearchTree

from pydub import AudioSegment

import time

END = 10000 #Sample for 10 seconds
THRESH = 0.6

def match(audio_name, mv_name):
    audio_file = AudioSegment.from_file(audio_name)[5000:(END + 5000)]
    mv_file = AudioSegment.from_file(mv_name)
    
    data = np.frombuffer(audio_file._data, np.int16)
    
    audio_channels = []
    audio_sparse_maps = [] #freq/time mappings of amp peaks in spectogram

    for i in range(audio_file.channels):
        audio_channels.append(data[i::audio_file.channels])

    for channel_data in audio_channels:
        smap = fp.get_sparse_map(channel_data, audio_file.frame_rate)
        audio_sparse_maps.append(list(smap))

    l = 0
    length = 120000 #mv_file.duration_seconds * 1000
    best = None
    mn = -1

    while((l + END) <= length):
        if(l%5000 == 0):
            print('At time', l/1000, '(s)')
        sample = mv_file[l:(l + END)]

        sample_channels = []
        sample_sparse_maps = []

        data = np.frombuffer(sample._data, np.int16)
        for i in range(sample.channels):
            sample_channels.append(data[i::sample.channels])

        #print(sample_channels[0][])

        for channel_data in sample_channels:
            smap = fp.get_sparse_map(channel_data, mv_file.frame_rate)
            sample_sparse_maps.append(list(smap))

        try:
            curr = difference(audio_sparse_maps, sample_sparse_maps)
        except():
            return (0, 0)
    
        if((mn == -1) or ((curr > 0) and (mn - curr >= THRESH))):
            mn = curr 
            best = l 
        #print(curr)    
        l += 500
    return (best - 5000, mn)

def difference(audio_maps, sample_maps):
    mean_offset = 0
    map_cnt = min(len(audio_maps), len(sample_maps))
    for i in range(map_cnt):
        mean_offset += offset(audio_maps[i], sample_maps[i])

    return (mean_offset / map_cnt)


def offset(mapA, mapB):
    #print('query start')
    init = time.time() * 1000
    mean_dist = 0
    st = SearchTree()
    #print('sizes:',len(mapA), len(mapB))
    random.shuffle(mapA) #Reduce tree height
    for i in mapA:
        #print(i[0], i[1])
        st.push(i[0], i[1])
    #print('building done. Time was', (time.time() * 1000 - init))
    init = time.time() * 1000
    for j in mapB:
        #print(j, st.query(j[0], j[1], False))
        res = st.query(j[0], j[1], False)
        mean_dist += res[0]
    
    #print('query end. Time was', (time.time() * 1000 - init), 'Visited count:', res[1])
    
    return (mean_dist / len(mapB))
'''
def offset(mapA, mapB):
    mean_dist = 0
    for i in mapA:
        min_dist = -1
        res = None
        for j in mapB:
            if(res == None):
                res = j 
                min_dist = dist(i[0], i[1], j[0], j[1])
            else:
                if(dist(i[0], i[1], j[0], j[1]) < min_dist):
                    min_dist = dist(i[0], i[1], j[0], j[1])
                    res = j 
        mean_dist += min_dist 
    return (mean_dist / len(mapA))
'''

def dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
